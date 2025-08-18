import os
import sys
import pickle
import numpy as np
import faiss
import re
import json
import io
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

# --- File Parsers ---
import PyPDF2
import docx

# --- TTS Libraries ---
import boto3
# Import pydub only when needed for audio generation
try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False
    print("Warning: pydub not available. Audio generation will be disabled.")

# Import playsound for audio playback
try:
    from playsound import playsound
    PLAYSOUND_AVAILABLE = True
except ImportError:
    PLAYSOUND_AVAILABLE = False
    print("Warning: playsound not available. Auto-playback will be disabled.")

# Import ffmpeg for audio combining (alternative to pydub)
try:
    import ffmpeg
    FFMPEG_AVAILABLE = True
except ImportError:
    FFMPEG_AVAILABLE = False
    print("Warning: ffmpeg-python not available. Audio combining will be disabled.")

# --- Configuration ---
DOCUMENTS_DIR = "documents"
INDEX_DIR = "index"
INDEX_FILE = os.path.join(INDEX_DIR, "faiss_index.bin")
DATA_FILE = os.path.join(INDEX_DIR, "data.pkl")
GOOGLE_API_KEY = "AIzaSyBLdZ-Z3Dec82Su91bYmcA7zOc8MtWeN3w"

# AWS Configuration
AWS_REGION = "us-east-1"  # Change this to your preferred region

# Configure Google Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

# Ensure directories exist
os.makedirs(DOCUMENTS_DIR, exist_ok=True)
os.makedirs(INDEX_DIR, exist_ok=True)

# --- Document Loading and Parsing ---

def parse_pdf(file_path):
    """Extracts text from a PDF file."""
    text = ""
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

def parse_docx(file_path):
    """Extracts text from a DOCX file."""
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def parse_txt(file_path):
    """Extracts text from a TXT file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def create_chunks(text, max_chunk_size=200, overlap=50):
    """
    Creates smaller, more focused chunks from text.
    
    Args:
        text: The text to chunk
        max_chunk_size: Maximum number of characters per chunk
        overlap: Number of characters to overlap between chunks
    
    Returns:
        List of text chunks
    """
    # Clean and normalize text
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Split into sentences first
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        # If adding this sentence would exceed max size, save current chunk and start new one
        if len(current_chunk) + len(sentence) > max_chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            
            # Start new chunk with overlap from previous chunk
            if overlap > 0 and current_chunk:
                # Find last few words for overlap
                words = current_chunk.split()
                overlap_text = " ".join(words[-5:])  # Last 5 words
                current_chunk = overlap_text + " " + sentence
            else:
                current_chunk = sentence
        else:
            if current_chunk:
                current_chunk += ". " + sentence
            else:
                current_chunk = sentence
    
    # Add the last chunk if it exists
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    # Filter out very short chunks
    chunks = [chunk for chunk in chunks if len(chunk) > 50]
    
    return chunks

def load_documents():
    """Loads and parses all documents from the DOCUMENTS_DIR."""
    # This set will keep track of files we have already indexed.
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'rb') as f:
            _, _, processed_files = pickle.load(f)
    else:
        processed_files = set()
    
    new_docs = {}
    print("Checking for new documents...")
    for filename in os.listdir(DOCUMENTS_DIR):
        if filename in processed_files:
            continue # Skip files that are already indexed
        
        file_path = os.path.join(DOCUMENTS_DIR, filename)
        content = ""
        try:
            if filename.endswith(".pdf"):
                content = parse_pdf(file_path)
            elif filename.endswith(".docx"):
                content = parse_docx(file_path)
            elif filename.endswith(".txt"):
                content = parse_txt(file_path)
            else:
                continue # Skip unsupported file types
            
            if content.strip():
                new_docs[filename] = content
                print(f"  - Found new document: {filename}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            
    return new_docs

# --- Core Indexing and Search Logic ---

def build_or_update_index():
    """Builds a new index or updates an existing one with new documents."""
    new_docs = load_documents()
    
    if not new_docs:
        print("No new documents to add. Index is up to date.")
        return

    # Load existing data if it exists
    if os.path.exists(INDEX_FILE):
        index = faiss.read_index(INDEX_FILE)
        with open(DATA_FILE, 'rb') as f:
            passages, metadata, processed_files = pickle.load(f)
    else:
        # Initialize new index and data structures
        model = SentenceTransformer('all-MiniLM-L6-v2') # Load model only once if needed
        embedding_dim = model.get_sentence_embedding_dimension()
        index = faiss.IndexFlatL2(embedding_dim)
        passages, metadata, processed_files = [], [], set()

    # Process new documents
    model = SentenceTransformer('all-MiniLM-L6-v2')
    for filename, content in new_docs.items():
        # Use improved chunking strategy
        chunks = create_chunks(content, max_chunk_size=200, overlap=50)
        if not chunks:
            continue

        print(f"Embedding {filename} ({len(chunks)} chunks)...")
        chunk_embeddings = model.encode(chunks, convert_to_numpy=True)
        
        # Add to index and data
        index.add(chunk_embeddings)
        passages.extend(chunks)
        metadata.extend([{'source': filename}] * len(chunks))
        processed_files.add(filename)

    # Save the updated index and data
    print("Saving index...")
    faiss.write_index(index, INDEX_FILE)
    with open(DATA_FILE, 'wb') as f:
        pickle.dump((passages, metadata, processed_files), f)
    
    print(f"Index updated successfully. Total passages: {index.ntotal}")

def perform_search(query_text, k=5):
    """Performs a basic search on the existing index."""
    if not os.path.exists(INDEX_FILE):
        print("Index not found. Please run 'add' command first.")
        return None

    # Load index and data
    index = faiss.read_index(INDEX_FILE)
    with open(DATA_FILE, 'rb') as f:
        passages, metadata, _ = pickle.load(f)

    # Perform search
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = model.encode([query_text], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, k)

    # Return results for further processing
    results = []
    for i, idx in enumerate(indices[0]):
        if idx < len(passages):
            results.append({
                'source': metadata[idx]['source'],
                'passage': passages[idx],
                'similarity_score': float(distances[0][i])
            })
    
    return results

def analyze_and_categorize(query_text):
    """
    Performs a two-stage analysis: retrieval + LLM categorization.
    
    Stage 1: Retrieval - Get top relevant passages
    Stage 2: LLM Analysis - Categorize and analyze passages
    """
    print(f"🔍 Analyzing query: '{query_text}'")
    print("=" * 60)
    
    # Stage 1: Retrieval
    print("📚 Stage 1: Retrieving relevant passages...")
    search_results = perform_search(query_text, k=5)
    
    if not search_results:
        print("❌ No search results found. Please ensure documents are indexed.")
        return
    
    print(f"✅ Retrieved {len(search_results)} relevant passages")
    
    # Stage 2: LLM Analysis
    print("\n Stage 2: Analyzing with Gemini AI...")
    
    try:
        # Prepare passages for analysis
        passages_text = ""
        for i, result in enumerate(search_results, 1):
            passage = result['passage']
            if len(passage) > 300:
                passage = passage[:300] + "..."
            passages_text += f"Passage {i} (Source: {result['source']}):\n{passage}\n\n"
        
        # Construct the analysis prompt
        prompt = f"""
You are an expert document analyst. Analyze the relationship between the user's query and the retrieved passages.

USER QUERY: "{query_text}"

RETRIEVED PASSAGES:
{passages_text}

TASK: For each passage, analyze its relationship to the query and categorize it as one of the following:
- Agreement: The passage supports or agrees with the query
- Conflict: The passage contradicts or disagrees with the query  
- Illustrative Example: The passage provides an example or case study related to the query
- Related Point: The passage discusses a related topic but doesn't directly support or contradict

REQUIREMENTS:
1. Provide a brief justification for each categorization
2. Quote relevant parts from each passage to support your analysis
3. Return the analysis in valid JSON format

Return your analysis in this exact JSON structure:
{{
    "query": "the original query",
    "analysis": [
        {{
            "passage_number": 1,
            "source": "filename",
            "passage_preview": "first 100 chars of passage",
            "category": "Agreement|Conflict|Illustrative Example|Related Point",
            "justification": "brief explanation of why this category",
            "relevant_quote": "specific quote from passage"
        }}
    ],
    "summary": "brief overall analysis of how the passages relate to the query"
}}
"""

              # Configure Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        # Generate response with JSON output
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3
            )
        )
        
        # Parse JSON response - handle markdown-wrapped JSON
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith('```json'):
            response_text = response_text[7:]  # Remove ```json
        if response_text.startswith('```'):
            response_text = response_text[3:]  # Remove ```
        if response_text.endswith('```'):
            response_text = response_text[:-3]  # Remove trailing ```
        
        # Parse the cleaned JSON
        analysis_result = json.loads(response_text.strip())
        
        # Display results
        print("\n📊 ANALYSIS RESULTS:")
        print("=" * 60)
        print(f"Query: {analysis_result['query']}")
        print("\nPassage Analysis:")
        
        for item in analysis_result['analysis']:
            print(f"\n🔸 Passage {item['passage_number']} ({item['source']})")
            print(f"   Category: {item['category']}")
            print(f"   Justification: {item['justification']}")
            print(f"   Quote: \"{item['relevant_quote']}\"")
        
        print(f"\n Summary: {analysis_result['summary']}")
        
        return analysis_result
        
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON response: {e}")
        print("Raw response:", response.text)
        return None
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        
        # Handle quota exceeded error gracefully
        if "429" in str(e) and "quota" in str(e).lower():
            print("⚠️  Gemini API quota exceeded. Providing fallback analysis...")
            
            # Create a fallback analysis based on search results
            fallback_analysis = {
                "query": query_text,
                "analysis": [],
                "summary": f"Analysis limited due to API quota. Found {len(search_results)} relevant passages."
            }
            
            for i, result in enumerate(search_results, 1):
                passage = result['passage']
                if len(passage) > 100:
                    passage = passage[:100] + "..."
                
                fallback_analysis["analysis"].append({
                    "passage_number": i,
                    "source": result['source'],
                    "passage_preview": passage,
                    "category": "Related Point",
                    "justification": "Passage found relevant to query through semantic search",
                    "relevant_quote": passage
                })
            
            print("✅ Fallback analysis created successfully!")
            return fallback_analysis
        
        return None

def generate_podcast_script(query_text, analysis_result):
    """
    Generates a podcast script using the analysis results.
    
    Args:
        query_text: The original user query
        analysis_result: The result from analyze_and_categorize function
    
    Returns:
        The generated podcast script as a string
    """
    print("\n🎙️ Stage 1: Generating podcast script...")
    
    try:
        # Prepare categorized passages for the script generation prompt
        categorized_passages = []
        for item in analysis_result['analysis']:
            categorized_passages.append({
                "category": item['category'],
                "source": item['source'],
                "text": item['relevant_quote']
            })
        
        # Construct the script generation prompt
        script_prompt = f"""
You are an expert podcast scriptwriter. Your task is to create a short, engaging 2-3 minute podcast script based on a user's query and a set of relevant text passages retrieved from their documents.

**Podcast Personas:**
- **Alex (Host):** Inquisitive, guides the conversation, and asks clarifying questions.
- **Dr. Sharma (Expert):** Provides the detailed, fact-based answers. Dr. Sharma's dialogue MUST be grounded in and directly derived from the "Retrieved Passages" provided. She should rephrase them for conversational flow but must not introduce outside information.

**Your Goal:**
Create a script that introduces the topic, explores different facets of it using the provided passages, and concludes with a brief summary.

---
**INPUT DATA:**

**User Query:** "{query_text}"

**Categorized Passages:**
{json.dumps(categorized_passages, indent=2)}
---

**SCRIPT OUTPUT:**

Please begin the script now. Format it as a conversation between Alex and Dr. Sharma, with each line starting with the speaker's name followed by a colon. Keep the total script length to approximately 2-3 minutes when spoken (roughly 300-450 words).

Example format:
Alex: Welcome to our podcast today. We're discussing [topic].

Dr. Sharma: [Expert response based on the passages]

Alex: [Follow-up question or transition]

Dr. Sharma: [Next expert response]
"""

        # Configure Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        # Generate the script
        response = model.generate_content(
            script_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7
            )
        )
        
        script_text = response.text.strip()
        
        # Clean up the script text
        if script_text.startswith('```'):
            script_text = script_text[3:]
        if script_text.endswith('```'):
            script_text = script_text[:-3]
        
        print("✅ Podcast script generated successfully!")
        print("\n📝 Generated Script:")
        print("=" * 60)
        print(script_text)
        print("=" * 60)
        
        return script_text
        
    except Exception as e:
        print(f"❌ Error generating podcast script: {e}")
        return None

def generate_podcast_audio(script_text, output_filename="podcast_output.mp3"):
    """
    Generates a two-speaker audio file from a script using AWS Polly.
    
    Args:
        script_text: The podcast script text
        output_filename: The output MP3 filename
    
    Returns:
        True if successful, False otherwise
    """
    if not PYDUB_AVAILABLE:
        print("\n❌ Audio generation is not available due to missing pydub dependency.")
        print("Please install pydub: pip install pydub")
        print("Note: On Python 3.13, you may need to install additional audio dependencies.")
        return False
    
    print("\n🎵 Stage 2: Generating podcast audio...")
    try:
        # Initialize AWS Polly client
        polly_client = boto3.client('polly', region_name=AWS_REGION)

        # Voice selection for the two speakers
        voice_alex = "Matthew"  # Male voice
        voice_sharma = "Joanna"  # Female voice

        # Create an empty audio segment to build the podcast
        final_audio = AudioSegment.empty()

        # Process each line of the script
        lines = script_text.strip().split('\n')
        for line in lines:
            if line.strip(): # Skip empty lines
                if line.startswith("Alex:"):
                    speaker_text = line.replace("Alex:", "").strip()
                    voice = voice_alex
                elif line.startswith("Dr. Sharma:"):
                    speaker_text = line.replace("Dr. Sharma:", "").strip()
                    voice = voice_sharma
                else:
                    # For intros or sound effects text, use a neutral voice or skip
                    continue
                
                # Generate audio for the line using AWS Polly
                response = polly_client.synthesize_speech(
                    Text=speaker_text,
                    OutputFormat='mp3',
                    VoiceId=voice,
                    Engine='neural'  # Use neural engine for better quality
                )
                
                # Load this audio segment with pydub and append
                audio_segment = AudioSegment.from_mp3(io.BytesIO(response['AudioStream'].read()))
                final_audio += audio_segment

        # Export the final combined audio to an MP3 file
        final_audio.export(output_filename, format="mp3")
        print(f"\n✅ Podcast successfully generated! Saved as {output_filename}")

        return True

    except Exception as e:
        print(f"\n❌ An error occurred during audio generation: {e}")
        print("Please ensure you have AWS credentials configured.")
        print("Set up AWS credentials using one of these methods:")
        print("1. AWS CLI: aws configure")
        print("2. Environment variables: AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
        print("3. AWS credentials file: ~/.aws/credentials")
        return False

def generate_podcast_audio_simple(script_text, output_filename="podcast_output.mp3"):
    """
    Generates individual audio files for each speaker line (fallback when pydub is not available).
    
    Args:
        script_text: The podcast script text
        output_filename: The base output filename
    
    Returns:
        Tuple of (success, audio_files_list) where success is boolean and audio_files_list is list of filenames
    """
    print("\n🎵 Stage 2: Generating podcast audio (simple mode)...")
    try:
        # Initialize AWS Polly client
        polly_client = boto3.client('polly', region_name=AWS_REGION)

        # Voice selection for the two speakers
        voice_alex = "Matthew"  # Male voice
        voice_sharma = "Joanna"  # Female voice

        # Process each line of the script
        lines = script_text.strip().split('\n')
        audio_files = []
        
        for i, line in enumerate(lines):
            if line.strip(): # Skip empty lines
                if line.startswith("Alex:"):
                    speaker_text = line.replace("Alex:", "").strip()
                    voice = voice_alex
                    speaker = "alex"
                elif line.startswith("Dr. Sharma:"):
                    speaker_text = line.replace("Dr. Sharma:", "").strip()
                    voice = voice_sharma
                    speaker = "sharma"
                else:
                    # For intros or sound effects text, use a neutral voice or skip
                    continue
                
                # Generate audio for the line using AWS Polly
                response = polly_client.synthesize_speech(
                    Text=speaker_text,
                    OutputFormat='mp3',
                    VoiceId=voice,
                    Engine='neural'  # Use neural engine for better quality
                )
                
                # Save individual audio file
                individual_filename = f"{output_filename.replace('.mp3', '')}_{speaker}_{i:02d}.mp3"
                with open(individual_filename, 'wb') as f:
                    f.write(response['AudioStream'].read())
                
                audio_files.append(individual_filename)
                print(f"  Generated: {individual_filename}")

        print(f"\n✅ Generated {len(audio_files)} individual audio files!")
        
        # Try to combine into a single file
        if FFMPEG_AVAILABLE:
            combined_success = combine_audio_files(audio_files, output_filename)
            if combined_success:
                print(f"🎉 Successfully created single podcast file: {output_filename}")
                # Clean up individual files
                for audio_file in audio_files:
                    try:
                        os.remove(audio_file)
                        print(f"  Cleaned up: {audio_file}")
                    except:
                        pass
                return True, [output_filename]  # Return the single combined file
            else:
                print("⚠️ Could not combine files, keeping individual files")
                return True, audio_files
        else:
            print("Note: Install ffmpeg-python to automatically combine files: pip install ffmpeg-python")
            return True, audio_files

    except Exception as e:
        print(f"\n❌ An error occurred during audio generation: {e}")
        print("Please ensure you have AWS credentials configured.")
        print("Set up AWS credentials using one of these methods:")
        print("1. AWS CLI: aws configure")
        print("2. Environment variables: AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
        print("3. AWS credentials file: ~/.aws/credentials")
        return False, []

def play_audio_sequence(base_filename, audio_files):
    """
    Plays all generated audio files in sequence.
    
    Args:
        base_filename: The base filename used for generation
        audio_files: List of generated audio filenames
    """
    if not PLAYSOUND_AVAILABLE:
        print("\n🎵 Auto-playback not available. Install playsound: pip install playsound")
        if len(audio_files) == 1:
            print(f"You can manually play the audio file: {audio_files[0]}")
        else:
            print("You can manually play the audio files in this order:")
            for i, filename in enumerate(audio_files, 1):
                print(f"  {i}. {filename}")
        return
    
    # If we have a single combined file, play it directly
    if len(audio_files) == 1:
        print(f"\n🎵 Playing complete podcast: {audio_files[0]}")
        print("Press Ctrl+C to stop playback")
        try:
            playsound(audio_files[0])
            print("\n🎉 Complete podcast playback finished!")
        except KeyboardInterrupt:
            print("\n⏹️ Playback stopped by user")
        except Exception as e:
            print(f"\n❌ Error during playback: {e}")
    else:
        # Play multiple files in sequence
        print(f"\n🎵 Playing complete podcast ({len(audio_files)} audio segments)...")
        print("Press Ctrl+C to stop playback")
        
        try:
            for i, filename in enumerate(audio_files, 1):
                print(f"  Playing segment {i}/{len(audio_files)}: {filename}")
                playsound(filename)
                print(f"  ✅ Completed segment {i}")
            
            print("\n🎉 Complete podcast playback finished!")
            
        except KeyboardInterrupt:
            print("\n⏹️ Playback stopped by user")
        except Exception as e:
            print(f"\n❌ Error during playback: {e}")
            print("You can still manually play the audio files")

def combine_audio_files(audio_files, output_filename):
    """
    Combines multiple audio files into a single file using ffmpeg.
    
    Args:
        audio_files: List of audio filenames to combine
        output_filename: The output combined audio filename
    
    Returns:
        True if successful, False otherwise
    """
    if not FFMPEG_AVAILABLE:
        print("\n❌ Audio combining not available. Install ffmpeg-python: pip install ffmpeg-python")
        print("You can manually combine the audio files using audio editing software.")
        return False
    
    if not audio_files:
        print("\n❌ No audio files to combine.")
        return False
    
    try:
        print(f"\n🔧 Combining {len(audio_files)} audio files into single file...")
        
        # Create a temporary file list for ffmpeg
        with open('temp_file_list.txt', 'w', encoding='utf-8') as f:
            for audio_file in audio_files:
                f.write(f"file '{audio_file}'\n")
        
        # Use ffmpeg to concatenate all files
        (
            ffmpeg
            .input('temp_file_list.txt', format='concat', safe=0)
            .output(output_filename, c='copy')
            .overwrite_output()
            .run(quiet=True)
        )
        
        # Clean up temporary file
        if os.path.exists('temp_file_list.txt'):
            os.remove('temp_file_list.txt')
        
        print(f"✅ Successfully combined audio files into: {output_filename}")
        return True
        
    except Exception as e:
        print(f"\n❌ Error combining audio files: {e}")
        # Clean up temporary file if it exists
        if os.path.exists('temp_file_list.txt'):
            os.remove('temp_file_list.txt')
        return False

def generate_podcast(query_text, output_filename="podcast_output.mp3"):
    """
    Complete podcast generation pipeline: analysis -> script -> audio.
    
    Args:
        query_text: The user's query
        output_filename: The output MP3 filename
    
    Returns:
        True if successful, False otherwise
    """
    print("🎙️ PODCAST GENERATION PIPELINE")
    print("=" * 60)
    
    # Stage 1: Analysis and categorization
    analysis_result = analyze_and_categorize(query_text)
    if not analysis_result:
        print("❌ Failed to analyze query. Cannot generate podcast.")
        return False
    
    # Stage 2: Generate podcast script
    script_text = generate_podcast_script(query_text, analysis_result)
    if not script_text:
        print("❌ Failed to generate podcast script.")
        return False
    
    # Stage 3: Generate audio
    if PYDUB_AVAILABLE:
        success = generate_podcast_audio(script_text, output_filename)
        if success:
            print("\n🎉 PODCAST GENERATION COMPLETE!")
            print(f"📁 Audio file: {output_filename}")
            print("🎵 You can now play the generated podcast!")
        else:
            print("\n❌ Podcast generation failed at audio stage.")
    else:
        success, audio_files = generate_podcast_audio_simple(script_text, output_filename)
        if success:
            if len(audio_files) == 1:
                print("\n PODCAST GENERATION COMPLETE!")
                print(f" Single audio file: {audio_files[0]}")
                print("🎵 You can now play the complete podcast!")
            else:
                print("\n PODCAST GENERATION COMPLETE!")
                print("📁 Individual audio files generated")
                print("🎵 You can play the individual audio files or combine them manually")

            # Ask user if they want to play the audio
            try:
                play_choice = input("\n🎵 Would you like to play the complete podcast now? (y/n): ").lower().strip()
                if play_choice == "y":
                    play_audio_sequence(output_filename, audio_files)
            except KeyboardInterrupt:
                print("\n⏹️ Skipping playback")
        else:
            print("\n❌ Podcast generation failed at audio stage.")
    
    return success

# --- Main CLI ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python app.py <command> [query]")
        print("Commands:")
        print("  add      - Indexes new documents from the 'documents' folder.")
        print("  search   - Basic search (legacy command).")
        print("  analyze  - Advanced analysis with Gemini AI categorization.")
        print("  podcast  - Generate a podcast from your query and documents.")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "add":
        build_or_update_index()
    elif command == "search":
        if len(sys.argv) < 3:
            print("Error: Please provide a search query.")
            print("Usage: python app.py search \"your search query here\"")
        else:
            query = " ".join(sys.argv[2:])
            results = perform_search(query)
            if results:
                print(f"\n--- Top {len(results)} results for '{query}' ---")
                for i, result in enumerate(results, 1):
                    passage = result['passage']
                    if len(passage) > 300:
                        passage = passage[:300] + "..."
                    print(f"\n{i}. Source: {result['source']}")
                    print(f"   Passage: \"{passage}\"")
                    print(f"   (Similarity Score: {result['similarity_score']:.4f})")
    elif command == "analyze":
        if len(sys.argv) < 3:
            print("Error: Please provide a query for analysis.")
            print("Usage: python app.py analyze \"your query here\"")
        else:
            query = " ".join(sys.argv[2:])
            analyze_and_categorize(query)
    elif command == "podcast":
        if len(sys.argv) < 3:
            print("Error: Please provide a query for podcast generation.")
            print("Usage: python app.py podcast \"your query here\"")
        else:
            query = " ".join(sys.argv[2:])
            generate_podcast(query)
    else:
        print(f"Unknown command: {command}")

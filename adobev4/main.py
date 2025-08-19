from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends, Query, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import json
import uuid
from datetime import datetime
import shutil
from pathlib import Path
from app import generate_podcast
# from API import generate_insights  # This module doesn't exist, removing import

# Import service layer functions from app.py
from app import (
    parse_pdf, parse_docx, parse_txt, create_chunks,
    build_or_update_index, perform_search, analyze_and_categorize,
    generate_podcast_script, generate_podcast_audio, generate_podcast_audio_simple,
    combine_audio_files, DOCUMENTS_DIR, INDEX_DIR, load_documents
)

# Import additional dependencies
import google.generativeai as genai
import boto3
from sentence_transformers import SentenceTransformer
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Configure FastAPI app
app = FastAPI(
    title="Adobe+ Document Analysis & Podcast Generation API",
    description="A comprehensive API for document management, analysis, and podcast generation",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import configuration
from config import config

# Configure Google Gemini API
genai.configure(api_key=config.GOOGLE_API_KEY)

# Initialize Gemini model for semantic analysis
try:
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')
    print("Gemini model initialized successfully")
except Exception as e:
    print(f"Warning: Could not initialize Gemini model: {e}")
    gemini_model = None

# Initialize embedding model for semantic search
try:
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    print("Embedding model initialized successfully")
except Exception as e:
    print(f"Warning: Could not initialize embedding model: {e}")
    embedding_model = None

# Global cache for embeddings
embeddings_cache = {}

# In-memory storage (replace with database in production)
documents_db = {}
personas_db = set()
reading_progress_db = {}

# Initialize documents_db with existing files on startup
def initialize_documents_db():
    """Load existing documents from the documents directory into documents_db"""
    try:
        documents_dir = "documents"
        if not os.path.exists(documents_dir):
            print("📁 Documents directory not found, creating it...")
            os.makedirs(documents_dir)
            return
        
        print("🔄 Initializing documents_db with existing files...")
        files = os.listdir(documents_dir)
        loaded_count = 0
        
        for filename in files:
            if filename.endswith(('.pdf', '.docx', '.txt')):
                file_path = os.path.join(documents_dir, filename)
                
                # Check if this file is already in documents_db
                file_already_loaded = any(
                    doc.get("file_path") == file_path for doc in documents_db.values()
                )
                
                if not file_already_loaded:
                    # Extract metadata and add to database
                    metadata = get_document_metadata(file_path, filename)
                    if metadata:
                        documents_db[metadata["id"]] = metadata
                        loaded_count += 1
                        print(f"   ✅ Loaded: {filename}")
        
        print(f"📚 Loaded {loaded_count} documents into documents_db")
        
    except Exception as e:
        print(f"❌ Error initializing documents_db: {e}")

# Initialize documents_db on startup (moved to after function definitions)

# Stopwords for keyword extraction
STOPWORDS = {
    "a","an","the","of","to","and","in","on","for","with","by","is","are","be",
    "was","were","as","at","from","or","that","this","it","its","into","about",
    "your","their","his","her","our","we","you","i"
}

WORD_RE = re.compile(r"[A-Za-z0-9_]+", re.UNICODE)

def tokenize(text: str) -> List[str]:
    """Tokenize text into words."""
    return [w.lower() for w in WORD_RE.findall(text)]

def keyword_set(text: str) -> set:
    """Extract keywords from text, excluding stopwords."""
    return {w for w in tokenize(text) if w not in STOPWORDS and len(w) > 2}

def get_semantic_embedding(text: str) -> np.ndarray:
    """Get semantic embedding for text using SentenceTransformer."""
    if embedding_model is None:
        return None
    
    if text in embeddings_cache:
        return embeddings_cache[text]
    
    try:
        embedding = embedding_model.encode([text])[0]
        embeddings_cache[text] = embedding
        return embedding
    except Exception as e:
        print(f"Error getting embedding: {e}")
        return None

def semantic_similarity(text1: str, text2: str) -> float:
    """Calculate semantic similarity between two texts."""
    if embedding_model is None:
        return 0.0
    
    emb1 = get_semantic_embedding(text1)
    emb2 = get_semantic_embedding(text2)
    
    if emb1 is None or emb2 is None:
        return 0.0
    
    # Cosine similarity
    similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
    return float(similarity)

def gemini_semantic_analysis(query: str, section_text: str, persona: str, job: str) -> Dict[str, Any]:
    """Use Gemini Flash API to analyze semantic relevance and relationship type."""
    if gemini_model is None:
        return {
            "relevance_score": 0.5,
            "relationship_type": "related",
            "explanation": "Semantic analysis not available"
        }
    
    try:
        prompt = f"""
        Analyze the semantic relationship between the query and the section text.
        
        Query: "{query}"
        Section Text: "{section_text[:1000]}..."
        Persona: {persona}
        Job: {job}
        
        Provide a JSON response with:
        1. relevance_score (0.0-1.0): How semantically relevant is the section to the query?
        2. relationship_type: "related", "contradicting", "example", "overlapping", "complementary"
        3. explanation: Brief explanation of the relationship
        4. key_concepts: List of key concepts that connect the query and section
        
        Response format:
        {{
            "relevance_score": 0.8,
            "relationship_type": "related",
            "explanation": "This section discusses cloud computing concepts that directly relate to the query about infrastructure deployment.",
            "key_concepts": ["cloud computing", "deployment", "infrastructure"]
        }}
        """
        
        response = gemini_model.generate_content(prompt)
        result = response.text.strip()
        
        # Try to parse JSON response
        try:
            parsed = json.loads(result)
            return parsed
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return {
                "relevance_score": 0.5,
                "relationship_type": "related",
                "explanation": "Semantic analysis completed but parsing failed",
                "key_concepts": []
            }
            
    except Exception as e:
        print(f"Gemini semantic analysis error: {e}")
        # Use enhanced fallback for quota exceeded or other errors
        return _generate_fallback_analysis(query, section_text, persona, job)

def _generate_fallback_analysis(query: str, section_text: str, persona: str, job: str) -> Dict[str, Any]:
    """Generate fallback analysis when Gemini API is unavailable."""
    # Simple keyword-based analysis
    query_lower = query.lower()
    section_lower = section_text.lower()
    
    # Calculate keyword overlap
    query_words = set(query_lower.split())
    section_words = set(section_lower.split())
    overlap = len(query_words & section_words)
    total_query_words = len(query_words)
    
    # Calculate relevance score based on keyword overlap
    if total_query_words > 0:
        relevance_score = min(0.8, overlap / total_query_words + 0.2)
    else:
        relevance_score = 0.5
    
    # Determine relationship type based on content
    relationship_type = "related"
    if any(word in section_lower for word in ["example", "instance", "case"]):
        relationship_type = "example"
    elif any(word in section_lower for word in ["however", "but", "contrary", "opposite"]):
        relationship_type = "contradicting"
    elif any(word in section_lower for word in ["similar", "like", "same", "also"]):
        relationship_type = "overlapping"
    
    # Generate explanation
    if relevance_score > 0.6:
        explanation = f"This section contains relevant information about {', '.join(list(query_words & section_words)[:3])} that aligns with your role as {persona.lower()}."
    else:
        explanation = f"This section provides complementary information that may support your understanding of {job.lower()}."
    
    # Extract key concepts
    key_concepts = list(query_words & section_words)[:5]
    
    return {
        "relevance_score": relevance_score,
        "relationship_type": relationship_type,
        "explanation": explanation,
        "key_concepts": key_concepts
    }

def generate_enhanced_relevance_explanation(section: Dict[str, Any], 
                                         current_section: str,
                                         persona: str, 
                                         job: str) -> str:
    """Generate an enhanced explanation of why a section is relevant."""
    section_text = section.get("text", "")
    section_title = section.get("section_title", "")
    document = section.get("document", "Unknown Document")
    relevance_score = section.get("contextual_score", section.get("relevance_score", 0))
    
    # Enhanced keyword analysis
    persona_keywords = keyword_set(persona)
    job_keywords = keyword_set(job)
    current_keywords = keyword_set(current_section) if current_section else set()
    section_keywords = keyword_set(section_text + " " + section_title)
    
    # Find overlapping concepts
    common_persona = persona_keywords & section_keywords
    common_job = job_keywords & section_keywords
    common_current = current_keywords & section_keywords
    
    # Determine relationship type
    relationship_type = "complementary"
    if relevance_score > 0.8:
        relationship_type = "highly relevant"
    elif relevance_score > 0.6:
        relationship_type = "closely related"
    elif common_current:
        relationship_type = "topically connected"
    
    # Build contextual explanation
    explanation_parts = []
    
    # Primary relevance reason
    if common_persona and common_job:
        key_terms = list((common_persona | common_job)[:3])
        explanation_parts.append(f"Addresses {', '.join(key_terms)} directly relevant to your role and objectives")
    elif common_current and len(common_current) >= 2:
        key_terms = list(common_current[:2])
        explanation_parts.append(f"Builds upon concepts like {', '.join(key_terms)} from your current reading")
    elif common_persona:
        key_terms = list(common_persona[:2])
        explanation_parts.append(f"Contains insights about {', '.join(key_terms)} relevant to your {persona.lower()} role")
    elif common_job:
        key_terms = list(common_job[:2])
        explanation_parts.append(f"Provides information about {', '.join(key_terms)} for your {job.lower()}")
    
    # Add document context if different document
    if document and current_section:
        if "current document" not in document.lower():
            explanation_parts.append(f"from {document}")
    
    # Add relevance qualifier
    if relevance_score > 0.7:
        explanation_parts.append("with high contextual relevance")
    elif relevance_score > 0.5:
        explanation_parts.append("with moderate contextual relevance")
    
    # Combine explanation parts
    if explanation_parts:
        explanation = " ".join(explanation_parts).capitalize()
        if not explanation.endswith('.'):
            explanation += "."
        return explanation
    else:
        return f"Contains complementary information that may support your understanding of {job.lower()}."

def find_related_sections_enhanced(current_page: int, 
                                  current_section: str,
                                  persona: str,
                                  job: str,
                                  all_sections: List[Dict[str, Any]],
                                  limit: int = 5) -> List[Dict[str, Any]]:
    """
    Find sections related to the current reading position using semantic search and Gemini Flash API.
    This implements a hybrid approach combining semantic embeddings, search, and AI analysis.
    """
    if not all_sections:
        return []
    
    # Filter out current page sections
    filtered_sections = [s for s in all_sections if s.get("page_number", s.get("page", 0)) != current_page]
    
    if not filtered_sections:
        return []
    
    # Build semantic search query
    query = f"{persona} {job}"
    if current_section:
        query += f" {current_section}"
    
    # Enhanced analysis approach
    enhanced_sections = []
    
    for section in filtered_sections:
        # Get Gemini semantic analysis
        section_text = f"{section.get('section_title', '')} {section.get('text', '')}"
        gemini_analysis = gemini_semantic_analysis(query, section_text, persona, job)
        
        # Use traditional scoring as fallback
        traditional_score = section.get("relevance_score", 0.5)
        
        # Calculate keyword-based similarity as fallback
        query_keywords = set(query.lower().split())
        section_keywords = set(section_text.lower().split())
        keyword_overlap = len(query_keywords & section_keywords) / max(len(query_keywords), 1)
        
        # Combine scores: keyword overlap + Gemini + traditional
        combined_score = (keyword_overlap * 0.3 + gemini_analysis["relevance_score"] * 0.5 + traditional_score * 0.2)
        
        enhanced_sections.append({
            **section,
            "keyword_score": keyword_overlap,
            "gemini_score": gemini_analysis["relevance_score"],
            "combined_score": combined_score,
            "relationship_type": gemini_analysis["relationship_type"],
            "gemini_explanation": gemini_analysis["explanation"],
            "key_concepts": gemini_analysis.get("key_concepts", [])
        })
    
    # Sort by combined score
    enhanced_sections.sort(key=lambda x: x["combined_score"], reverse=True)
    
    # Diversify by document and relationship type
    diversified_sections = []
    seen_documents = set()
    seen_relationship_types = set()
    
    for section in enhanced_sections:
        doc_name = section.get("document", "Unknown")
        relationship_type = section.get("relationship_type", "related")
        
        # Prioritize diverse documents and relationship types
        if len(diversified_sections) < limit:
            diversified_sections.append(section)
            seen_documents.add(doc_name)
            seen_relationship_types.add(relationship_type)
        elif (doc_name not in seen_documents or relationship_type not in seen_relationship_types) and len(diversified_sections) < limit * 2:
            diversified_sections.append(section)
            seen_documents.add(doc_name)
            seen_relationship_types.add(relationship_type)
    
    # Final selection: take top sections
    final_sections = diversified_sections[:limit]
    
    # Generate enhanced explanations
    related = []
    for section in final_sections:
        # Use Gemini explanation if available, otherwise fallback
        explanation = section.get("gemini_explanation")
        if not explanation or len(explanation) < 20:
            explanation = generate_enhanced_relevance_explanation(section, current_section, persona, job)
        
        related.append({
            "document": section.get("document", "Unknown Document"),
            "section_title": section.get("section_title", "Unknown Section"),
            "page_number": section.get("page_number", 1),
            "relevance_score": section.get("combined_score", 0.5),
            "explanation": explanation,
            "relationship_type": section.get("relationship_type", "related"),
            "key_concepts": section.get("key_concepts", [])
        })
    
    return related

# Ensure directories exist
os.makedirs(DOCUMENTS_DIR, exist_ok=True)
os.makedirs(INDEX_DIR, exist_ok=True)
os.makedirs("audio", exist_ok=True)

# Pydantic models for request/response
class DocumentAnalysisRequest(BaseModel):
    document_ids: List[str]
    persona: str
    job_to_be_done: str

class InsightRequest(BaseModel):
    text: str
    persona: str
    job_to_be_done: str
    document_context: Optional[str] = None

class SimplifyTextRequest(BaseModel):
    text: str

class DefineTermRequest(BaseModel):
    term: str
    context: str

class DocumentSyncRequest(BaseModel):
    document_id: str
    content: str
    filename: str

# Request model for podcast generation
class PodcastRequest(BaseModel):
    query: str
    output_filename: str | None = "podcast_output.mp3"

# Helper functions
def get_document_metadata(file_path: str, filename: str) -> Dict[str, Any]:
    """Extract metadata from document"""
    try:
        if filename.endswith('.pdf'):
            content = parse_pdf(file_path)
        elif filename.endswith('.docx'):
            content = parse_docx(file_path)
        elif filename.endswith('.txt'):
            content = parse_txt(file_path)
        else:
            return None
        
        # Generate outline from content
        chunks = create_chunks(content, max_chunk_size=200, overlap=50)
        outline = []
        for i, chunk in enumerate(chunks[:10]):  # First 10 chunks as outline
            outline.append({
                "level": "section",
                "text": chunk[:100] + "..." if len(chunk) > 100 else chunk,
                "page": i + 1
            })
        
        return {
            "id": str(uuid.uuid4()),
            "name": filename,
            "title": filename.replace('.pdf', '').replace('.docx', '').replace('.txt', ''),
            "outline": outline,
            "language": "en",  # Default to English
            "upload_timestamp": datetime.now().isoformat(),
            "file_path": file_path,
            "content": content
        }
    except Exception as e:
        print(f"Error extracting metadata from {filename}: {e}")
        return None

# Initialize documents_db on startup (after function definitions)
initialize_documents_db()

def save_uploaded_file(upload_file: UploadFile, destination: str) -> bool:
    """Save uploaded file to destination"""
    try:
        with open(destination, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
        return True
    except Exception as e:
        print(f"Error saving file {upload_file.filename}: {e}")
        return False

# API Endpoints

@app.post("/upload-pdfs")
async def upload_pdfs(
    files: List[UploadFile] = File(...),
    persona: Optional[str] = Form(None),
    job_to_be_done: Optional[str] = Form(None)
):
    """Upload PDF documents with metadata for analysis"""
    try:
        uploaded_docs = []
        
        for file in files:
            if not file.filename:
                continue
                
            # Validate file type
            if not file.filename.lower().endswith(('.pdf', '.docx', '.txt')):
                continue
            
            # Generate unique filename
            file_extension = Path(file.filename).suffix
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(DOCUMENTS_DIR, unique_filename)
            
            # Save file
            if save_uploaded_file(file, file_path):
                # Extract metadata
                metadata = get_document_metadata(file_path, file.filename)
                if metadata:
                    # Store in database
                    documents_db[metadata["id"]] = metadata
                    uploaded_docs.append(metadata)
                    
                    # Add persona if provided
                    if persona:
                        personas_db.add(persona)
        
        # Rebuild index with new documents using app.py logic
        build_or_update_index()
        
        return uploaded_docs
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.get("/documents")
async def get_documents():
    """Retrieve all uploaded documents"""
    try:
        return list(documents_db.values())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve documents: {str(e)}")

@app.get("/documents/{doc_id}/status")
async def get_document_status(doc_id: str):
    """Get the status of a specific document"""
    try:
        if doc_id not in documents_db:
            raise HTTPException(status_code=404, detail="Document not found")
        
        doc = documents_db[doc_id]
        
        # Check if file exists
        file_exists = os.path.exists(doc["file_path"])
        
        # Get file size if it exists
        file_size = 0
        if file_exists:
            try:
                file_size = os.path.getsize(doc["file_path"])
            except:
                file_size = 0
        
        return {
            "id": doc_id,
            "name": doc.get("name", ""),
            "title": doc.get("title", ""),
            "status": "available" if file_exists else "missing",
            "file_exists": file_exists,
            "file_size": file_size,
            "upload_timestamp": doc.get("upload_timestamp", ""),
            "language": doc.get("language", "en"),
            "outline": doc.get("outline", []),
            "content": doc.get("content", "")[:500] + "..." if doc.get("content") and len(doc.get("content", "")) > 500 else doc.get("content", "")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve document status: {str(e)}")

@app.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    """Delete a specific document"""
    try:
        if doc_id not in documents_db:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Remove file from filesystem
        doc = documents_db[doc_id]
        if os.path.exists(doc["file_path"]):
            os.remove(doc["file_path"])
        
        # Remove from database
        del documents_db[doc_id]
        
        # Rebuild index
        build_or_update_index()
        
        return {"message": "Document deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete document: {str(e)}")

@app.post("/index-documents")
async def index_documents():
        """Index all documents in the documents directory using app.py logic"""
        try:
            # Use the app.py build_or_update_index function
            build_or_update_index()
            return {"message": "Documents indexed successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to index documents: {str(e)}")

@app.post("/sync-document")
async def sync_document(request: DocumentSyncRequest):
    """Sync a document from HARSHALADOBE backend to adobev4 for indexing"""
    try:
        print(f"📄 Syncing document: {request.filename} (ID: {request.document_id})")
        
        # Save the document content to a file in the documents directory
        file_path = os.path.join(DOCUMENTS_DIR, f"{request.document_id}.txt")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(request.content)
        
        # Add to documents_db
        documents_db[request.document_id] = {
            "id": request.document_id,
            "name": request.filename,
            "file_path": file_path,
            "upload_timestamp": datetime.now().isoformat()
        }
        
        # Rebuild index to include the new document
        build_or_update_index()
        
        print(f"✅ Document synced and indexed successfully")
        return {"message": "Document synced and indexed successfully"}
        
    except Exception as e:
        print(f"❌ Error syncing document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to sync document: {str(e)}")

@app.post("/search-documents")
async def search_documents(query: str = Form(...), k: int = Form(5)):
    """Search documents using app.py logic"""
    try:
        # Use the app.py perform_search function
        results = perform_search(query, k)
        if results:
            return {
                "query": query,
                "results": results,
                "total_results": len(results)
            }
        else:
            return {
                "query": query,
                "results": [],
                "total_results": 0,
                "message": "No results found"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.post("/analyze-query")
async def analyze_query(query: str = Form(...), document_ids: Optional[str] = Form(None)):
    """Analyze a query using semantic search for specified documents or all indexed documents"""
    try:
        print(f"🔍 Performing semantic search for query: {query}")
        print(f"📚 Document IDs provided: {document_ids}")
        
        # Parse document IDs if provided
        target_doc_ids = []
        if document_ids:
            try:
                target_doc_ids = json.loads(document_ids)
                print(f"📋 Target document IDs: {target_doc_ids}")
            except json.JSONDecodeError:
                print("⚠️ Invalid document_ids JSON format")
        
        # Use semantic search to find relevant passages
        search_results = perform_search(query, k=10)  # Get more results to filter from
        
        if not search_results:
            print("⚠️ No search results found")
            return {
                "query": query,
                "analysis": [
                    {
                        "passage_number": 1,
                        "source": "no_results",
                        "passage_preview": "No relevant passages found in any documents.",
                        "category": "Related Point",
                        "justification": "The semantic search did not find any relevant passages for your query. Please try a different query or upload documents.",
                        "quote": "Try a different query or upload documents."
                    }
                ],
                "summary": f"Semantic search for '{query}' found no relevant passages. Please try a different query or upload documents."
            }
        
        print(f"🔍 Found {len(search_results)} total results from semantic search")
        
        # Filter results based on document IDs if provided
        filtered_results = search_results
        if target_doc_ids:
            filtered_results = []
            for result in search_results:
                source_file = result.get('source', '')
                # Check if the source file corresponds to any target document ID
                for doc_id in target_doc_ids:
                    if doc_id in source_file:
                        filtered_results.append(result)
                        break
            print(f"🔍 Filtered to {len(filtered_results)} results from target documents")
        
        if not filtered_results:
            print("⚠️ No results from target documents")
            return {
                "query": query,
                "analysis": [
                    {
                        "passage_number": 1,
                        "source": "no_target_results",
                        "passage_preview": "No relevant passages found in the specified documents.",
                        "category": "Related Point",
                        "justification": "The semantic search did not find any relevant passages for your query in the specified documents.",
                        "quote": "Try a different query or check other documents."
                    }
                ],
                "summary": f"Semantic search for '{query}' found no relevant passages in the specified documents."
            }
        
        # Convert filtered search results to analysis format
        analysis_items = []
        for i, result in enumerate(filtered_results[:5]):  # Limit to top 5 results
            # Determine category based on relevance score
            relevance_score = result.get('similarity_score', 0.5)
            if relevance_score > 0.8:
                category = "Key Insight"
            elif relevance_score > 0.6:
                category = "Direct Answer"
            else:
                category = "Related Point"
            
            # Get the passage content
            passage_content = result.get('passage', '')
            
            # Get document name for better display
            source_file = result.get('source', '')
            doc_name = source_file.replace('.pdf', '').replace('.docx', '').replace('.txt', '')
            
            # Create analysis item
            analysis_item = {
                "passage_number": i + 1,
                "source": doc_name,
                "passage_preview": passage_content[:200] + "..." if len(passage_content) > 200 else passage_content,
                "category": category,
                "justification": f"This passage from '{doc_name}' is relevant to your query '{query}' with a relevance score of {relevance_score:.2f}. It contains information that directly addresses your question.",
                "quote": passage_content[:300] + "..." if len(passage_content) > 300 else passage_content,
                "relevant_quote": passage_content[:300] + "..." if len(passage_content) > 300 else passage_content  # Keep for backward compatibility
            }
            analysis_items.append(analysis_item)
        
        # Create summary based on filtered search results
        summary = f"Semantic search found {len(analysis_items)} relevant passages for '{query}'"
        if target_doc_ids:
            summary += f" from the specified {len(target_doc_ids)} document(s)"
        summary += ". "
        if analysis_items:
            top_result = analysis_items[0]
            summary += f"The most relevant passage is from '{top_result['source']}' and is categorized as '{top_result['category']}'."
        
        return {
            "query": query,
            "analysis": analysis_items,
            "summary": summary
        }
        
    except Exception as e:
        print(f"❌ Semantic search error: {str(e)}")
        # Provide a fallback response instead of failing
        return {
            "query": query,
            "analysis": [
                {
                    "passage_number": 1,
                    "source": "error_fallback",
                    "passage_preview": "Semantic search encountered an issue...",
                    "category": "Related Point",
                    "justification": "The semantic search system encountered an error but is still functional.",
                    "quote": "Please try a different query or check back later."
                }
            ],
            "summary": f"Semantic search for '{query}' encountered an issue. The system is working to resolve this."
        }

@app.post("/analyze-documents")
async def analyze_documents(request: DocumentAnalysisRequest):
        """Analyze documents with persona and job context"""
        try:
            # Create a comprehensive query from the request
            query = f"{request.persona} {request.job_to_be_done}"
            if request.document_ids:
                query += f" documents: {', '.join(request.document_ids)}"
            
            # Use the app.py analyze_and_categorize function directly
            # This function handles document retrieval and analysis internally
            analysis_result = analyze_and_categorize(query)
            
            if not analysis_result:
                raise HTTPException(status_code=500, detail="Analysis failed")
            
            return {
                "analysis_results": analysis_result,
                "insights": [item["justification"] for item in analysis_result.get("analysis", [])]
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/insights")
async def generate_insights(request: InsightRequest):
    """Generate AI insights from text content"""
    try:
        # Use Gemini to generate insights
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        prompt = f"""
        Analyze the following text and generate insights based on the persona and job context.
        
        Text: {request.text}
        Persona: {request.persona}
        Job to be done: {request.job_to_be_done}
        Document Context: {request.document_context or "None"}
        
        Generate insights in the following JSON format:
        {{
            "insights": [
                {{
                    "type": "takeaway|fact|contradiction|connection|info|error",
                    "content": "insight description"
                }}
            ]
        }}
        """
        
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Parse JSON response
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        
        insights_result = json.loads(response_text.strip())
        return insights_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate insights: {str(e)}")

@app.post("/insights/generate")
async def generate_insights_from_query(request: Dict[str, Any]):
    """Generate insights from a query and passages"""
    try:
        query = request.get("query", "")
        passages = request.get("passages", [])
        
        if not query:
            raise HTTPException(status_code=400, detail="Query is required")
        
        if not passages:
            raise HTTPException(status_code=400, detail="At least one passage is required")
        
        # Combine passages into a single text
        combined_text = "\n\n".join(passages)
        
        # Use Gemini to generate insights
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        prompt = f"""
        Analyze the following query and passages to generate insights.
        
        Query: {query}
        Passages: {combined_text}
        
        Generate insights in the following JSON format:
        {{
            "query": "{query}",
            "insights": [
                {{
                    "type": "takeaway|fact|contradiction|connection|info|error",
                    "content": "insight description",
                    "relevance_score": 0.85,
                    "source_passage": "which passage this insight comes from"
                }}
            ],
            "summary": "Overall summary of insights",
            "key_themes": ["theme1", "theme2", "theme3"],
            "recommendations": [
                {{
                    "action": "recommended action",
                    "priority": "high|medium|low",
                    "rationale": "why this action is recommended"
                }}
            ]
        }}
        """
        
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Parse JSON response
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        
        insights_result = json.loads(response_text.strip())
        return insights_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate insights: {str(e)}")

@app.post("/comprehensive-insights")
async def generate_comprehensive_insights(request: InsightRequest):
    """Generate comprehensive insights with web facts and analysis"""
    try:
        # Use Gemini to generate comprehensive insights
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        prompt = f"""
        Generate comprehensive insights for the following text, considering the persona and job context.
        
        Text: {request.text}
        Persona: {request.persona}
        Job to be done: {request.job_to_be_done}
        Document Context: {request.document_context or "None"}
        
        Generate comprehensive analysis in the following JSON format:
        {{
            "insights": [
                {{
                    "type": "takeaway|fact|contradiction|connection|info|error",
                    "content": "insight description"
                }}
            ],
            "persona_insights": [
                {{
                    "type": "relevance|action|skill",
                    "content": "persona-specific insight"
                }}
            ],
            "topic_analysis": {{
                "main_themes": "main themes identified",
                "trending_topics": "trending topics related",
                "research_opportunities": "research opportunities"
            }},
            "web_facts": [
                {{
                    "type": "fact type",
                    "query": "search query",
                    "description": "fact description"
                }}
            ],
            "keywords": ["keyword1", "keyword2"],
            "search_queries": ["search query 1", "search query 2"]
        }}
        """
        
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Parse JSON response
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        
        comprehensive_result = json.loads(response_text.strip())
        return comprehensive_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate comprehensive insights: {str(e)}")



@app.post("/define-term")
async def define_term(request: DefineTermRequest):
    """Define terms in context"""
    try:
        term = request.term
        context = request.context
        
        if not term:
            raise HTTPException(status_code=400, detail="Term is required")
        
        # Use Gemini to define term
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        prompt = f"""
        Define the term "{term}" in the context of: {context}
        
        Provide a clear, concise definition that would be helpful for someone reading this context.
        """
        
        response = model.generate_content(prompt)
        definition = response.text.strip()
        
        return {
            "definition": definition
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to define term: {str(e)}")

@app.get("/library/documents")
async def get_library_documents(
    persona: Optional[str] = Query(None),
    job_to_be_done: Optional[str] = Query(None)
):
    """Get documents filtered by persona/job"""
    try:
        documents = list(documents_db.values())
        
        # Filter by persona if provided
        if persona:
            # This is a simple filter - in production you'd want more sophisticated filtering
            documents = [doc for doc in documents if persona.lower() in doc.get("title", "").lower()]
        
        # Filter by job if provided
        if job_to_be_done:
            # This is a simple filter - in production you'd want more sophisticated filtering
            documents = [doc for doc in documents if job_to_be_done.lower() in doc.get("title", "").lower()]
        
        return documents
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve library documents: {str(e)}")

@app.get("/library/personas")
async def get_personas():
    """Get available personas"""
    try:
        return list(personas_db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve personas: {str(e)}")

@app.post("/reading-progress")
async def track_reading_progress(
    doc_id: str = Form(...),
    current_page: int = Form(...),
    total_pages: int = Form(...),
    time_spent: int = Form(...)
):
    """Track reading progress"""
    try:
        if doc_id not in documents_db:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Calculate progress
        progress_percentage = (current_page / total_pages) * 100 if total_pages > 0 else 0
        time_spent_minutes = time_spent / 60  # Assuming time_spent is in seconds
        
        # Estimate remaining time (simple calculation)
        if progress_percentage > 0:
            estimated_total_minutes = time_spent_minutes / (progress_percentage / 100)
            estimated_remaining_minutes = estimated_total_minutes - time_spent_minutes
        else:
            estimated_total_minutes = 0
            estimated_remaining_minutes = 0
        
        # Store progress
        reading_progress_db[doc_id] = {
            "current_page": current_page,
            "total_pages": total_pages,
            "time_spent": time_spent,
            "progress_percentage": progress_percentage,
            "last_updated": datetime.now().isoformat()
        }
        
        return {
            "progress_percentage": progress_percentage,
            "time_spent_minutes": time_spent_minutes,
            "estimated_remaining_minutes": estimated_remaining_minutes,
            "estimated_total_minutes": estimated_total_minutes
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to track reading progress: {str(e)}")

@app.get("/pdf/{doc_id}")
async def get_pdf(doc_id: str):
    """Get PDF file for viewing"""
    try:
        print(f"🔍 PDF request for doc_id: {doc_id}")
        print(f"📚 Available documents in documents_db: {list(documents_db.keys())}")
        
        if doc_id not in documents_db:
            print(f"❌ Document {doc_id} not found in documents_db")
            raise HTTPException(status_code=404, detail="Document not found")
        
        doc = documents_db[doc_id]
        file_path = doc["file_path"]
        print(f"📄 File path: {file_path}")
        print(f"📄 Document info: {doc}")
        
        if not os.path.exists(file_path):
            print(f"❌ File not found at path: {file_path}")
            raise HTTPException(status_code=404, detail="File not found")
        
        print(f"✅ Serving PDF file: {file_path}")
        return FileResponse(file_path, media_type="application/pdf")
        
    except Exception as e:
        print(f"❌ Error serving PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve PDF: {str(e)}")

@app.get("/audio/{filename}")
async def get_audio(filename: str):
    """Get generated audio files"""
    try:
        # First try the audio directory
        audio_path = os.path.join("audio", filename)
        
        if os.path.exists(audio_path):
            return FileResponse(audio_path, media_type="audio/mpeg")
        
        # If not found in audio directory, try the project root
        file_path = os.path.join(os.path.dirname(__file__), filename)
        
        if os.path.exists(file_path):
            return FileResponse(file_path, media_type="audio/mpeg", filename=filename)
        else:
            raise HTTPException(status_code=404, detail="Audio file not found")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve audio: {str(e)}")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Debug endpoint to check documents_db
@app.get("/debug/documents")
async def debug_documents():
    """Debug endpoint to check documents_db contents"""
    return {
        "documents_count": len(documents_db),
        "document_ids": list(documents_db.keys()),
        "documents": documents_db
    }

# Debug endpoint to add a test document
@app.post("/debug/add-test-document")
async def add_test_document():
    """Add a test document to documents_db for testing"""
    try:
        # Find a PDF file in the documents directory
        documents_dir = "documents"
        pdf_files = [f for f in os.listdir(documents_dir) if f.endswith('.pdf')]
        
        if not pdf_files:
            raise HTTPException(status_code=404, detail="No PDF files found in documents directory")
        
        # Use the first PDF file
        pdf_filename = pdf_files[0]
        pdf_path = os.path.join(documents_dir, pdf_filename)
        
        # Create document metadata
        metadata = get_document_metadata(pdf_path, pdf_filename)
        if not metadata:
            raise HTTPException(status_code=500, detail="Failed to extract metadata from PDF")
        
        # Override the ID to match the one from the error
        test_doc_id = "7b6dd023-3d8f-4574-969e-caa4808e52fa"
        metadata["id"] = test_doc_id
        
        # Add to documents_db
        documents_db[test_doc_id] = metadata
        
        return {
            "message": "Test document added successfully",
            "document_id": test_doc_id,
            "document": metadata
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add test document: {str(e)}")

# Debug endpoint to reload all documents from directory
@app.post("/debug/reload-documents")
async def reload_documents():
    """Reload all documents from the documents directory into documents_db"""
    try:
        # Clear existing documents_db
        documents_db.clear()
        
        # Reinitialize documents_db
        initialize_documents_db()
        
        return {
            "message": "Documents reloaded successfully",
            "documents_count": len(documents_db),
            "document_ids": list(documents_db.keys())
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reload documents: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



@app.post("/generate-podcast")
def generate_podcast_endpoint(request: PodcastRequest):
    """
    Endpoint for podcast generation pipeline.
    """
    success = generate_podcast(request.query, request.output_filename)
    if success:
        return {
            "status": "success",
            "message": "Podcast generated successfully",
            "file": request.output_filename
        }
    else:
        return {
            "status": "error",
            "message": "Podcast generation failed"
        }


@app.get("/download-podcast/{filename}")
def download_podcast(filename: str):
    """
    Download the generated podcast file.
    """
    file_path = filename
    return FileResponse(path=file_path, filename=filename, media_type="audio/mpeg")

@app.post("/related-sections")
async def get_related_sections(
    document_ids: List[str] = Form(...),
    current_page: int = Form(...),
    current_section: str = Form(...),
    persona: str = Form(...),
    job_to_be_done: str = Form(...)
):
    """Get related sections from documents using enhanced HARSHALADOBE logic"""
    try:
        print(f"🔍 Finding related sections for page {current_page}, section: {current_section}")
        print(f"👤 Persona: {persona}, Job: {job_to_be_done}")
        print(f"📚 Document IDs: {document_ids}")
        
        # Get all sections from the documents using semantic search
        query = f"{current_section} {persona} {job_to_be_done}"
        search_results = perform_search(query, k=20)  # Get more results to work with
        
        if not search_results:
            print("⚠️ No search results found")
            return {
                "related_sections": []
            }
        
        # Convert search results to section format for enhanced analysis
        all_sections = []
        for result in search_results:
            # Filter by document IDs if provided
            if document_ids:
                source_file = result.get('source', '')
                if not any(doc_id in source_file for doc_id in document_ids):
                    continue
            
            section = {
                "document": result.get("source", "Unknown Document").replace('.pdf', '').replace('.docx', '').replace('.txt', ''),
                "section_title": result.get("passage", "")[:100] + "...",
                "page_number": result.get("page", 1),
                "relevance_score": result.get("similarity_score", 0.5),
                "text": result.get("passage", "")
            }
            all_sections.append(section)
        
        print(f"📋 Found {len(all_sections)} sections for enhanced analysis")
        
        # Use the enhanced related sections logic from HARSHALADOBE
        related_sections = find_related_sections_enhanced(
            current_page=current_page,
            current_section=current_section,
            persona=persona,
            job=job_to_be_done,
            all_sections=all_sections,
            limit=5
        )
        
        print(f"✅ Found {len(related_sections)} related sections")
        
        return {
            "related_sections": related_sections
        }
        
    except Exception as e:
        print(f"❌ Error in related sections: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get related sections: {str(e)}")

@app.post("/podcast")
async def generate_podcast_endpoint(
    text: str = Form(...),
    related_sections: List[str] = Form(...),
    insights: List[str] = Form(...)
):
    """Generate podcast from text and insights"""
    try:
        # Combine text with related sections and insights
        full_content = f"{text}\n\nRelated Sections:\n" + "\n".join(related_sections)
        full_content += f"\n\nInsights:\n" + "\n".join(insights)
        
        # Generate podcast using the existing function
        output_filename = f"podcast_{uuid.uuid4()}.mp3"
        success = generate_podcast(full_content, output_filename)
        
        if success:
            return {
                "script": full_content,
                "audio_url": f"/audio/{output_filename}"
            }
        else:
            raise HTTPException(status_code=500, detail="Podcast generation failed")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate podcast: {str(e)}")

@app.post("/simplify")
async def simplify_text_endpoint(request: SimplifyTextRequest):
    """Simplify text difficulty using AI"""
    try:
        text = request.text
        if not text or not text.strip():
            raise HTTPException(status_code=400, detail="Text is required")
        
        # Use Gemini to simplify text
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        prompt = f"""
        Simplify the following text to make it easier to understand while maintaining the core meaning:
        
        {text}
        
        Return only the simplified text without any additional formatting or explanations.
        """
        
        response = model.generate_content(prompt)
        simplified_text = response.text.strip()
        
        return {
            "text": simplified_text,
            "original": text
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions (like 400 for empty text)
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to simplify text: {str(e)}")

@app.get("/library/jobs")
async def get_jobs():
    """Get available jobs"""
    try:
        # This would typically come from a database
        # For now, return some sample jobs
        sample_jobs = [
            "Research and Analysis",
            "Content Creation",
            "Decision Making",
            "Problem Solving",
            "Learning and Development",
            "Strategic Planning"
        ]
        return sample_jobs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve jobs: {str(e)}")

@app.get("/cross-connections/{doc_id}")
async def get_cross_connections(
    doc_id: str,
    current_page: Optional[int] = Query(1, description="Current page number"),
    current_section: Optional[str] = Query("", description="Current section or selected text"),
    persona: Optional[str] = Query("", description="User persona"),
    job_to_be_done: Optional[str] = Query("", description="Job to be done")
):
    """Get related sections for a document (simplified connection endpoint)"""
    try:
        if doc_id not in documents_db:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Get the current document
        doc = documents_db[doc_id]
        doc_title = doc.get("title", "")
        doc_content = doc.get("content", "")
        
        # Extract selected text/section for analysis
        selected_text = current_section if current_section else doc_title
        if not selected_text and doc_content:
            # If no section provided, use first 200 characters of content
            selected_text = doc_content[:200]
        
        print(f"🔍 Related sections analysis for document: {doc_id}")
        print(f"📄 Selected text: {selected_text[:100]}...")
        print(f"👤 Persona: {persona}, Job: {job_to_be_done}")
        
        related_sections = []
        
        # Get related sections using the enhanced logic
        if selected_text and persona and job_to_be_done:
            try:
                print(f"🔄 Finding related sections for selected text")
                
                # Perform semantic search for related sections
                section_query = f"{selected_text} {persona} {job_to_be_done}"
                print(f"🔍 Search query: {section_query}")
                
                section_results = perform_search(section_query, k=15)
                print(f"🔍 Search returned: {len(section_results) if section_results else 0} results")
                
                if section_results:
                    # Convert to section format and filter for uniqueness
                    temp_sections = []
                    seen_documents = set()
                    seen_content_hashes = set()
                    
                    for i, result in enumerate(section_results):
                        try:
                            print(f"🔍 Processing result {i+1}: {result.get('source', 'Unknown')}")
                            
                            if result.get("document") != doc_id:  # Exclude current document
                                document_name = result.get("source", "Unknown Document").replace('.pdf', '').replace('.docx', '').replace('.txt', '')
                                content_text = result.get("passage", "")
                                
                                # Create a simple content hash for deduplication
                                content_hash = hash(content_text[:200])  # Use first 200 chars for hash
                                
                                # Skip if we've already seen this document or very similar content
                                if document_name in seen_documents or content_hash in seen_content_hashes:
                                    print(f"⏭️ Skipping duplicate: {document_name}")
                                    continue
                                
                                section = {
                                    "document": document_name,
                                    "section_title": content_text[:100] + "..." if len(content_text) > 100 else content_text,
                                    "page_number": result.get("page", 1),
                                    "relevance_score": result.get("similarity_score", 0.5),
                                    "text": content_text,
                                    "explanation": f"Related to selected text: '{selected_text[:50]}...'",
                                    "relationship_type": "content_similarity",
                                    "key_concepts": []
                                }
                                temp_sections.append(section)
                                seen_documents.add(document_name)
                                seen_content_hashes.add(content_hash)
                                print(f"✅ Added section from: {document_name}")
                        except Exception as result_error:
                            print(f"❌ Error processing result {i+1}: {result_error}")
                            continue
                    
                    # Sort by relevance and take unique sections (no fixed limit)
                    temp_sections.sort(key=lambda x: x["relevance_score"], reverse=True)
                    related_sections = temp_sections  # Take all unique sections
                    
                    print(f"✅ Found {len(related_sections)} unique related sections")
                else:
                    print("⚠️ No related sections found")
                    
            except Exception as section_error:
                print(f"❌ Error in related sections analysis: {section_error}")
                import traceback
                traceback.print_exc()
                related_sections = []
        
        return {
            "document_id": doc_id,
            "document_title": doc_title,
            "selected_text": selected_text,
            "related_sections": related_sections,
            "total_related_sections": len(related_sections),
            "analysis_summary": {
                "sections_found": len(related_sections),
                "average_relevance": sum([s["relevance_score"] for s in related_sections]) / len(related_sections) if related_sections else 0,
                "top_sources": list(set([s["document"] for s in related_sections])),
                "relevance_distribution": {
                    "high": len([s for s in related_sections if s["relevance_score"] > 0.7]),
                    "medium": len([s for s in related_sections if 0.4 <= s["relevance_score"] <= 0.7]),
                    "low": len([s for s in related_sections if s["relevance_score"] < 0.4])
                }
            },
            "metadata": {
                "analysis_timestamp": datetime.now().isoformat(),
                "section_query_used": f"{selected_text[:100]}... {persona} {job_to_be_done}" if selected_text and persona and job_to_be_done else "No section analysis",
                "analysis_type": "related_sections_only"
            }
        }
        
    except Exception as e:
        print(f"❌ Cross connections error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to get cross connections: {str(e)}")

@app.post("/strategic-insights")
async def generate_strategic_insights(request: InsightRequest):
    """Generate strategic insights from text content"""
    try:
        # Use Gemini to generate strategic insights
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        prompt = f"""
        Generate strategic insights for the following text, considering the persona and job context.
        
        Text: {request.text}
        Persona: {request.persona}
        Job to be done: {request.job_to_be_done}
        Document Context: {request.document_context or "None"}
        
        Generate strategic analysis in the following JSON format:
        {{
            "strategic_insights": {{
                "opportunities": [
                    {{
                        "insight": "opportunity description",
                        "priority": "high|medium|low",
                        "timeframe": "immediate|short-term|long-term"
                    }}
                ],
                "critical_decisions": [
                    {{
                        "decision": "decision description",
                        "factors": ["factor1", "factor2"],
                        "urgency": "high|medium|low"
                    }}
                ],
                "risks": [
                    {{
                        "risk": "risk description",
                        "impact": "high|medium|low",
                        "mitigation": "mitigation strategy"
                    }}
                ],
                "action_items": [
                    {{
                        "action": "action description",
                        "priority": "high|medium|low",
                        "effort": "low|medium|high"
                    }}
                ],
                "knowledge_gaps": [
                    {{
                        "gap": "gap description",
                        "importance": "high|medium|low",
                        "source_suggestions": ["suggestion1", "suggestion2"]
                    }}
                ],
                "strategic_context": {{
                    "relevance_to_role": "relevance description",
                    "business_impact": "impact description",
                    "competitive_advantage": "advantage description"
                }}
            }}
        }}
        """
        
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Parse JSON response
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        
        strategic_result = json.loads(response_text.strip())
        return strategic_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate strategic insights: {str(e)}")

@app.post("/contextual-analysis")
async def analyze_document_context(
    doc_id: str = Form(...),
    page_number: int = Form(...),
    section_text: str = Form(...)
):
    """Analyze document context for a specific section"""
    try:
        if doc_id not in documents_db:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Use Gemini to analyze context
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        prompt = f"""
        Analyze the following section from a document and provide contextual analysis.
        
        Document ID: {doc_id}
        Page Number: {page_number}
        Section Text: {section_text}
        
        Provide analysis in the following JSON format:
        {{
            "section_summary": "brief summary of the section",
            "contextual_significance": "why this section is important",
            "personal_relevance": "how this relates to the reader",
            "deeper_implications": ["implication1", "implication2"],
            "cross_references": ["reference1", "reference2"],
            "expert_perspective": "expert opinion on this section",
            "questions_to_consider": ["question1", "question2"],
            "next_steps": ["step1", "step2"],
            "confidence_score": 0.85
        }}
        """
        
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Parse JSON response
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        
        analysis_result = json.loads(response_text.strip())
        return analysis_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze document context: {str(e)}")

@app.post("/multi-document-insights")
async def generate_multi_document_insights(request: DocumentAnalysisRequest):
    """Generate insights across multiple documents"""
    try:
        # Use Gemini to generate multi-document insights
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        # Get document contents
        document_contents = []
        document_titles = []
        for doc_id in request.document_ids:
            if doc_id in documents_db:
                doc = documents_db[doc_id]
                document_contents.append(doc.get("content", ""))
                document_titles.append(doc.get("title", ""))
        
        combined_content = "\n\n".join(document_contents)
        
        prompt = f"""
        Analyze the following documents and generate comprehensive multi-document insights.
        
        Documents: {', '.join(document_titles)}
        Persona: {request.persona}
        Job to be done: {request.job_to_be_done}
        
        Combined Content: {combined_content[:2000]}...
        
        Generate insights in the following JSON format:
        {{
            "analyzed_documents": {len(document_titles)},
            "document_titles": {document_titles},
            "insights": {{
                "overarching_patterns": [
                    {{
                        "pattern": "pattern description",
                        "documents": ["doc1", "doc2"],
                        "evidence": ["evidence1", "evidence2"],
                        "significance": "why this pattern matters"
                    }}
                ],
                "contradictions": [
                    {{
                        "topic": "contradiction topic",
                        "doc1_position": "position in doc1",
                        "doc2_position": "position in doc2",
                        "doc1_evidence": "evidence from doc1",
                        "doc2_evidence": "evidence from doc2",
                        "impact": "impact of contradiction",
                        "resolution_suggestion": "how to resolve"
                    }}
                ],
                "knowledge_gaps": [
                    {{
                        "gap": "gap description",
                        "importance": "high|medium|low",
                        "impact_on_job": "how it affects the job",
                        "suggested_research": "what to research"
                    }}
                ],
                "synthesis_insights": [
                    {{
                        "insight": "synthesis insight",
                        "supporting_documents": ["doc1", "doc2"],
                        "implications": "what this means",
                        "confidence": 0.85
                    }}
                ],
                "actionable_recommendations": [
                    {{
                        "recommendation": "recommendation description",
                        "priority": "high|medium|low",
                        "timeframe": "immediate|short-term|long-term",
                        "based_on": "what this is based on",
                        "success_metrics": "how to measure success"
                    }}
                ]
            }}
        }}
        """
        
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Parse JSON response
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        
        multi_doc_result = json.loads(response_text.strip())
        return multi_doc_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate multi-document insights: {str(e)}")

# In-memory storage for highlights (replace with database in production)
highlights_db = {}

@app.post("/highlights")
async def add_highlight(highlight: Dict[str, Any]):
    """Add a highlight to a document"""
    try:
        document_name = highlight.get("documentName", "")
        if document_name not in highlights_db:
            highlights_db[document_name] = []
        
        highlights_db[document_name].append({
            "text": highlight.get("text", ""),
            "color": highlight.get("color", "yellow"),
            "page": highlight.get("page", 1),
            "documentName": document_name
        })
        
        return {"message": "Highlight added successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add highlight: {str(e)}")

@app.get("/highlights/{document_name}")
async def get_highlights(document_name: str):
    """Get highlights for a document"""
    try:
        decoded_name = document_name.replace("%20", " ")
        return highlights_db.get(decoded_name, [])
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get highlights: {str(e)}")

@app.get("/download-highlighted/{document_name}")
async def download_highlighted_pdf(document_name: str):
    """Download highlighted PDF (placeholder - would need PDF manipulation library)"""
    try:
        decoded_name = document_name.replace("%20", " ")
        
        # Find the document in the database
        doc_id = None
        for d_id, doc in documents_db.items():
            if doc.get("name", "") == decoded_name:
                doc_id = d_id
                break
        
        if not doc_id:
            raise HTTPException(status_code=404, detail="Document not found")
        
        doc = documents_db[doc_id]
        file_path = doc["file_path"]
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        # For now, return the original PDF
        # In a real implementation, you would add highlights to the PDF
        return FileResponse(file_path, media_type="application/pdf", filename=f"highlighted_{decoded_name}")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download highlighted PDF: {str(e)}")

# Create audio directory if it doesn't exist
os.makedirs("audio", exist_ok=True)

def cleanup_file(path: str):
    """A helper function to delete a file."""
    if os.path.exists(path):
        os.remove(path)
        print(f"🧹 Cleaned up file: {path}")

@app.post("/podcast/generate")
async def generate_podcast_and_get_filename(query: str = Form(...)):
    """
    Generates a podcast from a query and returns the filename.
    The file can be downloaded later using the /audio/{filename} endpoint.
    """
    try:
        # Create a unique filename to avoid conflicts
        # All generated audio will be stored in the 'audio' directory
        unique_id = uuid.uuid4()
        output_filename = os.path.join("audio", f"podcast_{unique_id}.mp3")
        
        print(f"🎙️ Generating podcast for query: '{query}' -> {output_filename}")
        
        # Call the main generation function from app.py
        # Note: We are now capturing two return values
        success, audio_files = generate_podcast(query, output_filename)
        
        if not success or not audio_files:
            raise HTTPException(status_code=500, detail="Podcast generation failed at the audio stage.")

        # The final, combined filename is the first (and likely only) item in the list
        final_filename = os.path.basename(audio_files[0])
        
        return {
            "status": "success",
            "message": "Podcast generated successfully.",
            "filename": final_filename,
            "download_url": f"/audio/{final_filename}"
        }

    except Exception as e:
        print(f"❌ Error during podcast generation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/podcast/download")
async def generate_and_download_podcast(query: str, background_tasks: BackgroundTasks):
    """
    Generates a podcast from a query and streams the audio file for direct download.
    The server file is automatically cleaned up after the download is complete.
    """
    try:
        # Create a unique filename for temporary storage
        unique_id = uuid.uuid4()
        output_filename = os.path.join("audio", f"podcast_{unique_id}.mp3")
        
        print(f"⬇️ Generating podcast for immediate download. Query: '{query}'")

        # Call the main generation function
        success, audio_files = generate_podcast(query, output_filename)

        if not success or not audio_files:
            raise HTTPException(status_code=500, detail="Failed to generate podcast audio.")

        final_filepath = audio_files[0]
        
        # Add a background task to delete the file after the response is sent
        background_tasks.add_task(cleanup_file, final_filepath)

        # Return the audio file as a streaming response
        return FileResponse(
            path=final_filepath,
            media_type="audio/mpeg",
            filename=f"podcast_for_{query[:20].replace(' ', '_')}.mp3" # A nice filename for the user
        )

    except Exception as e:
        print(f"❌ Error during podcast download generation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/audio/{filename}")
async def get_audio_file(filename: str):
    """
    Serve audio files for download.
    """
    try:
        file_path = os.path.join("audio", filename)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Audio file not found")
        
        return FileResponse(
            path=file_path,
            media_type="audio/mpeg",
            filename=filename
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to serve audio file: {str(e)}")


# app.include_router(generate_insights.router, prefix="/insights", tags=["Insights"])  # Removed - router doesn't exist
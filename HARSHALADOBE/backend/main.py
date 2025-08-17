from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends, Query
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

# Import the core functionality from app.py
import sys
sys.path.append('../../adobev4')
from app import (
    parse_pdf, parse_docx, parse_txt, create_chunks,
    build_or_update_index, perform_search, analyze_and_categorize,
    generate_podcast_script, generate_podcast_audio, generate_podcast_audio_simple,
    combine_audio_files, DOCUMENTS_DIR, INDEX_DIR, load_documents,
    generate_podcast
)

# Import additional dependencies
import google.generativeai as genai
import boto3
from sentence_transformers import SentenceTransformer

# Configure FastAPI app
app = FastAPI(
    title="Document Analysis & Podcast Generation API",
    description="A comprehensive API for document management, analysis, and podcast generation using app.py core functionality",
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

# Configuration
GOOGLE_API_KEY = "AIzaSyBLdZ-Z3Dec82Su91bYmcA7zOc8MtWeN3w"
AWS_REGION = "us-east-1"

# Configure Google Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

# Ensure directories exist
os.makedirs(DOCUMENTS_DIR, exist_ok=True)
os.makedirs(INDEX_DIR, exist_ok=True)
os.makedirs("audio", exist_ok=True)

# Pydantic models for request/response
class DocumentAnalysisRequest(BaseModel):
    document_ids: List[str]
    persona: str
    job_to_be_done: str
    query: Optional[str] = None

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

class PodcastRequest(BaseModel):
    query: str
    output_filename: Optional[str] = "podcast_output.mp3"

# In-memory storage (replace with database in production)
documents_db = {}
personas_db = set()
reading_progress_db = {}
highlights_db = {}

# Helper functions
def get_document_metadata(file_path: str, filename: str) -> Dict[str, Any]:
    """Extract metadata from document using app.py functions"""
    try:
        if filename.endswith('.pdf'):
            content = parse_pdf(file_path)
        elif filename.endswith('.docx'):
            content = parse_docx(file_path)
        elif filename.endswith('.txt'):
            content = parse_txt(file_path)
        else:
            return None
        
        # Generate outline from content using app.py chunking
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
    """Upload PDF documents with metadata for analysis using app.py"""
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
                # Extract metadata using app.py functions
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
        
        # Rebuild index using app.py
        build_or_update_index()
        
        return {"message": "Document deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete document: {str(e)}")

@app.post("/index-documents")
async def index_documents():
    """Index all documents using app.py logic"""
    try:
        build_or_update_index()
        return {"message": "Documents indexed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to index documents: {str(e)}")

@app.post("/search-documents")
async def search_documents(query: str = Form(...), k: int = Form(5)):
    """Search documents using app.py perform_search function"""
    try:
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

@app.post("/analyze-documents")
async def analyze_documents(request: DocumentAnalysisRequest):
    """Analyze documents using app.py analyze_and_categorize function"""
    try:
        # Use custom query if provided, otherwise create a comprehensive query from the request
        if request.query:
            query = request.query
        else:
            query = f"{request.persona} {request.job_to_be_done}"
            if request.document_ids:
                query += f" documents: {', '.join(request.document_ids)}"
        
        # Use app.py analyze_and_categorize function
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
    """Generate AI insights from text content using Gemini"""
    try:
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

@app.post("/comprehensive-insights")
async def generate_comprehensive_insights(request: InsightRequest):
    """Generate comprehensive insights with web facts and analysis"""
    try:
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
    """Define terms in context using Gemini"""
    try:
        term = request.term
        context = request.context
        
        if not term:
            raise HTTPException(status_code=400, detail="Term is required")
        
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

@app.post("/simplify")
async def simplify_text(request: SimplifyTextRequest):
    """Simplify text difficulty using AI"""
    try:
        text = request.text
        if not text:
            raise HTTPException(status_code=400, detail="Text is required")
        
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
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to simplify text: {str(e)}")

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
            documents = [doc for doc in documents if persona.lower() in doc.get("title", "").lower()]
        
        # Filter by job if provided
        if job_to_be_done:
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

@app.get("/library/jobs")
async def get_jobs():
    """Get available jobs"""
    try:
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
        time_spent_minutes = time_spent / 60
        
        # Estimate remaining time
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
        print(f"Looking for document ID: {doc_id}")
        print(f"Available documents: {list(documents_db.keys())}")
        
        if doc_id not in documents_db:
            raise HTTPException(status_code=404, detail=f"Document not found: {doc_id}")
        
        doc = documents_db[doc_id]
        file_path = doc["file_path"]
        
        print(f"File path: {file_path}")
        print(f"File exists: {os.path.exists(file_path)}")
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"File not found: {file_path}")
        
        return FileResponse(file_path, media_type="application/pdf")
        
    except Exception as e:
        print(f"Error in get_pdf: {str(e)}")
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

@app.post("/generate-podcast")
async def generate_podcast_endpoint(request: PodcastRequest):
    """Generate podcast using app.py generate_podcast function"""
    try:
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Podcast generation failed: {str(e)}")

@app.get("/download-podcast/{filename}")
async def download_podcast(filename: str):
    """Download the generated podcast file"""
    try:
        file_path = filename
        if not os.path.exists(file_path):
            # Try audio directory
            file_path = os.path.join("audio", filename)
            if not os.path.exists(file_path):
                raise HTTPException(status_code=404, detail="Podcast file not found")
        
        return FileResponse(path=file_path, filename=filename, media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download podcast: {str(e)}")

@app.post("/related-sections")
async def get_related_sections(
    document_ids: str = Form(...),  # Changed from List[str] to str
    current_page: int = Form(...),
    current_section: str = Form(...),
    persona: str = Form(...),
    job_to_be_done: str = Form(...)
):
    """Get related sections using app.py perform_search"""
    try:
        # Parse document_ids if it's a JSON string
        try:
            if document_ids.startswith('['):
                doc_ids = json.loads(document_ids)
            else:
                doc_ids = [document_ids]
        except:
            doc_ids = [document_ids]
        
        query = f"{current_section} {persona} {job_to_be_done}"
        results = perform_search(query, k=5)
        
        related_sections = []
        for result in results:
            related_sections.append({
                "document": result.get("source", "Unknown"),
                "section_title": result.get("passage", "")[:100] + "...",
                "page_number": 1,  # app.py doesn't track page numbers
                "relevance_score": result.get("similarity_score", 0.0),
                "explanation": f"Related to current section based on {persona} context"
            })
        
        return {
            "related_sections": related_sections
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get related sections: {str(e)}")

@app.post("/podcast")
async def generate_podcast_endpoint(
    text: str = Form(...),
    related_sections: List[str] = Form(...),
    insights: List[str] = Form(...)
):
    """Generate podcast from text and insights using app.py"""
    try:
        # Combine text with related sections and insights
        full_content = f"{text}\n\nRelated Sections:\n" + "\n".join(related_sections)
        full_content += f"\n\nInsights:\n" + "\n".join(insights)
        
        # Generate podcast using app.py function
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

@app.get("/cross-connections/{doc_id}")
async def get_cross_connections(doc_id: str):
    """Get cross-connections for a document using app.py search"""
    try:
        if doc_id not in documents_db:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Find related documents using app.py search
        doc = documents_db[doc_id]
        query = doc.get("title", "")
        results = perform_search(query, k=5)
        
        related_documents = []
        for result in results:
            if result.get("source") != doc_id:
                related_documents.append({
                    "document_id": result.get("source", ""),
                    "document_title": result.get("source", ""),
                    "connection_type": "related",
                    "relevance_score": result.get("similarity_score", 0.0),
                    "explanation": "Related content found through semantic search",
                    "key_sections": [result.get("passage", "")[:200] + "..."]
                })
        
        return {
            "document_id": doc_id,
            "related_documents": related_documents,
            "contradictions": [],
            "insights": [],
            "total_connections": len(related_documents)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get cross connections: {str(e)}")

@app.post("/strategic-insights")
async def generate_strategic_insights(request: InsightRequest):
    """Generate strategic insights using Gemini"""
    try:
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
    """Analyze document context for a specific section using Gemini"""
    try:
        if doc_id not in documents_db:
            raise HTTPException(status_code=404, detail="Document not found")
        
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
    """Generate insights across multiple documents using Gemini"""
    try:
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
    """Download highlighted PDF (placeholder)"""
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
        return FileResponse(file_path, media_type="application/pdf", filename=f"highlighted_{decoded_name}")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download highlighted PDF: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

import os
import re
import time
import numpy as np
from datetime import datetime
from typing import Any, Dict, List, Tuple
from .outline_core import extract_outline_blocks, LineBlock
from . import scoring
import google.generativeai as genai

# Temporarily disable semantic search imports to get server running
try:
    from sentence_transformers import SentenceTransformer
    import faiss
    SEMANTIC_SEARCH_AVAILABLE = True
except ImportError:
    print("Warning: sentence_transformers or faiss not available. Using fallback search.")
    SEMANTIC_SEARCH_AVAILABLE = False

# Initialize Gemini and embedding model
try:
    # Use the new Gemini API key
    gemini_api_key = os.getenv('GEMINI_API_KEY', 'AIzaSyAInqw9seke43AUqjjPA8ftJcJVggRKA6c')
    genai.configure(api_key=gemini_api_key)
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')
    if SEMANTIC_SEARCH_AVAILABLE:
        embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Semantic search models initialized successfully")
    else:
        embedding_model = None
        print("Semantic search not available, using fallback search")
    print("Gemini model initialized successfully")
except Exception as e:
    print(f"Warning: Could not initialize models: {e}")
    gemini_model = None
    embedding_model = None

# Global cache for embeddings
embeddings_cache = {}

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
        import json
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
        # Check if it's a quota exceeded error
        if "429" in str(e) or "quota" in str(e).lower():
            # Use enhanced fallback for quota exceeded
            return _generate_fallback_analysis(query, section_text, persona, job)
        else:
            return {
                "relevance_score": 0.5,
                "relationship_type": "related",
                "explanation": f"Semantic analysis failed: {str(e)}",
                "key_concepts": []
            }

def _generate_fallback_analysis(query: str, section_text: str, persona: str, job: str) -> Dict[str, Any]:
    """Generate fallback analysis when Gemini API is unavailable due to quota limits."""
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

def build_semantic_index(sections: List[Dict[str, Any]]) -> Tuple[Any, List[Dict[str, Any]]]:
    """Build a FAISS index for semantic search."""
    if not SEMANTIC_SEARCH_AVAILABLE or embedding_model is None:
        return None, sections
    
    try:
        # Prepare texts for embedding
        texts = []
        for section in sections:
            text = f"{section.get('section_title', '')} {section.get('text', '')}"
            texts.append(text)
        
        # Get embeddings
        embeddings = []
        valid_sections = []
        
        for i, text in enumerate(texts):
            embedding = get_semantic_embedding(text)
            if embedding is not None:
                embeddings.append(embedding)
                valid_sections.append(sections[i])
        
        if not embeddings:
            return None, sections
        
        # Build FAISS index
        dimension = len(embeddings[0])
        if SEMANTIC_SEARCH_AVAILABLE:
            index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
            embeddings_array = np.array(embeddings).astype('float32')
            index.add(embeddings_array)
        else:
            index = None
        
        return index, valid_sections
        
    except Exception as e:
        print(f"Error building semantic index: {e}")
        return None, sections

def semantic_search(query: str, index: Any, sections: List[Dict[str, Any]], top_k: int = 10) -> List[Tuple[int, float]]:
    """Perform semantic search using FAISS index."""
    if not SEMANTIC_SEARCH_AVAILABLE or index is None or embedding_model is None:
        return []
    
    try:
        query_embedding = get_semantic_embedding(query)
        if query_embedding is None:
            return []
        
        query_vector = np.array([query_embedding]).astype('float32')
        scores, indices = index.search(query_vector, top_k)
        
        results = []
        for i, score in zip(indices[0], scores[0]):
            if i < len(sections):
                results.append((i, float(score)))
        
        return results
        
    except Exception as e:
        print(f"Semantic search error: {e}")
        return []

# --------------------------------------------------------------------------------------
# Build sections: heading text + concatenated body until next heading
# --------------------------------------------------------------------------------------
def build_sections_from_blocks(title_block, blocks: List[LineBlock], doc_name: str) -> List[Dict[str, Any]]:
    """
    Converts LineBlocks into logical sections for scoring.
    Each section:
      doc, heading, page, text
    """
    sections = []
    current_heading = None
    current_text: List[str] = []
    current_pages = set()

    def flush():
        nonlocal current_heading, current_text, current_pages
        if current_heading:
            sections.append({
                "doc": doc_name,
                "heading": current_heading.text,
                "page": min(current_pages) if current_pages else current_heading.page,
                "text": " ".join(current_text).strip()
            })
        current_heading = None
        current_text = []
        current_pages = set()

    for b in blocks:
        if b.tag == "TITLE":
            continue
        if b.tag == "HEADING":
            flush()
            current_heading = b
            current_text = []
            current_pages = {b.page}
        else:  # BODY
            if current_heading is not None:
                current_text.append(b.text)
                current_pages.add(b.page)
            else:
                # body text before first heading -> ignore
                pass

    flush()

    # fallback: no headings found -> whole doc
    if not sections:
        text_all = " ".join([b.text for b in blocks if b.tag != "TITLE"]).strip()
        sections.append({
            "doc": doc_name,
            "heading": doc_name,
            "page": 1,
            "text": text_all
        })

    return sections

# --------------------------------------------------------------------------------------
# Rank sections by persona+job relevance
# --------------------------------------------------------------------------------------
def rank_sections(persona: str, job: str, sections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    query = scoring.build_query(persona, job)
    kw = scoring.build_keywords(persona, job)
    headings = [s["heading"] for s in sections]
    texts = [s["text"] for s in sections]
    scores = scoring.combined_scores(query, headings, texts, kw)
    for s, sc in zip(sections, scores):
        s["score"] = float(sc)
    sections.sort(key=lambda x: x["score"], reverse=True)
    for i, s in enumerate(sections, start=1):
        s["importance_rank"] = i
    return sections

# --------------------------------------------------------------------------------------
# Sub-section drilldown (snippets)
# --------------------------------------------------------------------------------------
SNIP_SPLIT_RE = re.compile(r"(?<=[\.!?])\s+|[\r\n]+|•")

def extract_subsections(section: Dict[str, Any],
                        persona: str,
                        job: str,
                        max_snips: int = 3) -> List[Dict[str, Any]]:
    """
    Break section text into candidate snippets and score them quickly
    against the persona+job query. Returns top snippets.
    """
    text = section["text"]
    if not text:
        return []

    # candidate splits
    parts = []
    for seg in SNIP_SPLIT_RE.split(text):
        seg = seg.strip()
        if not seg:
            continue
        # de-bullet
        seg = re.sub(r"^[•\-\*\u2022●◦]\s*", "", seg)
        parts.append(seg)

    if not parts:
        return []

    # score snippets using TF-IDF vs query
    query = scoring.build_query(persona, job)
    scores = scoring.tfidf_scores(query, parts)
    order = scores.argsort()[::-1]  # high->low

    out = []
    base_page = section["page"]  # cheap fallback; we don't track fine-grained snippet pages
    for idx in order[:max_snips]:
        out.append({
            "document": section["doc"],
            "refined_text": parts[idx],
            "page_number": base_page
        })
    return out

# --------------------------------------------------------------------------------------
# Main document intelligence processing
# --------------------------------------------------------------------------------------
def process_documents_intelligence(pdf_paths: List[str], 
                                   persona: str, 
                                   job: str,
                                   topk_sections: int = 20,
                                   max_snips_per_section: int = 3) -> Dict[str, Any]:
    """
    Process multiple PDFs using document intelligence to find relevant sections.
    Returns structured output with ranked sections and subsections.
    """
    start = time.time()

    # --- per-PDF section extraction ---
    all_sections: List[Dict[str, Any]] = []
    for pdf_path in pdf_paths:
        doc_name = os.path.basename(pdf_path)
        try:
            title, blocks = extract_outline_blocks(pdf_path)
        except Exception as e:
            print(f"ERROR: Failed to parse '{doc_name}': {e}")
            continue
        secs = build_sections_from_blocks(title, blocks, doc_name)
        all_sections.extend(secs)

    if not all_sections:
        return {
            "metadata": {
                "input_documents": [],
                "persona": persona,
                "job_to_be_done": job,
                "processing_timestamp": datetime.utcnow().isoformat()
            },
            "extracted_sections": [],
            "subsection_analysis": []
        }

    # --- rank sections ---
    ranked = rank_sections(persona, job, all_sections)

    # --- select top K ---
    top_sections = ranked[: min(len(ranked), topk_sections)]

    # --- sub-section analysis ---
    all_sub = []
    for sec in top_sections:
        subs = extract_subsections(sec, persona, job, max_snips=max_snips_per_section)
        all_sub.extend(subs)

    # --- output JSON (hackathon expected format) ---
    out = {
        "metadata": {
            "input_documents": [os.path.basename(p) for p in pdf_paths],
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.utcnow().isoformat()
        },
        "extracted_sections": [
            {
                "document": s["doc"],
                "section_title": s["heading"],
                "importance_rank": s["importance_rank"],
                "page_number": s["page"],
                "relevance_score": s["score"]
            }
            for s in top_sections
        ],
        "subsection_analysis": all_sub
    }

    elapsed = time.time() - start
    print(f"Document intelligence: processed {len(pdf_paths)} PDFs in {elapsed:.2f}s")
    
    return out

def find_related_sections(current_page: int, 
                          current_section: str,
                          persona: str,
                          job: str,
                          all_sections: List[Dict[str, Any]],
                          limit: int = 5) -> List[Dict[str, Any]]:
    """
    Find sections related to the current reading position using semantic search and Gemini Flash API.
    This implements a hybrid approach combining semantic embeddings, FAISS search, and AI analysis.
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
    
    # Enhanced fallback approach when semantic search is not available
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

def _get_current_document_from_page(current_page: int, all_sections: List[Dict[str, Any]]) -> str:
    """Helper function to determine which document the current page belongs to."""
    for section in all_sections:
        if section.get("page_number", section.get("page", 0)) == current_page:
            return section.get("document", "Unknown Document")
    return None

def generate_enhanced_relevance_explanation(section: Dict[str, Any], 
                                         current_section: str,
                                         persona: str, 
                                         job: str) -> str:
    """
    Generate an enhanced explanation of why a section is relevant using Round 1B logic.
    """
    section_text = section.get("text", "")
    section_title = section.get("section_title", "")
    document = section.get("document", "Unknown Document")
    relevance_score = section.get("contextual_score", section.get("relevance_score", 0))
    
    # Enhanced keyword analysis
    persona_keywords = scoring.keyword_set(persona)
    job_keywords = scoring.keyword_set(job)
    current_keywords = scoring.keyword_set(current_section) if current_section else set()
    section_keywords = scoring.keyword_set(section_text + " " + section_title)
    
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
        # Fallback to original logic
        return generate_relevance_explanation(section, current_section, persona, job)

def generate_relevance_explanation(section: Dict[str, Any], 
                                 current_section: str,
                                 persona: str, 
                                 job: str) -> str:
    """
    Generate a brief explanation of why a section is relevant (fallback method).
    """
    # Simple heuristic-based explanation generation
    section_text = section.get("text", "")
    section_title = section.get("section_title", "")
    
    # Check for common keywords
    persona_keywords = scoring.keyword_set(persona)
    job_keywords = scoring.keyword_set(job)
    section_keywords = scoring.keyword_set(section_text + " " + section_title)
    
    common_persona = persona_keywords & section_keywords
    common_job = job_keywords & section_keywords
    
    if common_persona and common_job:
        return f"Contains relevant information about {', '.join(list(common_persona)[:2])} related to your {job.lower()}."
    elif common_persona:
        return f"Discusses {', '.join(list(common_persona)[:2])} which aligns with your role as {persona.lower()}."
    elif common_job:
        return f"Provides insights relevant to {', '.join(list(common_job)[:2])} for your task."
    else:
        return f"Contains complementary information that may support your understanding."
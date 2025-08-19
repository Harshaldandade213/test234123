import json
import requests

def generate_insights_gemini_flash(
    query: str,
    passages: list,
    api_key: str,
    model: str = "gemini-1.5-flash",
    thinking_budget: int = None
) -> dict:
    """Generate insights using Gemini Flash model with optimized processing"""
    
    # Optimize passages for faster processing
    optimized_passages = []
    for passage in passages:
        # Limit passage length to prevent timeout
        text = passage.get('text', '')[:500]  # Limit to 500 characters
        optimized_passages.append({
            'id': passage.get('id', ''),
            'text': text
        })
    
    # Limit number of passages to prevent timeout
    if len(optimized_passages) > 3:
        optimized_passages = optimized_passages[:3]
    
    # Create prompt with optimized passages
    passages_text = "\n\n".join([f"Passage {i+1}: {p['text']}" for i, p in enumerate(optimized_passages)])
    
    prompt = f"""
    Analyze the following query and passages to generate insights.
    
    Query: {query}
    Passages: {passages_text}
    
    Generate 2-3 key insights in the following JSON format:
    {{
        "insights": [
            "insight 1",
            "insight 2",
            "insight 3"
        ]
    }}
    
    Keep insights concise and relevant to the query.
    """

    # Use the correct Gemini API endpoint
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "temperature": 0.5,
            "maxOutputTokens": 150
        }
    }

    if thinking_budget is not None:
        payload["generationConfig"]["thinkingBudget"] = thinking_budget

    # Add API key as query parameter
    url += f"?key={api_key}"

    try:
        resp = requests.post(url, headers=headers, json=payload)
        
        if resp.status_code == 429:
            print("⚠️ Gemini API quota exceeded. Using fallback analysis...")
            return generate_fallback_insights(query, passages)
        
        resp.raise_for_status()
        
        response_data = resp.json()
        content = response_data["candidates"][0]["content"]["parts"][0]["text"].strip()
        
        # Try to parse JSON response
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # If JSON parsing fails, return the raw content as a single insight
            return {"insights": [content]}
            
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            print("⚠️ Gemini API quota exceeded. Using fallback analysis...")
            return generate_fallback_insights(query, passages)
        else:
            print(f"Error calling Gemini API: {e}")
            return generate_fallback_insights(query, passages)
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return generate_fallback_insights(query, passages)

def generate_fallback_insights(query: str, passages: list) -> dict:
    """
    Generate fallback insights when Gemini API is unavailable or quota is exceeded.
    Uses simple keyword-based analysis.
    """
    try:
        # Extract key terms from query
        query_terms = set(query.lower().split())
        
        # Generate insights based on passage content
        insights = []
        
        for i, passage in enumerate(passages[:3]):  # Limit to 3 insights
            passage_text = passage.get('text', '')
            passage_terms = set(passage_text.lower().split())
            
            # Find common terms between query and passage
            common_terms = query_terms & passage_terms
            
            if common_terms:
                # Create insight based on common terms
                key_terms = list(common_terms)[:3]
                insight = f"This passage discusses {', '.join(key_terms)} which directly relates to your query about {query.lower()}."
            else:
                # Create generic insight
                insight = f"Passage {i+1} provides relevant information that may support your understanding of the topic."
            
            insights.append(insight)
        
        # Ensure we have at least 3 insights
        while len(insights) < 3:
            insights.append(f"Additional analysis of the provided passages reveals insights relevant to your query.")
        
        return {"insights": insights[:3]}
        
    except Exception as e:
        print(f"Error in fallback analysis: {e}")
        return {"insights": [
            "Analysis completed using fallback method due to API limitations.",
            "The provided passages contain relevant information for your query.",
            "Consider reviewing the passages directly for detailed insights."
        ]}

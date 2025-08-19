import json
import requests

def generate_insights_gemini_flash(
    query: str,
    passages: list,
    api_key: str,
    model: str = "gemini-2.5-flash",
    thinking_budget: int = None
) -> dict:
    """
    Calls Gemini 2.5 Flash API to generate short insights.

    Args:
      query (str): The query or prompt.
      passages (list): List of dicts {"id": ..., "text": ...}.
      api_key (str): Your Gemini API key.
      model (str): Model identifier (default: "gemini-2.5-flash").
      thinking_budget (int, optional): Limit internal reasoning—lower = faster, less costly.

    Returns:
      dict: JSON containing only the "insights" list.
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [{
            "role": "user",
            "content": (
                f"Query: {query}\n\n"
                f"Passages:\n{json.dumps(passages, indent=2)}\n\n"
                "Generate 3 very short insights (1 sentence each) based only on the passages.\n"
                "Output only valid JSON:\n"
                "{\n  \"insights\": [\"...\"]\n}"
            )
        }],
        "temperature": 0.5,
        "max_tokens": 150
    }

    if thinking_budget is not None:
        payload["thinking_budget"] = thinking_budget

    resp = requests.post(
        "https://gemini.googleapis.com/v1/chat/completions",  # placeholder endpoint
        headers=headers,
        json=payload
    )
    content = resp.json()["choices"][0]["message"]["content"].strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {"insights": [content]}

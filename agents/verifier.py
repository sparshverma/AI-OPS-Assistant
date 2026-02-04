import json
from llm.client import get_openai_client

SYSTEM_PROMPT = """
You are a Verifier Agent. Your job is to take the original user request and the results from the Executor Agent, and construct a final, natural language response.

Input:
- User Request
- Execution Results (JSON)

Tasks:
1. Verify if the execution results actually answer the user's request.
2. If successful, summarize the data cleanly.
3. If there are errors in the results (e.g., "error" keys), explain what went wrong and provide a graceful fallback or suggestion. Use your general knowledge to answer if the tool failed but the question is general (only if appropriate).
4. Do NOT hallucinate data not present in the results or common knowledge.
"""

def verify_results(user_input: str, results: dict) -> str:
    try:
        client = get_openai_client()
    except ValueError as e:
        return f"Error: {str(e)}"

    prompt = f"""
    User Request: {user_input}
    
    Execution Results:
    {json.dumps(results, indent=2)}
    """
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )
    
    return completion.choices[0].message.content

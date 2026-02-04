import json
from pydantic import BaseModel, Field
from typing import List
from llm.client import get_openai_client

class ToolCall(BaseModel):
    tool_name: str = Field(..., description="The name of the tool to call")
    arguments: dict = Field(..., description="The arguments to pass to the tool")
    step_description: str = Field(..., description="A short description of what this step does")

class Plan(BaseModel):
    steps: List[ToolCall] = Field(..., description="The list of steps to execute")

SYSTEM_PROMPT = """
You are a Planner Agent. Your goal is to break down a user's natural language request into a specific list of steps using available tools.

Available Tools:
1. github_tool:
   - Function: get_repo_info(owner: str, repo: str)
   - Description: Fetches stars, description, and URL for a GitHub repository.
   - Arguments: owner (string), repo (string)

2. weather_tool:
   - Function: get_weather(city: str)
   - Description: Fetches current temperature and weather condition for a city.
   - Arguments: city (string)

REQUIRED OUTPUT FORMAT:
You MUST output a valid JSON object matching exactly this structure:
{
  "steps": [
    {
      "tool_name": "name_of_tool_to_call",
      "arguments": {
        "arg_name": "arg_value"
      },
      "step_description": "Explanation of why this step is needed"
    }
  ]
}

EXAMPLE:
User: "Check stars for 'fastapi/fastapi' and weather in Berlin."
Output:
{
  "steps": [
    {
      "tool_name": "github_tool",
      "arguments": {
        "owner": "fastapi",
        "repo": "fastapi"
      },
      "step_description": "Fetching repository details for fastapi/fastapi to get star count."
    },
    {
      "tool_name": "weather_tool",
      "arguments": {
        "city": "Berlin"
      },
      "step_description": "Fetching current weather conditions in Berlin."
    }
  ]
}

Rules:
- Use only the tools listed.
- "tool_name" must be exactly "github_tool" or "weather_tool".
- All tool arguments must be inside the "arguments" dictionary.
"""

def generate_plan(user_input: str) -> dict:
    try:
        client = get_openai_client()
    except ValueError as e:
        return {"error": str(e)}

    # Use standard json_object mode. The strict prompt (SYSTEM_PROMPT) ensures correct keys.
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ],
        response_format={"type": "json_object"}
    )
    
    try:
        content = completion.choices[0].message.content
        plan_dict = json.loads(content)
        # Validate against the Pydantic model
        plan_obj = Plan(**plan_dict)
        return plan_obj.model_dump()
    except Exception as e:
        return {"error": f"Failed to generate plan: {e}"}

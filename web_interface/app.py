import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv

from agents.planner import generate_plan
from agents.executor import execute_plan
from agents.verifier import verify_results

load_dotenv()

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="web_interface/static"), name="static")

# Templates
templates = Jinja2Templates(directory="web_interface/templates")

class ChatRequest(BaseModel):
    message: str

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(request: ChatRequest):
    user_input = request.message
    
    # 1. Plan
    plan = generate_plan(user_input)
    if "error" in plan:
        return {"response": f"Planning Error: {plan['error']}"}
        
    # 2. Execute
    results = execute_plan(plan)
    
    # 3. Verify
    final_response = verify_results(user_input, results)
    
    return {"response": final_response}

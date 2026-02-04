import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def get_repo_info(owner: str, repo: str):
    """
    Fetches information about a GitHub repository.
    
    Args:
        owner (str): The owner of the repository.
        repo (str): The name of the repository.
        
    Returns:
        dict: A dictionary containing stars, description, and url, or an error message.
    """
    if not GITHUB_TOKEN:
        return {"error": "GITHUB_TOKEN not found in environment variables."}
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    url = f"https://api.github.com/repos/{owner}/{repo}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        return {
            "name": data.get("name"),
            "owner": owner,
            "stars": data.get("stargazers_count"),
            "description": data.get("description"),
            "url": data.get("html_url")
        }
    except requests.exceptions.HTTPError as err:
        if response.status_code == 404:
            return {"error": f"Repository '{owner}/{repo}' not found."}
        return {"error": f"GitHub API Error: {err}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

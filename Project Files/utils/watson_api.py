# utils/watson_api.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_ai_response(prompt):
    api_key = os.getenv("WATSON_API_KEY")
    project_id = os.getenv("WATSON_PROJECT_ID")
    url = os.getenv("WATSON_URL")
    
    if not all([api_key, project_id, url]):
        raise ValueError("Missing Watson API credentials in environment variables")
        
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "input": prompt,
        "project_id": project_id
    }
    
    try:
        response = requests.post(
            f"{url}/v1/generate",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        return response.json().get("results", [{}])[0].get("generated_text", "")
    except Exception as e:
        return f"Error calling Watson API: {str(e)}"

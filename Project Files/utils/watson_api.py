import os
import streamlit as st
import requests
from dotenv import load_dotenv

# Load .env file (for local development)
load_dotenv()  # Looks for .env in project root

def get_ai_response(prompt):
    try:
        # Fallback priority: 1. Streamlit secrets 2. .env 3. Raise error
        api_key = (
            st.secrets.get("WATSON_API_KEY") 
            or os.getenv("WATSON_API_KEY")  # Typo fixed: WASON -> WATSON
            or raise ValueError("Missing API Key")
        )
        
        project_id = (
            st.secrets.get("WATSON_PROJECT_ID") 
            or os.getenv("WATSON_PROJECT_ID")
            or raise ValueError("Missing Project ID")
        )
        
        url = (
            st.secrets.get("WATSON_URL") 
            or os.getenv("WATSON_URL") 
            or "https://us-south.ml.cloud.ibm.com"  # Default fallback
        )

        # Rest of your API call logic...
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.post(f"{url}/v1/generate", ...)
        return response.json()["results"][0]["generated_text"]
        
    except Exception as e:
        return f"❌ Error: {str(e)}"

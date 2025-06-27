import streamlit as st
import requests

def get_ai_response(prompt):
    try:
        # Get credentials from Streamlit secrets
        api_key = st.secrets["WATSON_API_KEY"]
        project_id = st.secrets["WATSON_PROJECT_ID"]
        url = st.secrets.get("WATSON_URL", "https://us-south.ml.cloud.ibm.com")
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "input": prompt,
            "project_id": project_id,
            "parameters": {
                "max_new_tokens": 200
            }
        }
        
        response = requests.post(
            f"{url}/v1/generate",
            headers=headers,
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        return response.json().get("results", [{}])[0].get("generated_text", "")
        
    except Exception as e:
        return f"❌ Error: {str(e)}"

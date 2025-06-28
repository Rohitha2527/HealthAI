import streamlit as st
import requests
import json

# ✅ Get secrets from Streamlit Cloud (or .streamlit/secrets.toml if local)
API_KEY = st.secrets.get("WATSONX_API_KEY")
PROJECT_ID = st.secrets.get("WATSONX_PROJECT_ID")

BASE_URL = "https://us-south.ml.cloud.ibm.com"
MODEL_ID = "ibm/granite-3-3-2b-instruct"  # ✅ Watsonx Granite model

# ✅ IAM Token Endpoint
IAM_URL = "https://iam.cloud.ibm.com/identity/token"

# ✅ Check for missing secrets
if not API_KEY or not PROJECT_ID:
    raise Exception("❌ API Key or Project ID missing in Streamlit secrets.")

# ✅ Function to get access token from IBM Cloud IAM
def get_access_token():
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": API_KEY
    }

    response = requests.post(IAM_URL, headers=headers, data=data)

    if response.status_code != 200:
        raise Exception(f"""
❌ Failed to get IAM token.

Status: {response.status_code}
Response: {response.text}
""")

    return response.json()["access_token"]

# ✅ Main function to send prompt and get AI response
def get_ai_response(prompt):
    access_token = get_access_token()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "model_id": MODEL_ID,
        "input": [prompt],
        "parameters": {
            "decoding_method": "sample",
            "temperature": 0.7,
            "top_k": 40,
            "top_p": 0.95,
            "max_new_tokens": 300
        },
        "project_id": PROJECT_ID
    }

    url = f"{BASE_URL}/ml/v1/text/generation?version=2024-05-01"

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["results"][0]["generated_text"]

    except requests.exceptions.HTTPError as err:
        return f"[ERROR] HTTP Error: {err}\nDetails: {response.text}"
    except Exception as e:
        return f"[ERROR] Other Error: {str(e)}"



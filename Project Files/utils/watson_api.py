import streamlit as st
import requests
import json

# ✅ Load from Streamlit Secrets
API_KEY = st.secrets.get("WATSONX_API_KEY")
PROJECT_ID = st.secrets.get("WATSONX_PROJECT_ID")

BASE_URL = "https://us-south.ml.cloud.ibm.com"
MODEL_ID = "ibm/granite-3-3-2b-instruct"  # ✅ Updated IBM Granite model


# ✅ STEP 1: Get IAM Access Token
def get_access_token():
    if not API_KEY:
        raise Exception("❌ API Key missing in Streamlit secrets.")

    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": API_KEY
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code != 200:
        raise Exception(f"""❌ Failed to get IAM token.
Status: {response.status_code}
Response: {response.text}
""")

    return response.json()["access_token"]


# ✅ STEP 2: Generate response using IBM Watsonx AI
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

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"""❌ Failed to get AI response.
Status: {response.status_code}
Response: {response.text}
""")

    return response.json()["results"][0]["generated_text"]



import streamlit as st
import requests
import json

# ✅ Load credentials from Streamlit secrets
API_KEY = st.secrets.get("WATSONX_API_KEY")
PROJECT_ID = st.secrets.get("WATSONX_PROJECT_ID")
BASE_URL = "https://us-south.ml.cloud.ibm.com"
MODEL_ID = "ibm/granite-3-8b-instruct"  # ✅ Recommended model (stable + supported)

# ✅ Check for missing secrets
if not API_KEY or not PROJECT_ID:
    raise Exception("❌ API Key or Project ID missing in Streamlit secrets.")

# ✅ Get IAM token from IBM Cloud
def get_access_token():
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": API_KEY
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code != 200:
        raise Exception(f"❌ Failed to get IAM token.\nStatus: {response.status_code}\nDetails: {response.text}")

    return response.json()["access_token"]

# ✅ Call Granite model and return output
def get_ai_response(prompt):
    access_token = get_access_token()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "model_id": MODEL_ID,
        "input": [prompt],  # Granite requires a list
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
        return f"❌ HTTP Error: {err}\nDetails: {response.text}"
    except Exception as e:
        return f"❌ Other Error: {str(e)}"

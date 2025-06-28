import streamlit as st
import os
import requests
import json
from dotenv import load_dotenv

# ✅ Load environment variables from .env
load_dotenv()

API_KEY = st.secrets.get("WATSONX_API_KEY")
PROJECT_ID = st.secrets.get("WATSONX_PROJECT_ID")

print("🔍 API Key First 6:", API_KEY[:6] if API_KEY else "❌ MISSING")
print("📁 Project ID:", PROJECT_ID if PROJECT_ID else "❌ MISSING")
BASE_URL = "https://us-south.ml.cloud.ibm.com"
MODEL_ID = "ibm/granite-3-3-2b-instruct"  # ✅ Recommended Granite model

# ✅ STEP 1: Get IAM Access Token
def get_access_token():
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": API_KEY
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code != 200:
        raise Exception(f"""
❌ Failed to get IAM token.

Status: {response.status_code}
Response: {response.text}
""")

    return response.json()["access_token"]


# ✅ STEP 2: Use the Granite model to generate a response
def get_ai_response(prompt):
    access_token = get_access_token()  # ✅ Step 1: get token

    # ✅ Step 2: Pass token in Authorization header
    headers = {
        "Authorization": f"Bearer {access_token}",   # ✅ Include token here
        "Content-Type": "application/json"
    }

    # ✅ Step 3: Build the payload for the model
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
        print("✅ Token starts with:", access_token[:10])
        print("✅ Sent to:", url)
        print("✅ Status:", response.status_code)
        print("✅ Raw Response:", response.text)

        response.raise_for_status()
        return response.json()["results"][0]["generated_text"]

    except requests.exceptions.HTTPError as err:
        return f"[ERROR] HTTP Error: {err}\nDetails: {response.text}"
    except Exception as e:
        return f"[ERROR] Other Error: {str(e)}"





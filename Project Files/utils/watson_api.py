import os
import requests
import json
from dotenv import load_dotenv

# ✅ Load environment variables from .env
load_dotenv()

# ✅ Set variables from environment
import os

# ✅ Reads from Streamlit Cloud secrets
API_KEY = os.environ.get("WATSONX_API_KEY")
PROJECT_ID = os.environ.get("WATSONX_PROJECT_ID")
print("🔍 Streamlit Secrets - API_KEY:", "✅ FOUND" if API_KEY else "❌ MISSING")
print("🔍 Streamlit Secrets - PROJECT_ID:", "✅ FOUND" if PROJECT_ID else "❌ MISSING")
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

    print("\n[INFO] Getting IAM token...")
    print("[INFO] API KEY (First 8 chars):", API_KEY[:8] + "..." if API_KEY else "[ERROR] API key missing")

    response = requests.post(url, headers=headers, data=data)
    print("[INFO] Status Code:", response.status_code)
    print("[INFO] Response Text:", response.text)

    if response.status_code != 200:
        return f"[ERROR] TOKEN ERROR {response.status_code}: {response.text}"

    return response.json()["access_token"]

# ✅ STEP 2: Use the Granite model to generate a response
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
        print("[INFO] Status Code:", response.status_code)
        print("[INFO] Response Text:", response.text)

        response.raise_for_status()
        return response.json()["results"][0]["generated_text"]

    except requests.exceptions.HTTPError as err:
        return f"[ERROR] HTTP Error: {err}\nDetails: {response.text}"
    except Exception as e:
        return f"[ERROR] Other Error: {str(e)}"




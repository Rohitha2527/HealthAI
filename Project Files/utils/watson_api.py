import os
import requests
import json
from dotenv import load_dotenv

# ✅ Load environment variables from .env
load_dotenv()

# ✅ Set variables from environment
API_KEY = os.getenv("WATSONX_API_KEY")
PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
BASE_URL = "https://us-south.ml.cloud.ibm.com"
MODEL_ID = "granite-13b-chat-v2"  # ✅ Use this officially supported Granite model

# ✅ STEP 1: Get IAM Access Token
def get_access_token():
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": API_KEY
    }

    print("\n[INFO] Getting IAM token...")
    response = requests.post(url, headers=headers, data=data)
    print("[INFO] Status Code:", response.status_code)

    if response.status_code != 200:
        return f"[ERROR] TOKEN ERROR {response.status_code}: {response.text}"

    return response.json()["access_token"]

# ✅ STEP 2: Use the Granite model to generate a response
def get_ai_response(prompt):
    access_token = get_access_token()
    if "[ERROR]" in access_token:
        return access_token

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

    # ✅ Correct endpoint for text generation
    url = f"{BASE_URL}/ml/v1/text/generation?version=2024-05-01"

    try:
        response = requests.post(url, headers=headers, json=payload)
        print("[INFO] Status Code:", response.status_code)
        print("[INFO] Response:", response.text)

        response.raise_for_status()
        return response.json()["results"][0]["generated_text"]

    except requests.exceptions.HTTPError as err:
        return f"[ERROR] HTTP Error: {err}\nDetails: {response.text}"
    except Exception as e:
        return f"[ERROR] Other Error: {str(e)}"

# ✅ Sample use
if __name__ == "__main__":
    prompt = "Explain the concept of zero trust security in simple terms."
    print(get_ai_response(prompt))


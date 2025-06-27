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
MODEL_ID = "ibm/granite-3-3-2b-instruct"  # ✅ Recommended Granite model

# ✅ STEP 1: Get IAM Access Token
def get_access_token():
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": API_KEY
    }

    print("\n🔍 Getting IAM token...")
    print("🔐 API KEY (First 8 chars):", API_KEY[:8] + "..." if API_KEY else "❌ MISSING")

    response = requests.post(url, headers=headers, data=data)

    print("📩 Status Code:", response.status_code)
    print("📄 Response Text:", response.text)

    response.raise_for_status()  # This is where any 400/401 error will raise
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
        "input": [prompt],  # ✅ IBM expects a list of strings
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

    print("\n📤 REQUEST PAYLOAD:")
    print(json.dumps(payload, indent=2))
    print("\n🔗 URL:", url)

    try:
        response = requests.post(url, headers=headers, json=payload)
        print("\n📥 RAW RESPONSE:")
        print(response.text)
        response.raise_for_status()
        return response.json()["results"][0]["generated_text"]
    except requests.exceptions.HTTPError as err:
        return f"\n❌ HTTP Error: {err}\nStatus: {response.status_code}\nDetails: {response.text}"
    except Exception as e:
        return f"\n❌ Other Error: {str(e)}"



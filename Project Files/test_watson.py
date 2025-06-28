import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WATSONX_API_KEY")

url = "https://iam.cloud.ibm.com/identity/token"
headers = {"Content-Type": "application/x-www-form-urlencoded"}
data = {
    "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
    "apikey": API_KEY
}

response = requests.post(url, headers=headers, data=data)

print("🔑 API Key starts with:", API_KEY[:10] + "..." if API_KEY else "❌ Not Found")
print("📡 Status Code:", response.status_code)
print("📥 Response:", response.text)


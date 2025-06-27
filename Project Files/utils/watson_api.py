



import os
import requests
from dotenv import load_dotenv
import json
# Load environment variables from .env file
load_dotenv()
# Retrieve API key and project ID from environment variables
API_KEY = os.getenv("WATSONX_API_KEY")
PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
BASE_URL = "https://us-south.ml.cloud.ibm.com"
MODEL_ID = "ibm/granite-13b-instruct-v2"
def get_access_token():
    """Retrieve access token for IBM Watson API."""
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": API_KEY
    }
    
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()["access_token"]
def get_ai_response(prompt):



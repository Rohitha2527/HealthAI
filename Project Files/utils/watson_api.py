 "input": prompt,
        "parameters": {
            "decoding_method": "sample",
            "temperature": 0.7,  # Add creativity but stay grounded
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
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()["results"][0]["generated_text"]
    except requests.exceptions.HTTPError as err:
        return f"\n❌ HTTP Error: {err}\nStatus: {response.status_code}\nDetails: {response.text}"
    except Exception as e:
        return f"\n❌ Other Error: {str(e)}"
# Example usage
if __name__ == "__main__":
    prompt = "What are the benefits of using AI in healthcare?"
    response = get_ai_response(prompt)
    print("\n📝 AI Response:", response)

import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

API_KEY = os.getenv("WATSONX_API_KEY")
PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
BASE_URL = "https://us-south.ml.cloud.ibm.com"
MODEL_ID = "ibm/granite-13b-instruct-v2"

def get_access_token():
url = "https://iam.cloud.ibm.com/identity/token"
headers = {"Content-Type": "application/x-www-form-urlencoded"}
data = {
"grant_type": "urn:ibm:params:oauth:grant-type:apikey",
"apikey": API_KEY
}
response = requests.post(url, headers=headers, data=data)
response.raise_for_status()
return response.json()["access_token"]

def get_ai_response(prompt):
access_token = get_access_token()

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

payload = {
    "model_id": MODEL_ID,
    "input": prompt,
    "parameters": {
        "decoding_method": "sample",
         "temperature": 0.7,              # add creativity but stay grounded
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
Copy message
Edit message
BLACKBOXAI

Code Overview

The provided code is a Python script that interacts with IBM's Watson AI service to generate text based on a given prompt. It uses the requests library to make HTTP requests and the dotenv library to manage environment variables.

Key Components

Imports:

os: For accessing environment variables.
requests: For making HTTP requests.
load_dotenv: To load environment variables from a .env file.
json: For handling JSON data.
Environment Variables:

API_KEY: The API key for authentication.
PROJECT_ID: The project ID for the Watson service.
BASE_URL: The base URL for the IBM Watson API.
MODEL_ID: The specific model to use for text generation.
Functions

get_access_token():

Purpose: Retrieves an access token for authentication.
Process:
Sends a POST request to the IBM IAM service with the API key.
Returns the access token from the response.
get_ai_response(prompt):

Purpose: Generates a response from the AI model based on the provided prompt.
Process:
Calls get_access_token() to get the access token.
Prepares the request headers and payload.
Sends a POST request to the text generation endpoint.
Handles the response and returns the generated text or an error message.
Error Handling

The code includes error handling for HTTP errors and general exceptions, providing informative messages in case of failures.
Common Issues

The error message indicates a problem with the URL, specifically a NameResolutionError. This suggests that the URL may be malformed or that there is a network issue.
Suggestions for Troubleshooting

Check the URL: Ensure that the BASE_URL is correctly formatted without any extra characters (e.g., quotes).

Network Connectivity: Verify that your network connection is stable and that you can reach the IBM Cloud services.

Environment Variables: Ensure that the WATSONX_API_KEY and WATSONX_PROJECT_ID are correctly set in your environment.

API Version: Confirm that the API version in the URL is correct and supported by the service.

By following these guidelines, you should be able to troubleshoot and resolve the issues with the script effectively.


show error

Copy message
Edit message
BLACKBOXAI

To display the error handling part of the code, here’s the relevant section from the get_ai_response function that captures and returns error messages:

python
10 lines
Click to expand
try:
response = requests.post(url, headers=headers, json=payload)
...
Explanation of Error Handling
Try Block:

The code attempts to send a POST request to the specified URL with the provided headers and payload.
It prints the raw response for debugging purposes.
If the response indicates an error (e.g., a 4xx or 5xx status code), response.raise_for_status() will raise an HTTPError.
Except Blocks:

requests.exceptions.HTTPError: This block catches HTTP errors specifically. It returns a formatted string that includes:
The error message.
The HTTP status code.
The details of the response.
General Exception: This block catches any other exceptions that may occur and returns a simple error message with the exception details.
Example of Error Output
If an error occurs during the request, the output might look like this:


Run
Copy code
❌ HTTP Error: 404 Client Error: Not Found for url: https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2024-05-01
Status: 404
Details: {"error": "Model not found"}
This output provides clear information about what went wrong, making it easier to diagnose and fix the issue.


rewrite code with zero errors

Copy message
Edit message
BLACKBOXAI

Here’s a revised version of your code with improvements for clarity, error handling, and best practices. This version ensures that it adheres to Python conventions and includes comments for better understanding.

python
69 lines
Click to close
import os
import requests
...
Key Improvements
Error Handling: The code now raises errors for bad responses immediately after the request is made, ensuring that any issues are caught early.

Comments: Added comments throughout the code to explain the purpose of each section and function.

Main Guard: Included a if __name__ == "__main__": block to allow for easy testing and execution of the script.

Consistent Formatting: Ensured consistent formatting and indentation for better readability.

Usage
To use this code:

Ensure you have the required packages installed (requests and python-dotenv).
Set up your .env file with the necessary WATSONX_API_KEY and WATSONX_PROJECT_ID.
Run the script, and it will generate a response based on the provided prompt.

Copy message
Export
Scroll to bottom


Web

Research

Upload
Follow us on


By using Blackbox you agree to the Terms and Privacy.


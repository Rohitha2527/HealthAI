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


# utils/watson_api.py

import streamlit as st
from transformers import pipeline

# ✅ Load Hugging Face Token from secrets
HF_TOKEN = st.secrets.get("HF_TOKEN")  # You must set this in `.streamlit/secrets.toml`

# ✅ Validate the token
if not HF_TOKEN:
    raise Exception("❌ Hugging Face token missing in Streamlit secrets.")

# ✅ Load the model (only once, cached)
@st.cache_resource
def load_model():
    return pipeline(
        "text-generation",
        model="ibm-granite/granite-3.3-25-instruct",  # Make sure this model exists on Hugging Face
        use_auth_token=HF_TOKEN
    )

generator = load_model()

# ✅ Call the model
def get_ai_response(prompt):
    try:
        output = generator(prompt, max_new_tokens=300, do_sample=True, temperature=0.7, top_k=40, top_p=0.95)
        return output[0]["generated_text"]
    except Exception as e:
        return f"❌ Hugging Face Error: {str(e)}"

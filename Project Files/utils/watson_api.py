import streamlit as st
from transformers import pipeline

# ✅ Load Hugging Face token from Streamlit secrets
HF_TOKEN = st.secrets.get("HF_TOKEN")

# ✅ Handle missing token gracefully
if not HF_TOKEN:
    st.error("❌ Hugging Face token is missing in Streamlit secrets.")
    st.stop()

# ✅ Cache the model load — runs only once
@st.cache_resource
def load_model():
    try:
        model = pipeline(
            "text-generation",
            model="ibm-granite/granite-3.3-25-instruct",  # Confirm this model exists on Hugging Face
            use_auth_token=HF_TOKEN
        )
        return model
    except Exception as e:
        st.error(f"❌ Failed to load model: {str(e)}")
        st.stop()

# ✅ Load the generator
generator = load_model()

# ✅ Wrap the model call
def get_ai_response(prompt):
    try:
        output = generator(
            prompt,
            max_new_tokens=300,
            do_sample=True,
            temperature=0.7,
            top_k=40,
            top_p=0.95
        )
        return output[0]["generated_text"]
    except Exception as e:
        return f"❌ Hugging Face Error: {str(e)}"


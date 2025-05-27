import requests
import streamlit as st

# Replace this with your Hugging Face token (get one from https://huggingface.co/settings/tokens)
API_TOKEN = "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"  # <-- Put your actual token here

API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query_hf_api(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 300,   # Increase token limit for longer answers
            "do_sample": True,
            "top_p": 0.9,
            "temperature": 0.7,
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        # The generated text may be in different keys depending on model
        if isinstance(data, list) and 'generated_text' in data[0]:
            return data[0]['generated_text']
        elif 'generated_text' in data:
            return data['generated_text']
        else:
            return "⚠️ Unexpected API response format."
    else:
        return f"❌ Error {response.status_code}: {response.text}"

st.title("🎓 Career Counseling Chatbot")

user_input = st.text_input("Ask me about career options:")

if user_input:
    with st.spinner("Thinking..."):
        answer = query_hf_api(user_input)
    st.markdown(f"**Bot:**\n\n{answer}")
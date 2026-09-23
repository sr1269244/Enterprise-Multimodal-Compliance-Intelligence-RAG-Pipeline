import os
import time
import joblib
import numpy as np
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ServerError, APIError
from sklearn.metrics.pairwise import cosine_similarity

# Streamlit Page Setup
st.set_page_config(page_title="RAG Teaching Assistant", page_icon="🎓", layout="centered")
st.title("🎓 RAG AI Teaching Assistant")
st.caption("Ask questions about your lecture transcripts")

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY is missing! Set it in `.env` locally or in Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# Cache data loading so it stays fast across interactions
@st.cache_resource
def load_data():
    return joblib.load('embeddings.joblib')

df = load_data()

def generate_with_retry(client, prompt):
    """Dynamically fetches active models and retries on temporary 503 traffic spikes."""
    try:
        available = [
            m.name.replace("models/", "") 
            for m in client.models.list() 
            if "generateContent" in getattr(m, "supported_generation_methods", ["generateContent"])
        ]
        flash_models = [m for m in available if "flash" in m]
        models_to_try = flash_models + [m for m in available if m not in flash_models]
    except Exception:
        models_to_try = ["gemini-3.6-flash", "gemini-3.8-flash", "gemini-1.5-flash"]

    if not models_to_try:
        models_to_try = ["gemini-3.6-flash", "gemini-1.5-flash"]

    last_error = None
    for model_name in models_to_try:
        for attempt in range(4):  # Retry up to 4 times per model
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                return response
            except ServerError as e:
                # Temporary 503 spike — wait and retry
                last_error = e
                time.sleep(3 * (attempt + 1))
            except APIError as e:
                # 404 or unsupported endpoint — try next valid model
                last_error = e
                break
            except Exception as e:
                last_error = e
                break

    raise RuntimeError(f"Unable to reach Google models right now. Details: {last_error}")

# User Query Input
user_query = st.text_input("Enter your question:", placeholder="e.g., What is an artificial neural network?")

if st.button("Search & Answer", type="primary"):
    if user_query.strip():
        with st.spinner("Searching video transcripts and generating response..."):
            try:
                # 1. Embed query
                response_embed = client.models.embed_content(
                    model="gemini-embedding-001",
                    contents=user_query
                )
                question_embedding = response_embed.embeddings[0].values

                # 2. Similarity search
                similarities = cosine_similarity(
                    np.vstack(df['embeddings']), 
                    [question_embedding]
                ).flatten()

                top_results = 5
                max_index = similarities.argsort()[::-1][:top_results]
                new_df = df.loc[max_index]

                # 3. Build prompt context
                chunks_text = ""
                for idx, row in new_df.iterrows():
                    chunks_text += f"- Video {row['number']} ({row['title']}) [{row['start']}s - {row['end']}s]: {row['text']}\n"

                prompt = f"""
You are a helpful teaching assistant.

Lecture Transcripts Context:
{chunks_text}

User Question: "{user_query}"

Instructions:
1. Provide a direct, clear answer based on the transcripts above.
2. Direct the user to the relevant video number and timestamp.
3. If the topic is not in the context, state that you can only answer questions related to the course data.
"""

                # 4. Generate answer
                response = generate_with_retry(client, prompt)

                # 5. Display Answer
                st.subheader("💡 Answer")
                st.write(response.text)

                # Display retrieved sources
                with st.expander("📚 View Matched Transcripts"):
                    st.dataframe(new_df[["number", "title", "start", "end", "text"]])

            except Exception as ex:
                st.error(f"Error: {ex}")
    else:
        st.warning("Please enter a valid question.")
        
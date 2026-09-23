import os
import time
import joblib
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from google import genai
from google.genai import types
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

df = joblib.load('embeddings.joblib')
query = input("\nAsk a question: ")

# Query embedding using gemini-embedding-001
res = client.models.embed_content(
    model="gemini-embedding-001",
    contents=query
)
q_embed = res.embeddings[0].values

# Similarity match
sims = cosine_similarity(np.vstack(df['embeddings']), [q_embed]).flatten()
top_df = df.loc[sims.argsort()[::-1][:5]]

# Build simple string context
context = ""
for idx, r in top_df.iterrows():
    context += f"Video {r['number']} ({r['title']}) [{r['start']}s - {r['end']}s]: {r['text']}\n"

prompt = f"Context:\n{context}\n\nQuestion: {query}\n\nAnswer clearly based on context and state video number and timestamp."

models = ["gemini-3.6-flash", "gemini-3.5-flash"]
response = None

for m in models:
    print(f"Connecting to model '{m}'...")
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=m,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3
                )
            )
            if response and response.text:
                break
        except Exception as e:
            err = str(e)
            if "503" in err or "high demand" in err.lower():
                print(f"  [Attempt {attempt+1}] Server busy for {m}. Retrying in 3s...")
                time.sleep(3)
            else:
                print(f"  Failed on {m}: {err}")
                break
    if response and response.text:
        break

if response and response.text:
    print("\n--- ANSWER ---")
    print(response.text)
    with open("response.txt", "w", encoding="utf-8") as f:
        f.write(response.text)
else:
    print("\nAll model attempts failed or are currently undergoing high server demand.")

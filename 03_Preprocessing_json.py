import os
import json
import time
import joblib
import pandas as pd
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is missing in your .env file!")

client = genai.Client(api_key=api_key)

def create_embeddings_batched(text_list, batch_size=10, delay=2):
    """
    Splits text_list into smaller batches to prevent 429 RESOURCE_EXHAUSTED errors.
    """
    all_embeddings = []
    
    for i in range(0, len(text_list), batch_size):
        batch = text_list[i : i + batch_size]
        print(f"  --> Processing batch {i // batch_size + 1} ({len(batch)} chunks)...")
        
        response = client.models.embed_content(
            model="gemini-embedding-001",
            contents=batch
        )
        
        batch_embeddings = [e.values for e in response.embeddings]
        all_embeddings.extend(batch_embeddings)
        
        # Pause briefly between batches to respect rate limits
        time.sleep(delay)
        
    return all_embeddings

jsons = os.listdir("newjsons")
my_dicts = []
chunk_id = 0

for json_file in jsons:
    with open(f"newjsons/{json_file}", "r", encoding="utf-8") as f:
        content = json.load(f)
        print(f"Creating embeddings for {json_file}")
        
        texts = [c['text'] for c in content['chunks']]
        embeddings = create_embeddings_batched(texts, batch_size=10, delay=2)
        
        for i, chunk in enumerate(content['chunks']):
            chunk['chunk_id'] = chunk_id
            chunk['embeddings'] = embeddings[i]
            chunk_id += 1
            my_dicts.append(chunk)

df = pd.DataFrame.from_records(my_dicts)
joblib.dump(df, 'embeddings.joblib')
print("Successfully generated embeddings.joblib with Gemini!")
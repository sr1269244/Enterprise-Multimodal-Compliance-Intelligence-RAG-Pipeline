import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

audios = os.listdir("audios")
os.makedirs("json", exist_ok=True)

for audio in audios:
    if "_" in audio:
        number = audio.split("_")[0]
        title = audio.split("_")[1][:-4]
        file_path = f"audios/{audio}"

        print(f"Uploading {audio} to Gemini...")
        audio_file = client.files.upload(file=file_path)

        prompt = f"""
        Transcribe the following audio file into JSON format.
        Include a 'chunks' array where each chunk contains:
        - "title": "{title}"
        - "number": "{number}"
        - "start": start time in seconds (float/int)
        - "end": end time in seconds (float/int)
        - "text": transcript of that chunk

        Also include top-level "text" field containing the full text transcript.
        Return ONLY valid JSON.
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[audio_file, prompt],
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        # Delete uploaded file from Gemini storage
        client.files.delete(name=audio_file.name)

        data = json.loads(response.text)

        with open(f"json/{audio}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

print("All audio files transcribed with Gemini!")
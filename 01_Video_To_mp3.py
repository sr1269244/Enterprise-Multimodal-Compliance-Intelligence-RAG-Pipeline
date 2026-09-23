import os
import subprocess

# Ensure the audios directory exists
os.makedirs("audios", exist_ok=True)

files = os.listdir("videos")
for file in files:
    file_name = os.path.splitext(file)[0]
    output_file = f"audios/{file_name}.mp3"
    
    # Convert video to MP3 using ffmpeg
    subprocess.run(["ffmpeg", "-i", f"videos/{file}", output_file])

print("Video to MP3 conversion complete!")
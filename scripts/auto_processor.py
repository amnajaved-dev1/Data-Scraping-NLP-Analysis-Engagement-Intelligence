import os
import csv
import whisper
from yt_dlp import YoutubeDL

# ────────────────────────────────────────────────────────────────
# CONFIGURATION
# ────────────────────────────────────────────────────────────────
VIDEO_FOLDER = "videos"
os.makedirs(VIDEO_FOLDER, exist_ok=True)

# Select the target reels you want to process
target_reels = ["Reel_01", "Reel_02", "Reel_03", "Reel_04", "Reel_05"]

# Load reels data from your CSV
reels = []
with open("reels_data.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        reels.append(row)

# ────────────────────────────────────────────────────────────────
# PART 1: AUTOMATIC VIDEO DOWNLOADING
# ────────────────────────────────────────────────────────────────
print("--- STARTING AUTOMATIC VIDEO DOWNLOADS ---")

for reel in reels:
    reel_id = reel["reel_id"]
    reel_link = reel["reel_link"]
    
    if reel_id in target_reels:
        output_path = os.path.join(VIDEO_FOLDER, f"{reel_id}.mp4")
        
        # Check if video is already downloaded to save time/bandwidth
        if os.path.exists(output_path):
            print(f"  {reel_id} already exists. Skipping download.")
            continue
            
        print(f"Downloading {reel_id} from {reel_link}...")
        
        ydl_opts = {
            'outtmpl': os.path.join(VIDEO_FOLDER, f"{reel_id}.%(ext)s"),
            'format': 'balthvideo*+bestaudio/best', # Downloads best combined quality
            'merge_output_format': 'mp4',
            'quiet': True,                          # Suppresses clutter logs
            'no_warnings': True
        }
        
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([reel_link])
            print(f"  Successfully downloaded: {output_path}")
        except Exception as e:
            print(f"  ❌ ERROR downloading {reel_id}: {e}")

print("\nDownloads complete!\n")

# ────────────────────────────────────────────────────────────────
# PART 2: WHISPER TRANSCRIPTION
# ────────────────────────────────────────────────────────────────
print("--- LOADING WHISPER MODEL ---")
model = whisper.load_model("base") 
print("Whisper ready!\n")

print("--- STARTING TRANSCRIPTION ---")
for reel in reels:
    reel_id = reel["reel_id"]
    
    if reel_id in target_reels:
        video_path = os.path.join(VIDEO_FOLDER, f"{reel_id}.mp4")

        if os.path.exists(video_path):
            print(f"Transcribing {reel_id}...")
            try:
                result = model.transcribe(video_path)
                transcript = result["text"].strip()
                reel["transcript"] = transcript
                print(f"  Done: {transcript[:80]}...")
            except Exception as e:
                print(f"  ❌ Whisper Error on {reel_id}: {e}")
                reel["transcript"] = ""
        else:
            print(f"  ⚠️ Skipping transcription for {reel_id} — File not found.")
            reel["transcript"] = ""
    else:
        # Keep other reels clear or unchanged
        reel["transcript"] = ""

# Save updated data back to CSV
fieldnames = list(reels[0].keys())
if "transcript" not in fieldnames:
    fieldnames.append("transcript")

with open("reels_data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(reels)

print("\n🎉 Success! reels_data.csv updated with transcripts via code.")
print("Now you can run your modified python classifier.py!")
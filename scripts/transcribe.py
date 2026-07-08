import whisper
import os
import csv

print("Loading Whisper model...")
model = whisper.load_model("base") 
print("Whisper ready!\n")

VIDEO_FOLDER = "videos"
target_reels = ["Reel_01", "Reel_02", "Reel_03", "Reel_04", "Reel_05"]

reels = []
with open("reels_data.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        reels.append(row)

print("Starting transcription for the 5 downloaded videos...\n")
for reel in reels:
    reel_id = reel["reel_id"]
    
    if reel_id in target_reels:
        video_path = os.path.join(VIDEO_FOLDER, f"{reel_id}.mp4")

        if os.path.exists(video_path):
            print(f"Transcribing {reel_id}...")
            result = model.transcribe(video_path)
            transcript = result["text"].strip()
            reel["transcript"] = transcript
            print(f"  Done: {transcript[:80]}...")
        else:
            print(f"  ⚠️ File not found for {reel_id} in the videos folder.")
            reel["transcript"] = ""
    else:
        reel["transcript"] = ""

fieldnames = list(reels[0].keys())
if "transcript" not in fieldnames:
    fieldnames.append("transcript")

with open("reels_data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(reels)

print("\n🎉 Done! reels_data.csv updated with transcripts.")
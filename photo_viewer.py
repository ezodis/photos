import os
import json
from datetime import datetime
from flask import Flask, send_from_directory, jsonify, render_template, request

app = Flask(__name__)

# Define the media folder
MEDIA_FOLDER = "/app/media"
OUTPUT_FILE = "/app/static/media.json"

# Supported file extensions
SUPPORTED_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".mp4", ".mov", ".avi", ".mkv")

def get_media_files():
    media_files = []
    for root, _, files in os.walk(MEDIA_FOLDER):
        for file in files:
            if file.lower().endswith(SUPPORTED_EXTENSIONS):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, MEDIA_FOLDER)
                timestamp = os.path.getmtime(file_path)
                date_taken = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
                year, month, day = date_taken.split("-")

                media_files.append({
                    "path": relative_path,
                    "date": date_taken,
                    "year": year,
                    "month": month,
                    "day": day
                })

    # Sort by date
    media_files.sort(key=lambda x: x["date"], reverse=True)
    return media_files

def save_json(data):
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/media.json")
def media_json():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 100))

    with open(OUTPUT_FILE, "r") as f:
        media_data = json.load(f)

    start = (page - 1) * limit
    end = start + limit
    return jsonify(media_data[start:end])

@app.route("/media/<path:filename>")
def media_files(filename):
    return send_from_directory(MEDIA_FOLDER, filename)

if __name__ == "__main__":
    media_data = get_media_files()
    save_json(media_data)
    app.run(host="0.0.0.0", port=5000, debug=True)  # Ensure Flask binds to 0.0.0.0
    
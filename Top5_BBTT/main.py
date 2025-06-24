# main.py

import argparse
import os
import json

from generate_top5 import generate_top5_metadata
from cli_top5builder import build_preview
from utils.slugify import slugify
from utils.validate_youtube import filter_valid_moments
from utils.fill_missing import fill_in_missing_moments
from utils.video_asset_builder import build_video_assets
from utils.json2video_builder import build_json2video_scene

def main():
    parser = argparse.ArgumentParser(description="Generate and produce a Top 5 baseball video")
    parser.add_argument("--topic", required=True, help="Topic title, e.g. 'Top 5 Bat Flips of the 2010s'")
    parser.add_argument("--download-clips", action="store_true", help="Download video clips for each moment")
    parser.add_argument("--build-json2video", action="store_true", help="Build JSON2Video scenes JSON")
    args = parser.parse_args()

    topic = args.topic.strip()
    slug = slugify(topic)

    # Paths
    json_path = os.path.join("outputs", "json", f"{slug}.json")
    txt_path = os.path.join("outputs", "txt", f"{slug}.txt")
    json2video_path = os.path.join("outputs", "json2video", f"{slug}.json")

    # Ensure folders
    os.makedirs("outputs/json", exist_ok=True)
    os.makedirs("outputs/txt", exist_ok=True)
    os.makedirs("outputs/json2video", exist_ok=True)

    # Step 1: Load or generate metadata
    if os.path.exists(json_path):
        print("📦 Using cached metadata...")
        with open(json_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
    else:
        print("✨ Generating metadata with OpenAI...")
        raw_data = generate_top5_metadata(topic)
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(raw_data, f, indent=2)

    # Step 2: Validate YouTube availability
    print("🔍 Validating YouTube availability...")
    valid_data = filter_valid_moments(raw_data)

    # Step 3: Fill in missing ranks
    if len(valid_data) < 5:
        print(f"⚠️ Only {len(valid_data)} valid entries. Attempting to fill in {5 - len(valid_data)} more...")
        fillers = fill_in_missing_moments(topic, valid_data, 5 - len(valid_data))
        print("🔁 Re-validating new moments...")
        valid_fillers = filter_valid_moments(fillers)
        valid_data += valid_fillers

    # Final safeguard
    valid_data = valid_data[:5]
    if len(valid_data) < 5:
        print("❌ Could not find 5 usable clips. Aborting.")
        return

    # Step 4: Build and save preview
    print("📝 Saving preview text...")
    preview = build_preview(topic, valid_data, save_txt=True)
    print(f"✅ Preview saved to {txt_path}")

    # Step 5: Download clips (optional)
    clip_paths = None
    if args.download_clips:
        print("📥 Downloading clips...")
        clip_paths = build_video_assets(valid_data, topic_slug=slug)
        print("✅ Downloaded all clips.")

    # Step 6: Build JSON2Video scene (optional)
    if args.build_json2video:
        if not clip_paths:
            print("⚠️ Cannot build JSON2Video file without downloaded clips.")
            return

        print("🎬 Building JSON2Video scene file...")
        json2video = build_json2video_scene(clip_paths, valid_data)
        with open(json2video_path, "w", encoding="utf-8") as f:
            json.dump(json2video, f, indent=2)
        print(f"✅ JSON2Video file saved to {json2video_path}")

if __name__ == "__main__":
    main()

# utils/video_asset_builder.py

import os
import subprocess
from utils.slugify import slugify

def download_clip(youtube_url_or_query: str, title_slug: str, topic_slug: str, base_dir="assets/clips", is_search=True) -> str | None:
    """
    Download the first YouTube result or direct video by URL using yt-dlp.
    Returns path to local .mp4 or None.
    """
    topic_dir = os.path.join(base_dir, topic_slug)
    os.makedirs(topic_dir, exist_ok=True)

    source = f"ytsearch1:{youtube_url_or_query}" if is_search else youtube_url_or_query
    output_path = os.path.join(topic_dir, f"{title_slug}.mp4")

    cmd = [
        "yt-dlp",
        source,
        "-f", "mp4",
        "-o", output_path,
        "--no-playlist",
        "--quiet",
        "--no-warnings"
    ]

    try:
        subprocess.run(cmd, check=True)
        if os.path.exists(output_path):
            print(f"✅ Clip downloaded: {output_path}")
            return output_path
        else:
            print(f"❌ Download failed: {output_path} not found")
            return None
    except subprocess.CalledProcessError as e:
        print(f"❌ yt-dlp error: {e}")
        return None

def build_video_assets(data: list[dict], topic_slug: str, base_dir="assets/clips") -> list[str]:
    """
    Downloads clips for each moment. Returns a list of local .mp4 paths (or None if failed).
    """
    clip_paths = []

    for moment in data:
        title = moment.get("title", f"clip_{moment['rank']}")
        title_slug = slugify(title)

        search_query = moment.get("youtube_search")
        resolved_url = moment.get("youtube_url")  # comes from validator
        source = resolved_url if resolved_url else search_query
        is_search = resolved_url is None

        print(f"\n🎬 #{moment['rank']} - {title}")
        print(f"🔎 Using {'search' if is_search else 'direct URL'}: {source}")

        clip_path = download_clip(source, title_slug, topic_slug, base_dir, is_search=is_search)

        if clip_path:
            clip_paths.append(clip_path)
        else:
            print(f"⚠️ Failed to download clip: {title}")
            clip_paths.append(None)

    return clip_paths

# cli_top5builder.py
import os
from utils.youtube_search import generate_youtube_search_url
from utils.slugify import slugify

def build_preview(topic: str, data: list, save_txt: bool = True) -> list[dict]:
    """
    Enhances Top 5 data with YouTube links, prints a preview, and optionally saves to a .txt file.
    """
    if not data or not isinstance(data, list):
        print("❌ Invalid or missing metadata")
        return []

    # Add YouTube search URLs (if needed)
    for moment in data:
        moment["youtube_search"] = generate_youtube_search_url(moment["youtube_search"])

    slug = slugify(topic)
    lines = [f"📌 {topic}\n"]

    for moment in data:
        lines.append(f"#{moment['rank']}: {moment['title']}")
        lines.append(f"- Player(s): {', '.join(moment['player']) if isinstance(moment['player'], list) else moment['player']}")
        lines.append(f"- Team(s): {', '.join(moment['team']) if isinstance(moment['team'], list) else moment['team']}")
        lines.append(f"- Date: {moment['date']}")
        lines.append(f"- Description: {moment['description']}")
        lines.append(f"- YouTube Search: {moment['youtube_search']}")
        lines.append(f"- Timestamp Hint: {moment.get('timestamp_hint', 'N/A')}\n")

    preview_text = "\n".join(lines)
    print("\n" + preview_text)

    if save_txt:
        os.makedirs("outputs/txt", exist_ok=True)
        txt_path = os.path.join("outputs", "txt", f"{slug}.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(preview_text)

    return data

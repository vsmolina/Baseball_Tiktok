# utils/validate_youtube.py

import subprocess
import re

def validate_youtube_search(query: str) -> str | None:
    """
    Try to resolve the best YouTube video for a search query using yt-dlp.
    Returns the URL if successful, else None.
    """
    try:
        result = subprocess.run(
            ["yt-dlp", f"ytsearch1:{query}", "--print", "%(webpage_url)s"],
            capture_output=True, text=True, check=True
        )
        url = result.stdout.strip()
        return url if url.startswith("http") else None
    except subprocess.CalledProcessError:
        return None

def strip_fallback_words(query: str) -> list[str]:
    """
    Generate fallback versions of a query by removing non-essential keywords.
    """
    STRIP_WORDS = ["walk-off", "game", "inning", "home run", "homer", "run", "2010s", "ALDS", "NLCS", "World Series"]
    stripped_queries = []

    base = query
    for word in STRIP_WORDS:
        base = re.sub(rf"\b{word}\b", "", base, flags=re.IGNORECASE).strip()
        if base and base not in stripped_queries:
            stripped_queries.append(base)

    return stripped_queries

def resolve_best_youtube_url(search_query: str) -> str | None:
    """
    Attempt original query, then stripped fallbacks if needed.
    """
    url = validate_youtube_search(search_query)
    if url:
        return url

    for fallback in strip_fallback_words(search_query):
        print(f"🔁 Trying fallback: {fallback}")
        url = validate_youtube_search(fallback)
        if url:
            return url

    return None

def filter_valid_moments(metadata: list[dict]) -> list[dict]:
    """
    Returns metadata entries that have valid YouTube results.
    Adds `youtube_url` to each valid entry.
    """
    valid = []

    for moment in metadata:
        query = moment.get("youtube_search", "")
        print(f"\n🔍 Validating: {query}")
        url = resolve_best_youtube_url(query)

        if url:
            print(f"✅ Found: {url}")
            moment["youtube_url"] = url
            valid.append(moment)
        else:
            print(f"❌ No usable video for: {query}")

    return valid

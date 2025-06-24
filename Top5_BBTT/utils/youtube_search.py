import urllib.parse

def generate_youtube_search_url(query: str) -> str:
    """
    Return a YouTube search URL based on a query string.
    Example: "Jose Bautista bat flip 2015" → "https://www.youtube.com/results?search_query=Jose+Bautista+bat+flip+2015"
    """
    base_url = "https://www.youtube.com/results"
    encoded_query = urllib.parse.urlencode({"search_query": query})
    return f"{base_url}?{encoded_query}"

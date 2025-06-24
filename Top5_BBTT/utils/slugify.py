import re

def slugify(text: str) -> str:
    """
    Convert a string to a safe lowercase slug for filenames.
    Example: "Top 5 Bat Flips of the 2010s" → "top_5_bat_flips_of_the_2010s"
    """
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)        # Remove non-alphanumerics
    text = re.sub(r"[\s-]+", "_", text)         # Replace whitespace/dash with underscore
    return text.strip("_")

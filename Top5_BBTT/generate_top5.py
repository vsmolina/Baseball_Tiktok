import os
import json
import openai
from dotenv import load_dotenv
from utils.slugify import slugify

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_top5_metadata(topic: str, use_cache: bool = True) -> list[dict]:
    filename = slugify(topic) + ".json"
    output_path = os.path.join("outputs", "json", filename)

    if use_cache and os.path.exists(output_path):
        print(f"📦 Using cached metadata: {output_path}")
        with open(output_path, "r", encoding="utf-8") as f:
            return json.load(f)

    print("✨ Generating new metadata with OpenAI...")

    prompt = f"""
You are a baseball historian and content producer. I am making a TikTok video titled: "{topic}".
Give me a ranked list of the 5 most iconic moments that match this theme.

Each moment should be a JSON object with these **exact field names**:

- "rank" (integer 1 to 5)
- "title" (string)
- "player" (string or list of player names)
- "team" (string or list of team names)
- "date" (string, e.g., "June 22, 2021")
- "description" (1 to 2 sentence string)
- "youtube_search" (string: best search terms for finding the clip on YouTube)
- "timestamp_hint" (string: approximate time or inning)

Only include moments that return clear results when searched on YouTube using the given search string. 
Avoid moments that are hard to find, only available as highlight recaps, or don't have direct game footage.

If you're unsure whether a moment is available or too obscure, skip it and find another.
Prioritize viral, iconic moments with high view counts and clear search terms.

Respond ONLY with a valid JSON array of 5 such objects. Do not include any explanation or markdown formatting.
Only include moments from 2010 to today.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        raw = response.choices[0].message.content.strip()

        # Handle badly wrapped output
        if raw.startswith("```json"):
            raw = raw[len("```json"):].strip()
        if raw.endswith("```"):
            raw = raw[:-3].strip()

        print("🔍 Raw content before parsing:\n", raw)

        try:
            parsed = json.loads(raw)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(parsed, f, indent=2)
            print(f"✅ Metadata saved to {output_path}")
            return parsed
        except Exception as json_err:
            print("❌ Failed to parse GPT output as JSON. Raw response:")
            print(raw)
            raise json_err

    except Exception as e:
        print(f"❌ Error contacting OpenAI: {e}")
        return []

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
        generate_top5_metadata(topic)
    else:
        print("Please provide a topic as a command-line argument.")

    
# .venv\Scripts\Activate.ps1

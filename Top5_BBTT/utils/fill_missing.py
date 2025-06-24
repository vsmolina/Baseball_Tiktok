# utils/fill_missing.py

import os
import openai
import json
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def fill_in_missing_moments(topic: str, existing: list[dict], needed_count: int) -> list[dict]:
    """
    Re-prompts GPT to generate additional Top 5 moments to fill in missing slots.
    Avoids duplicates.
    """
    used_titles = [m["title"] for m in existing]
    used_players = [p for m in existing for p in ([m["player"]] if isinstance(m["player"], str) else m["player"])]

    prompt = f"""
You are a baseball content creator. I need to finish a video titled "{topic}" which ranks iconic moments from 2010–today.

I already have the following {len(existing)} moments:
{json.dumps(used_titles, indent=2)}

Give me {needed_count} more unique moments that:
- Are from 2010 onward
- Do not feature the same players or moment titles above
- Are likely to have full game footage on YouTube
- Are emotional, dramatic, or viral

Format them as a JSON array using these fields:
- "rank": integer (starting after the last one)
- "title": short string
- "player": string or list
- "team": string or list
- "date": e.g. "October 14, 2015"
- "description": 1–2 sentences
- "youtube_search": search terms to find it
- "timestamp_hint": e.g. "9th inning", "extra innings"

Do not repeat players or titles.
Return ONLY a raw JSON array.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        raw = response.choices[0].message.content.strip()

        if raw.startswith("```json"):
            raw = raw[len("```json"):].strip()
        if raw.endswith("```"):
            raw = raw[:-3].strip()

        extra = json.loads(raw)

        # Patch ranks to follow the last one
        last_rank = max(m["rank"] for m in existing)
        for i, m in enumerate(extra):
            m["rank"] = last_rank + i + 1

        return extra[:needed_count]

    except Exception as e:
        print(f"❌ Error filling in missing moments: {e}")
        return []

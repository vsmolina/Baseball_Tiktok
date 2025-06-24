def format_moment_for_script(moment):
    return f"""#{moment['rank']}: {moment['title']}
Player: {moment['player']}
Teams: {moment['team']}
Date: {moment['date']}
What Happened: {moment['description']}
Search YouTube: {moment['youtube_search']}
Timestamp Hint: {moment.get('timestamp_hint', 'N/A')}
"""

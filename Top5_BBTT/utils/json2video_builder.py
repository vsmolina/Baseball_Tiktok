def build_json2video_scene(clip_paths: list[str], metadata: list[dict]) -> dict:
    scenes = []

    # Intro scene using built-in template
    scenes.append({
        "elements": [
            {
                "type": "text",
                "text": "Top 5 Catches in the 2010s",
                "template": "text/title",
                "start": 0,
                "duration": 3,
                "animation": {
                    "name": "fadeIn",
                    "duration": 1
                }
            }
        ],
        "duration": 3
    })

    for path, moment in zip(clip_paths, metadata):
        if not path:
            continue

        scenes.append({
            "elements": [
                {
                    "type": "video",
                    "src": path.replace("\\", "/"),
                    "start": 0,
                    "duration": 10,
                    "style": "top: 0; left: 0; width: 100%; height: 100%;",
                    "transition": {
                        "in": "fade",
                        "out": "fade"
                    }
                },
                {
                    "type": "text",
                    "text": moment["title"],
                    "template": "text/lower-third",
                    "start": 0.5,
                    "duration": 3.5,
                    "animation": {
                        "name": "slideInUp",
                        "duration": 1
                    }
                }
            ]
        })

    return {
        "scenes": scenes
    }

import requests
import json

class StoryAgent:
    def __init__(self):
        self.api_url = "http://your ip/v1/chat/completions"
        self.model = "gemma-3-12b-it"

    def stream_story(self, prompt, session_id):
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.8,
            "stream": True
        }

        buffer = ""  # 累積文字片段

        with requests.post(self.api_url, json=payload, stream=True) as response:
            for line in response.iter_lines():
                if line:
                    decoded = line.decode("utf-8")
                    if decoded.startswith("data: "):
                        data = decoded[6:]
                        if data.strip() == "[DONE]":
                            if buffer:
                                yield buffer
                            break
                        try:
                            piece = json.loads(data)["choices"][0]["delta"].get("content", "")
                            buffer += piece
                            if "\n" in piece or piece.endswith("。") or piece.endswith("！"):
                                yield buffer
                                buffer = ""
                        except Exception as e:
                            yield f"[錯誤] {str(e)}"

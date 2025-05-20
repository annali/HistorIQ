import requests

def ask_ai(prompt):
    # 本地的 LM Studio API endpoint
    url = "http://your ip/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "gemma-3-12b-it",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        res = requests.post(url, json=data, headers=headers)
        return res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"無法取得 AI 回覆：{e}"

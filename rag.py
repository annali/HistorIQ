class RAGRetriever:
    def __init__(self):
        self.knowledge_base = {
            "孔明借東風": {
                "context": "赤壁之戰前夕，諸葛亮觀察天象，預測東風將起，以火攻大破曹操水軍。",
                "source": "https://zh.wikipedia.org/wiki/赤壁之戰"
            },
            "項羽烏江自刎": {
                "context": "楚漢相爭末期，項羽兵敗突圍至烏江邊，不肯過江逃生，選擇自刎殉國。",
                "source": "https://zh.wikipedia.org/wiki/項羽"
            }
        }

    def retrieve(self, query):
        for keyword, data in self.knowledge_base.items():
            if keyword in query:
                return f"[歷史背景]：{data['context']}\n\n[來源連結]({data['source']})"
        return "[目前未找到對應背景資料]"

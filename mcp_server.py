from rag import RAGRetriever
from story_agent import StoryAgent
from uuid import uuid4

class MCPServer:
    def __init__(self):
        self.sessions = {}
        self.rag = RAGRetriever()
        self.agent = StoryAgent()

    def get_session_id(self):
        return str(uuid4())

    def stream_story(self, user_input, session_id):
        print("🚀 發送 prompt 至 LLM")
        if session_id not in self.sessions:
            self.sessions[session_id] = []

        history = self.sessions[session_id]
        context = "\n".join([f"使用者：{q}\nAI：{a}" for q, a in history])
        external_knowledge = self.rag.retrieve(user_input)

        prompt = f'''
            你是一位歷史小說作家，擅長將真實歷史人物與事件轉化為可出版的精彩小說故事。
            
            當使用者輸入一個歷史人物或事件名稱（如：司馬懿、黃巾之亂、赤壁之戰），請立即構思並撰寫一篇劇情生動、細節豐富、充滿畫面感的歷史小說。
            
            請務必嚴格根據該人物或事件所處的真實歷史朝代、背景、時間、人事物，進行故事描寫。
            - 不可穿越錯時代人物，例如不可將唐朝事件與清朝人物混合，也不可虛構不存在該時代的要素。
            - 歷史場景與人物請考據真實背景與關係後進行文學敘事。
            
            請適度引用該時代的詩詞、經典詞句、歷史語錄，使讀者能增進人文素養與語感，並透過故事更喜歡經典與歷史。
            
            每篇故事需包含 4~6 個章節，章節標題應由你根據劇情自行創作，具有文學性與主題意象（如「忍人所不能忍」、「風起西北」等）。
            
            - 使用 Markdown 格式：
              - `#` 為主標題（主題名稱）
              - `##` 為章節標題（動態生成）
              - 每章合理分段、包含角色心理、對話、場景與歷史衝突
            - 請勿輸出任何 AI 思考過程、分析或技術語言
            - 請勿描述角色動作或場景（除非為小說描寫階段）
            - 內容需符合小說級敘事品質，可直接用於出書
            - 字數約100字以上
            
            {external_knowledge}
            
            {context}
            {user_input}
            '''
        return self.agent.stream_story(prompt, session_id)

    def summarize(self, content):
        prompt = f"請將以下歷史故事內容濃縮為三句話摘要，輸出使用 Markdown 清單格式，請使用 - 作為每一句的開頭：\n{content}"
        return self.agent.get_response(prompt, self.get_session_id())

    def chapter_titles(self, topic):
        prompt = f"請幫我針對主題『{topic}』規劃一本精彩的歷史小說章節目錄，每章節請簡要敘述主軸，使用 markdown 清單格式。"
        return self.agent.get_response(prompt, self.get_session_id())

    def variant_style(self, content, style):
        prompt = f"請用{style}風格重寫以下歷史故事內容，保持事實正確：\n{content}"
        return self.agent.get_response(prompt, self.get_session_id())

    def continue_story(self, content):
        prompt = f"你剛剛寫了一段精彩的歷史小說，請從下方內容繼續寫下去，延續劇情風格並使用 markdown 格式：\n{content}"
        return self.agent.get_response(prompt, self.get_session_id())

    def answer_about_story(self, story, question):
        prompt = f"""
            你是一位歷史顧問與學者，剛剛讀者讓你生成了一篇小說內容，現在讀者根據小說內容提出一個問題。
            
            請你根據小說中的敘述內容與歷史背景，僅用問答形式回答問題。
            - **不要續寫故事**
            - **不要加入章節或情節**
            - **請勿描述角色動作或場景**
            - 直接用知識與推理清楚回答即可。
            
            【小說內容】
            {story}
            
            【讀者問題】
            {question}
            
            請直接作答：
            """
        return self.agent.get_response(prompt, self.get_session_id())


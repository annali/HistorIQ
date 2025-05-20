# HistorIQ
HistorIQ 是一個基於模型上下文協議（Model Context Protocol, MCP）架構的 AI 歷史小說平台。整合了 RAG（Retrieval-Augmented Generation）、AI Agent、與本地部署的大語言模型（LLM），讓使用者能夠以自然語言提問歷史事件、人物與文化主題，系統則透過多階段推理與知識檢索生成具脈絡性的回答。

## 主要特色

- **AI 多輪互動**：支援上下文記憶的 AI 回答能力
- **RAG 模型整合**：結合資料庫知識檢索與語言模型生成，提升正確性與可信度
- **MCP 架構實作**：明確劃分 MCP Server / Client / Agent / RAG 模組，架構清晰
- **故事式回應**：支援章節生成與延伸探索，適合用於歷史教育與知識導覽
- **語音輸入與朗讀**：提供講書人模式，打造沉浸式學習體驗
- **本專案遵循 MCP（Model Context Protocol）模型上下文協議 的設計原則，並實作以下關鍵模組與規範：**

| 模組                 | 說明                                                    | 實作狀態   |
| ------------------ | ----------------------------------------------------- | ------ |
| `MCP Server`       | 作為上下文協議核心中介，處理多輪對話狀態、代理分流、語境管理與任務調度                   | ✅ 已完成  |
| `MCP Client (Web)` | 提供使用者互動入口，支援問題輸入、上下文顯示、按鈕互動等                          | ✅ 已完成  |
| `AI Agent`         | 接收 Server 任務委派，進行多步推理與角色化內容生成                         | ✅ 已完成  |
| `RAG Retriever`    | 檢索外部知識內容（如歷史資料庫）並回傳上下文給 AI 模型使用                       | ✅ 已完成  |
| `LLM 接口模組`         | 支援本地 LLM（如 LM Studio）語言模型的 API 呼叫與回應解析       | ✅ 已完成  |
| `功能選單控制`           | 故事結束後提供互動按鈕，如「延伸故事」、「轉換風格」等操作，並由 MCP Server 分派對應服務    | ✅ 已完成  |
| `上下文管理機制`          | 每位使用者會有獨立 session ID，並記錄歷史問答脈絡，提供語境維持功能               | ✅ 已完成  |
| `多模組解耦架構`          | 各模組（RAG、Agent、Server、Client）具備明確職責與獨立維護界線             | ✅ 已完成  |
| `延伸任務鏈設計`          | 支援故事後續分支與按鈕觸發任務，如「AI 講書人」、「產出摘要」等                     | ✅ 已完成  |
| `MCP 規範相容性`        | 遵守 MCP 的 Request/Response 與任務分層邏輯，可擴展至更多 Agent 或 Tool | ✅ 初步完成 |

## 整體架構與功能模組概覽
| 模組層          | 元件                     | 說明                     |
| ------------ | ---------------------- | ---------------------- |
| `MCP Client` | `index.html`, `app.py` | 前端頁面與 Web API 入口       |
| `MCP Server` | `mcp_server.py`        | 實作所有 AI 邏輯與服務功能        |
| `AI Agent`   | `story_agent.py`       | 呼叫 LLM 生成內容（Gemma）     |
| `RAG`        | `rag.py`               | 向量搜尋補充知識背景（已掛入 prompt） |

## MCP Server 所提供的服務總表
| 函式                 | API               | 功能描述            |
| ------------------ | ----------------- | --------------- |
| `stream_story()`   | `/stream`         | 根據輸入主題串流生成歷史小說  |
| `summarize()`      | `/summarize`      | 三句話濃縮故事摘要       |
| `chapter_titles()` | `/chapter-titles` | 自動生成章節標題與概要     |
| `variant_style()`  | `/variant-style`  | 以指定風格（如詩意）重寫內容  |
| `continue_story()` | `/continue-story` | 從原內容延續劇情並追加後續章節 |

## 使用者互動功能（前端整合）
| 功能按鈕      | 描述             | 對應 API            |
| --------- | -------------- | ----------------- |
| `開始朗讀` | 文字朗讀並同步高亮段落    | Web Speech API    |
| `摘要`   | 產出三句簡潔摘要       | `/summarize`      |
| `章節`   | 章節目錄建議（含主題與描述） | `/chapter-titles` |
| `換風格`  | 詩意/史詩風改寫內容     | `/variant-style`  |
| `續寫故事` | 延續章節，保持敘事連貫性   | `/continue-story` |

## 特殊優化設計亮點
- ✅ 輸入欄與功能區 固定在底部
- ✅ AI 串流輸出時，內容由上往下自然堆疊
- ✅ 使用 Markdown 格式排版，美觀清晰
- ✅ 引導 AI 融合歷代詩詞與經典語錄，提升人文素養
- ✅ 具備基本 RAG 植入，可擴充知識強化模組


## 前端ui畫面展示
#### 剛開始的畫面
![image](https://github.com/user-attachments/assets/396b3464-5c43-49d3-980d-8817228eab4a)

#### 文章產製完畢的畫面
![image](https://github.com/user-attachments/assets/c1987c21-c9df-4291-843d-bc9dbf71d2b4)

#### 點擊摘要按鈕後的畫面
![image](https://github.com/user-attachments/assets/13594882-5a7e-4e14-97b4-cea83a4694ad)

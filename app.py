from flask import Flask, render_template, request, session, Response, jsonify
from uuid import uuid4
from mcp_server import MCPServer
import markdown2

app = Flask(__name__)
app.secret_key = "a-super-secret-key"

mcp = MCPServer()

@app.route("/")
def index():
    if "session_id" not in session:
        session["session_id"] = str(uuid4())
    return render_template("index.html", response="", history=[])

@app.route("/stream", methods=["GET"])
def stream():
    user_input = request.args.get("question", "")
    session_id = session.get("session_id", str(uuid4()))

    def generate():
        for chunk in mcp.stream_story(user_input, session_id):
            yield f"data: {chunk}\n\n"
    return Response(generate(), content_type='text/event-stream')

@app.route("/summarize", methods=["POST"])
def summarize():
    content = request.json.get("content")
    summary = mcp.summarize(content)
    if hasattr(summary, '__iter__') and not isinstance(summary, str):
        summary = ''.join(summary)  # 將 generator 合併成字串
    return jsonify({"summary": summary})

@app.route("/chapter-titles", methods=["POST"])
def chapter_titles():
    topic = request.json.get("topic")
    return jsonify({"titles_md": mcp.chapter_titles(topic)})

@app.route("/variant-style", methods=["POST"])
def variant_style():
    content = request.json.get("content")
    style = request.json.get("style")
    return jsonify({"styled_text": mcp.variant_style(content, style)})

@app.route("/continue-story", methods=["POST"])
def continue_story():
    content = request.json.get("content")
    continuation = mcp.continue_story(content)
    return jsonify({"continued": continuation})


@app.route("/qa-on-story", methods=["POST"])
def qa_on_story():
    data = request.json
    story = data.get("story")
    question = data.get("question")
    response = mcp.answer_about_story(story, question)
    return jsonify({"answer": response})


if __name__ == "__main__":
    app.run(debug=True)


import os

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from rag.retriever import retrieve, get_unique_sources
from rag.generator import generate_answer


app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/ask", methods=["POST"])
def ask():

    try:
        data = request.get_json()

        question = data.get("question", "").strip()

        if not question:
            return jsonify({
                "error": "Question is required"
            }), 400

        chunks = retrieve(question, top_k=10)

        if not chunks:
            return jsonify({
                "answer": "I could not find relevant information in the report.",
                "sources": []
            })

        answer = generate_answer(question, chunks)

        sources = get_unique_sources(chunks)

        return jsonify({
            "answer": answer,
            "sources": sources
        })

    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({
            "error": "An error occurred while processing the question."
        }), 500


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )

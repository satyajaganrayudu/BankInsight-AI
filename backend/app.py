from flask import Flask, render_template, request, jsonify

from rag.retriever import retrieve, get_unique_sources
from rag.generator import generate_answer


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")




@app.route("/api/ask", methods=["POST"])
def ask():

    data = request.get_json()

    question = data.get("question", "").strip()

    if not question:
        return jsonify({
            "answer": "Please enter a question.",
            "sources": []
        }), 400


    # Simple greetings should not query the RAG system
    greetings = {
        "hi",
        "hello",
        "hey",
        "hii",
        "hiii",
        "good morning",
        "good afternoon",
        "good evening"
    }

    if question.lower() in greetings:

        return jsonify({
            "answer": (
                "Hello! 👋 I'm BankInsight AI. "
                "Ask me something about your financial report."
            ),
            "sources": []
        })


    try:

        # Retrieve candidate chunks
        chunks = retrieve(
            question,
            top_k=10
        )

        if not chunks:

            return jsonify({
                "answer": (
                    "I couldn't find relevant information "
                    "in the financial report."
                ),
                "sources": []
            })


        # Generate answer
        answer = generate_answer(
            question,
            chunks
        )


        # Determine relevant sources
        sources = []

        question_lower = question.lower()


        # Standalone questions
        if "standalone" in question_lower:

            for chunk in chunks:

                section = (
                    chunk.get("section") or ""
                ).lower()

                if "standalone financial results" in section:

                    source = {
                        "page": chunk.get("page"),
                        "section": chunk.get("section")
                    }

                    if source not in sources:
                        sources.append(source)


        # Consolidated questions
        elif "consolidated" in question_lower:

            for chunk in chunks:

                section = (
                    chunk.get("section") or ""
                ).lower()

                if "consolidated financial results" in section:

                    source = {
                        "page": chunk.get("page"),
                        "section": chunk.get("section")
                    }

                    if source not in sources:
                        sources.append(source)


        # If no explicit standalone/consolidated request,
        # use the best relevant retrieved source.
        else:

            if chunks:

                best = chunks[0]

                sources.append({
                    "page": best.get("page"),
                    "section": best.get("section")
                })


        return jsonify({
            "answer": answer,
            "sources": sources
        })


    except Exception as e:

        print("ERROR:", e)

        return jsonify({
            "answer": (
                "Something went wrong while "
                "processing your question."
            ),
            "sources": []
        }), 500


if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )
from retriever import retrieve
from generator import generate_answer


def main():

    print("==============================")
    print("       BANK INSIGHT AI")
    print("          RAG TEST")
    print("==============================")

    question = input(
        "\nAsk a question about the report: "
    )

    # --------------------------------
    # RETRIEVAL
    # --------------------------------

    print("\n==============================")
    print("RETRIEVING RELEVANT INFORMATION")
    print("==============================")

    chunks = retrieve(
        question,
        top_k=10
    )

    print(f"\nRetrieved {len(chunks)} candidate chunks")

    # Show retrieved chunks
    for i, chunk in enumerate(chunks):

        print(f"\n--- CANDIDATE {i + 1} ---")

        print("Page:", chunk["page"])
        print("Section:", chunk["section"])
        print("Distance:", chunk["distance"])

        print("\nContent:")
        print(chunk["text"][:1200])

    # --------------------------------
    # GENERATION
    # --------------------------------

    print("\n==============================")
    print("GENERATING ANSWER WITH GEMINI")
    print("==============================")

    answer = generate_answer(
        question,
        chunks
    )

    # --------------------------------
    # FINAL ANSWER
    # --------------------------------

    print("\n==============================")
    print("FINAL ANSWER")
    print("==============================")

    print(answer)

    # --------------------------------
    # SOURCES
    # --------------------------------

    print("\n==============================")
    print("SOURCES")
    print("==============================")

    seen = set()

    for chunk in chunks:

        key = (
            chunk["page"],
            chunk["section"]
        )

        if key not in seen:

            print(
                f"Page {chunk['page']} - "
                f"{chunk['section']}"
            )

            seen.add(key)


if __name__ == "__main__":
    main()
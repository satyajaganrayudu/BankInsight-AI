import chromadb

from embeddings import model


CHROMA_PATH = "../vectorstore/chroma"


def search(question, top_k=3):

    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    collection = client.get_collection(
        name="bankinsight_q1_v2"
    )

    # Convert user question into an embedding
    query_embedding = model.encode(
        [question],
        normalize_embeddings=True
    )

    # Search ChromaDB
    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=top_k
    )

    return results


if __name__ == "__main__":

    question = input(
        "Ask a question about the report: "
    )

    results = search(question,top_k=8)

    print("\n==============================")
    print("RETRIEVED RESULTS")
    print("==============================")

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for i in range(len(documents)):

        print(f"\n--- RESULT {i + 1} ---")

        print("Page:", metadatas[i]["page"])

        print(
            "Section:",
            metadatas[i]["section"]
        )

        print(
            "Distance:",
            distances[i]
        )

        print("\nContent:")

        print(documents[i])	
from retriever import retrieve


question = "What was HDFC Bank's standalone net profit for the quarter ended June 30, 2026?"

print("==============================")
print("   CHROMA CLOUD RETRIEVER TEST")
print("==============================")

chunks = retrieve(question, top_k=5)

print(f"\nRetrieved {len(chunks)} chunks")

for i, chunk in enumerate(chunks, 1):

    print(f"\n--- RESULT {i} ---")

    print("Page:", chunk["page"])
    print("Section:", chunk["section"])
    print("Distance:", chunk["distance"])

    print("\nContent:")
    print(chunk["text"][:1000])
from ingest import extract_pdf
from chunker import create_chunks
from embeddings import create_embeddings


PDF_PATH = "../data/Q1_FY_Report.pdf"


print("1. Extracting PDF...")

pages = extract_pdf(PDF_PATH)

print("Pages:", len(pages))


print("\n2. Creating chunks...")

chunks = create_chunks(pages)

print("Chunks:", len(chunks))


print("\n3. Creating embeddings...")

embeddings = create_embeddings(chunks)


print("\n==============================")
print("EMBEDDING TEST")
print("==============================")

print("Number of chunks:", len(chunks))

print("Embedding shape:", embeddings.shape)

print("First vector:")

print(embeddings[0])

print("\nVector dimension:", len(embeddings[0]))
import os
import chromadb

from dotenv import load_dotenv

from embeddings import create_embeddings
from ingest import extract_pdf
from chunker import create_chunks


# Load environment variables from backend/.env
load_dotenv(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".env"
    )
)


PDF_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "Q1_FY_Report.pdf"
)

COLLECTION_NAME = "bankinsight_q1_v2"


def build_vector_database():

    print("==============================")
    print("   BANK INSIGHT AI")
    print("   CHROMA CLOUD INGESTION")
    print("==============================")

    # --------------------------------------------------
    # 1. Extract PDF
    # --------------------------------------------------

    print("\n1. Extracting PDF...")

    pages = extract_pdf(PDF_PATH)

    print(f"Pages: {len(pages)}")


    # --------------------------------------------------
    # 2. Create chunks
    # --------------------------------------------------

    print("\n2. Creating chunks...")

    chunks = create_chunks(pages)

    print(f"Chunks: {len(chunks)}")


    # --------------------------------------------------
    # 3. Create embeddings
    # --------------------------------------------------

    print("\n3. Creating embeddings...")

    embeddings = create_embeddings(chunks)

    print(
        f"Embeddings shape: {embeddings.shape}"
    )


    # --------------------------------------------------
    # 4. Connect to Chroma Cloud
    # --------------------------------------------------

    print("\n4. Connecting to Chroma Cloud...")

    api_key = os.getenv("CHROMA_API_KEY")
    tenant = os.getenv("CHROMA_TENANT")
    database = os.getenv("CHROMA_DATABASE")

    if not api_key:
        raise ValueError(
            "CHROMA_API_KEY not found in backend/.env"
        )

    if not tenant:
        raise ValueError(
            "CHROMA_TENANT not found in backend/.env"
        )

    if not database:
        raise ValueError(
            "CHROMA_DATABASE not found in backend/.env"
        )


    print("API key: loaded")
    print("Tenant: loaded")
    print(f"Database: {database}")


    client = chromadb.CloudClient(
        api_key=api_key,
        tenant=tenant,
        database=database
    )


    # --------------------------------------------------
    # 5. Get / create collection
    # --------------------------------------------------

    print(
        f"\n5. Using collection: {COLLECTION_NAME}"
    )

    try:

        collection = client.get_collection(
            name=COLLECTION_NAME
        )

        print("Existing collection found.")

    except Exception:

        print("Collection does not exist.")
        print("Creating collection...")

        collection = client.create_collection(
            name=COLLECTION_NAME
        )


    # --------------------------------------------------
    # 6. Delete existing documents
    # --------------------------------------------------

    existing_count = collection.count()

    print(
        f"Existing documents: {existing_count}"
    )


    if existing_count > 0:

        print(
            "Deleting existing documents..."
        )

        existing = collection.get()

        existing_ids = existing.get("ids", [])

        if existing_ids:

            collection.delete(
                ids=existing_ids
            )

        print("Existing documents deleted.")


    # --------------------------------------------------
    # 7. Prepare data
    # --------------------------------------------------

    print("\n6. Preparing documents...")

    ids = [
        f"chunk_{i}"
        for i in range(len(chunks))
    ]


    documents = [
        chunk["text"]
        for chunk in chunks
    ]


    metadatas = [
        {
            "page": chunk["page"],
            "section": chunk["section"],
            "source": chunk["source"]
        }
        for chunk in chunks
    ]


    # --------------------------------------------------
    # 8. Upload to Chroma Cloud
    # --------------------------------------------------

    print("\n7. Uploading to Chroma Cloud...")

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )


    # --------------------------------------------------
    # 9. Verify
    # --------------------------------------------------

    print("\n==============================")
    print("   CHROMA CLOUD READY")
    print("==============================")

    print(
        "Documents stored:",
        collection.count()
    )


if __name__ == "__main__":

    build_vector_database()
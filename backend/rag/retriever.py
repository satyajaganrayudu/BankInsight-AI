import os
import chromadb

from dotenv import load_dotenv
from .embeddings import model


# Load backend/.env
load_dotenv(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".env"
    )
)


COLLECTION_NAME = "bankinsight_q1_v2"


def get_chroma_collection():

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

    client = chromadb.CloudClient(
        api_key=api_key,
        tenant=tenant,
        database=database
    )

    collection = client.get_collection(
        name=COLLECTION_NAME
    )

    return collection


def retrieve(question, top_k=10):

    collection = get_chroma_collection()

    # Convert question into embedding
    query_embedding = model.encode(
        [question],
        normalize_embeddings=True
    )

    # Search Chroma Cloud
    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=top_k
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    chunks = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        chunks.append({
            "page": metadata.get("page"),
            "section": metadata.get("section"),
            "source": metadata.get("source"),
            "distance": distance,
            "text": document
        })

    return chunks


def get_unique_sources(chunks):

    sources = []
    seen = set()

    for chunk in chunks:

        key = (
            chunk.get("page"),
            chunk.get("section")
        )

        if key in seen:
            continue

        seen.add(key)

        sources.append({
            "page": chunk.get("page"),
            "section": chunk.get("section")
        })

    return sources

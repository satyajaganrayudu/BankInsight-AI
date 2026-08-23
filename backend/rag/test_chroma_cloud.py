import os
import chromadb
from dotenv import load_dotenv


# ============================================================
# LOAD .ENV
# ============================================================

load_dotenv(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".env"
    )
)


print("==============================")
print("       CHROMA CLOUD TEST")
print("==============================")


# ============================================================
# READ CHROMA CREDENTIALS
# ============================================================

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
print("Database:", database)


# ============================================================
# CONNECT TO CHROMA CLOUD
# ============================================================

client = chromadb.CloudClient(
    api_key=api_key,
    tenant=tenant,
    database=database
)


# ============================================================
# TEST CONNECTION
# ============================================================

print()
print("Testing connection...")

heartbeat = client.heartbeat()

print("Heartbeat:", heartbeat)


# ============================================================
# LIST COLLECTIONS
# ============================================================

print()
print("Collections:")

collections = client.list_collections()


if not collections:

    print("No collections found.")

else:

    for collection in collections:

        print(
            "-",
            collection.name
        )


# ============================================================
# SUCCESS
# ============================================================

print()
print("==============================")
print("CHROMA CLOUD CONNECTION OK")
print("==============================")
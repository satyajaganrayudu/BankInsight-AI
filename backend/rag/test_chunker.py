from ingest import extract_pdf
from chunker import create_chunks


pages = extract_pdf("../data/Q1_FY_Report.pdf")

chunks = create_chunks(pages)

print("Total chunks:", len(chunks))

for i, chunk in enumerate(chunks[:5]):

    print("\n====================")
    print("CHUNK:", i + 1)
    print("PAGE:", chunk["page"])
    print("SOURCE:", chunk["source"])
    print("====================")

    print(chunk["text"])
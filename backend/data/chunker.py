def create_chunks(pages, chunk_size=500, overlap=150):

    chunks = []

    for page in pages:

        text = page["text"]
        page_number = page["page"]

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end].strip()

            if chunk_text:

                chunks.append({
                    "text": chunk_text,
                    "page": page_number,
                    "source": "Q1_FY_Report.pdf"
                })

            start += chunk_size - overlap

    return chunks
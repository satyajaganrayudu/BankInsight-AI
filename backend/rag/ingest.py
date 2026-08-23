import pymupdf


def extract_pdf(pdf_path="../data/Q1_FY_Report.pdf"):
    pages = []

    document = pymupdf.open(pdf_path)

    for page_number, page in enumerate(document, start=1):
        text = page.get_text("text")

        if text.strip():
            pages.append({
                "page": page_number,
                "text": text.strip()
            })

    document.close()

    return pages


if __name__ == "__main__":

    pages = extract_pdf()

    print("Total pages:", len(pages))

    for page in pages[:2]:
        print("\nPAGE:", page["page"])
        print(page["text"][:1000])
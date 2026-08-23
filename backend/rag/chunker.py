import re


def clean_text(text):
    """Clean PDF extraction noise while preserving useful structure."""

    # Normalize common PDF extraction issues
    text = text.replace("\r", "\n")

    # Fix repeated whitespace
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    return text.strip()


def detect_section(text):
    """Detect the major section represented by the page."""

    section_keywords = [
        "UNAUDITED STANDALONE FINANCIAL RESULTS",
        "CONSOLIDATED FINANCIAL RESULTS",
        "STANDALONE SEGMENT",
        "CONSOLIDATED SEGMENT",
        "FINANCIAL METRICS",
        "PRODUCT-WISE ADVANCES",
        "BALANCE SHEET",
        "CASH FLOW",
        "NOTES TO ACCOUNTS",
        "INDEPENDENT AUDITOR",
    ]

    upper_text = text.upper()

    for keyword in section_keywords:

        if keyword in upper_text:
            return keyword.title()

    return "General"


def detect_unit(text):
    """Detect common financial units."""

    unit_patterns = [
        r"\(in crore\)",
        r"\(₹ crore\)",
        r"\(₹ bn\)",
        r"\(in ₹ crore\)",
        r"\(in %\)",
    ]

    for pattern in unit_patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(0)

    return None


def create_chunks(
    pages,
    chunk_size=500,
    overlap=200
):

    chunks = []

    for page in pages:

        page_number = page["page"]

        text = clean_text(
            page["text"]
        )

        if not text:
            continue

        section = detect_section(text)

        unit = detect_unit(text)

        start = 0

        while start < len(text):

            end = min(
                start + chunk_size,
                len(text)
            )

            chunk_text = text[
                start:end
            ].strip()

            if chunk_text:

                # Add document context to every chunk.
                context = (
                    "Document: HDFC Bank "
                    "Q1 FY Financial Report\n"
                    f"Page: {page_number}\n"
                    f"Section: {section}\n"
                )

                if unit:
                    context += f"Unit: {unit}\n"

                context += "\n"

                final_text = (
                    context +
                    chunk_text
                )

                chunks.append({
                    "text": final_text,
                    "page": page_number,
                    "section": section,
                    "source": "Q1_FY_Report.pdf"
                })

            if end >= len(text):
                break

            start = end - overlap

    return chunks
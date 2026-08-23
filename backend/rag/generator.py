import os
import random

from dotenv import load_dotenv
from google import genai


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


# ============================================================
# LOAD GEMINI API KEYS
# ============================================================

API_KEYS = []

for i in range(1, 20):

    key = os.getenv(
        f"GEMINI_API_KEY_{i}"
    )

    if key:
        API_KEYS.append(key.strip())


if not API_KEYS:

    raise ValueError(
        "No Gemini API keys found in backend/.env"
    )


print(
    f"Loaded {len(API_KEYS)} Gemini API keys"
)


# ============================================================
# GENERATE ANSWER
# ============================================================

def generate_answer(question, chunks):

    # --------------------------------------------------------
    # BUILD CONTEXT
    # --------------------------------------------------------

    context_parts = []

    for i, chunk in enumerate(chunks):

        context_parts.append(
            f"""
==============================
SOURCE {i + 1}
==============================

Page: {chunk.get("page")}
Section: {chunk.get("section")}

Content:
{chunk.get("text", "")}
"""
        )

    context = "\n".join(context_parts)


    # --------------------------------------------------------
    # GEMINI PROMPT
    # --------------------------------------------------------

    prompt = f"""
You are BankInsight AI, an assistant that answers questions
using ONLY the provided financial report context.

USER QUESTION:
{question}

FINANCIAL REPORT CONTEXT:
{context}

IMPORTANT RULES:

1. Answer using ONLY the financial report context above.

2. Pay close attention to the exact wording of the question.

3. Distinguish between:
   - Standalone Financial Results
   - Consolidated Financial Results
   - Segment information
   - Subsidiary information
   - Auditor information

4. If the question asks for "standalone", prioritize the
   "Unaudited Standalone Financial Results" section.

5. If the question asks for "consolidated", prioritize the
   "Unaudited Consolidated Financial Results" section.

6. Do NOT use a subsidiary's financial result as the answer
   for HDFC Bank itself.

7. Match the requested date exactly.

8. Match the requested financial metric exactly.

9. When multiple numbers are present, determine which number
   belongs to the requested row and requested period.

10. Remember that financial tables may contain several columns.
    The first value normally corresponds to the most recent
    quarter shown in the table.

11. Do not blindly combine numbers from different rows,
    sections, or reporting periods.

12. Do not guess.

13. If the answer is present in the context, ALWAYS provide
    the answer.

14. If the question is a greeting such as "hi" or "hello",
    respond naturally and do not search for a financial answer.

15. Keep the answer concise and useful.

16. Give the answer in this format when it is a financial
    question:

Answer:
<direct answer>

Explanation:
<short explanation>

Source:
Page <page number> - <section>

17. If there are multiple possible interpretations, explain
    the distinction clearly.

Now answer the user's question.
"""


    # --------------------------------------------------------
    # SHUFFLE API KEYS
    # --------------------------------------------------------

    available_keys = API_KEYS.copy()

    random.shuffle(
        available_keys
    )


    # --------------------------------------------------------
    # TRY EACH API KEY
    # --------------------------------------------------------

    last_error = None

    for api_key in available_keys:

        try:

            print(
                f"Trying Gemini API key ...{api_key[-6:]}"
            )


            # Create Gemini client
            client = genai.Client(
                api_key=api_key
            )


            # Generate response
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )


            print(
                "Gemini response successful"
            )


            return response.text


        except Exception as e:

            last_error = e

            error_text = str(e)


            # ------------------------------------------------
            # QUOTA ERROR
            # ------------------------------------------------

            if (
                "429" in error_text
                or "RESOURCE_EXHAUSTED" in error_text
                or "quota" in error_text.lower()
            ):

                print(
                    f"Gemini key ...{api_key[-6:]} "
                    "has exceeded its quota."
                )

                print(
                    "Trying another API key..."
                )

                continue


            # ------------------------------------------------
            # OTHER ERROR
            # ------------------------------------------------

            print(
                f"Gemini error with key ...{api_key[-6:]}"
            )

            print(
                error_text
            )

            raise


    # ========================================================
    # ALL KEYS FAILED
    # ========================================================

    raise RuntimeError(
        "All Gemini API keys have exceeded their quota."
    )
# 🏦 BankInsight AI

> An AI-powered financial report question-answering system using **Retrieval-Augmented Generation (RAG)**, **Chroma Cloud**, **Sentence Transformers**, **Gemini**, and **Flask**.

BankInsight AI allows users to ask natural-language questions about financial reports and receive answers grounded in the uploaded financial documents, along with relevant source pages and sections.

---

## 📌 Problem Statement

Financial reports are often large, complex, and difficult to navigate.

Finding specific information such as:

- Net profit
- Total income
- Capital adequacy ratio
- Interest earned
- Operating expenses
- Consolidated profit
- Standalone financial results

usually requires manually searching through multiple pages.

### Problem

Traditional document search mainly relies on keyword matching and may return multiple occurrences of the same term.

For example:

> "What was HDFC Bank's standalone net profit for the quarter ended June 30, 2026?"

A simple keyword search may return information from:

- Standalone results
- Consolidated results
- Subsidiary results
- Previous quarters
- Full-year results

This can lead to incorrect answers.

### Solution

BankInsight AI uses **Retrieval-Augmented Generation (RAG)** to:

1. Extract information from financial reports.
2. Split the document into meaningful chunks.
3. Convert chunks into vector embeddings.
4. Store embeddings in Chroma Cloud.
5. Retrieve the most relevant chunks for a user's question.
6. Pass the retrieved context to Gemini.
7. Generate an answer using the financial report context.
8. Display relevant source pages and sections.

---

# 🏗️ System Architecture

```text
                         ┌──────────────────────┐
                         │    Financial PDF     │
                         │   Q1_FY_Report.pdf   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    PDF Extraction    │
                         │      ingest.py       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      Chunking        │
                         │     chunker.py       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Embedding Model    │
                         │ Sentence Transformers│
                         │    384 dimensions   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     Chroma Cloud     │
                         │    Vector Database   │
                         │ bankinsight_q1_v2    │
                         └──────────┬───────────┘
                                    │
                              User Question
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      Flask API       │
                         │       app.py         │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      Retriever       │
                         │    retriever.py      │
                         └──────────┬───────────┘
                                    │
                              Relevant Chunks
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       Gemini         │
                         │     generator.py     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     Final Answer     │
                         │    + Explanation     │
                         │      + Sources       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Flask Frontend    │
                         │    HTML + CSS + JS   │
                         └──────────────────────┘
```

---

# 🧠 What is RAG?

RAG stands for:

**Retrieval-Augmented Generation**

Instead of asking an AI model to answer a question purely from its own knowledge, RAG first retrieves relevant information from a private knowledge base.

The general process is:

```text
User Question
      ↓
Question Embedding
      ↓
Vector Search
      ↓
Relevant Document Chunks
      ↓
LLM / Gemini
      ↓
Grounded Answer
```

This allows the system to answer questions based on the uploaded financial report.

---

# 📂 Project Structure

```text
BankInsightAI/
│
├── backend/
│   │
│   ├── app.py
│   │
│   ├── .env
│   ├── .env.example
│   ├── requirements.txt
│   │
│   ├── data/
│   │   └── Q1_FY_Report.pdf
│   │
│   ├── rag/
│   │   ├── ingest.py
│   │   ├── chunker.py
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   ├── retriever.py
│   │   ├── generator.py
│   │   └── test_*.py
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   └── static/
│       ├── css/
│       │   └── style.css
│       │
│       └── js/
│           └── app.js
│
└── frontend/
```

---

# 🔄 RAG Pipeline

## 1. PDF Extraction

### File

```text
rag/ingest.py
```

The financial PDF is read and converted into structured text.

Example:

```text
Financial Report
       ↓
Page 1
Page 2
Page 3
...
Page 16
```

The system keeps useful metadata such as:

- Page number
- Section
- Source document

---

# 2. Document Chunking

### File

```text
rag/chunker.py
```

Large document pages are divided into smaller chunks.

For the current HDFC Bank report:

```text
16 PDF pages
      ↓
168 chunks
```

Each chunk contains information such as:

```python
{
    "text": "...",
    "page": 1,
    "section": "Unaudited Standalone Financial Results",
    "source": "HDFC Bank Q1 FY Financial Report"
}
```

Chunking allows the vector database to search smaller pieces of information instead of the entire document.

---

# 3. Embeddings

### File

```text
rag/embeddings.py
```

The project uses a Sentence Transformer embedding model.

Text is converted into numerical vectors.

Example:

```text
"What was the standalone net profit?"
                    ↓
             Embedding Model
                    ↓
       [0.021, -0.153, 0.087, ...]
```

The current system generates:

```text
168 embeddings
384 dimensions
```

The vectors represent the semantic meaning of the document chunks.

---

# 4. Chroma Cloud

### File

```text
rag/vector_store.py
```

The embeddings, document text, and metadata are stored in **Chroma Cloud**.

Current collection:

```text
bankinsight_q1_v2
```

Current database:

```text
bankinsight
```

The collection currently contains:

```text
168 documents
```

Each stored record contains:

```text
ID
Document
Embedding
Metadata
```

Metadata:

```text
page
section
source
```

This allows the application to return source information together with the generated answer.

---

# 5. Retrieval

### File

```text
rag/retriever.py
```

When a user asks:

```text
What was HDFC Bank's standalone net profit?
```

the question is converted into an embedding.

Chroma Cloud performs a similarity search.

The system retrieves the most relevant chunks.

```text
Question
    ↓
Question Embedding
    ↓
Chroma Cloud
    ↓
Top-K Relevant Chunks
```

A retrieved chunk looks like:

```python
{
    "page": 1,
    "section": "Unaudited Standalone Financial Results",
    "source": "HDFC Bank Q1 FY Financial Report",
    "distance": 0.57,
    "text": "..."
}
```

The `distance` represents the similarity-search distance returned by Chroma.

---

# 6. Gemini Generation

### File

```text
rag/generator.py
```

The retrieved document chunks are passed to Gemini.

The prompt instructs Gemini to:

- Use the supplied financial report context.
- Pay attention to the exact question.
- Distinguish standalone and consolidated results.
- Match the requested date.
- Match the requested financial metric.
- Avoid guessing.
- Avoid using subsidiary information as HDFC Bank's result.
- Provide a clear answer.
- Provide an explanation.
- Provide source information.

The generation flow is:

```text
User Question
      +
Retrieved Context
      ↓
    Gemini
      ↓
Answer
Explanation
Source
```

---

# 7. Flask API

### File

```text
backend/app.py
```

Flask connects the frontend to the RAG pipeline.

Example API endpoint:

```http
POST /api/ask
```

Request:

```json
{
    "question": "What was the standalone net profit?"
}
```

The backend performs:

```text
Question
   ↓
Retriever
   ↓
Chroma Cloud
   ↓
Relevant Chunks
   ↓
Gemini
   ↓
Answer
   ↓
JSON Response
```

Example response:

```json
{
    "answer": "HDFC Bank's standalone net profit was ₹19,059.72 crore.",
    "sources": [
        {
            "page": 1,
            "section": "Unaudited Standalone Financial Results"
        }
    ]
}
```

---

# 🎨 Frontend

The project uses Flask templates for the frontend.

Technologies:

```text
HTML
CSS
JavaScript
```

The interface provides:

- Chat interface
- User questions
- AI answers
- Source cards
- Suggested questions
- Financial report context

Example suggested questions:

```text
What was the standalone net profit?

What was the total income?

What was the capital adequacy ratio?
```

---

# 🔎 Example RAG Query

### User Question

```text
What was HDFC Bank's standalone net profit for the quarter ended June 30, 2026?
```

### Retrieval

The system searches Chroma Cloud and retrieves relevant chunks from the financial report.

The most relevant standalone result is found in:

```text
Page 1
Unaudited Standalone Financial Results
```

### Generated Answer

```text
HDFC Bank's standalone net profit for the quarter ended
June 30, 2026, was ₹19,059.72 crore.
```

### Source

```text
Page 1
Unaudited Standalone Financial Results
```

---

# 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web server and API |
| HTML | Frontend structure |
| CSS | Frontend styling |
| JavaScript | Frontend interaction |
| Sentence Transformers | Text embeddings |
| Chroma Cloud | Vector database |
| Gemini | Answer generation |
| python-dotenv | Environment variables |
| PDF extraction library | Financial report extraction |

---

# 🔐 Environment Variables

Create:

```text
backend/.env
```

Add:

```env
GEMINI_API_KEY=your_gemini_api_key

CHROMA_API_KEY=your_chroma_api_key
CHROMA_TENANT=your_chroma_tenant
CHROMA_DATABASE=bankinsight
```

Never commit the actual `.env` file to GitHub.

Use `.env.example`:

```env
GEMINI_API_KEY=

CHROMA_API_KEY=
CHROMA_TENANT=
CHROMA_DATABASE=
```

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/BankInsightAI.git
cd BankInsightAI
```

---

## 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

Activate:

```powershell
venv\Scripts\activate
```

---

## 3. Install dependencies

```powershell
pip install -r requirements.txt
```

---

## 4. Configure environment variables

Create:

```text
backend/.env
```

Add your Gemini and Chroma Cloud credentials:

```env
GEMINI_API_KEY=your_key

CHROMA_API_KEY=your_key
CHROMA_TENANT=your_tenant
CHROMA_DATABASE=bankinsight
```

---

# 📥 Building the Vector Database

Place the financial PDF inside:

```text
backend/data/
```

Example:

```text
backend/data/Q1_FY_Report.pdf
```

Then run:

```powershell
cd backend
python rag/vector_store.py
```

Expected output:

```text
1. Extracting PDF...
Pages: 16

2. Creating chunks...
Chunks: 168

3. Creating embeddings...
Embeddings shape: (168, 384)

4. Connecting to ChromaDB...

5. Storing data in ChromaDB...

==============================
   CHROMA CLOUD READY
==============================
Documents stored: 168
```

---

# 🔎 Testing Chroma Cloud Retrieval

Run:

```powershell
python rag/test_cloud_retriever.py
```

Expected output:

```text
==============================
   CHROMA CLOUD RETRIEVER TEST
==============================

Retrieved 5 chunks

--- RESULT 1 ---
Page: 13
Section: General
...
```

---

# 🚀 Running the Application

From the backend directory:

```powershell
python app.py
```

The Flask server starts at:

```text
http://127.0.0.1:5000
```

Open the address in your browser.

---

# 📊 Complete Data Flow

```text
                  OFFLINE / INGESTION
                  ==================

                Q1_FY_Report.pdf
                       │
                       ▼
                  ingest.py
                       │
                       ▼
                  chunker.py
                       │
                       ▼
                embeddings.py
                       │
                       ▼
                 Chroma Cloud
                       │
                       │
                       │
                       ▼
                  STORED DATA


                  ONLINE / QUERY
                  ==============

                  User Question
                       │
                       ▼
                    Flask
                    app.py
                       │
                       ▼
                 retriever.py
                       │
                       ▼
                 Chroma Cloud
                       │
                       ▼
               Relevant Chunks
                       │
                       ▼
                 generator.py
                       │
                       ▼
                    Gemini
                       │
                       ▼
                 Final Answer
                       │
                       ▼
                  Flask API
                       │
                       ▼
                  Frontend UI
```

---

# 🧩 Core Components

## `app.py`

Responsible for:

- Starting Flask.
- Serving the frontend.
- Receiving API requests.
- Calling the retriever.
- Calling the generator.
- Returning the final response.

---

## `ingest.py`

Responsible for:

- Reading the financial PDF.
- Extracting page text.
- Preserving page information.

---

## `chunker.py`

Responsible for:

- Splitting extracted text.
- Creating manageable retrieval units.
- Preserving metadata.

---

## `embeddings.py`

Responsible for:

- Loading the embedding model.
- Converting text into vector representations.

---

## `vector_store.py`

Responsible for:

- Extracting the PDF.
- Creating chunks.
- Generating embeddings.
- Connecting to Chroma Cloud.
- Creating/updating the collection.
- Uploading documents, embeddings, and metadata.

---

## `retriever.py`

Responsible for:

- Connecting to Chroma Cloud.
- Converting the user question into an embedding.
- Performing vector similarity search.
- Returning relevant chunks.
- Returning unique source pages.

---

## `generator.py`

Responsible for:

- Loading Gemini configuration.
- Building the RAG prompt.
- Sending retrieved context to Gemini.
- Generating the final answer.

---

# 🎯 Why Chroma Cloud?

The project originally used a local Chroma database.

The architecture was later changed to Chroma Cloud.

### Local

```text
Application
    ↓
Local Chroma Database
    ↓
Local Disk
```

### Current

```text
Application
    ↓
Chroma Cloud
    ↓
Cloud Vector Database
```

This makes the vector database accessible independently from the local machine and is more suitable for deploying the application.

---

# 🔢 Current Vector Database

The current financial report produces:

```text
PDF Pages:       16
Chunks:          168
Embedding Size:  384
Collection:      bankinsight_q1_v2
Database:        bankinsight
Storage:         Chroma Cloud
```

---

# 🎯 Key Features

- 📄 Financial PDF question answering
- 🔎 Semantic vector search
- ☁️ Chroma Cloud vector database
- 🤖 Gemini-powered answers
- 📚 Source page references
- 🏦 Standalone vs consolidated distinction
- 📊 Financial metric retrieval
- 💬 Conversational interface
- 🔐 Environment-based secret management
- 🧩 Modular RAG architecture
- 🌐 Flask REST API

---

# 🧪 Example Questions

```text
What was HDFC Bank's standalone net profit?

What was the total income?

What was the capital adequacy ratio?

What was the consolidated net profit?

What was the operating profit?

What was the interest earned?

What were the total operating expenses?

What was the profit before tax?
```

---

# 🔮 Future Improvements

Potential future improvements:

- Multiple financial reports
- PDF upload from the UI
- Automatic document ingestion
- Multi-document search
- Financial comparison between quarters
- Financial charts
- Table extraction
- Authentication
- Chat history
- Streaming AI responses
- Hybrid keyword + vector search
- Reranking
- Citation highlighting
- Report comparison
- Financial trend analysis
- User-specific document collections

---

# 📚 Concepts Demonstrated

This project demonstrates practical implementation of:

- Retrieval-Augmented Generation
- Vector databases
- Embeddings
- Semantic search
- Large Language Models
- Prompt engineering
- REST APIs
- Flask
- Cloud databases
- Document processing
- Metadata handling
- Frontend/backend integration

---

# 🧠 RAG in One Diagram

```text
                    DOCUMENT
                       │
                       ▼
                 Extract Text
                       │
                       ▼
                    Chunk
                       │
                       ▼
                   Embed
                       │
                       ▼
                CHROMA CLOUD
                       │
                       │
              ┌────────┘
              │
              ▼
        USER QUESTION
              │
              ▼
            Embed
              │
              ▼
        Similarity Search
              │
              ▼
       Relevant Documents
              │
              ▼
            GEMINI
              │
              ▼
        Grounded Answer
              │
              ▼
          SOURCE PAGES
```

---

# 🔐 Security Notes

Never commit API keys to GitHub.

The following files should remain private:

```text
.env
```

The `.gitignore` should contain:

```gitignore
.env
.env.*
!.env.example
```

The repository should only contain:

```text
.env.example
```

with empty values.

---

# 🚀 Project Status

```text
✅ PDF extraction
✅ Document chunking
✅ Embedding generation
✅ Chroma Cloud integration
✅ Vector database creation
✅ Semantic retrieval
✅ Gemini generation
✅ Flask API
✅ Flask frontend
✅ Source references
✅ Standalone/consolidated distinction
```

---

# 👨‍💻 Project

**BankInsight AI**

An AI-powered financial report assistant demonstrating how RAG can be applied to financial documents.

The core pipeline is:

```text
PDF
 ↓
Extract
 ↓
Chunk
 ↓
Embed
 ↓
Chroma Cloud
 ↓
Retrieve
 ↓
Gemini
 ↓
Flask API
 ↓
Frontend
 ↓
Answer + Sources
```

---

## ⭐ Future Vision

BankInsight AI can eventually become a complete financial intelligence platform capable of analyzing multiple companies, financial years, quarters, reports, and financial metrics through natural-language interaction.

```text
              BANKINSIGHT AI
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
     Reports     Companies    Metrics
        │           │           │
        └───────────┼───────────┘
                    ▼
              RAG Pipeline
                    │
                    ▼
             Financial AI
                    │
                    ▼
       Answers + Analysis + Sources
```

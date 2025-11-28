# 🦅 HawkAI: Sociological Concept Explorer

HawkAI is a **Retrieval-Augmented Generation (RAG)** semantic search engine designed to bridge the gap between abstract academic theories and real-world human experiences.

Built for the **Department of Sociology** @UNCW, this tool allows researchers and students to input complex sociological concepts (e.g., *"Anomie"* or *"The Bystander Effect"*) and instantly retrieve relevant, emotional personal narratives from a secure corpus of student writing.

---

## 🚀 Key Features

* **Semantic Vector Search:** Uses high-dimensional vector embeddings (`embedding-001`) to find matches based on *meaning* and *sentiment*, not just keyword overlap.
* **Context-Aware Analysis:** Retrieves the single most relevant student narrative and feeds it into **Google's Gemini 1.5 Flash** model to generate a custom analysis.
* **Automated Pipeline:** Custom ETL (Extract, Transform, Load) scripts to ingest, clean, and embed hundreds of unstructured `.docx` and `.pdf` documents.
* **Optimized Performance:** Implements a caching system (JSON/Pickle) to ensure sub-second query speeds on lightweight hardware (deployed on PythonAnywhere).

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **AI & LLM:** Google Gemini API (`gemini-1.5-flash`, `embedding-001`)
* **Backend:** Flask (REST API)
* **Data Processing:** NumPy (Vector Math/Dot Product), PyMuPDF (PDF parsing), python-docx
* **Frontend:** HTML5, Bootstrap 5, Vanilla JavaScript
* **Deployment:** PythonAnywhere

---

## 🧠 How It Works (The RAG Architecture)

HawkAI operates in two distinct phases to maximize efficiency and accuracy.

### Phase 1: The "Indexer" (`setup.py`)
1.  **Ingestion:** Scans a directory of raw student papers (Word & PDF).
2.  **Embedding:** Sends text in batched requests to the Gemini Embedding API to generate 768-dimensional vectors.
3.  **Caching:** Saves the text and vectors into a local database (`embeddingDatabase.json`), handling API rate limits automatically.

### Phase 2: The "Runtime" (`app.py` & `runtime.py`)
1.  **Query:** User inputs a concept (e.g., "Imposter Syndrome").
2.  **Vector Math:** The system embeds the query and performs a **Cosine Similarity/Dot Product** calculation against the cached database.
3.  **Retrieval:** Identifies the narrative with the highest similarity score.
4.  **Synthesis:** Constructs a prompt with the retrieved text and instructs the LLM to:
    * Extract a specific *personal anecdote* (quote).
    * Summarize the context.
    * Explain the sociological concept using the story as evidence.

# 🦅 HawkAI

**A Retrieval-Augmented Generation platform that connects students to each other's experiences through semantic search.**

HawkAI is the first custom LLM application of its kind at UNCW. Rather than generating content from a general-purpose model, it searches a corpus of 500+ student essays by *meaning and emotional context*, retrieves the most relevant narrative, and generates a structured sociological analysis, enabling students to query and connect with their peers' past work.

Built for the Department of Sociology & Criminology at the University of North Carolina Wilmington as part of ongoing LLM research. 
Research paper: *Generating Connections, Not Content: The Hawk AI Place-Based LLM* (Elliott, Engelman, Oh, Butler).

---

## The Problem

Most LLMs treat users as isolated individuals querying a generic knowledge base. Students writing about shared experiences — identity, community, belonging, inequality — had no way to discover that their peers had grappled with the same concepts. Hundreds of reflective essays sat in folders, disconnected from each other and from future students.

## The Solution

HawkAI bridges that gap. A student inputs a sociological concept like *"Anomie"* or *"The Beauty Myth"*, and the system:

1. **Embeds the query** into a high-dimensional vector using Google's `embedding-001` model
2. **Searches the entire knowledge base** via dot-product similarity, ranking narratives by relevance, not keyword overlap
3. **Generates a structured response** through Gemini 2.5 Pro: a direct quote from the matched narrative, a contextual summary, and an academic analysis applying the concept

The result is a tool that teaches sociological thinking *through the lived experiences of real students*.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      ETL Pipeline                       │
│                       setup.py                          │
│                                                         │
│   .docx / .pdf  ──►  Text Extraction  ──►  Gemini      │
│     documents         (docx, PyMuPDF)      Embedding    │
│                                             API         │
│                            │                            │
│                            ▼                            │
│                   embeddingDatabase.json                 │
│                   (vector index cache)                   │
└─────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│                   Runtime Pipeline                       │
│                     runtime.py                          │
│                                                         │
│   User Query  ──►  Embed Query  ──►  Dot-Product        │
│                     (Gemini)         Similarity          │
│                                      (NumPy)            │
│                                         │               │
│                                         ▼               │
│                                  Best Narrative         │
│                                         │               │
│                                         ▼               │
│                                  Gemini 2.5 Pro         │
│                                  (Structured Output)    │
└─────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│                    Flask Web App                         │
│                       app.py                            │
│                                                         │
│   index.html  ◄──►  /api/hawkai  ◄──►  Runtime          │
│   (frontend)         (POST endpoint)    Functions       │
└─────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
HawkAI/
├── app.py              # Flask web server & API endpoint
├── runtime.py          # Core logic: embedding, search, generation
├── setup.py            # ETL pipeline: document ingestion & indexing
├── main.py             # CLI entry point for testing queries
├── templates/
│   └── index.html      # Frontend interface
└── embeddingDatabase.json  # Cached vector index (not in repo)
```

### Module Breakdown

**`setup.py`** — ETL Pipeline
- Reads `.docx` files (python-docx) and `.pdf` files (PyMuPDF) from a target directory
- Batch-embeds all extracted text via Gemini's embedding API
- Serializes the text + embedding pairs to a JSON cache file

**`runtime.py`** — Search & Generation
- Loads the cached vector index into memory
- Embeds incoming user queries with the same model
- Computes dot-product similarity across all narrative vectors using NumPy
- Passes the top-ranked narrative + user concept into a structured prompt for Gemini 2.5 Pro

**`app.py`** — Web Application
- Loads the vector index on startup
- Serves the frontend and exposes a `/api/hawkai` POST endpoint
- Returns the generated analysis and similarity score as JSON

**`main.py`** — CLI Testing
- Standalone script for running queries against the index without the web server

---

## How It Works

### 1. Building the Index (One-Time Setup)

```bash
python setup.py
```

This ingests all documents from the target folder, embeds each one through the Gemini API, and writes the full index to `embeddingDatabase.json`.

### 2. Running the Application

```bash
export GOOGLE_API_KEY=your_key_here
python app.py
```

The server loads the cached index into memory and starts listening on `http://localhost:5001`.

### 3. Querying

Send a POST request to `/api/hawkai`:

```json
{
  "concept": "The Looking Glass Self"
}
```

Response:

```json
{
  "result": "Quote from Student Narrative: ...\n\nBrief Summary: ...\n\nDescription of Sociological Concept: ...",
  "score": 0.8234
}
```

---

## Tech Stack

- **Language:** Python
- **Web Framework:** Flask
- **LLM / Embedding API:** Google Gemini (embedding-001, Gemini 2.5 Pro)
- **Vector Math:** NumPy
- **Document Parsing:** python-docx, PyMuPDF (fitz)
- **Caching:** JSON serialization
- **Deployment:** PythonAnywhere

---

## Background

This project evolved through 20+ prototype iterations over the course of a year. It started as an exploration of Copilot Studio for classroom engagement, grew into a custom Gemini API integration, and ultimately became the technical foundation for a research paper on place-based LLMs.

The core thesis of the research: LLMs don't have to be tools for individual productivity. They can be platforms for connecting people through shared narrative. HawkAI is the proof of concept.

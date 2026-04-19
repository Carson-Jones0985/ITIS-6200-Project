# Prompt Injection Attacks on a RAG-Based AI Assistant
ITIS-6200 | Carson Jones & Kartheek Jonnalagadda

A Retrieval Augmented Generation (RAG) question & answer assistant that demonstrates prompt injection attacks and defenses using LLaMA 3, LangChain, and ChromaDB.

---

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.ai/) installed and running

---

## Installation

**1. Clone the repository:**
```bash
git clone <https://github.com/Carson-Jones0985/ITIS-6200-Project.git>
cd ITIS-6200-Project
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Pull the required Ollama model:**
```bash
ollama pull llama3
```

---

## Running the App

```bash
python -m streamlit run app.py
```
---

## Generating Attack PDFs

Run this once to generate the attack PDFs used for testing:

```bash
python pdf_attack.py
```

This will create two PDFs in the `attack_pdfs/` folder:
- `attack_visible.pdf` — financial report with a visible injection (50% lower values)
- `attack_hidden.pdf` — financial report with a hidden white text injection
- `cannot_help_visible.pdf` — injection that hijacks the LLM to refuse all responses
- `cannot_help_hidden.pdf` — hidden version of the above

---

## Usage

1. Start the app and upload a PDF using the file uploader
2. Type a question about the document in the text box
3. Use the **Defense Controls** in the left sidebar to toggle protections on and off

---

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
python generate_attack_pdfs.py
```

This will create two PDFs in the `attack_pdfs/` folder:
- `attack_visible_numbers.pdf` — financial report with a visible injection (50% lower values)
- `attack_hidden_numbers.pdf` — financial report with a hidden white text injection
- `attack_visible_cannot_help.pdf` — injection that hijacks the LLM to refuse all responses
- `attack_hidden_cannot_help.pdf` — hidden version of the above

---

## Usage

1. Start the app and upload a PDF using the file uploader
2. Type a question about the document in the text box
3. Use the **Defense Controls** in the left sidebar to toggle protections on and off

---

## Running the Success Case

1. Start the app: `python -m streamlit run app.py`
2. Ensure all three defenses are toggled **ON** in the sidebar
3. Generate attack PDFs if not already done: `python generate_attack_pdfs.py`
4. Upload any attack PDF from the `attack_pdfs/` folder
5. Ask "What is the net profit?"
6. The system should return the correct value and show defense activity in the Defense Details panel

## Running the Failure Case

1. Turn **all defenses OFF** in the sidebar
2. Upload `attack_pdfs/attack_visible_numbers.pdf`
3. Ask "What is the net profit?"
4. The LLM will return $60,000 instead of $120,000 — the attack succeeded
5. Upload `attack_pdfs/attack_visible_cannot_help.pdf`
6. Ask any question — the LLM will refuse to respond
7. Upload `attack_pdfs/visible_around_ifc.pdf`, turn **only sanitization ON**
8. Ask any question — the rephrased injection evades the sanitizer and succeeds

## How It Works

### Attack Implementation
Malicious PDFs are crafted using `fpdf2` with injection text embedded either as visible plaintext or hidden white text. When ingested, PyMuPDF extracts all text including the hidden injection, which gets stored in ChromaDB and retrieved alongside legitimate content.

### Information Flow Control (Biba)
Document chunks are assigned LOW integrity. Before building the LLM prompt, each chunk is scanned for control phrases. Chunks containing injection language are cleaned line-by-line — only the malicious lines are removed, preserving the financial data.

### Input Sanitization
Retrieved chunks are scanned line-by-line against a list of known injection phrases. Flagged lines are stripped before the chunk reaches the LLM, keeping the legitimate content intact.

### Output Filtering
After the LLM generates a response, it is checked against a list of suspicious patterns. If a match is found the response is intercepted before reaching the user.

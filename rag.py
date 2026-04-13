import fitz  # PyMuPDF
from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Initialize shared components
embeddings = OllamaEmbeddings(model="llama3")
vectorstore = Chroma(
    collection_name="documents",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)
llm = Ollama(model="llama3")


def ingest_pdf(file_path):
    """Extract text from PDF, chunk it, and store in ChromaDB."""
    
    # Extract raw text from every page
    doc = fitz.open(file_path)
    full_text = "\n".join(page.get_text() for page in doc)
    doc.close()

    # Split into overlapping chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_text(full_text)

    # Embed and store in ChromaDB
    vectorstore.add_texts(chunks)

    return len(chunks)


def query(question):
    """Retrieve relevant chunks and pass them to LLaMA 3."""

    # Find the 4 most relevant chunks
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    docs = retriever.get_relevant_documents(question)

    # Combine chunks into a context block
    context = "\n\n".join(doc.page_content for doc in docs)

    # Build the prompt
    prompt = f"""You are a helpful assistant. Use only the context below to answer the question. If the answer is not in the context, say "I don't know."

Context:
{context}

Question: {question}
Answer:"""

    # Step 4: Send to LLaMA 3 and return response
    return llm(prompt)
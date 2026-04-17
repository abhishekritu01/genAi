# 🚀 2-Week AI Engineer Project Plan
### Build → Break → Fix → Deploy → Ace the Interview

> **Goal:** Build 3 production-grade AI projects in 2 weeks that give you real war stories, debugging experience, and live demos to show interviewers.
>
> **Time required:** 3-4 hours/day
>
> **Cost:** ~$5-15 total (OpenAI API credits + free hosting)
>
> **End result:** 3 deployed projects + GitHub portfolio + real answers to every scenario question

---

## 📋 The 3 Projects

| # | Project | What You Build | Key Skills Proven |
|---|---------|---------------|-------------------|
| 1 | **DocMind** — RAG Q&A System | Upload any PDF → ask questions → get cited answers | Chunking, embeddings, vector DB, reranking, evaluation |
| 2 | **AutoAgent** — Research Agent | Give a topic → agent searches, reasons, writes a report | Agents, tool calling, LangGraph, streaming, LLMOps |
| 3 | **SmartChat** — Production Chatbot | Multi-user chat with memory, auth, monitoring, CI/CD | Memory, MLOps, deployment, observability, cost tracking |

---

## 🗓️ Full 2-Week Day-by-Day Plan

---

# WEEK 1 — Project 1: DocMind (RAG Q&A System)

---

## Day 1 — Setup + Naive RAG

**Goal:** Get a working RAG pipeline from scratch. No libraries hiding the magic.

### Morning (2 hours) — Environment Setup

```bash
# 1. Create project
mkdir docmind && cd docmind
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install langchain langchain-openai langchain-community \
            chromadb pypdf sentence-transformers \
            fastapi uvicorn python-multipart \
            tiktoken python-dotenv ragas

# 3. Setup .env
echo "OPENAI_API_KEY=your-key-here" > .env
echo "LANGCHAIN_API_KEY=your-langsmith-key" >> .env
echo "LANGCHAIN_TRACING_V2=true" >> .env
echo "LANGCHAIN_PROJECT=docmind-dev" >> .env

# 4. Get a test PDF (use any PDF — your resume, a paper, anything)
```

### Afternoon (2 hours) — Build Naive RAG

```python
# src/naive_rag.py
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

load_dotenv()

def build_naive_rag(pdf_path: str):
    # Step 1: Load PDF
    loader = PyPDFLoader(pdf_path)
    docs   = loader.load()
    print(f"Loaded {len(docs)} pages")

    # Step 2: Chunk
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = splitter.split_documents(docs)
    print(f"Created {len(chunks)} chunks")

    # Step 3: Embed + store
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectordb   = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory="./chroma_db"
    )
    print(f"Stored in ChromaDB")

    # Step 4: Build chain
    llm   = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectordb.as_retriever(search_kwargs={"k": 5}),
        return_source_documents=True
    )
    return chain

if __name__ == "__main__":
    chain  = build_naive_rag("test.pdf")
    result = chain.invoke("What is this document about?")
    print("Answer:", result["result"])
    print("Sources:", [d.metadata for d in result["source_documents"]])
```

### Evening Task — Intentionally Break It
```
Try these queries and note what fails:
1. Ask something that's definitely in the document — does it answer correctly?
2. Ask something NOT in the document — does it hallucinate or say it doesn't know?
3. Ask a very specific detail — does chunking cause it to lose context?

Write down 3 failure cases. You'll fix them tomorrow.
```

**✅ Day 1 Deliverable:** Working naive RAG that you can query. 3 documented failure cases.

---

## Day 2 — Advanced RAG (HyDE + Reranking)

**Goal:** Fix yesterday's failures with production techniques.

### Morning (2 hours) — Add HyDE

```python
# src/advanced_retrieval.py
from langchain.chains import HypotheticalDocumentEmbedder
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

def build_hyde_retriever(vectordb: Chroma):
    """HyDE: embed a hypothetical answer instead of the raw query."""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    hyde_embeddings = HypotheticalDocumentEmbedder.from_llm(
        llm=llm,
        embeddings=OpenAIEmbeddings(model="text-embedding-3-small"),
        prompt_key="web_search"
    )

    return vectordb.as_retriever(
        search_kwargs={"k": 20}  # Retrieve more, rerank later
    )

# src/reranker.py
from sentence_transformers import CrossEncoder
import numpy as np

class LocalReranker:
    def __init__(self):
        # Free local cross-encoder (downloads ~90MB first time)
        self.model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    def rerank(self, query: str, docs: list, top_n: int = 5) -> list:
        if not docs:
            return docs

        # Score each doc against the query
        pairs  = [[query, doc.page_content] for doc in docs]
        scores = self.model.predict(pairs)

        # Sort by score descending
        scored = sorted(zip(scores, docs), key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored[:top_n]]

# Test: compare naive vs reranked results
def compare_retrieval(query: str, vectordb: Chroma, reranker: LocalReranker):
    # Naive: top-5 by cosine similarity
    naive_docs = vectordb.similarity_search(query, k=5)

    # Advanced: top-20 cosine → rerank → top-5
    candidate_docs = vectordb.similarity_search(query, k=20)
    reranked_docs  = reranker.rerank(query, candidate_docs, top_n=5)

    print("=== NAIVE TOP-3 ===")
    for doc in naive_docs[:3]:
        print(f"  - {doc.page_content[:100]}...")

    print("\n=== RERANKED TOP-3 ===")
    for doc in reranked_docs[:3]:
        print(f"  - {doc.page_content[:100]}...")
```

### Afternoon (2 hours) — Add Query Expansion

```python
# src/query_expansion.py
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import ChatOpenAI
import logging

logging.basicConfig()
logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)

def build_multi_query_retriever(vectordb, llm=None):
    """Generate 3 query variants, retrieve for each, deduplicate."""
    if llm is None:
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    return MultiQueryRetriever.from_llm(
        retriever=vectordb.as_retriever(search_kwargs={"k": 5}),
        llm=llm
    )

# src/full_pipeline.py — combine everything
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

RAG_PROMPT = ChatPromptTemplate.from_template("""
You are a document assistant. Answer ONLY using the provided context.
If the answer is not in the context, say "I don't have that information."
After your answer, cite the sources as [Page X].

Context:
{context}

Question: {question}

Answer:""")

def advanced_rag_chain(query: str, vectordb, reranker):
    # 1. Retrieve candidates (more than needed)
    candidates = vectordb.similarity_search(query, k=20)

    # 2. Rerank
    top_docs = reranker.rerank(query, candidates, top_n=5)

    # 3. Build context with page citations
    context = "\n\n".join([
        f"[Page {doc.metadata.get('page', 'N/A')}]: {doc.page_content}"
        for doc in top_docs
    ])

    # 4. Generate answer
    llm    = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    chain  = RAG_PROMPT | llm | StrOutputParser()
    answer = chain.invoke({"context": context, "question": query})

    return {"answer": answer, "sources": top_docs}
```

**✅ Day 2 Deliverable:** Advanced RAG with HyDE + reranking. Run the same 3 failure cases from Day 1 — note improvements.

---

## Day 3 — FastAPI Backend + Evaluation

**Goal:** Wrap everything in an API and measure quality with RAGAS.

### Morning (2 hours) — FastAPI Backend

```python
# main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil, os, time

app = FastAPI(title="DocMind API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state (use Redis in production)
pipeline_cache = {}

class QueryRequest(BaseModel):
    doc_id: str
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: list[dict]
    latency_ms: int
    tokens_used: int

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a PDF and index it."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(400, "Only PDF files supported")

    # Save file
    doc_id    = file.filename.replace(".pdf", "").replace(" ", "_")
    file_path = f"uploads/{doc_id}.pdf"
    os.makedirs("uploads", exist_ok=True)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Build pipeline
    from src.ingestion import build_pipeline
    pipeline_cache[doc_id] = build_pipeline(file_path, doc_id)

    return {"doc_id": doc_id, "status": "indexed",
            "chunks": pipeline_cache[doc_id]["chunk_count"]}

@app.post("/query", response_model=QueryResponse)
async def query_document(request: QueryRequest):
    """Query an indexed document."""
    if request.doc_id not in pipeline_cache:
        raise HTTPException(404, f"Document '{request.doc_id}' not found. Upload first.")

    start     = time.time()
    pipeline  = pipeline_cache[request.doc_id]
    result    = pipeline["chain"](request.question)
    latency   = int((time.time() - start) * 1000)

    return QueryResponse(
        answer=result["answer"],
        sources=[{"page": d.metadata.get("page"), "text": d.page_content[:200]}
                 for d in result["sources"]],
        latency_ms=latency,
        tokens_used=result.get("tokens", 0)
    )

@app.get("/health")
def health():
    return {"status": "ok", "indexed_docs": list(pipeline_cache.keys())}
```

### Afternoon (2 hours) — Add RAGAS Evaluation

```python
# src/evaluate.py
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision,
)
from datasets import Dataset

def run_evaluation(pipeline, test_cases: list[dict]) -> dict:
    """
    test_cases format:
    [{"question": "...", "ground_truth": "..."}]
    """
    questions, answers, contexts, ground_truths = [], [], [], []

    for case in test_cases:
        result = pipeline["chain"](case["question"])
        questions.append(case["question"])
        answers.append(result["answer"])
        contexts.append([d.page_content for d in result["sources"]])
        ground_truths.append(case["ground_truth"])

    dataset = Dataset.from_dict({
        "question":     questions,
        "answer":       answers,
        "contexts":     contexts,
        "ground_truth": ground_truths,
    })

    results = evaluate(
        dataset,
        metrics=[faithfulness, answer_relevancy, context_recall, context_precision]
    )

    print("\n📊 Evaluation Results:")
    print(f"  Faithfulness:       {results['faithfulness']:.3f}")
    print(f"  Answer Relevancy:   {results['answer_relevancy']:.3f}")
    print(f"  Context Recall:     {results['context_recall']:.3f}")
    print(f"  Context Precision:  {results['context_precision']:.3f}")

    return results

# Create test cases for YOUR document
# (manually write 5-10 Q&A pairs based on the document content)
TEST_CASES = [
    {"question": "What is the main topic?", "ground_truth": "..."},
    {"question": "What are the key findings?", "ground_truth": "..."},
    # Add more based on your PDF
]
```

**✅ Day 3 Deliverable:** Running FastAPI server. RAGAS scores for your pipeline. Screenshot of evaluation results.

---

## Day 4 — Simple Frontend + Chunk Size Experiments

**Goal:** Build a UI and understand chunking tradeoffs through experiments.

### Morning (1.5 hours) — Simple HTML Frontend

```html
<!-- static/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>DocMind</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; }
        .upload-area { border: 2px dashed #ccc; padding: 30px; text-align: center; margin-bottom: 20px; }
        .chat-box { border: 1px solid #ccc; height: 400px; overflow-y: auto; padding: 15px; margin-bottom: 10px; }
        .message { margin: 10px 0; padding: 10px; border-radius: 8px; }
        .user { background: #e3f2fd; text-align: right; }
        .bot  { background: #f5f5f5; }
        .source { font-size: 0.8em; color: #666; margin-top: 5px; }
        input[type=text] { width: 80%; padding: 10px; }
        button { padding: 10px 20px; background: #2196F3; color: white; border: none; cursor: pointer; border-radius: 4px; }
    </style>
</head>
<body>
    <h1>📄 DocMind — Ask Your Documents</h1>

    <div class="upload-area">
        <input type="file" id="fileInput" accept=".pdf">
        <br><br>
        <button onclick="uploadFile()">Upload PDF</button>
        <p id="uploadStatus"></p>
    </div>

    <div class="chat-box" id="chatBox"></div>

    <div>
        <input type="text" id="questionInput" placeholder="Ask a question about your document..."
               onkeypress="if(event.key==='Enter') askQuestion()">
        <button onclick="askQuestion()">Ask</button>
    </div>

    <script>
        let currentDocId = null;

        async function uploadFile() {
            const file = document.getElementById('fileInput').files[0];
            if (!file) { alert('Select a PDF first'); return; }

            document.getElementById('uploadStatus').textContent = 'Uploading and indexing...';
            const formData = new FormData();
            formData.append('file', file);

            const res  = await fetch('/upload', { method: 'POST', body: formData });
            const data = await res.json();

            currentDocId = data.doc_id;
            document.getElementById('uploadStatus').textContent =
                `✅ Indexed! ${data.chunks} chunks created. Now ask questions.`;
        }

        async function askQuestion() {
            const question = document.getElementById('questionInput').value.trim();
            if (!question || !currentDocId) return;

            addMessage(question, 'user');
            document.getElementById('questionInput').value = '';

            const res = await fetch('/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ doc_id: currentDocId, question })
            });
            const data = await res.json();

            const sourcesText = data.sources
                .map(s => `[Page ${s.page}]`)
                .join(', ');
            addMessage(data.answer + `\n\n📄 Sources: ${sourcesText}\n⏱️ ${data.latency_ms}ms`, 'bot');
        }

        function addMessage(text, type) {
            const box = document.getElementById('chatBox');
            const div = document.createElement('div');
            div.className = `message ${type}`;
            div.innerText = text;
            box.appendChild(div);
            box.scrollTop = box.scrollHeight;
        }
    </script>
</body>
</html>
```

### Afternoon (2 hours) — Chunking Experiments

```python
# experiments/chunk_experiment.py
# THIS IS THE MOST IMPORTANT EXERCISE — run this and understand the results

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
import time, json

def test_chunk_size(pdf_path: str, chunk_size: int, chunk_overlap: int,
                   test_question: str, ground_truth: str) -> dict:
    """Test how chunk size affects retrieval quality."""
    from langchain_community.document_loaders import PyPDFLoader

    # Load and chunk
    docs     = PyPDFLoader(pdf_path).load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    chunks = splitter.split_documents(docs)

    # Index
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectordb   = Chroma.from_documents(
        chunks, embeddings,
        collection_name=f"test_chunk_{chunk_size}"
    )

    # Query
    start    = time.time()
    results  = vectordb.similarity_search(test_question, k=5)
    latency  = (time.time() - start) * 1000

    # Score: is ground truth in top results?
    combined_context = " ".join([r.page_content for r in results])
    hit = ground_truth.lower() in combined_context.lower()

    return {
        "chunk_size":    chunk_size,
        "num_chunks":    len(chunks),
        "latency_ms":    round(latency, 2),
        "ground_truth_found": hit,
        "top_chunk_preview": results[0].page_content[:150] if results else ""
    }

# Run experiment with your PDF
PDF_PATH      = "test.pdf"
TEST_QUESTION = "What is the main conclusion?"    # Change to match your PDF
GROUND_TRUTH  = "key phrase from the answer"      # Change to match your PDF

results = []
for chunk_size in [200, 500, 1000, 2000]:
    result = test_chunk_size(PDF_PATH, chunk_size, chunk_size // 10,
                             TEST_QUESTION, GROUND_TRUTH)
    results.append(result)
    print(f"Chunk size {chunk_size}: {result}")

# What you should observe:
# - Small chunks (200): many chunks, precise matching, but lose context
# - Medium chunks (500): sweet spot for most documents
# - Large chunks (1000+): full context but noisy embeddings, slower
print("\n💡 Key insight: smaller chunks = better precision, less context")
print("   Larger chunks = more context, noisier embeddings")
```

**✅ Day 4 Deliverable:** Working UI. Documented chunk experiment results with your own observations.

---

## Day 5 — Deploy DocMind to Production

**Goal:** Ship it. Real URL. Show it to someone.

### Morning (2 hours) — Prepare for Deployment

```
# Project structure should look like:
docmind/
├── main.py              # FastAPI app
├── src/
│   ├── ingestion.py
│   ├── retrieval.py
│   ├── reranker.py
│   └── evaluate.py
├── static/
│   └── index.html
├── requirements.txt
├── Dockerfile
├── .env.example         # Never commit .env!
├── .gitignore
└── README.md
```

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m appuser && chown -R appuser /app
USER appuser

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```
# requirements.txt
fastapi==0.111.0
uvicorn==0.30.0
langchain==0.2.0
langchain-openai==0.1.0
langchain-community==0.2.0
chromadb==0.5.0
pypdf==4.0.0
sentence-transformers==3.0.0
ragas==0.1.0
python-multipart==0.0.9
python-dotenv==1.0.0
tiktoken==0.7.0
```

### Afternoon (2 hours) — Deploy to Railway (Free)

```bash
# Option 1: Railway (easiest, free tier)
# 1. Go to railway.app, sign up with GitHub
# 2. New Project → Deploy from GitHub Repo
# 3. Add environment variable: OPENAI_API_KEY
# 4. Railway auto-detects Dockerfile, deploys in 3 minutes

# Option 2: Render (also free)
# 1. Go to render.com
# 2. New Web Service → Connect GitHub
# 3. Build Command: pip install -r requirements.txt
# 4. Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT

# Option 3: Hugging Face Spaces (free, great for demos)
# 1. Create Space, choose Gradio or Docker
# 2. Push code, add OPENAI_API_KEY as secret

# After deployment: test your live URL
curl https://your-app.railway.app/health
```

### Write Your README

```markdown
# DocMind — AI Document Q&A

**Live Demo:** https://your-url.railway.app

## What it does
Upload any PDF → Ask questions → Get cited answers powered by RAG

## Technical Architecture
- **Chunking:** RecursiveCharacterTextSplitter (500 tokens, 50 overlap)
- **Embeddings:** OpenAI text-embedding-3-small (1536 dims)
- **Vector DB:** ChromaDB (HNSW index)
- **Retrieval:** Retrieve top-20 → Cross-encoder rerank → top-5
- **Generation:** GPT-4o-mini with citation prompting
- **Evaluation:** RAGAS (faithfulness: 0.87, answer relevancy: 0.91)

## What I Learned
- Chunk size 500 outperforms 200 and 1000 for my test docs (documented in experiments/)
- Reranking improved precision@5 by ~30% over cosine similarity alone
- HyDE helps most for abstract/conceptual questions, less for factual lookups

## Tech Stack
FastAPI · LangChain · ChromaDB · OpenAI · Docker · Railway
```

**✅ Day 5 Deliverable:** DocMind is LIVE at a public URL. GitHub repo with README and eval scores.

---

## Day 6 — Week 1 Review + Interview Practice

**Goal:** Solidify what you learned before starting Project 2.

### Morning (1.5 hours) — Write Your War Stories

Answer these questions from memory (no looking at code):

```
1. What was the biggest failure you encountered with naive RAG?
   → How did you diagnose it?
   → How did you fix it?

2. What surprised you about chunk size experiments?
   → What chunk size worked best and WHY?

3. How much did reranking actually help?
   → Specific numbers from your RAGAS evaluation

4. What would you do differently if you had to rebuild this?

5. How would you scale DocMind to handle 10,000 documents?
```

### Afternoon (1.5 hours) — Practice Explaining Your Project

Practice this 2-minute explanation out loud:

```
"I built DocMind — a production RAG system. The architecture is:
ingest PDFs → chunk at 500 tokens → embed with text-embedding-3-small
→ store in ChromaDB → at query time: retrieve top-20 candidates
→ cross-encoder reranking to top-5 → GPT-4o-mini generation with citations.

I evaluated it with RAGAS and got faithfulness of X and answer relevancy of Y.

The biggest thing I learned was [your real insight from the experiments].
When I changed chunk size from 500 to 1000, recall went up but precision
dropped because the embeddings got noisier. [Real observation from your experiments]

I deployed it on Railway, it's live at [URL]."
```

**✅ Day 6 Deliverable:** Written war stories document. Can explain project in 2 minutes without notes.

---

# WEEK 2 — Project 2 (Day 7-9) + Project 3 (Day 10-13) + Final Day

---

## Day 7 — Project 2: AutoAgent Setup + Basic Agent

**Goal:** Build a research agent that can use tools to gather and synthesize information.

### Morning (2 hours) — Setup + First Agent

```bash
mkdir autoagent && cd autoagent
pip install langchain langgraph langchain-openai \
            langchain-community tavily-python \
            fastapi uvicorn streamlit python-dotenv

# Get free Tavily API key at tavily.com (100 searches/month free)
echo "TAVILY_API_KEY=your-key" >> .env
```

```python
# src/basic_agent.py
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

# Define tools
search_tool = TavilySearchResults(max_results=3)

@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression. Input: math expression as string."""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error: {e}"

@tool
def summarize_findings(findings: str) -> str:
    """Summarize a list of research findings into a structured report.
    Input: raw findings text."""
    llm = ChatOpenAI(model="gpt-4o-mini")
    return llm.invoke(f"Summarize these findings clearly:\n{findings}").content

# Create agent
tools = [search_tool, calculate, summarize_findings]
llm   = ChatOpenAI(model="gpt-4o", temperature=0)
agent = create_react_agent(llm, tools)

# Test
result = agent.invoke({
    "messages": [("user", "What are the latest developments in LLM quantization? "
                           "Summarize in 3 key points.")]
})
print(result["messages"][-1].content)
```

### Afternoon (2 hours) — LangGraph Custom Agent

```python
# src/research_agent.py
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
import operator

class ResearchState(TypedDict):
    messages:   Annotated[list, operator.add]
    topic:      str
    iterations: int
    report:     str

tools    = [TavilySearchResults(max_results=5)]
llm      = ChatOpenAI(model="gpt-4o", temperature=0).bind_tools(tools)
tool_node = ToolNode(tools)

RESEARCH_SYSTEM = """You are a research agent. Your job is to:
1. Search for information about the given topic
2. Gather at least 3-5 relevant facts
3. When you have enough information, write a structured report

Be thorough but concise. Always cite your sources."""

def agent_node(state: ResearchState):
    from langchain_core.messages import SystemMessage
    messages = [SystemMessage(content=RESEARCH_SYSTEM)] + state["messages"]
    response = llm.invoke(messages)
    return {
        "messages": [response],
        "iterations": state.get("iterations", 0) + 1
    }

def should_continue(state: ResearchState) -> str:
    last_message = state["messages"][-1]

    # Safety: max iterations
    if state.get("iterations", 0) >= 8:
        return "end"

    # If no tool calls, agent is done
    if not last_message.tool_calls:
        return "end"

    return "tools"

# Build graph
graph = StateGraph(ResearchState)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)
graph.set_entry_point("agent")
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", "end": END})
graph.add_edge("tools", "agent")

research_app = graph.compile()

def run_research(topic: str) -> str:
    result = research_app.invoke({
        "messages": [("user", f"Research this topic thoroughly: {topic}")],
        "topic":    topic,
        "iterations": 0,
        "report":   ""
    })
    return result["messages"][-1].content
```

**✅ Day 7 Deliverable:** Working research agent. Test it on 3 different topics.

---

## Day 8 — Add Streaming + Memory + Human-in-Loop

**Goal:** Make the agent production-ready with streaming responses and HITL.

### Morning (2 hours) — Streaming Agent

```python
# src/streaming_agent.py
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio, json

app = FastAPI()

async def stream_agent_response(topic: str):
    """Stream agent's thinking + final answer."""
    async for event in research_app.astream_events(
        {"messages": [("user", f"Research: {topic}")],
         "topic": topic, "iterations": 0, "report": ""},
        version="v2"
    ):
        event_type = event["event"]

        # Stream LLM tokens
        if event_type == "on_chat_model_stream":
            chunk = event["data"]["chunk"]
            if chunk.content:
                yield f"data: {json.dumps({'type': 'token', 'content': chunk.content})}\n\n"

        # Show when tools are called
        elif event_type == "on_tool_start":
            tool_name  = event["name"]
            tool_input = event["data"].get("input", {})
            yield f"data: {json.dumps({'type': 'tool_call', 'tool': tool_name, 'input': str(tool_input)[:100]})}\n\n"

        # Show tool results
        elif event_type == "on_tool_end":
            yield f"data: {json.dumps({'type': 'tool_result', 'tool': event['name']})}\n\n"

    yield f"data: {json.dumps({'type': 'done'})}\n\n"

@app.get("/research/stream")
async def research_stream(topic: str):
    return StreamingResponse(
        stream_agent_response(topic),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    )
```

### Afternoon (2 hours) — Human-in-the-Loop

```python
# src/hitl_agent.py — Agent pauses and asks for human approval
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END

checkpointer = MemorySaver()

# Same graph but compiled with interrupt_before
hitl_app = graph.compile(
    checkpointer=checkpointer,
    interrupt_before=["tools"]  # Pause before every tool use
)

def run_with_approval(topic: str, thread_id: str = "thread-1"):
    config = {"configurable": {"thread_id": thread_id}}

    # Start the agent
    result = hitl_app.invoke(
        {"messages": [("user", f"Research: {topic}")],
         "topic": topic, "iterations": 0, "report": ""},
        config
    )

    while True:
        state = hitl_app.get_state(config)

        # Check if we're at a breakpoint
        if not state.next:
            # Agent is done
            return state.values["messages"][-1].content

        # Show pending tool call
        last_msg = state.values["messages"][-1]
        if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
            tc = last_msg.tool_calls[0]
            print(f"\n🔧 Agent wants to call: {tc['name']}")
            print(f"   With input: {tc['args']}")

            approval = input("   Approve? (y/n): ").strip().lower()
            if approval != "y":
                # Inject rejection into state
                from langchain_core.messages import HumanMessage
                hitl_app.update_state(
                    config,
                    {"messages": [HumanMessage(content="Tool call rejected. Try a different approach.")]},
                    as_node="agent"
                )

        # Continue from breakpoint
        result = hitl_app.invoke(None, config)
```

**✅ Day 8 Deliverable:** Streaming agent with SSE. HITL demo where you can approve/reject tool calls.

---

## Day 9 — Deploy AutoAgent + Add Cost Tracking

### Morning (1.5 hours) — Cost Tracking

```python
# src/cost_tracker.py
from langchain_community.callbacks import get_openai_callback
import json
from datetime import datetime

class CostTracker:
    def __init__(self):
        self.sessions = []

    def track_research(self, topic: str, run_func):
        """Track cost and tokens for a research run."""
        with get_openai_callback() as cb:
            result = run_func(topic)

        record = {
            "timestamp":          datetime.utcnow().isoformat(),
            "topic":              topic,
            "total_tokens":       cb.total_tokens,
            "prompt_tokens":      cb.prompt_tokens,
            "completion_tokens":  cb.completion_tokens,
            "cost_usd":           round(cb.total_cost, 6),
            "llm_calls":          cb.successful_requests,
        }
        self.sessions.append(record)

        print(f"\n💰 Cost Breakdown:")
        print(f"   Total tokens:  {cb.total_tokens:,}")
        print(f"   LLM calls:     {cb.successful_requests}")
        print(f"   Total cost:    ${cb.total_cost:.4f}")

        return result, record

    def summary(self):
        total_cost = sum(s["cost_usd"] for s in self.sessions)
        print(f"\n📊 Session Summary: {len(self.sessions)} runs, ${total_cost:.4f} total")
```

### Afternoon (2 hours) — Deploy

```bash
# Deploy AutoAgent to Railway/Render (same as Project 1)

# Add Streamlit frontend for better demo
# streamlit_app.py
import streamlit as st
import requests, json

st.title("🔬 AutoAgent — AI Research Assistant")
st.caption("Powered by GPT-4o + Tavily Search + LangGraph")

topic = st.text_input("Research topic:", placeholder="e.g. Latest advances in RAG systems 2025")

if st.button("Start Research") and topic:
    with st.spinner("Researching..."):
        # Show streaming output
        response = requests.get(f"{API_URL}/research/stream",
                               params={"topic": topic}, stream=True)

        tool_calls_container = st.expander("🔧 Agent's actions", expanded=True)
        answer_container     = st.empty()
        full_answer = ""

        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode().replace("data: ", ""))
                if data["type"] == "tool_call":
                    tool_calls_container.write(f"🔍 Searching: {data['input']}")
                elif data["type"] == "token":
                    full_answer += data["content"]
                    answer_container.markdown(full_answer)
```

**✅ Day 9 Deliverable:** AutoAgent deployed with cost tracking. Streamlit UI. GitHub README with architecture.

---

## Day 10 — Project 3: SmartChat Setup + Multi-User Auth

**Goal:** Production chatbot with persistent memory, real auth, and monitoring.

### Morning (2 hours) — Project Setup + Auth

```bash
mkdir smartchat && cd smartchat
pip install fastapi uvicorn langchain langchain-openai \
            redis motor pymongo python-jose[cryptography] \
            passlib[bcrypt] langsmith prometheus-client \
            python-dotenv pydantic-settings
```

```python
# src/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
import os

SECRET_KEY  = os.getenv("SECRET_KEY", "change-in-production-32-char-minimum")
ALGORITHM   = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

pwd_context    = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme  = OAuth2PasswordBearer(tokenUrl="token")

# Fake user DB (use real DB in production)
USERS_DB = {
    "alice": {"username": "alice", "hashed_password": pwd_context.hash("alice123")},
    "bob":   {"username": "bob",   "hashed_password": pwd_context.hash("bob123")},
}

def create_access_token(data: dict) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({**data, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload  = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username not in USERS_DB:
            raise HTTPException(status_code=401, detail="User not found")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### Afternoon (2 hours) — Persistent Memory

```python
# src/memory.py
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.messages import HumanMessage, AIMessage
import json, os
from datetime import datetime

class UserMemoryManager:
    def __init__(self, user_id: str):
        self.user_id    = user_id
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

        # Per-user vector store for semantic memory
        self.memory_db = Chroma(
            collection_name=f"memory_{user_id}",
            embedding_function=self.embeddings,
            persist_directory=f"./user_data/{user_id}/memory"
        )

    def save_conversation_insight(self, insight: str):
        """Store an important fact extracted from conversation."""
        self.memory_db.add_texts(
            texts=[insight],
            metadatas=[{"user_id": self.user_id, "timestamp": datetime.utcnow().isoformat()}]
        )

    def recall_relevant_memories(self, current_message: str, k: int = 3) -> list[str]:
        """Retrieve memories relevant to current message."""
        if self.memory_db._collection.count() == 0:
            return []
        results = self.memory_db.similarity_search_with_score(current_message, k=k)
        return [doc.page_content for doc, score in results if score < 0.5]  # Lower = more similar

    def extract_and_save_insight(self, conversation: list[dict]):
        """Use LLM to extract memorable facts from recent conversation."""
        if len(conversation) < 2:
            return

        recent_turns = conversation[-4:]  # Last 2 turns
        llm          = ChatOpenAI(model="gpt-4o-mini", temperature=0)

        prompt = f"""
        Extract any personal preferences, facts, or goals the user mentioned.
        Return as a JSON list of short strings. If nothing memorable, return [].

        Conversation:
        {json.dumps(recent_turns, indent=2)}
        """

        try:
            insights = json.loads(llm.invoke(prompt).content)
            for insight in insights[:3]:  # Max 3 per turn
                self.save_conversation_insight(insight)
        except json.JSONDecodeError:
            pass  # Silently skip if extraction fails
```

**✅ Day 10 Deliverable:** Auth system working. Per-user memory storing and retrieving.

---

## Day 11 — Add Monitoring + Cost Dashboard

**Goal:** Real observability — see what's happening in production.

### Morning (2 hours) — LangSmith + Prometheus

```python
# src/monitoring.py
import os
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import FastAPI, Response
from langsmith import traceable

# Prometheus metrics
REQUEST_COUNT = Counter("chat_requests_total",   "Total chat requests", ["user_id", "status"])
RESPONSE_TIME = Histogram("chat_response_seconds", "Response time", ["user_id"])
TOKEN_COUNT   = Counter("tokens_used_total",     "Tokens used",    ["model", "token_type"])
COST_TOTAL    = Counter("cost_usd_total",        "Total cost USD", ["model"])
ACTIVE_USERS  = Gauge("active_users",            "Active users in last hour")

def record_llm_metrics(user_id: str, model: str, prompt_tokens: int,
                       completion_tokens: int, latency: float, status: str):
    from calculate_cost import calculate_cost

    REQUEST_COUNT.labels(user_id=user_id, status=status).inc()
    RESPONSE_TIME.labels(user_id=user_id).observe(latency)
    TOKEN_COUNT.labels(model=model, token_type="prompt").inc(prompt_tokens)
    TOKEN_COUNT.labels(model=model, token_type="completion").inc(completion_tokens)
    COST_TOTAL.labels(model=model).inc(
        calculate_cost(model, prompt_tokens, completion_tokens)
    )

# Expose metrics endpoint for Prometheus scraping
def add_metrics_endpoint(app: FastAPI):
    @app.get("/metrics")
    def metrics():
        return Response(generate_latest(), media_type="text/plain")
```

### Afternoon (2 hours) — Cost Dashboard

```python
# src/cost_dashboard.py
# Simple HTML dashboard showing cost/usage per user

DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>SmartChat Admin Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial; max-width: 1000px; margin: 40px auto; padding: 20px; }
        .card { border: 1px solid #ddd; padding: 20px; margin: 10px; border-radius: 8px; }
        .metric { font-size: 2em; font-weight: bold; color: #2196F3; }
    </style>
</head>
<body>
    <h1>📊 SmartChat Dashboard</h1>

    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;">
        <div class="card">
            <div>Total Requests Today</div>
            <div class="metric" id="totalRequests">-</div>
        </div>
        <div class="card">
            <div>Total Cost Today</div>
            <div class="metric" id="totalCost">-</div>
        </div>
        <div class="card">
            <div>Avg Response Time</div>
            <div class="metric" id="avgLatency">-</div>
        </div>
    </div>

    <div class="card">
        <h3>Requests Over Time</h3>
        <canvas id="requestChart" height="100"></canvas>
    </div>

    <script>
        async function loadStats() {
            const res  = await fetch('/admin/stats', {
                headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
            });
            const data = await res.json();
            document.getElementById('totalRequests').textContent = data.total_requests;
            document.getElementById('totalCost').textContent = '$' + data.total_cost_usd.toFixed(4);
            document.getElementById('avgLatency').textContent = data.avg_latency_ms + 'ms';
        }
        loadStats();
        setInterval(loadStats, 30000);  // Refresh every 30s
    </script>
</body>
</html>
"""
```

**✅ Day 11 Deliverable:** Prometheus metrics endpoint. Cost per user tracked. Admin dashboard showing live stats.

---

## Day 12 — Add CI/CD + Automated Eval

**Goal:** Professional deployment pipeline. Every push is automatically tested.

### Morning (2 hours) — GitHub Actions Pipeline

```yaml
# .github/workflows/ci.yml
name: SmartChat CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with: { python-version: '3.11' }

      - name: Install dependencies
        run: pip install -r requirements.txt pytest

      - name: Run unit tests
        run: pytest tests/unit/ -v

      - name: Run prompt eval
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          python eval/run_evals.py --output eval_results.json
          python eval/check_regression.py --threshold 0.80

      - name: Upload eval results
        uses: actions/upload-artifact@v3
        with:
          name: eval-results
          path: eval_results.json

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to Railway
        run: |
          curl -X POST "${{ secrets.RAILWAY_DEPLOY_WEBHOOK }}"
```

### Afternoon (2 hours) — Write Tests

```python
# tests/unit/test_memory.py
import pytest
from src.memory import UserMemoryManager

def test_memory_stores_and_retrieves():
    memory = UserMemoryManager("test_user")
    memory.save_conversation_insight("User prefers Python over JavaScript")
    memories = memory.recall_relevant_memories("What programming language do I prefer?")
    assert any("Python" in m for m in memories)

def test_memory_filters_irrelevant():
    memory = UserMemoryManager("test_user2")
    memory.save_conversation_insight("User likes hiking on weekends")
    memories = memory.recall_relevant_memories("Tell me about quantum physics")
    # Should not return hiking memory for unrelated query
    assert len(memories) == 0 or "hiking" not in memories[0].lower()

# tests/unit/test_auth.py
from src.auth import create_access_token, get_current_user

def test_token_creation_and_validation():
    token    = create_access_token({"sub": "alice"})
    username = get_current_user(token)
    assert username == "alice"

# eval/run_evals.py
import json
from src.chat import chat_with_memory

EVAL_CASES = [
    {"input": "What is the capital of France?",
     "expected_contains": "Paris"},
    {"input": "Write a Python hello world",
     "expected_contains": "print"},
    {"input": "Summarize: The sky is blue because of Rayleigh scattering",
     "expected_contains": "Rayleigh"},
]

def run_evals(output_file: str = "eval_results.json"):
    results = []
    for case in EVAL_CASES:
        response = chat_with_memory("eval_user", case["input"])
        passed   = case["expected_contains"].lower() in response.lower()
        results.append({"case": case["input"], "passed": passed, "response": response[:200]})

    score = sum(1 for r in results if r["passed"]) / len(results)
    print(f"Eval score: {score:.2f} ({sum(1 for r in results if r['passed'])}/{len(results)} passed)")

    with open(output_file, "w") as f:
        json.dump({"score": score, "results": results}, f, indent=2)

    return score
```

**✅ Day 12 Deliverable:** GitHub Actions running on every push. Evals as quality gate. Tests passing.

---

## Day 13 — Deploy SmartChat + Full Integration Test

### Morning (1.5 hours) — Final Deployment

```bash
# docker-compose.yml for local production testing
version: "3.8"
services:
  api:
    build: .
    ports: ["8000:8000"]
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - LANGCHAIN_API_KEY=${LANGCHAIN_API_KEY}
      - SECRET_KEY=${SECRET_KEY}
      - REDIS_URL=redis://redis:6379
    depends_on: [redis]

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]

# Test the full stack locally
docker-compose up --build

# Then deploy to Railway/Render with these env vars
```

### Afternoon (2 hours) — Integration Testing

```python
# tests/integration/test_full_flow.py
import requests

BASE_URL = "http://localhost:8000"

def test_full_user_journey():
    # 1. Register / login
    token_res = requests.post(f"{BASE_URL}/token",
                              data={"username": "alice", "password": "alice123"})
    assert token_res.status_code == 200
    token = token_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Send first message
    chat_res = requests.post(f"{BASE_URL}/chat",
                             json={"message": "My name is Alice and I love Python"},
                             headers=headers)
    assert chat_res.status_code == 200
    assert "response" in chat_res.json()

    # 3. Verify memory works in next message
    memory_res = requests.post(f"{BASE_URL}/chat",
                               json={"message": "What's my name?"},
                               headers=headers)
    assert "Alice" in memory_res.json()["response"]

    # 4. Check cost tracking
    stats_res = requests.get(f"{BASE_URL}/admin/stats", headers=headers)
    assert stats_res.json()["total_requests"] >= 2

    print("✅ All integration tests passed!")

test_full_user_journey()
```

**✅ Day 13 Deliverable:** SmartChat deployed. All 3 projects live. Integration tests passing.

---

## Day 14 — Portfolio Polish + Interview Preparation

**Goal:** Make everything shine. Prepare your stories.

### Morning (2 hours) — GitHub Portfolio

```markdown
# Update each project's README with this structure:

## Project Name
**Live Demo:** [URL]

### What it does (1 paragraph)

### Architecture diagram
[Simple ASCII or image]

### Technical decisions I made
| Decision | Choice | Why I chose it | What I learned |
|----------|--------|----------------|----------------|
| Chunk size | 500 tokens | Best precision/recall balance in my tests | Smaller = better precision, larger = more context |
| Vector DB | ChromaDB | Free, local, perfect for single-server scale | Would switch to Qdrant/Pinecone at 1M+ vectors |
| Reranker | Cross-encoder/ms-marco | Free, 30% precision improvement | API rerankers (Cohere) are faster but cost money |

### What I would do differently at scale
[2-3 concrete points]

### Eval results
| Metric | Score | Baseline |
|--------|-------|---------|
| Faithfulness | 0.87 | 0.73 (naive RAG) |
| Answer Relevancy | 0.91 | 0.78 |
```

### Afternoon (2 hours) — Interview Story Preparation

Write detailed answers to these. From real experience in your projects:

```
STORY 1: "Tell me about a time the AI gave wrong answers and how you fixed it"
→ Project 1: When chunk size was too large (1000 tokens), the embedding
  captured multiple topics and retrieval was noisy. Answer: reduced to 500
  and added reranking. Show your RAGAS before/after scores.

STORY 2: "How would you evaluate if your RAG system is working?"
→ Built a golden test set of 20 Q&A pairs from my PDF.
  Used RAGAS: faithfulness started at 0.73 (naive), got to 0.87 (with reranking).
  Also monitored production with LangSmith traces.

STORY 3: "What's your experience with agents?"
→ Built AutoAgent in Project 2. Biggest lesson: agents need max_iterations
  or they loop forever. Also learned that streaming with SSE makes the
  agent feel much more responsive — you see it thinking.

STORY 4: "How do you handle cost in production?"
→ In Project 3, added cost tracking per user. Found that the system prompt
  was 30% of cost. Added prompt caching which cut that cost by 85%.
  Also built model tiering: simple questions → gpt-4o-mini, complex → gpt-4o.

STORY 5: "Walk me through debugging an LLM issue"
→ In Project 1, answers were wrong for specific questions. Debugged:
  1. Checked if right chunk was retrieved (it wasn't)
  2. Found chunk size was too large — splitting mid-sentence
  3. Switched to sentence-aware splitting
  4. Re-ran eval: context_recall went from 0.62 to 0.81
```

---

## 🏁 What You Have After 2 Weeks

### 3 Live Projects
- **DocMind:** https://docmind.railway.app
- **AutoAgent:** https://autoagent.railway.app
- **SmartChat:** https://smartchat.railway.app

### GitHub Portfolio
- 3 repos with professional READMEs
- Architecture decisions documented
- Eval results with real numbers
- CI/CD pipelines running

### Real Interview Answers
Every scenario question answered from personal experience:
- ✅ "Tell me about a RAG failure you debugged"
- ✅ "What's your chunking strategy and why?"
- ✅ "How did you evaluate quality?"
- ✅ "How did you handle cost?"
- ✅ "Walk me through your agent architecture"
- ✅ "How did you deploy this to production?"

---

## 📊 Skills You've Proven

| Skill | Where You Proved It |
|-------|-------------------|
| RAG pipeline | Project 1: built, evaluated, improved |
| Chunking strategy | Project 1: ran chunk size experiments with data |
| Reranking | Project 1: cross-encoder, measured improvement |
| RAGAS evaluation | Project 1: real faithfulness/relevancy scores |
| LangGraph agents | Project 2: custom graph with state management |
| Tool calling | Project 2: search + calculate + custom tools |
| Streaming (SSE) | Project 2: real-time token streaming |
| Human-in-the-loop | Project 2: LangGraph breakpoints |
| Persistent memory | Project 3: vector DB per user |
| JWT auth | Project 3: production auth system |
| Cost tracking | Project 3: per-user cost dashboard |
| Prometheus monitoring | Project 3: metrics endpoint |
| CI/CD for LLMs | Project 3: GitHub Actions with eval gate |
| Docker deployment | All 3 projects |
| Production debugging | Every project — real bugs, real fixes |

---

## 💡 Tips for Each Interview Type

### Screening Call (30 min)
```
Lead with: "I recently built 3 AI projects and deployed them.
Let me show you [project URL] while we talk."

Having a live demo changes everything. Most candidates only have theory.
```

### Technical Interview (60 min)
```
When asked about any concept:
1. Explain the theory (from your notes)
2. Immediately say "I implemented this in [project]"
3. Share a specific number: "reranking improved precision by 30%"
4. Mention what failed: "the first approach didn't work because..."

Interviewers hire people who've broken things and fixed them.
```

### System Design (45 min)
```
Always start with your simplest working version (what you built),
then layer on scale requirements.

"In my DocMind project I used ChromaDB. At 1M+ documents I'd switch
to Pinecone because... and here's the migration strategy I'd use..."
```

### Behavioral / Final Round
```
Every behavioral question maps to your projects:
"Tell me about a challenge" → chunk size experiment failures
"Tell me about a time you improved performance" → RAGAS before/after
"Tell me about working under constraints" → staying within OpenAI rate limits
```

---

## 🚀 After 2 Weeks: You're Ready

You will have:
- **3 deployed projects** that prove you can build AND ship
- **Real numbers** from evaluations (not guesses)
- **Debugging stories** from things that actually broke
- **Production experience** with Docker, CI/CD, monitoring
- **A GitHub profile** that speaks for itself

**The interviewer will ask: "Have you built anything with LLMs?"**

**Your answer: "Yes — here are 3 deployed projects. Let me show you."**

---

*2-Week Plan | AI Engineer Interview Preparation | 2025-2026*
*Companion to: AI Interview Notes Parts 1, 2, 3 + 100 Q&A Guide*

























# 🚀 DataMind — AI Database Assistant

> Ask questions in plain English → get answers from your database using LLMs

---

## 📌 Overview

**DataMind** is a production-style AI system that converts natural language queries into SQL, executes them safely on a database, and returns human-readable answers.

### 💡 Example

**User Input:**

```
Show top users by revenue last month
```

**System Output:**

```
Alice is the top user with ₹1500 revenue, followed by Bob with ₹2000.
```

---

## 🏗️ Architecture

```
Frontend (Chat UI)
        ↓
FastAPI Backend
        ↓
Pipeline:
   1. Schema Loader
   2. LLM → SQL Generator
   3. SQL Validator (safety)
   4. SQL Executor (Postgres)
   5. Retry Fix (if fails)
   6. Answer Generator
        ↓
Response (Answer + SQL + Result)
```

---

## 📁 Project Structure

```
datamind/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── db/
│   │   ├── connection.py
│   │   ├── schema.py
│   │   └── seed.sql
│   │
│   ├── llm/
│   │   ├── sql_generator.py
│   │   ├── answer_generator.py
│   │   └── retry_fix.py
│   │
│   ├── core/
│   │   ├── validator.py
│   │   └── pipeline.py
│   │
│   ├── api/
│   │   └── routes.py
│   │
│   └── models/
│       └── schemas.py
│
├── static/
│   └── index.html
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Start Database

```yaml
# docker-compose.yml
version: "3.8"
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: datamind
    ports:
      - "5432:5432"
```

---

### 2️⃣ Sample Data

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    country TEXT
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INT,
    amount FLOAT,
    created_at DATE
);

INSERT INTO users (name, country) VALUES
('Alice', 'India'),
('Bob', 'USA'),
('Charlie', 'India');

INSERT INTO orders (user_id, amount, created_at) VALUES
(1, 500, '2026-03-10'),
(1, 1000, '2026-03-15'),
(2, 2000, '2026-03-20'),
(3, 700, '2026-03-25');
```

---

## 🧠 Core Components

---

### 🔹 1. Schema Loader

```python
def get_schema():
    return """
Tables:
users(id, name, country)
orders(id, user_id, amount, created_at)
"""
```

---

### 🔹 2. SQL Generator

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def generate_sql(question, schema):
    prompt = f"""
Schema:
{schema}

Generate SQL for:
{question}

Return only SQL.
"""
    return llm.invoke(prompt).content.strip()
```

---

### 🔹 3. SQL Validator (Safety Layer)

```python
def validate_sql(query):
    blocked = ["DELETE", "DROP", "UPDATE", "INSERT", "ALTER"]

    if any(word in query.upper() for word in blocked):
        raise ValueError("Unsafe query")

    if not query.lower().startswith("select"):
        raise ValueError("Only SELECT allowed")
```

---

### 🔹 4. Execute Query

```python
def execute_query(query):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
```

---

### 🔹 5. Retry Fix (Important Feature)

```python
def fix_sql(question, bad_sql, error, schema):
    prompt = f"""
SQL failed:
{bad_sql}

Error:
{error}

Fix using schema:
{schema}

Return only SQL.
"""
    return llm.invoke(prompt).content.strip()
```

---

### 🔹 6. Answer Generator

```python
def generate_answer(question, sql, result):
    prompt = f"""
Question: {question}
SQL: {sql}
Result: {result}

Convert into a natural answer.
"""
    return llm.invoke(prompt).content
```

---

### 🔹 7. Main Pipeline

```python
def run_pipeline(question):
    schema = get_schema()

    sql = generate_sql(question, schema)

    try:
        validate_sql(sql)
        result = execute_query(sql)
    except Exception as e:
        sql = fix_sql(question, sql, str(e), schema)
        validate_sql(sql)
        result = execute_query(sql)

    answer = generate_answer(question, sql, result)

    return {
        "question": question,
        "sql": sql,
        "result": result,
        "answer": answer
    }
```

---

## 🚀 API

### Endpoint

```
GET /ask?q=your-question
```

### Example

```
/ask?q=top users by revenue
```

---

## ⭐ Advanced Features (Add These)

### ✅ Schema grounding

Reduces hallucination

### ✅ Retry mechanism

Auto-fixes broken SQL

### ✅ Query explanation

```
"explanation": "Grouped orders by user and summed revenue"
```

### ✅ Chat memory

Follow-up queries

### ✅ Row limit

```
LIMIT 10
```

---

## ⚠️ Challenges Faced

| Problem              | Solution         |
| -------------------- | ---------------- |
| Wrong SQL            | Schema prompting |
| Unsafe queries       | Validator layer  |
| Query errors         | Retry mechanism  |
| Hallucinated columns | Strict schema    |

---

## 📊 What I Learned

* LLMs need schema context to generate correct SQL
* Safety layers are critical in production
* Retry loops significantly improve reliability
* Prompt engineering impacts accuracy heavily

---

## 🧠 Interview Explanation

> “I built a Text-to-SQL system where the LLM generates SQL from natural language. I added a validation layer to block unsafe queries, a retry mechanism to fix errors, and schema grounding to improve accuracy. The system executes queries on Postgres and converts results into human-readable answers.”

---

## 🔥 Future Improvements

* Use query planner validation
* Add role-based access control
* Replace Postgres with scalable DB (e.g., distributed)
* Add caching layer (Redis)

---

## 🏁 Tech Stack

* FastAPI
* PostgreSQL
* LangChain
* OpenAI GPT-4o-mini
* Docker

---

## 🎯 Final Result

✅ Natural Language → SQL
✅ Safe execution
✅ Auto error fixing
✅ Human-readable responses

---

## 💡 Why This Project Matters

This project demonstrates:

* Real-world AI + backend integration
* Production safety handling
* LLM reliability engineering
* Strong system design skills

---

🚀 **This is a high-impact project for AI Engineer roles**

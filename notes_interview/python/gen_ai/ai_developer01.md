# 🤖 AI Developer Interview Notes
### Comprehensive Reference for Technical Interviews (Junior → Senior)

> **How to use this document:** Each section includes definitions for junior (🟢 1yr) and senior (🔴 7yr) developers, code examples, diagrams, best practices, and interview tips. Use `Ctrl+F` to jump to any topic.

---

## 📋 Table of Contents

1. [LangChain & LangGraph](#1-langchain--langgraph)
2. [Tool Calling in LLMs](#2-tool-calling-in-llms)
3. [MCP – Model Context Protocol](#3-mcp--model-context-protocol)
4. [Vector Databases](#4-vector-databases)
5. [Embeddings](#5-embeddings)
6. [RAG – Retrieval-Augmented Generation](#6-rag--retrieval-augmented-generation)
7. [Persistence Mechanisms](#7-persistence-mechanisms)
8. [Databases (SQL, NoSQL & LLM Integration)](#8-databases)
9. [Pinecone](#9-pinecone)

---

## 1. LangChain & LangGraph

### 1.1 What is LangChain?

| Level | Definition |
|-------|-----------|
| 🟢 Junior | LangChain is a Python/JS framework that makes it easier to build applications with Large Language Models (LLMs). Think of it as "LEGO blocks" for AI — it gives you pre-built pieces like prompt templates, memory, tools, and chains to connect them. |
| 🔴 Senior | LangChain is an orchestration framework providing abstractions over LLM APIs, document loaders, vector stores, memory backends, and agent runtimes. It standardises component interfaces (Runnable protocol via LCEL), enabling composable, observable, and testable LLM pipelines. |

### 1.2 Core LangChain Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     LangChain Stack                         │
├─────────────┬───────────────┬──────────────┬───────────────┤
│  Models     │  Prompts      │  Memory      │  Tools        │
│  (LLMs,     │  (Templates,  │  (Buffer,    │  (Search,     │
│  Chat, Emb) │  Few-shot)    │  Summary,    │  Calculator,  │
│             │               │  VectorStore)│  Custom APIs) │
├─────────────┴───────────────┴──────────────┴───────────────┤
│               Chains / LCEL (Runnable Protocol)             │
├─────────────────────────────────────────────────────────────┤
│               Agents (ReAct, OpenAI Functions, etc.)        │
├─────────────────────────────────────────────────────────────┤
│               Callbacks & Tracing (LangSmith)               │
└─────────────────────────────────────────────────────────────┘
```

### 1.3 LCEL – LangChain Expression Language

LCEL uses the `|` pipe operator to chain Runnables together.

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Define components
prompt = ChatPromptTemplate.from_template("Tell me a joke about {topic}")
model  = ChatOpenAI(model="gpt-4o")
parser = StrOutputParser()

# Chain them using LCEL pipe operator
chain = prompt | model | parser

# Invoke
result = chain.invoke({"topic": "Python"})
print(result)
```

**Why LCEL over legacy chains?**
- Automatic streaming support
- Async-first (`ainvoke`, `astream`)
- Built-in retry / fallback
- LangSmith tracing out of the box

### 1.4 Memory Types

| Memory Type | Description | Use Case |
|-------------|-------------|----------|
| `ConversationBufferMemory` | Stores full history verbatim | Short conversations |
| `ConversationSummaryMemory` | Summarises older turns | Long conversations |
| `ConversationBufferWindowMemory` | Keeps last K turns | Bounded context |
| `VectorStoreRetrieverMemory` | Semantic retrieval from past | Long-term user memory |

```python
from langchain.memory import ConversationBufferWindowMemory
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain

memory = ConversationBufferWindowMemory(k=5)  # Keep last 5 turns
llm    = ChatOpenAI()

chain = ConversationChain(llm=llm, memory=memory, verbose=True)
chain.predict(input="Hi, I'm Alice")
chain.predict(input="What's my name?")  # LLM has memory of the first turn
```

---

### 1.5 What is LangGraph?

| Level | Definition |
|-------|-----------|
| 🟢 Junior | LangGraph lets you build AI agents that can make decisions, use tools, and loop — like a flowchart where the AI decides which path to take next. |
| 🔴 Senior | LangGraph is a stateful, graph-based orchestration library built on LangChain. Nodes are Python functions; edges are conditional transitions. State is a typed dict passed through the graph. It supports cycles (unlike DAG-only frameworks), persistence (checkpointers), streaming, and human-in-the-loop breakpoints. |

### 1.6 LangGraph Core Concepts

```
┌────────────────────────────────────────────────────────┐
│                   LangGraph Flow                       │
│                                                        │
│  START ──► [Node: Call LLM] ──► [Conditional Edge]    │
│                                       │                │
│                          ┌────────────┴───────────┐   │
│                          ▼                         ▼   │
│                   [Tool Node]               END ◄──┘   │
│                          │                             │
│                          └──────────► [Call LLM again] │
└────────────────────────────────────────────────────────┘
          State flows through every node as a dict
```

### 1.7 LangGraph Example – Simple ReAct Agent

```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
import operator

# 1. Define State
class AgentState(TypedDict):
    messages: Annotated[list, operator.add]  # append-only list

# 2. Define a tool
@tool
def search_web(query: str) -> str:
    """Search the internet for information."""
    return f"Results for: {query}"

# 3. Setup model with tools
tools  = [search_web]
model  = ChatOpenAI(model="gpt-4o").bind_tools(tools)

# 4. Define nodes
def call_model(state: AgentState):
    response = model.invoke(state["messages"])
    return {"messages": [response]}

tool_node = ToolNode(tools)

# 5. Routing logic
def should_continue(state: AgentState):
    last_msg = state["messages"][-1]
    return "tools" if last_msg.tool_calls else END

# 6. Build graph
graph = StateGraph(AgentState)
graph.add_node("agent",  call_model)
graph.add_node("tools",  tool_node)
graph.set_entry_point("agent")
graph.add_conditional_edges("agent", should_continue)
graph.add_edge("tools", "agent")  # loop back after tool use

app = graph.compile()
result = app.invoke({"messages": [("user", "What is the weather in NYC?")]})
```

### 1.8 LangGraph with Persistence (Checkpointing)

```python
from langgraph.checkpoint.sqlite import SqliteSaver

# Persist state across sessions
with SqliteSaver.from_conn_string(":memory:") as checkpointer:
    app = graph.compile(checkpointer=checkpointer)
    
    config = {"configurable": {"thread_id": "user-123"}}
    app.invoke({"messages": [("user", "Remember I like Python")]}, config)
    
    # Later — state is restored from checkpoint
    app.invoke({"messages": [("user", "What language do I like?")]}, config)
```

### 1.9 LangChain vs LangGraph – When to Use Which

| Scenario | Use |
|----------|-----|
| Simple Q&A chain | LangChain (LCEL) |
| RAG pipeline | LangChain (LCEL) |
| Multi-step agent with loops | LangGraph |
| Human-in-the-loop approval | LangGraph (breakpoints) |
| Multi-agent workflows | LangGraph |
| State that must persist across sessions | LangGraph (checkpointers) |

### 💡 Interview Tips – LangChain & LangGraph
- Know the difference between **chains** and **agents** — agents decide *which* tool to call; chains execute a fixed sequence.
- Be ready to explain **LCEL's Runnable interface** and why it replaced the legacy chain classes.
- For senior roles: explain **LangGraph's cycle support** vs directed acyclic graphs and why it matters for agentic loops.
- Mention **LangSmith** for observability/debugging when discussing production deployments.

---

## 2. Tool Calling in LLMs

### 2.1 What is Tool Calling?

| Level | Definition |
|-------|-----------|
| 🟢 Junior | Tool calling lets the AI say "I need to use a calculator / search / database" instead of guessing the answer. The model outputs structured JSON telling your code *which* function to run and *with what arguments*. |
| 🔴 Senior | Tool/function calling is a structured output capability where the model emits a `tool_use` block (JSON-serialised function name + args) instead of, or alongside, natural language. The host application executes the function, appends the result to the conversation, and re-invokes the model. This enables grounding, external API access, stateful actions, and multi-step reasoning. |

### 2.2 How Tool Calling Works – Sequence

```
User: "What is AAPL stock price?"
         │
         ▼
┌─────────────────┐
│   LLM receives  │◄── Tools schema in system prompt / API params
│   message +     │
│   tool defs     │
└────────┬────────┘
         │  Model decides to call a tool
         ▼
  { "tool": "get_stock_price",
    "args": { "ticker": "AAPL" } }
         │
         ▼
┌─────────────────┐
│  Your Code      │  Executes get_stock_price("AAPL")
│  Runs function  │  Returns: "$195.42"
└────────┬────────┘
         │  Result appended to conversation
         ▼
┌─────────────────┐
│  LLM receives   │  Now generates final answer
│  tool result    │  "AAPL is currently trading at $195.42"
└─────────────────┘
```

### 2.3 OpenAI / Anthropic Tool Calling Example

```python
import openai, json

client = openai.OpenAI()

# Define tool schema
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"},
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
                },
                "required": ["city"]
            }
        }
    }
]

# Actual function
def get_weather(city: str, unit: str = "celsius") -> dict:
    # In production: call a real weather API
    return {"city": city, "temp": 22, "unit": unit, "condition": "Sunny"}

messages = [{"role": "user", "content": "What's the weather in Paris?"}]

# First call
response = client.chat.completions.create(
    model="gpt-4o", messages=messages, tools=tools
)

msg = response.choices[0].message

if msg.tool_calls:
    for tc in msg.tool_calls:
        args   = json.loads(tc.function.arguments)
        result = get_weather(**args)
        
        messages.append(msg)  # append assistant msg with tool call
        messages.append({
            "role":         "tool",
            "tool_call_id": tc.id,
            "content":      json.dumps(result)
        })

# Second call – model now has the tool result
final = client.chat.completions.create(
    model="gpt-4o", messages=messages
)
print(final.choices[0].message.content)
```

### 2.4 LangChain Tool Calling

```python
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b

@tool
def get_word_length(word: str) -> int:
    """Return the number of characters in a word."""
    return len(word)

llm   = ChatOpenAI(model="gpt-4o")
tools = [multiply, get_word_length]

# Bind tools to the model
llm_with_tools = llm.bind_tools(tools)

result = llm_with_tools.invoke("How many letters in 'langchain'?")
# Inspect tool calls
print(result.tool_calls)
# [{'name': 'get_word_length', 'args': {'word': 'langchain'}, 'id': '...'}]
```

### 2.5 Parallel Tool Calling

Modern models (GPT-4o, Claude 3+) can call **multiple tools in one turn**:

```python
# Model might respond with:
[
  {"name": "get_weather",    "args": {"city": "London"}},
  {"name": "get_stock_price","args": {"ticker": "FTSE"}}
]
# Run both in parallel, append results, re-invoke
```

### 2.6 Common Tool Use Cases

| Use Case | Tool |
|----------|------|
| Up-to-date information | Web search |
| Structured data retrieval | Database query |
| Math / computations | Calculator / code interpreter |
| Sending emails/notifications | Email API |
| Reading/writing files | Filesystem |
| Calendar management | Calendar API |
| Code execution | Sandboxed runner |

### 💡 Interview Tips – Tool Calling
- Explain the **two-turn conversation pattern** (call → result → final answer).
- Know how to handle **tool errors** gracefully (pass error message as tool result, let model recover).
- Senior: discuss **parallel tool calling**, **forced tool use** (`tool_choice="required"`), and **schema design best practices** (clear descriptions improve model accuracy).

---

## 3. MCP – Model Context Protocol

### 3.1 What is MCP?

| Level | Definition |
|-------|-----------|
| 🟢 Junior | MCP (Model Context Protocol) is a standardised way for AI assistants to connect to external tools and data sources — like a USB standard for AI. Instead of writing custom integrations for every tool, MCP gives a common protocol. |
| 🔴 Senior | MCP is an open protocol (by Anthropic, Nov 2024) that standardises how LLM hosts/clients expose tools, resources, and prompts to models. It separates the *server* (capability provider) from the *client* (AI application), using JSON-RPC 2.0 over stdio or SSE. Enables a marketplace of reusable capability servers. |

### 3.2 MCP Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    MCP Client (AI App)                  │
│   e.g. Claude Desktop, VS Code, LangChain agent         │
└──────────────────────┬──────────────────────────────────┘
                       │ JSON-RPC 2.0
              ┌────────┴────────┐
              │   MCP Protocol  │  (stdio / SSE / HTTP)
              └────────┬────────┘
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │ MCP      │  │ MCP      │  │ MCP      │
  │ Server A │  │ Server B │  │ Server C │
  │(Postgres)│  │(GitHub)  │  │(Slack)   │
  └──────────┘  └──────────┘  └──────────┘
```

### 3.3 MCP Core Primitives

| Primitive | Description | Example |
|-----------|-------------|---------|
| **Tools** | Functions the model can call | `run_query`, `create_issue` |
| **Resources** | Read-only data the model can access | File contents, DB rows |
| **Prompts** | Reusable prompt templates | Code review template |
| **Sampling** | Server requests model completions | Recursive agent calls |

### 3.4 Building a Simple MCP Server (Python)

```python
# Install: pip install mcp
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import asyncio

app = Server("my-tool-server")

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="add_numbers",
            description="Add two numbers together",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["a", "b"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "add_numbers":
        result = arguments["a"] + arguments["b"]
        return [TextContent(type="text", text=str(result))]
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
```

### 3.5 MCP vs Function Calling – Key Differences

| Aspect | MCP | OpenAI Function Calling |
|--------|-----|------------------------|
| Scope | Cross-application standard | Model-specific API feature |
| Deployment | Separate server process | Inline in API call |
| Reusability | Server reusable by any MCP client | Defined per-request |
| Resources | First-class primitive | Not supported |
| Streaming | SSE support | Streaming completions |
| Ecosystem | Growing open marketplace | Proprietary per-provider |

### 3.6 MCP Workflow (Step-by-Step)

```
1. MCP Client starts → discovers available MCP servers
2. Client sends `initialize` request to each server
3. Server responds with capabilities (tools, resources, prompts)
4. User sends message to AI
5. AI decides to use a tool → client calls server via JSON-RPC
6. Server executes tool → returns result
7. Result added to context → AI generates final response
```

### 💡 Interview Tips – MCP
- MCP is still emerging (2024–2025) — knowing it signals you stay current.
- Key selling point: **separation of concerns** between capability providers and AI apps.
- Compare with **OpenAI Plugins** (deprecated) and **LangChain Tools** — MCP is transport-agnostic and open.

---

## 4. Vector Databases

### 4.1 What is a Vector Database?

| Level | Definition |
|-------|-----------|
| 🟢 Junior | A vector database stores numbers (vectors/embeddings) that represent the meaning of text, images, etc. You can search it by *meaning* — "find things similar to this" — rather than exact keyword matches. |
| 🔴 Senior | A vector database is purpose-built for storing and querying high-dimensional float vectors (typically 768–3072 dimensions). It uses Approximate Nearest Neighbor (ANN) algorithms (HNSW, IVF, LSH) to perform sub-linear similarity search at scale, with metadata filtering. Differs from adding pgvector to Postgres: dedicated systems handle indexing, replication, and filtering at billion-vector scale. |

### 4.2 How Vector Search Works

```
Query: "best pizza in Rome"
            │
            ▼
    ┌──────────────────┐
    │ Embedding Model  │  → [0.23, -0.81, 0.44, ..., 0.12]  (1536 dims)
    └──────────────────┘
            │
            ▼
    ┌──────────────────────────────────┐
    │      Vector Database              │
    │  Compare query vector against    │
    │  all stored vectors using        │
    │  cosine similarity / dot product │
    └──────────────────────────────────┘
            │
            ▼
    Top-K most similar documents:
    1. "Trastevere neighborhood has amazing pizza" (score: 0.92)
    2. "Rome food guide – where to eat"           (score: 0.88)
    3. "Italian pizza history"                    (score: 0.71)
```

### 4.3 Similarity Metrics

| Metric | Formula | Best For |
|--------|---------|----------|
| **Cosine Similarity** | `cos(θ) = A·B / (‖A‖ × ‖B‖)` | Text (direction matters, not magnitude) |
| **Dot Product** | `A · B` | When vectors are normalised |
| **Euclidean Distance** | `‖A - B‖` | Image embeddings, spatial data |

### 4.4 ANN Index Types ( Approximate Nearest Neighbor)

| Algorithm | Description | Pros | Cons |
|-----------|-------------|------|------|
| **HNSW** (Hierarchical Navigable Small World) | Graph-based multi-layer index | Very fast query, high recall | High memory usage |
| **IVF** (Inverted File Index) | Cluster-based: query only nearest clusters | Lower memory, tunable | Slower than HNSW |
| **LSH** (Locality Sensitive Hashing) | Hash similar vectors to same bucket | Very fast, low memory | Lower recall |
| **PQ** (Product Quantization) | Compress vectors by splitting | Scales to billions | Accuracy loss |

### 4.5 Vector Database Comparison

| Feature | **Pinecone** | **Weaviate** | **FAISS** | **Chroma** | **Qdrant** | **pgvector** |
|---------|-------------|-------------|---------|----------|----------|------------|
| Type | Managed Cloud | Open/Cloud | Library | Embedded/Cloud | Open/Cloud | Postgres Ext |
| Scale | Billions | Hundreds of millions | Millions (single node) | Millions | Hundreds of millions | Millions |
| Metadata Filter | ✅ Advanced | ✅ GraphQL | ❌ Basic | ✅ Basic | ✅ Advanced | ✅ SQL |
| Multi-vector | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ |
| Hosting | Fully managed | Self-hosted / Cloud | Self | Self / Cloud | Self / Cloud | Self |
| Best For | Production RAG | Hybrid search | Research/offline | Dev/prototyping | Production | Existing PG stack |

### 4.6 FAISS Example (In-Memory)

```python
import faiss
import numpy as np

# Create index for 768-dim vectors
dimension = 768
index = faiss.IndexFlatL2(dimension)  # Exact L2 search

# Add vectors (simulate embeddings)
np.random.seed(42)
vectors = np.random.rand(1000, dimension).astype('float32')
index.add(vectors)

# Query
query   = np.random.rand(1, dimension).astype('float32')
k       = 5   # top-5 results
distances, indices = index.search(query, k)

print("Top-5 closest indices:", indices)
print("Distances:", distances)

# Production: use IndexHNSWFlat for speed
hnsw_index = faiss.IndexHNSWFlat(dimension, 32)  # 32 = M parameter
hnsw_index.add(vectors)
```

### 4.7 Metadata Filtering

```python
# Pinecone example with metadata filter
results = index.query(
    vector=query_embedding,
    top_k=10,
    filter={
        "category": {"$eq": "technology"},
        "year":     {"$gte": 2023}
    },
    include_metadata=True
)
```

### 💡 Interview Tips – Vector DBs
- Know the difference between **exact** (brute-force) and **approximate** (ANN) search.
- FAISS is a **library**, not a database — no persistence, no server, no metadata filtering out of the box.
- For senior: discuss **hybrid search** (dense vectors + sparse BM25), **re-ranking**, and **multi-tenancy** (namespaces in Pinecone).
- Mention **dimensionality reduction** trade-offs (PCA, PQ) for scaling.

---

## 5. Embeddings

### 5.1 What are Embeddings?

| Level | Definition |
|-------|-----------|
| 🟢 Junior | An embedding converts text (or images) into a list of numbers where similar meanings end up close together in "number-space". "King" and "Queen" will have similar numbers; "King" and "Pizza" will be very different. |
| 🔴 Senior | Embeddings are dense vector representations in a learned latent space where semantic similarity correlates with geometric proximity (cosine/dot-product distance). Generated by encoder models (BERT-family, OpenAI text-embedding-3, etc.) trained on large corpora with contrastive or masked-language-model objectives. |

### 5.2 Types of Embeddings

| Type | Description | Models | Use Case |
|------|-------------|--------|----------|
| **Text** | Sentence / paragraph → vector | `text-embedding-3-small`, `all-MiniLM-L6-v2` | Semantic search, RAG |
| **Word** | Individual word → vector | Word2Vec, GloVe, FastText | NLP features |
| **Image** | Image → vector | CLIP, ViT, ResNet | Image search |
| **Multimodal** | Text + Image → shared space | CLIP, GPT-4V | Cross-modal search |
| **Code** | Code snippet → vector | CodeBERT, `text-embedding-3` | Code search, deduplication |
| **Graph** | Graph nodes → vector | Node2Vec, GraphSAGE | Recommendation, KG |

### 5.3 Generating Text Embeddings

```python
# --- OpenAI ---
from openai import OpenAI
client = OpenAI()

response = client.embeddings.create(
    input="The quick brown fox",
    model="text-embedding-3-small"  # 1536 dims; 3-large = 3072 dims
)
vector = response.data[0].embedding   # list of 1536 floats

# --- HuggingFace sentence-transformers (local, free) ---
from sentence_transformers import SentenceTransformer

model    = SentenceTransformer("all-MiniLM-L6-v2")  # 384 dims, fast
texts    = ["Hello world", "Hola mundo", "Bonjour le monde"]
vectors  = model.encode(texts)   # shape: (3, 384)

# --- LangChain abstraction ---
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector     = embeddings.embed_query("What is AI?")
documents  = embeddings.embed_documents(["Doc 1", "Doc 2"])
```

### 5.4 Cosine Similarity Calculation

```python
import numpy as np

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

v1 = np.array([1.0, 0.5, -0.3])
v2 = np.array([0.9, 0.6, -0.2])
print(cosine_similarity(v1, v2))  # ~0.997 (very similar)
```

### 5.5 Embedding Model Comparison

| Model | Dims | Speed | Quality | Cost |
|-------|------|-------|---------|------|
| `text-embedding-3-small` | 1536 | Fast | Good | Low ($) |
| `text-embedding-3-large` | 3072 | Slower | Best | Higher ($$) |
| `text-embedding-ada-002` | 1536 | Fast | Legacy | Low ($) |
| `all-MiniLM-L6-v2` | 384 | Very Fast | OK | Free (local) |
| `all-mpnet-base-v2` | 768 | Medium | Good | Free (local) |
| `bge-large-en-v1.5` | 1024 | Medium | Excellent | Free (local) |

### 5.6 Chunking Strategy for Embeddings

```
Document → Split into chunks → Embed each chunk → Store in vector DB

Chunking strategies:
┌─────────────────────────────────────────────────────────┐
│ Fixed-size:    every 500 chars, 100 char overlap        │
│ Sentence:      split on punctuation                     │
│ Recursive:     try \n\n → \n → ' ' → '' (LangChain)    │
│ Semantic:      embed + cluster similar sentences        │
│ Document-aware: by markdown headers, HTML tags          │
└─────────────────────────────────────────────────────────┘
```

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " ", ""]
)

docs   = splitter.create_documents(["Your long document text here..."])
chunks = [d.page_content for d in docs]
```

### 💡 Interview Tips – Embeddings
- Explain why **cosine similarity** is preferred over Euclidean for text (magnitude shouldn't matter).
   ans - Cosine similarity measures the angle between vectors, making it invariant to magnitude differences, which is crucial for text embeddings where the length of the vector doesn't necessarily indicate relevance.


- Discuss **dimensionality reduction** (Matryoshka Representation Learning lets you truncate vectors).
   ans - Matryoshka Representation Learning is a technique that allows you to create nested, multi-resolution embeddings. By truncating the vector at different lengths, you can have a "small" embedding for fast retrieval and a "large" embedding for more nuanced understanding, all from the same base representation.
- Senior: know about **late interaction** (ColBERT), **bi-encoder vs cross-encoder** trade-offs for retrieval vs re-ranking.
    ans - Bi-encoders independently encode queries and documents, allowing for efficient retrieval using vector similarity. Cross-encoders jointly encode query-document pairs, providing higher accuracy at the cost of increased computation, making them suitable for re-ranking top candidates retrieved by a bi-encoder.
- Chunking is often the #1 RAG quality lever — be ready to discuss strategies.
    ans - Effective chunking ensures that the context provided to the LLM is coherent and relevant. Strategies include fixed-size chunks with overlap, sentence-based splitting, recursive splitting using multiple separators, semantic chunking based on embedding similarity, and document-aware chunking that respects natural boundaries like markdown headers or HTML tags.

---

## 6. RAG – Retrieval-Augmented Generation

### 6.1 What is RAG?

| Level | Definition |
|-------|-----------|
| 🟢 Junior | RAG is a way to give the AI access to your own documents. Instead of the AI guessing, it first searches your knowledge base, finds relevant text, and then uses that text to answer. |
| 🔴 Senior | RAG is an architectural pattern that augments LLM generation with retrieved context from an external knowledge source, reducing hallucinations and enabling knowledge updates without fine-tuning. The pipeline: `encode query → retrieve top-K` `chunks → stuff into prompt` → `generate grounded response.` |

### 6.2 Standard (Naive) RAG Pipeline

```
User Query
    │
    ▼
[Embed Query]  →  query_vector = embed("What is LangChain?")
    │
    ▼
[Vector DB Retrieval]  →  top_k_docs = db.search(query_vector, k=5)
    │
    ▼
[Prompt Construction]
    │  "Answer based on this context:
    │   {context}
    │   Question: {question}"
    ▼
[LLM Generation]  →  Final Answer
```

```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 1. Ingest documents
from langchain_community.document_loaders import TextLoader
loader = TextLoader("knowledge_base.txt")
docs   = loader.load()       

splitter   = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks     = splitter.split_documents(docs)             # split into smaller pieces for better retrieval

# 2. Create vector store
embeddings = OpenAIEmbeddings()                         # default: text-embedding-3-small
vectordb   = Chroma.from_documents(chunks, embeddings)   # create vector DB and add chunks as vectors

# 3. Build retrieval chain
llm   = ChatOpenAI(model="gpt-4o")
chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectordb.as_retriever(search_kwargs={"k": 5})     # retrieve top-5 relevant chunks
)

# 4. Query
result = chain.invoke("What are LangChain's key features?")
print(result["result"])
```

---

# 📘 RAG Types – Complete Interview Notes (Detailed)

---

## 🔹 6.3.1 Self-RAG

### ✅ Definition

Self-RAG extends traditional RAG by adding a **self-reflection mechanism**, where the model evaluates and improves its own behavior during generation. Instead of blindly retrieving and generating, the model uses special **reflection tokens** to reason about each step and self-correct if needed.

---

### 🔄 Diagram

```
Query
  │
  ▼
[Should I retrieve?]  ←── Reflection token: RETRIEVE / NO_RETRIEVE
  │
  ├── YES → [Retrieve docs] → [Are docs relevant?] ←── Reflection token: RELEVANT / IRRELEVANT
  │                               │
  │                               ▼
  │                          [Generate] → [Is answer supported?] ←── Reflection token: SUPPORTED / UNSUPPORTED
  │                                           │
  │                                           ▼
  │                                  [Is answer useful?] ←── Reflection token: score 1–5
  │                                           │
  │                               ┌───────────┴───────────┐
  │                               ▼                       ▼
  │                         Score ≥ 4               Score < 4
  │                         [Return Answer]    [Re-retrieve / Regenerate]
  └── NO → [Generate directly]
```

---

### 🏷️ Reflection Tokens

| Token | Meaning |
|-------|---------|
| `[Retrieve]` | Does this query need retrieval? |
| `[IsREL]` | Is the retrieved passage relevant? |
| `[IsSUP]` | Does the generated text follow from the passage? |
| `[IsUSE]` | Is the final output useful? (score 1–5) |

---

### ⚙️ How It Works

1. Model first decides if retrieval is needed (`[Retrieve]`)
2. Retrieves documents (if required)
3. Evaluates relevance of retrieved docs (`[IsREL]`)
4. Generates answer
5. Checks grounding — is answer supported by docs? (`[IsSUP]`)
6. Evaluates usefulness with score 1–5 (`[IsUSE]`)
7. If score is low → retries (re-retrieve or regenerate)
8. Reflections can be logged to tools like **LangSmith** for observability and debugging

---

### 🔍 When to Use

* When hallucination risk is high
* When answer quality must be validated
* In production systems needing monitoring/debugging

---

### 🎯 Key Idea

> Model **thinks, evaluates, and corrects itself** — instead of blindly generating responses

---

### ✅ Benefits

* Strong hallucination control
* Self-improving pipeline
* Better observability (logs, scores)
* Higher trust in answers

---

### ⚠️ Trade-offs

* Higher latency (extra reasoning steps)
* More token usage (cost ↑)
* Slightly complex to implement

---

### 🆚 Self-RAG vs CRAG

| | Self-RAG | CRAG |
|-|----------|------|
| Fixes | Retrieval decision + generation quality | Retrieval quality only |
| How | Reflection tokens at every step | Evaluator before generation |
| Self-correction | Yes (re-retrieve or regenerate) | Yes (refine query or web search) |

---

## 🔹 6.3.2 CRAG – Corrective RAG

### ✅ Definition

CRAG improves RAG by **evaluating retrieval quality before generation** and actively correcting poor retrieval. Instead of passing bad documents to the LLM, CRAG grades them and either refines the query, re-retrieves, or falls back to web search.

---

### 🔄 Diagram

```
Query → Retrieve → [Relevance Evaluator]
                         │
              ┌──────────┼──────────────┐
              ▼          ▼              ▼
          CORRECT    AMBIGUOUS      INCORRECT
              │          │              │
              │    Refine + Retrieve  Web Search
              │          │              │
              └──────────┴──────────────┘
                         │
                 [Knowledge Refiner]
                 (strip irrelevant parts)
                         │
                 [Generate Answer]
```

---

### ⚙️ How It Works

1. Retrieve documents from vector store
2. Evaluate retrieval quality using LLM or classifier (grades: Correct / Ambiguous / Incorrect)
3. If **Correct** → proceed to generation
4. If **Ambiguous** → refine query and re-retrieve
5. If **Incorrect** → fall back to web search (e.g. Tavily)
6. Strip irrelevant parts via Knowledge Refiner
7. Generate final answer with clean context

---

### 💻 Code (LangGraph Pattern)

```python
from langgraph.graph import StateGraph

def grade_retrieval(state):
    """Evaluate if retrieved docs are relevant."""
    score = relevance_grader.invoke({
        "question": state["question"],
        "document": state["documents"][0].page_content
    })
    return "correct" if score.binary_score == "yes" else "incorrect"

# Route based on retrieval grade
graph.add_conditional_edges(
    "grade_documents",
    grade_retrieval,
    {"correct": "generate", "incorrect": "web_search"}
)
```

---

### 🔍 When to Use

* When retrieval quality is inconsistent
* When knowledge base is noisy or outdated
* Enterprise search systems

---

### 🎯 Key Idea

> Fix **retrieval first**, then generate — less garbage-in, less garbage-out

---

### ✅ Benefits

* Better context quality
* More accurate answers
* Robust to bad retrieval

---

### ⚠️ Trade-offs

* Extra evaluation step (latency ↑)
* Requires good relevance scoring
* Slightly more complex pipeline

---

## 🔹 6.3.3 Hybrid RAG

### ✅ Definition

Hybrid RAG combines **dense (embedding-based / semantic)** and **sparse (keyword-based / BM25)** retrieval. Dense retrieval captures meaning; sparse retrieval captures exact keywords. Results from both are merged using **Reciprocal Rank Fusion (RRF)** for the best of both worlds.

---

### 🔄 Diagram

```
Query
  │
  ├──► Dense Retrieval (semantic embeddings) → [doc1, doc3, doc7]
  │
  └──► Sparse Retrieval (BM25/TF-IDF)        → [doc2, doc3, doc9]
                │
                ▼
    [Reciprocal Rank Fusion (RRF)]
    Merge & re-rank combined results
                │
                ▼
        [doc3, doc1, doc2, doc7, ...]
                │
                ▼
          [LLM Generate]
```

---

### ⚙️ How It Works

1. Run dense retrieval → captures semantic similarity
2. Run sparse retrieval → captures exact keyword matches
3. Merge both result lists using RRF (assigns scores based on rank position)
4. Send top-k merged docs to LLM

---

### 💻 Code

```python
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import FAISS

dense_retriever  = FAISS.from_documents(docs, embeddings).as_retriever(k=5)
sparse_retriever = BM25Retriever.from_documents(docs, k=5)

hybrid = EnsembleRetriever(
    retrievers=[sparse_retriever, dense_retriever],
    weights=[0.5, 0.5]
)
results = hybrid.invoke("What is LangGraph?")
```

---

### 🔍 When to Use

* General-purpose search
* QA systems
* Production RAG (recommended default)

---

### 🎯 Key Idea

> Combine **semantic meaning + exact keyword match** — dense misses keywords, sparse misses context

---

### ✅ Benefits

* Best recall
* Handles diverse query types
* Industry standard
* Balanced performance

---

### ⚠️ Trade-offs

* Slightly more compute
* Needs weight tuning (dense vs sparse ratio)

---

## 🔹 6.3.4 Agentic RAG

### ✅ Definition

Agentic RAG allows the LLM to act as an **autonomous agent**, deciding *when*, *what*, and *how many times* to retrieve before generating a final answer. Retrieval is no longer a fixed one-time step — it becomes iterative and goal-driven.

---

### 🔄 Diagram

```
User Query
    │
    ▼
 [Agent LLM]
    │
    ├── Think: "I need info on X" → [Retrieve X] → append to context
    │
    ├── Think: "Now I need info on Y" → [Retrieve Y] → append to context
    │
    ├── Think: "I also need Z" → [Retrieve Z] → append to context
    │
    └── Think: "I have enough" → [Generate Final Answer]
```

---

### ⚙️ How It Works

1. LLM receives query and breaks it into sub-tasks
2. Decides what information is needed first
3. Calls retrieval tool (multiple times as needed)
4. Builds context iteratively after each retrieval
5. Decides when it has enough context
6. Produces final answer

---

### 🔍 When to Use

* Multi-hop reasoning ("Who founded the company that acquired X?")
* Complex workflows requiring multiple data sources
* Tool-using LLM agents

---

### 🎯 Key Idea

> Retrieval is **iterative and decision-driven** — the agent retrieves only what it needs, when it needs it

---

### ✅ Benefits

* Handles complex, multi-step queries
* Flexible and intelligent retrieval
* Works well with tools and APIs

---

### ⚠️ Trade-offs

* Higher latency (multiple retrieval calls)
* Harder to control and debug
* More expensive (more LLM calls)

---

## 🔹 6.3.5 Modular RAG

### ✅ Definition

Modular RAG designs the RAG pipeline as **independent, swappable components** — like microservices. Each module (retriever, re-ranker, compressor, generator) can be upgraded or replaced without rebuilding the entire system.

---

### 🔄 Diagram

```
Query
  │
  ▼
[Retriever]        ← swap: Vector / BM25 / Graph / Web
  │
  ▼
[Re-ranker]        ← swap: Cross-encoder / Cohere / LLM-based
  │
  ▼
[Compressor]       ← swap: LLMChainExtractor / ContextualCompression
  │
  ▼
[Generator]        ← swap: GPT-4 / Claude / Llama
  │
  ▼
[Answer]
```

---

### ⚙️ How It Works

1. Retrieve documents via chosen retriever
2. Re-rank to surface the most relevant ones
3. Compress to fit context window efficiently
4. Generate answer using chosen LLM
5. Any module can be swapped independently

---

### 🔍 When to Use

* Production systems requiring flexibility
* Teams experimenting with different components
* Large-scale, scalable architectures

---

### 🎯 Key Idea

> Build RAG like **microservices** — swap any component without breaking the pipeline

---

### ✅ Benefits

* High flexibility and easy upgrades
* Better experimentation and A/B testing
* Production-ready and maintainable

---

### ⚠️ Trade-offs

* More engineering effort upfront
* Integration complexity between modules

---

## 🔹 6.3.6 Online RAG vs Offline RAG

### ✅ Definition

The distinction is based on **when the index is updated**. Offline RAG indexes data at ingestion time (batch). Online RAG updates the index in real-time as new data arrives, keeping responses always fresh.

---

### 🔄 Diagram

```
Offline RAG:
  Data (batch) → [Index at ingestion] → Retrieve → Generate
  ⚠️ Index can become stale over time

Online RAG:
  Data (stream) → [Live index update] → Retrieve → Generate
  ✅ Index always current
```

---

### ⚙️ How It Works

| | **Offline RAG** | **Online RAG** |
|-|-----------------|----------------|
| Index updated | At ingestion (batch) | In real-time / streaming |
| Latency | Low (pre-computed) | Higher (live ingestion) |
| Freshness | Can go stale | Always current |
| Cost | Low | Higher |
| Use case | Static docs (PDFs, manuals) | News, live support tickets |

---

### 🔍 When to Use

* **Offline** → static, slow-changing data (PDFs, documentation, knowledge bases)
* **Online** → dynamic, fast-changing data (news feeds, live customer support, social media)

---

### 🎯 Key Idea

> Tradeoff: **speed and cost vs freshness** — use offline unless data freshness is critical

---

### ✅ Benefits

**Offline** → Fast, cheap, simple to build

**Online** → Always up-to-date, handles real-time queries

---

### ⚠️ Trade-offs

* Online = higher latency + infrastructure cost
* Offline = stale data risk, needs scheduled re-indexing

---

## 🔹 6.3.7 Graph RAG

### ✅ Definition

Graph RAG replaces or augments the vector store with a **knowledge graph**, enabling multi-hop reasoning over structured entity relationships. Unlike vector search (which retrieves similar text chunks), Graph RAG traverses entity connections to answer questions that require linking multiple facts.

---

### 🔄 Diagram

```
Documents
    │
    ▼
[Entity & Relation Extraction]
    │
    ▼
[Knowledge Graph DB]  (Neo4j, Amazon Neptune, Nebula)
    │
    ├── (Apple) ──[founded_by]──► (Steve Jobs)
    ├── (Apple) ──[makes]──► (iPhone)
    └── (iPhone) ──[runs]──► (iOS)
    │
    ▼
[Graph Traversal]  → Start from "Apple", traverse 2–3 hops
    │
    ▼
[Generate Answer with Graph Context]
```

---

### ⚙️ How It Works

1. Extract entities and relations from documents
2. Build knowledge graph (nodes = entities, edges = relationships)
3. Store in graph DB (Neo4j, Neptune, etc.)
4. On query: traverse graph starting from relevant entity
5. Collect connected facts across multiple hops
6. Generate answer using graph context

---

### 🔍 When to Use

* Multi-hop questions ("Who founded the company that makes the iPhone?")
* Enterprise knowledge systems with rich relationships
* Domains where relationships matter more than raw text similarity

---

### 🎯 Key Idea

> Use **structured relationships instead of text similarity** — ideal when facts must be connected across multiple steps

---

### ✅ Benefits

* Strong multi-hop reasoning
* Structured, explainable knowledge
* Handles complex relational queries

---

### ⚠️ Trade-offs

* Complex setup (graph building, entity extraction)
* Requires graph database infrastructure
* Overkill for simple keyword or semantic search

---

---

# 🧠 Final Quick Comparison

| Type | Core Idea | Best For | Key Weakness |
|------|-----------|----------|--------------|
| **Self-RAG** | Model reflects on its own retrieval & generation | Reducing hallucinations | Higher latency & cost |
| **CRAG** | Fixes bad retrieval before generating | Noisy or inconsistent KB | Extra evaluation step |
| **Hybrid RAG** | Dense + sparse retrieval merged via RRF | General-purpose, best recall | Weight tuning needed |
| **Agentic RAG** | LLM decides when/what to retrieve | Complex multi-step queries | Harder to control |
| **Modular RAG** | Swappable pipeline components | Production flexibility | Engineering overhead |
| **Online RAG** | Real-time index updates | Live/fast-changing data | Higher cost & latency |
| **Graph RAG** | Knowledge graph traversal | Multi-hop relational queries | Complex to set up |

---

# 🆚 Key Distinctions to Remember

| Confusion | Clarification |
|-----------|--------------|
| Self-RAG vs CRAG | CRAG fixes *retrieval quality only*; Self-RAG fixes *retrieval decision + generation quality* |
| Hybrid vs Agentic | Hybrid improves *how* you retrieve; Agentic improves *when and what* you retrieve |
| Modular vs Agentic | Modular is about *architecture*; Agentic is about *behavior* |
| Online vs Offline | Same pipeline, different *indexing strategy* |

---

# 🚀 Final Interview Line

> "Modern RAG systems go beyond simple retrieve-then-generate by adding self-reflection (Self-RAG), retrieval correction (CRAG), hybrid search, and agent-based decision-making — each targeting a different failure mode to improve accuracy, reliability, and scalability."

---

## 7. Persistence Mechanisms

### 7.1 Why Persistence Matters in AI Systems

| Level | Definition |
|-------|-----------|
| 🟢 Junior | Persistence means saving the AI's "memory" so it remembers things between conversations or across different users. Without it, every chat starts fresh. |
| 🔴 Senior | Persistence in LLM systems encompasses: conversation state (checkpointing), semantic memory (vector stores), episodic memory (event logs), and cached completions. Design decisions impact latency, cost, privacy, and correctness. |

### 7.2 Types of Persistence

```
┌─────────────────────────────────────────────────────────────┐
│              Persistence in AI Systems                      │
├──────────────────┬──────────────────┬───────────────────────┤
│ Conversation     │ Semantic Memory  │ Cache                  │
│ State            │                  │                        │
├──────────────────┼──────────────────┼───────────────────────┤
│ • Message history│ • Vector DB      │ • Prompt caching       │
│ • LangGraph      │ • User facts     │ • Response caching     │
│   checkpoints    │ • Long-term docs │ • Embedding cache      │
│ • Thread IDs     │                  │                        │
├──────────────────┼──────────────────┼───────────────────────┤
│ Redis, SQLite,   │ Pinecone, Chroma │ Redis, Mem-cache,      │
│ Postgres         │ Weaviate         │ DynamoDB               │
└──────────────────┴──────────────────┴───────────────────────┘
```

### 7.3 LangGraph Checkpointing

```python
# SQLite checkpointer (dev)
from langgraph.checkpoint.sqlite import SqliteSaver
checkpointer = SqliteSaver.from_conn_string("checkpoints.db")

# Postgres checkpointer (production)
from langgraph.checkpoint.postgres import PostgresSaver
checkpointer = PostgresSaver.from_conn_string(
    "postgresql://user:pass@localhost/mydb"
)

app = graph.compile(checkpointer=checkpointer)

# Each thread_id is an isolated conversation
config = {"configurable": {"thread_id": "user-42-session-7"}}
result = app.invoke({"messages": [("user", "Hello")]}, config)

# Get full conversation history
history = list(app.get_state_history(config))
```

### 7.4 Conversation Memory Patterns

```python
# Pattern 1: Redis-backed message history
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

history = RedisChatMessageHistory(session_id="user-123", url="redis://localhost:6379")

chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: RedisChatMessageHistory(session_id, url="redis://localhost:6379"),
    input_messages_key="input",
    history_messages_key="history"
)

chain_with_history.invoke(
    {"input": "What did I just say?"},
    config={"configurable": {"session_id": "user-123"}}
)
```

### 7.5 Prompt Caching

means saving the static parts of your prompt (like system instructions or long documents) so you don't have to pay for them every time.

OpenAI and Anthropic support **prompt caching** — cache the static system prompt prefix to reduce cost and latency:

```python
# Anthropic: cache_control for long system prompts
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "<VERY LONG DOCUMENT>",
            "cache_control": {"type": "ephemeral"}  # Cache this prefix
        }
    ],
    messages=[{"role": "user", "content": "Summarise the document"}]
)
# First call: tokens written to cache
# Subsequent calls with same prefix: cache hit, ~90% cost reduction
```

### 7.6 Semantic / Long-Term Memory with Vector DB

```python
# Store facts about a user long-term
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

user_memory_db = Chroma(
    collection_name="user_memory",
    embedding_function=OpenAIEmbeddings()
)

# Save a fact
user_memory_db.add_texts(
    texts=["User prefers Python over JavaScript"],
    metadatas=[{"user_id": "alice", "timestamp": "2025-01-01"}]
)

# Retrieve relevant memories at conversation start
memories = user_memory_db.similarity_search(
    "What language does the user prefer?",
    k=3,
    filter={"user_id": "alice"}
)
```

### 7.7 Caching LLM Responses

```python
from langchain.cache import InMemoryCache, SQLiteCache
from langchain.globals import set_llm_cache

# Development: in-memory cache
set_llm_cache(InMemoryCache())

# Production: SQLite cache (persists to disk)
set_llm_cache(SQLiteCache(database_path="llm_cache.db"))

# Now repeated identical prompts return cached results instantly
llm = ChatOpenAI()
llm.invoke("What is 2+2?")  # First call: hits API
llm.invoke("What is 2+2?")  # Second call: returns from cache
```

### 7.8 Persistence Best Practices

| Practice | Why |
|----------|-----|
| Use `thread_id` to isolate user sessions | Prevent cross-user context leakage |
| TTL (Time-To-Live) on cached memories | Avoid stale data, reduce storage |
| Summarise old messages instead of truncating | Preserve context, fit context window |
| Separate short-term (buffer) from long-term (vector) memory | Right tool for each scope |
| Encrypt stored conversation history | User privacy & compliance |
| Version your vector DB collections | Safe schema migrations |

### 💡 Interview Tips – Persistence
- Distinguish **stateless** (no memory between calls) vs **stateful** (LangGraph checkpointing) agents.
- Know the **context window problem**: why you can't just keep appending messages forever.
- Senior: discuss **memory management strategies** — summarisation, sliding window, semantic retrieval — and when each is appropriate.

---

## 8. Databases

### 8.1 SQL Databases

| Level | Definition |
|-------|-----------|
| 🟢 Junior | SQL databases store data in tables with rows and columns (like Excel). Great for structured data where you know the schema upfront. Use SQL queries to read/write. |
| 🔴 Senior | RDBMS provide ACID guarantees, normalised schemas, and declarative query via SQL. Optimal for transactional workloads, complex joins, and data integrity. Choose: Postgres (feature-rich, JSON support, pgvector), MySQL (web standard), SQLite (embedded). |

#### SQL with LangChain (Text-to-SQL)

```python
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent

db    = SQLDatabase.from_uri("sqlite:///employees.db")
llm   = ChatOpenAI(model="gpt-4o", temperature=0)
agent = create_sql_agent(llm, db=db, verbose=True)

result = agent.invoke("How many employees are in the engineering department?")
# Agent generates SQL: SELECT COUNT(*) FROM employees WHERE dept='Engineering'
# Executes it, returns natural language answer
```

---

### 8.2 NoSQL Databases

| Type | Database | Use Case | Data Model |
|------|----------|----------|------------|
| Document | MongoDB, Firestore | Flexible schemas, nested docs | JSON documents |
| Key-Value | Redis, DynamoDB | Caching, sessions | Key → Value |
| Column-family | Cassandra, HBase | Time-series, IoT | Wide rows |
| Graph | Neo4j, Amazon Neptune | Relationships, KGs | Nodes + Edges |
| Time-series | InfluxDB, TimescaleDB | Metrics, logs | Time-stamped rows |

#### MongoDB with LangChain

```python
from langchain_mongodb import MongoDBAtlasVectorSearch
from pymongo import MongoClient

client = MongoClient("mongodb+srv://...")
collection = client["ai_db"]["documents"]

vectorstore = MongoDBAtlasVectorSearch(
    collection=collection,
    embedding=OpenAIEmbeddings(),
    index_name="vector_index"
)

# MongoDB Atlas provides both document storage AND vector search
results = vectorstore.similarity_search("AI frameworks", k=5)
```

---

### 8.3 SQL vs NoSQL Decision Matrix

| Factor | SQL | NoSQL |
|--------|-----|-------|
| Schema | Fixed, enforced | Flexible, dynamic |
| Transactions | Full ACID | Usually BASE (eventual consistency) |
| Scaling | Vertical (mostly) | Horizontal (sharding) |
| Query | Complex JOINs | Simple lookups + aggregations |
| Use with LLMs | Text-to-SQL, metadata store | Conversation history, user prefs |
| Best for | Financial data, inventory | User profiles, logs, events |

---

### 8.4 Redis – AI Use Cases

```python
import redis
import json

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# 1. Cache LLM responses
cache_key = f"llm_cache:{hash('What is LangChain?')}"
if cached := r.get(cache_key):
    result = json.loads(cached)
else:
    result = llm.invoke("What is LangChain?")
    r.setex(cache_key, 3600, json.dumps(str(result)))  # TTL: 1 hour

# 2. Rate limiting
pipe = r.pipeline()
pipe.incr(f"rate_limit:user123")
pipe.expire(f"rate_limit:user123", 60)
count, _ = pipe.execute()
if count > 100:
    raise Exception("Rate limit exceeded")

# 3. Pub/Sub for streaming AI responses
# Producer (LLM stream)
for chunk in llm.stream("Write a story"):
    r.publish("ai_stream:session-1", chunk.content)
```

---

### 8.5 pgvector – Postgres as Vector DB

```sql
-- Enable extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create table with embedding column
CREATE TABLE documents (
    id         SERIAL PRIMARY KEY,
    content    TEXT,
    metadata   JSONB,
    embedding  VECTOR(1536)  -- OpenAI text-embedding-3-small
);

-- Create HNSW index for fast search
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops);

-- Similarity search (cosine distance)
SELECT content, 1 - (embedding <=> '[0.1, 0.2, ...]'::vector) AS score
FROM   documents
ORDER  BY embedding <=> '[0.1, 0.2, ...]'::vector
LIMIT  5;
```

```python
from langchain_community.vectorstores import PGVector

CONNECTION_STRING = "postgresql://user:pass@localhost/vectordb"

vectorstore = PGVector(
    connection_string=CONNECTION_STRING,
    embedding_function=OpenAIEmbeddings(),
    collection_name="my_docs"
)

vectorstore.add_documents(docs)
results = vectorstore.similarity_search("query", k=5)
```

### 💡 Interview Tips – Databases
- Know when to use **pgvector** (existing Postgres stack, small scale) vs dedicated vector DB (large scale, advanced filtering).
- Text-to-SQL is a hot topic — mention **schema introspection**, **query validation**, and **SQL injection risks**.
- Senior: discuss **database per service** patterns in microservices, **CQRS** for read/write separation, **database connection pooling** (PgBouncer) for LLM apps with high concurrency.

---

## 9. Pinecone

### 9.1 What is Pinecone?

| Level | Definition |
|-------|-----------|
| 🟢 Junior | Pinecone is a cloud-based vector database. You store your text embeddings there, and when users ask questions, you search Pinecone to find the most relevant information instantly. No server setup needed. |
| 🔴 Senior | Pinecone is a fully-managed, serverless vector database offering sub-10ms p99 query latency at billion-vector scale. Supports namespaces for multi-tenancy, hybrid search (dense + sparse), metadata filtering, and pod-based or serverless index types. It handles ANN index management (HNSW), replication, and horizontal scaling. |

### 9.2 Pinecone Architecture

```
Your Application
     │
     ▼
Pinecone Client SDK (Python / JS)
     │
     ▼
┌────────────────────────────────────────┐
│           Pinecone Service             │
│  ┌──────────┐  ┌──────────────────┐   │
│  │  Index   │  │   Namespaces      │   │
│  │          │  │  ┌────┐ ┌────┐   │   │
│  │  HNSW /  │  │  │ ns1│ │ ns2│   │   │
│  │  IVFPQ   │  │  └────┘ └────┘   │   │
│  └──────────┘  └──────────────────┘   │
│                                        │
│  Metadata Filtering  │  Hybrid Search  │
└────────────────────────────────────────┘
```

### 9.3 Pinecone Setup & CRUD

```python
from pinecone import Pinecone, ServerlessSpec

# Initialize
pc = Pinecone(api_key="YOUR_API_KEY")

# Create index (serverless)
pc.create_index(
    name="my-rag-index",
    dimension=1536,        # match your embedding model
    metric="cosine",       # cosine | dotproduct | euclidean
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
)

# Connect to index
index = pc.Index("my-rag-index")

# Upsert vectors
vectors = [
    {
        "id":       "doc-001",
        "values":   [0.1, 0.2, ...],   # 1536 floats
        "metadata": {"source": "docs/readme.md", "category": "setup"}
    },
    {
        "id":       "doc-002",
        "values":   [0.4, 0.1, ...],
        "metadata": {"source": "docs/api.md", "category": "reference"}
    }
]
index.upsert(vectors=vectors, namespace="prod")

# Query with metadata filter
results = index.query(
    vector=[0.3, 0.15, ...],
    top_k=5,
    namespace="prod",
    filter={"category": {"$eq": "setup"}},
    include_metadata=True
)

for match in results["matches"]:
    print(f"Score: {match['score']:.3f} | Source: {match['metadata']['source']}")

# Delete
index.delete(ids=["doc-001"], namespace="prod")

# Index statistics
stats = index.describe_index_stats()
print(f"Total vectors: {stats['total_vector_count']}")
```

### 9.4 Pinecone + LangChain Integration

```python
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone

pc         = Pinecone(api_key="YOUR_API_KEY")
index      = pc.Index("my-rag-index")
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Create / connect to vector store
vectorstore = PineconeVectorStore(index=index, embedding=embeddings)

# Add documents
from langchain_core.documents import Document

docs = [
    Document(page_content="LangChain is an LLM framework", metadata={"source": "intro"}),
    Document(page_content="LangGraph enables stateful agents", metadata={"source": "guide"}),
]
vectorstore.add_documents(docs)

# Retrieve
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5, "filter": {"source": "guide"}}
)
results = retriever.invoke("What is LangGraph?")
```

### 9.5 Pinecone Hybrid Search

```python
from pinecone_text.sparse import BM25Encoder

# Encode sparse (keyword) vectors
bm25    = BM25Encoder().default()
docs    = ["LangChain is great", "Pinecone stores vectors"]
bm25.fit(docs)

sparse_vectors = bm25.encode_documents(docs)
query_sparse   = bm25.encode_queries("vector store")
query_dense    = embeddings.embed_query("vector store")

# Upsert with both dense and sparse
index.upsert(vectors=[
    {
        "id":      "doc-1",
        "values":  query_dense,
        "sparse_values": sparse_vectors[0],
        "metadata": {"text": docs[0]}
    }
])

# Query with hybrid (alpha controls dense/sparse mix: 1.0 = pure dense, 0.0 = pure sparse)
results = index.query(
    vector=query_dense,
    sparse_vector=query_sparse,
    top_k=5,
    alpha=0.7,   # 70% dense, 30% sparse
    include_metadata=True
)
```

### 9.6 Pinecone Namespaces (Multi-tenancy)

```python
# Each user/tenant gets their own namespace
# Vectors in different namespaces never mix

# Upsert for tenant A
index.upsert(vectors=[{"id": "doc-1", "values": [...]}], namespace="tenant-a")

# Upsert for tenant B
index.upsert(vectors=[{"id": "doc-1", "values": [...]}], namespace="tenant-b")

# Query only within tenant A's namespace
results = index.query(vector=[...], top_k=5, namespace="tenant-a")
```

### 9.7 Serverless vs Pod-Based Indexes

| Feature | Serverless | Pod-based |
|---------|-----------|----------|
| Pricing | Pay per query | Pay per pod |
| Scale-to-zero | ✅ | ❌ |
| Cold start | Possible | None |
| Latency | Good | Best |
| Hybrid search | ✅ | ✅ |
| Use case | Variable workloads | High-throughput production |

### 9.8 Pinecone Best Practices

| Practice | Recommendation |
|----------|---------------|
| Batch upserts | Use batches of 100 vectors per request |
| Dimension match | Ensure vector dim == index dim exactly |
| Metadata design | Keep metadata small (< 40KB per vector) |
| Namespaces | One namespace per tenant/environment |
| Re-indexing | Use a staging index for safe migrations |
| Monitoring | Use `describe_index_stats()` for capacity planning |
| Avoid hot spots | Randomise IDs to distribute write load |

### 9.9 Common Pinecone Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `DIMENSION_MISMATCH` | Vector dim ≠ index dim | Check embedding model output size |
| `QUOTA_EXCEEDED` | Free tier limit hit | Upgrade plan or delete unused vectors |
| `INVALID_FILTER` | Wrong filter syntax | Check `$eq`, `$in`, `$gte` operators |
| Slow upsert | Large payload, single request | Batch into 100-vector chunks |
| Stale results | Old vectors not updated | Upsert uses same ID to overwrite |

### 💡 Interview Tips – Pinecone
- Know the difference between **serverless** and **pod-based** indexes and when to choose each.
- Explain **namespaces** for multi-tenancy vs separate indexes (namespaces are cheaper, indexes are more isolated).
- Senior: discuss **hybrid search alpha tuning**, **index cold starts** in serverless, and the trade-off between **recall and latency** via `top_k` and `nprobe`.
- Always mention **idempotent upserts** — same ID overwrites existing vector.

---

## 🗂️ Quick Reference Cheat Sheet

### LangChain Key Classes

```python
from langchain_openai          import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts    import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter   import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma, FAISS
from langchain.chains          import RetrievalQA
from langchain.memory          import ConversationBufferWindowMemory
```

### LangGraph Key Classes

```python
from langgraph.graph           import StateGraph, END
from langgraph.prebuilt        import ToolNode
from langgraph.checkpoint.sqlite import SqliteSaver
```

### Embedding Models Quick Reference

```
text-embedding-3-small  →  1536 dims  (best cost/quality for most RAG)
text-embedding-3-large  →  3072 dims  (highest quality)
all-MiniLM-L6-v2        →  384 dims   (local, fast, free)
bge-large-en-v1.5       →  1024 dims  (best local quality)
```

### RAG Types Summary

| Type | Key Feature | When to Use |
|------|------------|-------------|
| Naive RAG | Simple retrieve + generate | Prototypes, simple QA |
| Advanced RAG | Re-ranking, query expansion | Production RAG |
| Self-RAG | Model reflects on retrieval/generation | Quality-critical |
| CRAG | Corrects bad retrieval with web search | Knowledge gaps |
| Hybrid RAG | Dense + sparse retrieval | Best recall |
| Agentic RAG | Agent decides when to retrieve | Complex multi-hop QA |
| Graph RAG | Knowledge graph traversal | Entity-rich domains |
| Modular RAG | Plug-and-play components | Large-scale systems |

---

## 📝 General Interview Tips

1. **Always mention production concerns**: latency, cost, observability (LangSmith), error handling.
2. **Know the trade-offs**: exact search vs ANN, in-memory vs persistent, local models vs APIs.
3. **RAGAS for RAG evaluation** is a signal of production experience.
4. **LangSmith** for tracing/debugging LangChain pipelines.
5. **When in doubt, ask about scale**: the right answer often depends on volume.
6. **Cite alternatives**: show you know the ecosystem (not just one tool).
7. **LCEL over legacy**: if asked about LangChain chains, default to the modern LCEL pattern.
8. **Security**: mention prompt injection, API key management, PII in embeddings.

---

*Generated: 2025 | Topics: LangChain, LangGraph, Tool Calling, MCP, Vector DBs, Embeddings, RAG, Persistence, Databases, Pinecone*
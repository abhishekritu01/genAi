# 🤖 AI Developer Interview Notes — Part 3
### The Missing 20% That Wins Interviews | Junior (🟢) → Senior (🔴)

> **Companion to Parts 1 & 2.** Covers the gaps that separate mid-level from senior: Advanced Retrieval, Evals, LLM Internals, Quantization, Long-Context, MLOps, Reasoning Models, Multimodal, Privacy, and System Design.

---

## 📋 Table of Contents

1. [Tokenization & Sampling — Deep Dive](#1-tokenization--sampling--deep-dive)
2. [Advanced Retrieval — HyDE, Re-ranking & Query Transforms](#2-advanced-retrieval--hyde-re-ranking--query-transforms)
3. [Evaluation — LLM-as-Judge & Benchmarks](#3-evaluation--llm-as-judge--benchmarks)
4. [Quantization & Inference Optimization](#4-quantization--inference-optimization)
5. [Long-Context Strategies & Failure Modes](#5-long-context-strategies--failure-modes)
6. [Model Versioning & MLOps for LLMs](#6-model-versioning--mlops-for-llms)
7. [Chain-of-Thought Variants & Reasoning Models](#7-chain-of-thought-variants--reasoning-models)
8. [Multimodal LLMs](#8-multimodal-llms)
9. [Data Privacy, Memorization & Compliance](#9-data-privacy-memorization--compliance)
10. [System Design — End-to-End AI Products](#10-system-design--end-to-end-ai-products)
11. [Master Cheat Sheet](#11-master-cheat-sheet)

---

## 1. Tokenization & Sampling — Deep Dive

### 1.1 Why Tokenization Is a Senior Interview Topic

Tokenization sits at the intersection of model cost, language quality, and security. Interviewers probe it to see whether you understand what an LLM actually processes — not just the text you send, but the numeric token IDs derived from it.

### 1.2 Tokenization Algorithms

| Algorithm | Used By | Core Idea | Key Property |
|-----------|---------|-----------|--------------|
| **BPE** (Byte-Pair Encoding) | GPT-2/3/4, Llama, Mistral | Merge most frequent byte pairs iteratively | Bottom-up, vocabulary learned from corpus |
| **WordPiece** | BERT, DistilBERT | Greedy likelihood maximisation on sub-words | `##` prefix for continuation tokens |
| **SentencePiece (Unigram)** | Llama, T5, Gemma | Probabilistic, language-agnostic, byte-fallback | Handles any language without pre-tokenisation |
| **Tiktoken (OpenAI BPE)** | GPT-4o, text-embedding-3 | Optimised BPE, pure Python/Rust, no whitespace rules | ~4 chars per token for English |

#### BPE in Plain English
1. Start with every character as its own token: `[h, e, l, l, o, w, o, r, l, d]`
2. Count all adjacent pairs. Most frequent pair → merged into new token.
3. Repeat until vocabulary size reached (e.g. 50,257 for GPT-2).
4. `"hello"` becomes `['hello']` if seen often enough, or `['hel', 'lo']` otherwise.

```python
import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

# Token counts vary by language & content type
print(enc.encode("Hello, world!"))          # [9906, 11, 1917, 0]  → 4 tokens
print(enc.encode("こんにちは"))              # 5 tokens (Japanese is denser)
print(enc.encode("1234567890"))              # 5 tokens (digits split individually)
print(enc.encode("SELECT * FROM users"))     # 5 tokens (SQL keywords merge)

# Practical: estimate cost before API call
def estimate_cost(text: str, model="gpt-4o", price_per_1m=5.0) -> float:
    tokens = len(tiktoken.encoding_for_model(model).encode(text))
    return (tokens / 1_000_000) * price_per_1m
```

---

### 1.3 Sampling Strategies

The model outputs a probability distribution over the entire vocabulary at each step. The sampling strategy determines how you pick the next token from that distribution.

| Strategy | How It Works | Temperature | When to Use |
|----------|-------------|-------------|-------------|
| **Greedy** | Always pick argmax (highest probability token) | Effectively 0 | Deterministic factual tasks |
| **Temperature Sampling** | Divide logits by T before softmax. Low T → sharper, high T → flatter | 0.0–2.0 | Most general tasks (default 0.7) |
| **Top-k** | Sample only from top k tokens by probability | Works with temp | Prevents low-prob token selection |
| **Top-p (Nucleus)** | Sample from smallest set whose cumulative prob ≥ p | Works with temp | More adaptive than top-k |
| **Beam Search** | Maintain B candidate sequences, pick highest joint prob | N/A | Translation, structured generation |
| **Min-p** | Discard tokens below `p × max_prob` threshold | Works with temp | Newer Llama default, better quality |
| **Repetition Penalty** | Divide logits of already-seen tokens by penalty factor | Works with temp | Long-form generation, chat |

```python
# Visualising what temperature does to the distribution
import numpy as np

logits = np.array([2.0, 1.5, 0.8, 0.2, -0.5])  # raw model outputs

def softmax(x): return np.exp(x) / np.exp(x).sum()

def apply_temperature(logits, T):
    return softmax(logits / T)

print("T=0.1 (near-greedy):", apply_temperature(logits, 0.1))
# [0.993, 0.007, 0.000, 0.000, 0.000]  — almost always picks token 0

print("T=1.0 (default):   ", apply_temperature(logits, 1.0))
# [0.483, 0.292, 0.142, 0.069, 0.014]  — token 0 likely but not certain

print("T=2.0 (creative):  ", apply_temperature(logits, 2.0))
# [0.338, 0.275, 0.213, 0.123, 0.050]  — much flatter, more variety
```

### 1.4 Token Gotchas — Frequently Asked

- **Tokenization is asymmetric**: encoding and decoding are not exact inverses for all byte sequences.
- **Numbers are tokenized character-by-character** in some models — `'1234'` may be `['1','2','3','4']` — which is why LLMs are bad at arithmetic by default.
- **Context length limits are in TOKENS not characters** — a 128K token limit is ~96,000 English words but far fewer for code with many special characters.
- **Special tokens are model-specific** — `[INST]`, `<|system|>`, `<|user|>` delimiters vary. Using wrong delimiters with a local model is a common bug.
- **Prompt injection via tokenization**: attackers can craft inputs where a natural-language boundary doesn't align with a token boundary.

> 💡 **Interview Tip:** When asked "what's the difference between top_p and temperature?" — explain that temperature reshapes the **entire** distribution while top_p **truncates** it. They're complementary, not equivalent. Setting `top_p=1.0` effectively disables nucleus sampling.

---

## 2. Advanced Retrieval — HyDE, Re-ranking & Query Transforms

### 2.1 The Problem With Naive RAG

Naive RAG embeds the user's question and retrieves the most similar chunks. This fails in three predictable ways:
- **Query-document mismatch**: questions are short and abstract; answers are long and specific.
- **Poor recall**: top-5 chunks miss key info that ranks 8th or 12th.
- **Poor precision**: retrieved chunks are semantically adjacent but don't actually answer the question.

---

### 2.2 HyDE — Hypothetical Document Embeddings

> **Core Idea:** Instead of embedding the query directly, ask the LLM to write a hypothetical ideal answer — then embed *that* for retrieval. The embedding of a detailed answer is much closer to real document embeddings than the embedding of a short question.

**Intuition:** If a user asks "what causes aurora borealis?", the query embedding may be near encyclopedia entries about phenomena in general. But if you generate "Aurora borealis is caused by charged solar particles interacting with Earth's magnetic field...", that embedding lands right next to the actual document you want.

```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Step 1: Generate hypothetical document from the query
hyde_prompt = ChatPromptTemplate.from_template(
    "Write a detailed paragraph that would perfectly answer this question.\n"
    "Be factual and specific. Do not say you are answering a question.\n"
    "Question: {question}"
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
hyde_chain = hyde_prompt | llm | StrOutputParser()

def hyde_retrieve(question: str, vectorstore, k: int = 5):
    # Generate hypothetical answer
    hypothetical_doc = hyde_chain.invoke({"question": question})

    # Embed the HYPOTHETICAL ANSWER (not the question)
    embeddings = OpenAIEmbeddings()
    hyp_vector  = embeddings.embed_query(hypothetical_doc)

    # Search using the hypothesis vector
    results = vectorstore.similarity_search_by_vector(hyp_vector, k=k)
    return results

# LangChain built-in abstraction:
from langchain.chains import HypotheticalDocumentEmbedder

hyde_embedder = HypotheticalDocumentEmbedder.from_llm(
    llm=llm,
    embeddings=OpenAIEmbeddings(),
    prompt_key="web_search"
)
# HyDE improves recall by 10-30% on knowledge-intensive tasks
```

> 💡 **Interview Tip:** HyDE adds ~200-400ms latency (one extra LLM call) and works best when queries are short and documents are long/detailed. Mention the tradeoff: extra latency vs recall improvement. It performs poorly when the LLM hallucinates in the hypothetical answer.

---

### 2.3 Query Transformation Techniques

| Technique | How It Works | Benefit | Extra Cost |
|-----------|-------------|---------|------------|
| **Multi-Query Retrieval** | LLM generates 3-5 paraphrases; retrieve for each; deduplicate | Higher recall for ambiguous queries | 3-5x retrieval + 1 LLM call |
| **Step-Back Prompting** | Abstract to a higher-level concept first | Retrieves foundational context | 1 extra LLM call |
| **Query Decomposition** | Break complex query into sub-questions; answer each; synthesize | Multi-hop reasoning | N LLM calls |
| **RAG-Fusion (RRF)** | Multi-query + Reciprocal Rank Fusion for merging ranked lists | Best recall of all methods | 3-5x retrieval + merging |
| **HyDE** | Generate hypothetical answer; embed that instead | Bridges query-doc gap | 1 LLM call |

```python
# Multi-Query Retrieval with LangChain
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0)
retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
    llm=llm,
)

# LangChain auto-generates prompts like:
# Original: "How does attention work in transformers?"
# Generated: "Explain the self-attention mechanism in neural networks"
# Generated: "What is the mathematical formula for transformer attention?"
# Generated: "Why do language models use attention instead of recurrence?"

docs = retriever.invoke("How does attention work in transformers?")
# Returns deduplicated union of all retrieval results
```

---

### 2.4 Re-Ranking — The Most Important RAG Improvement

Re-ranking is a second-stage filter: retrieve a large candidate set (top-20 to top-50), then score each candidate against the query using a more expensive but accurate model, and return the truly top-5.

> **Bi-encoder vs Cross-encoder:** Embedding models are bi-encoders — they encode query and document independently. Cross-encoders see BOTH query and document together — 10-100x more accurate but too slow for first-stage retrieval. Re-ranking uses cross-encoders AFTER fast bi-encoder retrieval.

```python
# Option 1: Cohere Rerank (managed API — simplest)
import cohere

co = cohere.Client("COHERE_API_KEY")

def cohere_rerank(query: str, documents: list[str], top_n: int = 5):
    results = co.rerank(
        query=query,
        documents=documents,
        model="rerank-english-v3.0",
        top_n=top_n
    )
    return [(r.index, r.relevance_score) for r in results.results]

# Option 2: Local cross-encoder (free, slower)
from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def local_rerank(query: str, docs: list[str], top_n: int = 5):
    pairs  = [[query, doc] for doc in docs]
    scores = reranker.predict(pairs)
    ranked = sorted(zip(scores, docs), key=lambda x: x[0], reverse=True)
    return [doc for _, doc in ranked[:top_n]]

# Option 3: LangChain ContextualCompressionRetriever
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CohereRerank

compressor = CohereRerank(top_n=5, model="rerank-english-v3.0")
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=vectorstore.as_retriever(search_kwargs={"k": 20}),
)
# Retrieve 20 → rerank → return top 5  ← best production pattern
```

> 💡 **Interview Tip:** The single most impactful RAG improvement is almost always: increase retrieval `k` to 20-50, then rerank to top 5. This costs one extra API call but can double answer quality. Always mention this when asked "how would you improve a RAG system?"

---

### 2.5 Contextual Compression

Even after reranking, retrieved chunks may contain irrelevant sentences. Contextual compression extracts only the relevant portions before passing to the LLM.

```python
from langchain.retrievers.document_compressors import LLMChainExtractor, EmbeddingsFilter
from langchain.retrievers import ContextualCompressionRetriever
from langchain_openai import OpenAIEmbeddings

# LLM-based extraction (expensive but precise)
compressor = LLMChainExtractor.from_llm(llm)

# EmbeddingsFilter (fast, no LLM needed)
ef = EmbeddingsFilter(embeddings=OpenAIEmbeddings(), similarity_threshold=0.76)
compression_retriever = ContextualCompressionRetriever(
    base_compressor=ef,
    base_retriever=vectorstore.as_retriever(search_kwargs={"k": 10}),
)
```

---

## 3. Evaluation — LLM-as-Judge & Benchmarks

### 3.1 Why Evaluation Separates Junior from Senior

Any engineer can build a RAG pipeline. Senior engineers can tell you **objectively** whether it's getting better or worse. Interviewers probe eval to find people who've shipped to production — because without evals, you're flying blind.

---

### 3.2 LLM-as-Judge Pattern

> **Core Idea:** Use a strong LLM (GPT-4o, Claude Opus) to score the outputs of your application LLM. More reliable than BLEU/ROUGE for open-ended tasks, cheaper than human labeling at scale, and automatable in CI/CD.

```python
# G-Eval style: LLM judge with chain-of-thought scoring
from openai import OpenAI
import json

judge_client = OpenAI()

JUDGE_PROMPT = """
You are an expert evaluator. Score the following answer on a scale of 1-5.

Criteria: {criteria}
Question: {question}
Reference answer: {reference}
Model answer: {answer}

First, reason step by step about the quality. Then output:
{{"reasoning": "...", "score": <1-5>}}
Only output valid JSON. No markdown.
"""

def llm_judge(question, answer, reference, criteria="correctness and completeness"):
    response = judge_client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": JUDGE_PROMPT.format(
                criteria=criteria, question=question,
                reference=reference, answer=answer
            )
        }],
        temperature=0.0
    )
    return json.loads(response.choices[0].message.content)

# Pairwise comparison (more reliable than absolute scores)
PAIRWISE_PROMPT = """
Which answer is better for the question? Output only 'A', 'B', or 'tie'.
Question: {question}
Answer A: {answer_a}
Answer B: {answer_b}
"""
```

---

### 3.3 Evaluation Frameworks

| Framework | Focus | Key Metrics | Best For |
|-----------|-------|-------------|----------|
| **RAGAS** | RAG pipeline quality | Faithfulness, Answer Relevancy, Context Recall, Context Precision | RAG system evals |
| **LangSmith Evals** | LangChain pipeline quality | Custom criteria, string matching, LLM graders | Any LangChain app |
| **DeepEval** | LLM output quality | G-Eval, Hallucination, Toxicity, Bias, RAG metrics | Comprehensive LLM evals |
| **TruLens** | LLM app quality | Groundedness, QA relevance, context relevance | Production monitoring |
| **Promptfoo** | Prompt regression testing | Custom assertions, LLM graders, diff testing | CI/CD prompt testing |
| **Evals (OpenAI)** | Custom benchmarks | Match, includes, LLM-graded, code execution | Systematic A/B prompt tests |

---

### 3.4 Key Industry Benchmarks — Must Know

| Benchmark | Measures | Score to Know |
|-----------|----------|---------------|
| **MMLU** | 57 subjects: STEM, humanities, social science. Multi-choice. | GPT-4: ~86%, Claude 3.5: ~88% |
| **HumanEval** | Code generation: 164 Python problems. pass@k metric. | GPT-4o: ~90%, Llama 3.1 70B: ~80% |
| **GSM8K** | Grade school math word problems. Chain-of-thought helps. | GPT-4: ~92% with CoT |
| **HELM** | Holistic: 7 metrics × 42 scenarios. Comprehensive. | Used for model selection decisions |
| **MT-Bench** | Multi-turn conversation quality. LLM-as-judge (GPT-4). | Score /10, GPT-4: ~9.0 |
| **LMSYS Chatbot Arena** | ELO rating from human pairwise preferences. Live. | Most realistic quality signal |
| **BIG-Bench Hard** | Hard reasoning tasks that GPT-3 couldn't do. 23 tasks. | Shows reasoning capability ceiling |
| **SWE-Bench** | Software engineering: GitHub issues resolved. Agentic. | GPT-4o: ~9%, Claude: ~49% (2024) |

---

### 3.5 Building an Eval Pipeline for Production

1. **Create a golden dataset**: 50-200 hand-curated (question, expected_answer) pairs covering happy paths and edge cases.
2. **Define metrics**: pick 3-5 relevant metrics. More metrics = slower pipeline.
3. **Baseline**: run eval on current system. Store results.
4. **Gate**: every PR that changes prompts/models/retrieval must run evals and improve or match baseline.
5. **Monitor online**: sample 1-5% of live traffic; run LLM judge asynchronously; alert on score drop.

```python
# Minimal eval pipeline with DeepEval
from deepeval import evaluate
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric, HallucinationMetric
from deepeval.test_case import LLMTestCase

test_cases = [
    LLMTestCase(
        input="What is LangGraph?",
        actual_output=rag_pipeline("What is LangGraph?"),
        expected_output="LangGraph is a stateful graph-based agent framework...",
        retrieval_context=[...retrieved_chunks...]
    )
]

metrics = [
    AnswerRelevancyMetric(threshold=0.7, model="gpt-4o"),
    FaithfulnessMetric(threshold=0.7, model="gpt-4o"),
    HallucinationMetric(threshold=0.3, model="gpt-4o"),
]

results = evaluate(test_cases, metrics)
# Integrate into pytest with @pytest.mark.parametrize for CI/CD
```

> 💡 **Interview Tip:** Mention the "evals triangle" — **offline evals** (golden set), **shadow evals** (live traffic sample), and **online monitoring**. This shows you've thought about both correctness and drift over time.

---

## 4. Quantization & Inference Optimization

### 4.1 What Is Quantization?

> Quantization reduces the numerical precision of model weights from 32-bit or 16-bit floating point to lower precision (8-bit integers, 4-bit integers, etc.). This reduces memory footprint and speeds up inference, with a small and often acceptable accuracy tradeoff.

| Format | Bits/Weight | Memory (7B model) | Quality Loss | Use Case |
|--------|-------------|-------------------|--------------|----------|
| FP32 | 32 bits | ~28 GB | None (baseline) | Training only |
| FP16 / BF16 | 16 bits | ~14 GB | Minimal | Training + GPU inference |
| INT8 (GPTQ/bitsandbytes) | 8 bits | ~7 GB | Slight | Single GPU inference |
| INT4 (GPTQ, AWQ) | 4 bits | ~3.5 GB | Moderate | Consumer GPU (RTX 3090) |
| GGUF Q4_K_M | ~4.5 bits avg | ~4 GB | Moderate | CPU inference (llama.cpp) |
| GGUF Q8_0 | 8 bits | ~7 GB | Minimal | CPU with good quality |
| 2-bit (GPTQ/EXL2) | 2 bits | ~1.8 GB | Significant | Extreme memory constraints |

---

### 4.2 Quantization Methods Compared

| Method | When Applied | How It Works | Best For |
|--------|-------------|--------------|----------|
| **PTQ** (Post-Training Quantization) | After training, no fine-tuning | Round weights to lower precision | Fast deployment, slight quality drop |
| **GPTQ** | One-time calibration on small dataset | Layer-wise quantization minimizing output error | 4-bit models on GPU |
| **AWQ** (Activation-aware) | Calibration on few samples | Protect salient weights (1% that matter most) | Best 4-bit quality |
| **GGUF / llama.cpp** | CPU deployment | Mixed-precision: key layers stay FP16 | Local deployment on laptops |
| **QLoRA** | During fine-tuning | 4-bit NF4 base + FP16 adapters | Fine-tuning on consumer GPU |

```python
# Load quantized model with bitsandbytes (4-bit)
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
import torch

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",            # NormalFloat4 — best quality
    bnb_4bit_compute_dtype=torch.bfloat16, # compute in BF16
    bnb_4bit_use_double_quant=True,        # quantize the quantization constants too
)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B-Instruct",
    quantization_config=bnb_config,
    device_map="auto"
)
# 8B model now fits in ~5 GB VRAM vs ~16 GB in FP16

# Run GGUF on CPU with llama.cpp Python bindings
from llama_cpp import Llama

llm = Llama(
    model_path="Meta-Llama-3.1-8B-Q4_K_M.gguf",
    n_ctx=8192,     # context window
    n_threads=8,    # CPU threads
    n_gpu_layers=0  # 0 = CPU only; set to 35 to offload layers to GPU
)
response = llm("What is quantization?", max_tokens=200)
```

---

### 4.3 Inference Optimization Techniques

#### KV Cache
Attention requires computing Key and Value matrices for every token in the context. The KV cache stores these after first computation so they're reused on subsequent tokens.

- **Memory bottleneck**: KV cache grows with sequence length. A 70B model with 128K context can need 40+ GB for KV cache alone.
- **PagedAttention** (vLLM): manages KV cache in non-contiguous memory pages, similar to OS virtual memory. Reduces memory waste by ~90%.

#### Speculative Decoding

```python
# Concept: use a small draft model to predict 4-8 tokens,
# verify in parallel with the big model

# Small model (e.g. Llama-3.2-1B) generates draft tokens cheaply:
#   draft: ["The", "capital", "of", "France", "is", "Paris"]

# Big model (e.g. Llama-3.1-70B) verifies ALL draft tokens in ONE forward pass:
#   accept: ["The", "capital", "of", "France", "is", "Paris"] ✓
#   or reject at "France": ["The", "capital", "of", "England"] — replace from here

# Result: 2-3x throughput improvement when draft acceptance rate is high
# Works best when output is predictable (code, structured text)

from transformers import AutoModelForCausalLM, AutoTokenizer

target_model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.1-70B")
draft_model  = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-1B")

inputs  = tokenizer("The capital of France is", return_tensors="pt")
outputs = target_model.generate(
    **inputs,
    assistant_model=draft_model,  # enables speculative decoding
    max_new_tokens=100
)
```

#### Batching & Parallelism

| Technique | What It Does | Benefit |
|-----------|-------------|---------|
| **Static Batching** | Wait for a full batch before processing any request | Simple but adds latency for early requests |
| **Continuous Batching** | Process each sequence at its own pace; add new requests mid-flight | 20-30x higher throughput vs static batching |
| **Tensor Parallelism** | Split weight matrices across multiple GPUs | Linear scaling for large models across GPUs |
| **Pipeline Parallelism** | Each GPU handles N layers sequentially | Enables models larger than single GPU VRAM |
| **Flash Attention** | Fused CUDA kernel; avoids materializing full attention matrix | 2-4x faster attention, 10x less memory |

> 💡 **Interview Tip:** For "how would you scale LLM inference?": mention (1) continuous batching via vLLM/TGI, (2) quantization to reduce GPU memory, (3) speculative decoding for latency, (4) caching for repeated prompts. This shows full-stack awareness.

---

## 5. Long-Context Strategies & Failure Modes

### 5.1 The Lost-in-the-Middle Problem

> **Research Finding (Liu et al., 2023):** LLMs perform significantly worse at retrieving facts placed in the **middle** of long contexts. Performance is best for facts at the very beginning or end. This means naive full-document stuffing is unreliable even within the context window.

**Practical implication:** if you have a 50-page document and the answer is on page 25, naive retrieval may fail even if the full document fits in context. You still need chunking and retrieval — not just "put it all in context".

---

### 5.2 Long-Context Strategies

| Strategy | Approach | Pros | Cons |
|----------|----------|------|------|
| **Full document in context** | Stuff entire doc into 200K context | Simple, no retrieval needed | Expensive, lost-in-middle problem |
| **Hierarchical retrieval** | Retrieve summaries first, drill into relevant sections | Efficient, preserves structure | Two-stage complexity |
| **Sliding window with overlap** | Process in overlapping chunks, aggregate answers | Handles arbitrarily long docs | May miss cross-chunk reasoning |
| **Map-reduce** | LLM processes each chunk independently, reducer combines | Parallelisable | May miss global context |
| **RAPTOR** (recursive abstraction) | Build tree of summaries; retrieve at any level | Best for multi-hop questions | Expensive indexing |

```python
# RAPTOR-style hierarchical indexing
from langchain_openai import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter

def build_raptor_index(docs: list[str], levels: int = 3):
    llm = ChatOpenAI(model="gpt-4o-mini")
    all_nodes = {}  # level → list of summaries

    # Level 0: original chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text("\n".join(docs))
    all_nodes[0] = chunks

    for level in range(1, levels + 1):
        prev_level = all_nodes[level - 1]
        summaries = []
        batch_size = max(1, len(prev_level) // 5)
        for i in range(0, len(prev_level), batch_size):
            batch   = "\n---\n".join(prev_level[i:i+batch_size])
            summary = llm.invoke(f"Summarize concisely:\n{batch}").content
            summaries.append(summary)
        all_nodes[level] = summaries

    return all_nodes  # Index all levels into vector store
```

---

### 5.3 Needle-in-a-Haystack Tests

The standard benchmark for evaluating long-context models. A specific fact is placed at different positions (0%, 25%, 50%, 75%, 100%) across documents of varying lengths, then the model is asked to retrieve it.

- GPT-4o and Claude 3.5 Sonnet score near-perfectly even at 128K tokens.
- Smaller open-source models often degrade significantly at >16K tokens.
- **Position 50% (middle) is the hardest** for almost all models.

> 💡 **Interview Tip:** Context window size and context **utilization** are different things. A 1M context window doesn't mean the model reliably uses facts from position 500K. Always cite the lost-in-the-middle paper and recommend retrieval over full-context for precision-sensitive tasks.

---

## 6. Model Versioning & MLOps for LLMs

### 6.1 Why LLM MLOps Is Different

Traditional ML deploys a model binary. LLM systems deploy a **model + prompt + retrieval pipeline + tools** — all four can change independently. This creates novel versioning and deployment challenges.

| Change Type | Risk | Testing Approach |
|-------------|------|-----------------|
| Prompt wording change | Medium — can silently degrade quality | Run eval suite before merge |
| Model version upgrade | Medium — API drift, new behavior | A/B test on 5% traffic first |
| Embedding model change | High — must re-index ALL documents | Blue-green index swap |
| Retrieval pipeline change | Medium-High — affects recall across all queries | Eval on golden query set |
| Tool / function signature change | High — breaks agent workflows | Integration tests + replay testing |

---

### 6.2 Experiment Tracking with MLflow

```python
import mlflow

mlflow.set_experiment("rag-pipeline-v2")

with mlflow.start_run(run_name="hyde-rerank-experiment"):
    mlflow.log_params({
        "embedding_model":  "text-embedding-3-small",
        "llm_model":        "gpt-4o",
        "chunk_size":       500,
        "chunk_overlap":    50,
        "top_k_retrieval":  20,
        "top_k_rerank":     5,
        "use_hyde":         True,
        "temperature":      0.0,
    })

    eval_results = run_eval_suite()
    mlflow.log_metrics({
        "faithfulness":       eval_results["faithfulness"],
        "answer_relevancy":   eval_results["answer_relevancy"],
        "context_recall":     eval_results["context_recall"],
        "avg_latency_ms":     eval_results["avg_latency_ms"],
        "avg_cost_per_query": eval_results["avg_cost_usd"],
    })

    # Log the prompt template as artifact
    mlflow.log_text(RAG_SYSTEM_PROMPT, "system_prompt.txt")
```

---

### 6.3 Safe Deployment Patterns

#### Blue-Green Deployment for Embedding Index Changes
1. Build the new index (green) with the updated embedding model — do NOT touch the live index (blue).
2. Run eval suite against green index. Compare metrics vs blue baseline.
3. If green passes: update the router to point new traffic at green. Keep blue for instant rollback.
4. After 24h of stable traffic: decommission blue index.

#### Canary Deployment for Prompt Changes

```python
async def route_request(user_query: str, user_id: str) -> dict:
    # Deterministic per user_id so same user always gets same variant
    bucket = hash(user_id) % 100
    use_new_prompt = bucket < 5  # 5% canary

    if use_new_prompt:
        result  = await run_new_prompt_pipeline(user_query)
        variant = "canary"
    else:
        result  = await run_current_pipeline(user_query)
        variant = "control"

    # Log both for comparison
    await log_to_langsmith(user_query, result, variant=variant)
    return result

# After enough traffic: compare LLM judge scores for canary vs control
# Only promote to 100% if canary scores are statistically better
```

---

### 6.4 Data Flywheel for Continuous Improvement

The virtuous cycle of: **logs → curate → fine-tune/prompt optimize → better model → better logs.**

1. Log all LLM inputs and outputs (with user consent and PII scrubbing).
2. Identify failures via LLM judge or thumbs-down signals.
3. Curate a "hard examples" dataset from failures.
4. Use hard examples for prompt optimization (DSPy) or fine-tuning.
5. Deploy improved model. Measure uplift. Repeat.

> 💡 **Interview Tip:** Senior candidates are expected to talk about the **data side** of ML. Saying "I'd collect production logs and use them to create a fine-tuning dataset" signals production maturity.

---

## 7. Chain-of-Thought Variants & Reasoning Models

### 7.1 CoT Variants — Quick Reference

| Variant | Core Idea | When to Use |
|---------|-----------|-------------|
| **Standard CoT** | "Think step by step" — linear reasoning chain | Multi-step math, logic, planning |
| **Zero-Shot CoT** | Append "Let's think step by step" — no examples needed | Quick reasoning improvement |
| **Self-Consistency** | Sample N reasoning chains (temp > 0), majority vote on final answer | High-stakes answers |
| **Tree of Thoughts (ToT)** | Branch multiple reasoning paths; evaluate each; backtrack from dead ends | Combinatorial problems |
| **Graph of Thoughts (GoT)** | Non-linear: merge, aggregate, refine across thought nodes | Complex multi-perspective reasoning |
| **Program-of-Thought (PoT)** | Model writes CODE instead of reasoning; code is executed for the answer | Math, calculation-heavy tasks |
| **ReAct** | Interleave reasoning (Thought) with tool actions (Act) and observations | Agentic tasks with tools |
| **Reflexion** | Agent reflects on past failures and stores verbal memories | Tasks requiring iterative improvement |

---

### 7.2 Self-Consistency — Most Reliable CoT Enhancement

```python
from langchain_openai import ChatOpenAI
from collections import Counter

def self_consistent_answer(question: str, n_samples: int = 5) -> str:
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)  # Non-zero temp for diversity

    prompt = f"""Solve step by step, then give a final answer on the last line.
Format: 'Final Answer: <answer>'
Question: {question}"""

    answers = []
    for _ in range(n_samples):
        response = llm.invoke(prompt).content
        for line in reversed(response.split("\n")):
            if "Final Answer:" in line:
                answers.append(line.split("Final Answer:")[1].strip())
                break

    if not answers:
        return "Could not extract answers"
    most_common, count = Counter(answers).most_common(1)[0]
    return f"{most_common} (agreed by {count}/{len(answers)} chains)"

# Self-consistency improves GSM8K accuracy from ~56% to ~78% for GPT-3
```

---

### 7.3 OpenAI o1/o3 and Reasoning Models

> **What Changed:** o1/o3 models (and similar: Claude's extended thinking, DeepSeek-R1) use **test-time compute** — they spend tokens on internal "thinking" before producing an output. This is trained in via RLVR (Reinforcement Learning with Verifiable Rewards), not just prompting.

| Aspect | Standard LLM (GPT-4o) | Reasoning Model (o1/o3) |
|--------|----------------------|------------------------|
| Reasoning approach | Follows CoT in prompt if asked | Internal chain-of-thought trained in |
| Latency | 2-10 seconds for typical response | 30-120+ seconds for hard problems |
| Token cost | Lower — prompt + completion | Higher — hidden thinking tokens + output |
| Prompting style | Detailed system prompts, CoT triggers | Less prompting needed; brief is better |
| Best tasks | General Q&A, RAG, summarization | Hard math, multi-step code, complex reasoning |

```python
# Using o1/o3 effectively — different rules than GPT-4o
from openai import OpenAI

client = OpenAI()

# o1: don't use system prompt (not well supported), brief user prompt is better
response = client.chat.completions.create(
    model="o3",
    messages=[{
        "role": "user",
        # Keep prompt simple — model handles its own reasoning
        "content": "Prove that sqrt(2) is irrational."
    }],
    reasoning_effort="high",          # "low" | "medium" | "high"
    max_completion_tokens=16000,       # includes hidden thinking tokens
)

# Cost note: o3 uses 10-1000x more tokens per request than GPT-4o
# Use only for tasks that genuinely need deep reasoning
```

> 💡 **Interview Tip:** When asked about o1/o3 — explain that these models were trained with **RLVR** (rewarded for getting math/code problems *correct*), which led to emergent reasoning chains. This is different from **RLHF** which optimizes for human preference. The reasoning is *trained in*, not prompted in.

---

## 8. Multimodal LLMs

### 8.1 Multimodal Architecture Overview

| Component | Purpose | Example |
|-----------|---------|---------|
| **Vision Encoder** | Convert image to patch embeddings | ViT — image split into 16×16 patches |
| **Projection Layer** | Map vision embeddings to LLM token space | Linear layer or MLP adapter |
| **Language Model Backbone** | Process combined text + vision tokens | Standard transformer decoder |
| **Text Decoder** | Generate output tokens | Same as standard LLM generation |

---

### 8.2 Practical Multimodal API Usage

```python
# Anthropic vision API
import anthropic, base64

client = anthropic.Anthropic()

# Method 1: base64 encoded image
with open("chart.png", "rb") as f:
    image_data = base64.standard_b64encode(f.read()).decode("utf-8")

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": image_data
                }
            },
            {"type": "text", "text": "Describe the trends in this chart."}
        ]
    }]
)

# Method 2: URL (OpenAI)
from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": "https://example.com/chart.png"}},
            {"type": "text", "text": "What does this chart show?"}
        ]
    }]
)
```

---

### 8.3 Multimodal RAG — Document Understanding

| Approach | How | Best For |
|----------|-----|----------|
| **Text extraction + OCR** | Extract text from PDFs; use Tesseract/AWS Textract for images | Text-heavy documents |
| **Multimodal embedding** | Embed images directly with CLIP; store image vectors | Visually-rich documents |
| **Page-as-image** | Render each PDF page as image; use vision LLM to describe; embed descriptions | Complex layouts, charts |
| **ColPali** | End-to-end multimodal retriever; embeds document pages as images | Best quality for complex docs |
| **Unstructured.io** | Parse PDFs, Word, PowerPoint with structure preservation | Production document ingestion |

```python
# Page-as-image RAG pattern
import fitz  # PyMuPDF
import base64
from openai import OpenAI

def extract_page_descriptions(pdf_path: str) -> list[str]:
    client = OpenAI()
    doc    = fitz.open(pdf_path)
    descs  = []

    for page_num in range(len(doc)):
        page      = doc[page_num]
        pix       = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x scale for quality
        img_bytes = pix.tobytes("png")
        img_b64   = base64.standard_b64encode(img_bytes).decode()

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
                {"type": "text", "text": "Describe ALL content including text, tables, and figures."}
            ]}]
        )
        descs.append(f"Page {page_num + 1}: {response.choices[0].message.content}")

    return descs  # Embed these descriptions for retrieval
```

---

## 9. Data Privacy, Memorization & Compliance

### 9.1 Training Data Memorization

> **Critical Security Risk:** LLMs can memorize and reproduce verbatim text from training data — including PII, API keys, passwords, and copyrighted content. Carlini et al. showed GPT-2 could be prompted to reproduce credit card numbers from training data.

| Risk | Description | Mitigation |
|------|-------------|------------|
| **PII leakage** | Model reproduces real names, emails, SSNs from training | Differential privacy during training; PII scrubbing |
| **Credential exposure** | Model recalls API keys or passwords seen during training | Secrets scanning in training data pipeline |
| **Copyright reproduction** | Model reproduces book passages, licensed code | Deduplication + content filtering in pretraining data |
| **Fine-tune data leakage** | Fine-tuning on internal docs → model leaks proprietary info | PII scrubbing before fine-tuning; evaluate for leakage |
| **Embedding inversion** | Embeddings can be approximately reversed to recover source text | Don't store sensitive raw text alongside its embedding |

---

### 9.2 Differential Privacy in Fine-tuning

```python
# DP-SGD with Opacus (PyTorch)
from opacus import PrivacyEngine
from torch.optim import Adam

optimizer = Adam(model.parameters(), lr=5e-5)

privacy_engine = PrivacyEngine()

model, optimizer, data_loader = privacy_engine.make_private_with_epsilon(
    module=model,
    optimizer=optimizer,
    data_loader=train_loader,
    epochs=3,
    target_epsilon=8.0,   # Privacy budget: lower = more private, lower accuracy
    target_delta=1e-5,    # Probability of privacy failure
    max_grad_norm=1.0,    # Gradient clipping threshold
)

# epsilon=8 is commonly used; epsilon=1 is very strict; epsilon=50+ is loose
epsilon = privacy_engine.get_epsilon(delta=1e-5)
print(f"Current privacy budget spent: epsilon={epsilon:.2f}")
```

---

### 9.3 GDPR & AI Compliance — Interview Topics

| Requirement | Implication for AI Systems |
|-------------|--------------------------|
| **Right to erasure (Art. 17)** | If a user's data was used to fine-tune a model, deleting the data may require model retraining. Avoid fine-tuning on user data if possible. |
| **Data minimisation (Art. 5)** | Only embed and store the minimum data needed. Strip PII before embedding. |
| **Purpose limitation** | Data collected for one purpose (e.g. support chat) cannot be repurposed for training without explicit consent. |
| **Data residency** | EU customer data must stay in EU regions. Check your vector DB and LLM API providers' DPAs. |
| **EU AI Act (2024)** | High-risk AI systems require documentation, human oversight, and conformity assessments. Classify your system's risk level. |

> 💡 **Interview Tip:** At enterprise companies: expect questions about GDPR and what happens when a user requests deletion. The correct answer: (1) avoid fine-tuning on user data, (2) PII scrubbing before embedding, (3) audit logs for all LLM calls, (4) machine unlearning as a research area.

---

## 10. System Design — End-to-End AI Products

### 10.1 How to Approach AI System Design Questions

The interviewer wants to see: tradeoff thinking, knowledge of failure modes before they happen, and reasoning about scale, cost, and quality simultaneously.

1. **Clarify**: query volume? latency requirement? accuracy target? budget? data sensitivity?
2. **Start simple**: describe the naive solution first (direct LLM call, no RAG).
3. **Identify failure modes**: where does the simple solution break?
4. **Layer in complexity**: add retrieval, caching, agents only where needed.
5. **Discuss eval**: how would you know it's working?
6. **Discuss production**: monitoring, versioning, rollback.

---

### 10.2 Design: Enterprise Document Q&A System (100K users)

**Requirements assumed:** 100K DAU, peak 500 QPS, P95 < 3s, EU data residency, faithfulness > 0.85.

| Component | Choice | Why |
|-----------|--------|-----|
| LLM | Azure OpenAI GPT-4o (EU region) | Data residency; managed SLA; prompt caching |
| Embeddings | text-embedding-3-small | Best cost/quality ratio |
| Vector DB | Azure AI Search or Qdrant (EU) | Native Azure integration or self-hosted EU compliance |
| Cache | Redis Cluster | Session memory + LLM response cache; TTL control |
| Reranking | Cohere Rerank v3 (EU endpoint) | 20% recall improvement; 50ms overhead acceptable |
| Queue | Azure Service Bus | Rate limiting; async processing; burst handling |
| Observability | LangSmith + Azure Monitor | Trace every call; alert on latency/cost anomalies |
| Auth | Azure AD + row-level security in vector DB | Users only retrieve documents they can access |

**Request flow:**
1. User query → API Gateway → auth check (JWT) → rate limit check (Redis)
2. Cache lookup: `hash(user_id + query)` → Redis. Cache hit: return in <100ms.
3. Multi-query generation: GPT-4o-mini generates 3 query variants (~300ms)
4. Parallel retrieval: top-20 chunks per variant from vector DB (~150ms)
5. Rerank: Cohere reranks 60 candidates to top-5 (~100ms)
6. Prompt assembly + GPT-4o call with prompt caching (~1-2s)
7. Stream response to user; log asynchronously to LangSmith

**Cost optimization:**
- Prompt caching for the 2,000-token system prompt: saves ~80% on system prompt tokens.
- GPT-4o-mini for query expansion (not GPT-4o): saves 10x on that step.
- LLM response cache (Redis, 1h TTL): expect 15-30% cache hit rate.

---

### 10.3 Design: AI Code Review Agent

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Architecture | LangGraph agent | Multi-step: read PR → retrieve context → analyze → generate review |
| Context retrieval | Code-aware chunking (by function/class) | Semantic boundaries matter more in code |
| Code embeddings | text-embedding-3-small or CodeBERT | CodeBERT better for cross-language search |
| Linter integration | Tool calls to pylint/eslint in sandbox | Ground suggestions in actual lint errors |
| Human-in-loop | LangGraph breakpoint before posting review | Prevent hallucinated reviews posting automatically |
| Eval | Compare suggestions vs senior engineer review on 200 past PRs | Ground truth for measuring agent quality |

> 💡 **Interview Tip:** In system design always bring up: (1) **permission/access control** — who can see what? (2) **cost at scale** — what's the monthly bill at 1M queries? (3) **graceful degradation** — what happens when the LLM API is down? (4) **eval strategy** — how will you know version 2 is better than version 1?

---

## 11. Master Cheat Sheet

### Advanced RAG Decision Tree

| Problem Observed | Solution |
|-----------------|---------|
| Retrieval misses relevant docs | Add HyDE + multi-query retrieval |
| Retrieved docs are relevant but answer is wrong | Add reranking (Cohere or cross-encoder) |
| Chunks are too long and noisy | Add contextual compression (EmbeddingsFilter) |
| User asks ambiguous questions | Add query decomposition (break into sub-questions) |
| Keywords matter as much as semantics | Switch to hybrid retrieval (dense + BM25 with RRF) |
| Multi-hop questions fail | Switch to agentic RAG or RAPTOR hierarchical indexing |
| Freshness matters | Implement online RAG with streaming ingestion |

---

### Inference Optimization Decision Tree

| Goal | Technique |
|------|-----------|
| Fit model in less GPU memory | Quantize: INT8 for minimal quality loss, INT4 (AWQ) for max compression |
| Reduce latency for chat | Enable streaming; use speculative decoding; optimize TTFT |
| Maximize throughput for batch | Use continuous batching (vLLM); increase batch size |
| Run locally on laptop | Use GGUF Q4_K_M format — good quality/speed tradeoff |
| Scale to 1000+ concurrent users | vLLM with PagedAttention + horizontal scaling |
| Reduce repeated prompt cost | Prompt caching (Anthropic) or KV cache persistence |

---

### Benchmark Quick Reference

| Benchmark | Measures | Why It's Asked |
|-----------|----------|----------------|
| MMLU | General knowledge, 57 subjects | Model selection for general-purpose apps |
| HumanEval | Code generation quality | Model selection for coding assistants |
| GSM8K | Math reasoning | Does model need o1 or does GPT-4o suffice? |
| MT-Bench | Multi-turn conversation | Chatbot quality — most relevant to production apps |
| LMSYS Arena ELO | Human preference, live | Most realistic signal for chat quality |
| SWE-Bench | Software engineering tasks | Agentic coding capability |

---

### The 10 Questions That Decide Senior Offers

1. **"How would you improve a RAG pipeline that gives wrong answers?"**
   → Chunking → HyDE → Rerank → Eval loop. Name the specific tool (Cohere Rerank, DeepEval).

2. **"What's the difference between top_p and temperature?"**
   → Temperature reshapes the ENTIRE distribution. top_p truncates it. They're complementary, not equivalent.

3. **"How does speculative decoding work?"**
   → Draft model generates cheaply; big model verifies in parallel. 2-3x throughput when acceptance rate is high.

4. **"What is the lost-in-the-middle problem?"**
   → Middle context is underutilized. Always use retrieval for precision tasks even with large context windows.

5. **"How do you evaluate a RAG system without human labels?"**
   → RAGAS (reference-free faithfulness + relevancy) + LLM-as-judge (G-Eval pattern).

6. **"How would you deploy a prompt change safely?"**
   → Canary deployment (5% traffic) + eval comparison before 100% rollout. Never change prompts without baseline.

7. **"What is quantization and when would you use it?"**
   → Precision reduction for memory/speed. Use AWQ for best INT4 quality on GPU; GGUF Q4_K_M for CPU.

8. **"What are the privacy risks of fine-tuning on user data?"**
   → Memorization, GDPR right-to-erasure complexity. Use DP-SGD or avoid fine-tuning on user data entirely.

9. **"How does o1 differ from GPT-4o?"**
   → Test-time compute, RLVR training (not RLHF), no system prompt needed, higher latency/cost, better for hard reasoning.

10. **"Design a multi-tenant RAG system."**
    → Pinecone namespaces (or row-level security in Qdrant), per-user memory, audit logs, data residency constraints.

---

### OWASP Top 10 for LLMs — Part 3 Additions

| # | Vulnerability | Part 3 Context |
|---|--------------|----------------|
| 1 | Prompt Injection | Indirect injection via RAG-retrieved poisoned documents |
| 4 | Model Denial of Service | Large RAPTOR indexes or speculative decoding can exhaust resources |
| 6 | Sensitive Info Disclosure | Training data memorization — fine-tuning on user data |
| 8 | Excessive Agency | Agentic RAG making unintended write operations |
| 9 | Overreliance | Not having evals means silent quality degradation |
| 10 | Model Theft | Embedding inversion attacks on stored vectors |

---

### Senior-Level Differentiators Checklist

- [ ] Can you explain HyDE and when NOT to use it?
- [ ] Can you implement a cross-encoder reranker from scratch?
- [ ] Can you set up a RAGAS eval pipeline with custom metrics?
- [ ] Do you know the difference between AWQ and GPTQ?
- [ ] Can you explain PagedAttention and why it matters?
- [ ] Do you know the lost-in-the-middle paper and its implications?
- [ ] Can you describe a data flywheel for LLM improvement?
- [ ] Can you explain RLVR vs RLHF and why o1 reasoning works?
- [ ] Do you know the GDPR implications for fine-tuning on user data?
- [ ] Can you design a multi-tenant, compliant RAG system end-to-end?

---

*Part 3 of 3  |  2025–2026*
*Read alongside Part 1 (LangChain, LangGraph, Tool Calling, MCP, Vector DBs, RAG, Pinecone) and Part 2 (LLM Fundamentals, Prompt Engineering, Agents, Observability, Fine-tuning, Streaming, Security, Deployment)*
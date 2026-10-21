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

---

### 🔷 CONCEPT OVERVIEW: Tokenization

> **What:** Tokenization is the process of converting raw text into smaller numeric units called **tokens** — the actual input an LLM processes. A token can be a word, part of a word, a character, or even a byte, depending on the algorithm.

> **Why:** LLMs don't understand raw text — they work on numbers. Tokenization bridges human-readable text and machine-processable numbers. It also governs cost (API billing is per token), context limits (measured in tokens), and security (prompt injection can exploit token boundaries).

> **How (Step-by-Step):**
> 1. Text is read as a raw string: `"Hello, world!"`
> 2. The tokenizer vocabulary (trained on a corpus) maps character sequences to token IDs
> 3. The string is split into the best matching vocabulary units: `['Hello', ',', ' world', '!']`
> 4. Each unit maps to an integer ID: `[9906, 11, 1917, 0]`
> 5. These IDs are fed into the model's embedding layer

> **Benefits:**
> - Enables efficient text compression (avg ~4 chars per token in English)
> - Handles multiple languages and code via sub-word splitting
> - Consistent input format across all model calls

> **Key Terms:**
> - **Token:** The basic unit of input/output for an LLM; can be a word, sub-word, or character
> - **Vocabulary:** The fixed set of all known tokens a model was trained with (e.g., 50,257 for GPT-2)
> - **BPE (Byte-Pair Encoding):** Iteratively merges the most frequent character pairs to build vocabulary
> - **WordPiece:** Similar to BPE but uses likelihood maximisation; marks continuations with `##`
> - **SentencePiece:** Language-agnostic tokenizer; handles any script without pre-processing
> - **Tiktoken:** OpenAI's fast, optimised BPE tokenizer used by GPT-4 family
> - **Token ID:** The integer that represents a token in the model's embedding lookup table

---

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

### 🔷 CONCEPT OVERVIEW: Sampling Strategies

> **What:** After the model produces a probability distribution over its entire vocabulary for the next token, a **sampling strategy** determines which token to actually pick. Different strategies balance creativity vs. determinism.

> **Why:** Picking always the highest-probability token (greedy) produces repetitive, boring output. Pure random sampling produces gibberish. Sampling strategies strike the right balance for each use case — creative writing vs. factual Q&A vs. code generation.

> **How (Step-by-Step):**
> 1. The model computes logits (raw scores) for all vocabulary tokens
> 2. A temperature value divides all logits (reshaping the distribution)
> 3. Softmax converts logits into probabilities (0–1, summing to 1)
> 4. Top-k or top-p filters trim the distribution to the most likely candidates
> 5. A token is sampled from the remaining distribution
> 6. The selected token is appended to the context; the process repeats

> **Benefits:**
> - Temperature lets you tune creativity without retraining
> - Top-p adapts dynamically to each step's distribution (unlike fixed top-k)
> - Beam search produces globally optimal sequences for structured tasks

> **Key Terms:**
> - **Logits:** Raw unnormalized scores output by the model before softmax
> - **Softmax:** Function converting logits to probabilities that sum to 1
> - **Temperature (T):** Scalar that divides logits; T<1 sharpens, T>1 flattens distribution
> - **Top-k:** Restricts sampling to the k highest-probability tokens
> - **Top-p (Nucleus Sampling):** Restricts sampling to the smallest set of tokens whose cumulative probability ≥ p
> - **Beam Search:** Maintains B best candidate sequences simultaneously; picks highest joint probability
> - **Min-p:** Discards tokens whose probability falls below `p × max_probability`; newer alternative to top-p
> - **Repetition Penalty:** Reduces probability of tokens already seen in the output to prevent loops
> - **Greedy Decoding:** Always picks the single most likely next token; fully deterministic

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

---

### 🔷 CONCEPT OVERVIEW: Advanced RAG Retrieval

> **What:** Advanced retrieval techniques go beyond naive "embed the query → find similar chunks." They include methods like HyDE, multi-query retrieval, re-ranking, and query decomposition — all designed to improve what gets retrieved before passing context to the LLM.

> **Why:** Naive RAG fails because: (1) short questions don't embed similarly to long answers, (2) the truly relevant chunk may not be in the top-5, and (3) retrieved chunks may be topically adjacent but not actually useful. Advanced retrieval solves each of these systematically.

> **How (General Flow):**
> 1. Receive user query
> 2. Optionally transform the query (HyDE / multi-query / decomposition)
> 3. Retrieve a broad candidate set (top-20 to top-50) using embeddings
> 4. Re-rank candidates using a more accurate cross-encoder model
> 5. Optionally compress chunks to extract only the relevant sentences
> 6. Pass the final top-N chunks as context to the LLM

> **Benefits:**
> - Dramatically improves recall (finding the right chunk) and precision (using only relevant content)
> - Modular — each stage can be swapped independently
> - Measurable — each improvement can be evaluated with RAGAS metrics

> **Key Terms:**
> - **Recall:** Did we retrieve the chunk that contains the answer? (Did we find it at all?)
> - **Precision:** Of what we retrieved, how much is actually relevant?
> - **Bi-encoder:** Embeds query and document independently; fast but less accurate
> - **Cross-encoder:** Sees query and document together; slow but much more accurate
> - **Re-ranking:** A second-stage pass using a cross-encoder to re-order retrieved candidates
> - **HyDE:** Hypothetical Document Embeddings — embed a generated answer instead of the raw query
> - **RRF (Reciprocal Rank Fusion):** Algorithm for merging multiple ranked lists into one
> - **Contextual Compression:** Extracting only the relevant sentences from a retrieved chunk

---

### 2.1 The Problem With Naive RAG

Naive RAG embeds the user's question and retrieves the most similar chunks. This fails in three predictable ways:
- **Query-document mismatch**: questions are short and abstract; answers are long and specific.
- **Poor recall**: top-5 chunks miss key info that ranks 8th or 12th.
- **Poor precision**: retrieved chunks are semantically adjacent but don't actually answer the question.

---

### 🔷 CONCEPT OVERVIEW: HyDE (Hypothetical Document Embeddings)

> **What:** HyDE is a retrieval technique where, instead of embedding the user's raw question, you first ask the LLM to generate a hypothetical ideal answer — then embed *that* answer for retrieval.

> **Why:** A short question like "what causes aurora borealis?" embeds differently from the encyclopedic documents that answer it. A generated answer ("Aurora borealis is caused by charged solar particles interacting with Earth's magnetic field…") embeds much closer to real documents — bridging the query-document embedding gap.

> **How (Step-by-Step):**
> 1. User submits query: "What causes aurora borealis?"
> 2. LLM generates a hypothetical answer: "Aurora borealis is caused by…"
> 3. The hypothetical answer (not the query) is embedded into a vector
> 4. Vector search retrieves documents closest to that hypothesis vector
> 5. Retrieved documents are passed to the LLM with the original question

> **Benefits:**
> - Improves recall by 10–30% on knowledge-intensive tasks
> - Works particularly well when queries are short and documents are long
> - No changes needed to the index or document embeddings

> **Key Terms:**
> - **Hypothetical Document:** An LLM-generated answer used as a search proxy instead of the query
> - **Embedding Gap:** The semantic distance between a short question and a detailed document answer
> - **Query-Document Mismatch:** The core problem HyDE addresses — questions and answers don't embed similarly
> - **Hallucination Risk:** If the LLM hallucinates in the hypothetical, the embedding may point to wrong documents

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

### 🔷 CONCEPT OVERVIEW: Query Transformation Techniques

> **What:** Query transformation is a family of techniques that modify or expand the user's original query before retrieval — generating multiple paraphrases, breaking it into sub-questions, or abstracting it to a higher level — to improve recall and handle ambiguity.

> **Why:** A single query often doesn't capture all the ways relevant information might be phrased in documents. By generating multiple variants or sub-questions, you cast a wider net and find more relevant chunks.

> **How (Multi-Query Example):**
> 1. User asks: "How does attention work in transformers?"
> 2. LLM generates 3 paraphrases: "Explain self-attention mechanism", "What is the math behind transformer attention?", "Why do LLMs use attention over recurrence?"
> 3. Each paraphrase is used to retrieve top-5 chunks independently
> 4. All results are deduplicated and combined
> 5. The combined result set is passed to the LLM with the original question

> **Benefits:**
> - Multi-query significantly improves recall for ambiguous or complex questions
> - Query decomposition handles multi-hop questions that require chaining facts
> - Step-back prompting retrieves foundational context that naive queries miss

> **Key Terms:**
> - **Multi-Query Retrieval:** Generate paraphrases of the query; retrieve for each; deduplicate
> - **Step-Back Prompting:** Abstact the query to a broader concept before retrieval
> - **Query Decomposition:** Break a complex question into sub-questions; answer each; synthesize
> - **RAG-Fusion:** Multi-query + Reciprocal Rank Fusion for merging results from multiple retrievals
> - **Deduplication:** Removing duplicate retrieved chunks that appear across multiple query variants

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

### 🔷 CONCEPT OVERVIEW: Re-Ranking

> **What:** Re-ranking is a two-stage retrieval pattern where you first retrieve a large candidate set (top-20 to top-50) using fast embedding similarity, then re-score each candidate using a slower but more accurate cross-encoder model, returning only the best top-N.

> **Why:** Bi-encoder embeddings are fast but treat query and document independently — they miss nuanced relevance. Cross-encoders read query and document together (like a mini reading comprehension), yielding far more accurate relevance scores. Re-ranking applies cross-encoders only to a pre-filtered set, balancing accuracy and speed.

> **How (Step-by-Step):**
> 1. Bi-encoder retrieves top-20 candidate chunks from vector DB
> 2. Each candidate is paired with the query: `[query, chunk_1], [query, chunk_2], …`
> 3. Cross-encoder scores each pair (0–1 relevance score)
> 4. Candidates are sorted by cross-encoder score
> 5. Top-5 scoring chunks are passed to the LLM as context

> **Benefits:**
> - Often the single highest-impact RAG improvement available
> - Doesn't require re-indexing or changing the vector DB
> - Can double answer quality with only ~50–100ms added latency
> - Works with any retrieval system as a plug-in second stage

> **Key Terms:**
> - **Bi-encoder:** Encodes query and document independently into vectors; used for fast first-stage retrieval
> - **Cross-encoder:** Processes query and document together; much more accurate but 10–100x slower
> - **Cohere Rerank:** Managed re-ranking API; easiest production option
> - **ms-marco-MiniLM:** Popular open-source cross-encoder model for local re-ranking
> - **Candidate Set:** The large initial pool (top-20 to top-50) retrieved before re-ranking
> - **ContextualCompressionRetriever:** LangChain abstraction combining retrieval + reranking in one call

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

---

### 🔷 CONCEPT OVERVIEW: LLM Evaluation

> **What:** LLM evaluation is the practice of systematically measuring how well an LLM-powered system performs — using automated metrics, benchmark datasets, or another LLM as a judge — rather than relying on manual review.

> **Why:** Without evals, you're flying blind. You can't tell if a prompt change made things better or worse, if a model upgrade degraded quality, or if RAG improvements actually helped. Senior engineers are expected to treat model quality as rigorously as software correctness.

> **How (Building an Eval Pipeline):**
> 1. Create a golden dataset: 50–200 hand-curated (question, expected_answer) pairs
> 2. Define 3–5 metrics relevant to your task (e.g., faithfulness, relevancy, hallucination rate)
> 3. Run the system against the golden set; record baseline scores
> 4. On every change (prompt, model, retrieval), re-run evals and compare to baseline
> 5. Sample 1–5% of live production traffic; run judge asynchronously; alert on drops

> **Benefits:**
> - Catches regressions before they reach users
> - Enables safe, evidence-based iteration on prompts and models
> - Automatable in CI/CD pipelines for continuous quality gates

> **Key Terms:**
> - **Golden Dataset:** A curated set of (input, expected_output) pairs used as ground truth
> - **LLM-as-Judge:** Using a strong LLM (GPT-4o, Claude Opus) to score outputs of another LLM
> - **RAGAS:** Evaluation framework for RAG pipelines; measures faithfulness, relevancy, context recall
> - **G-Eval:** LLM-judge pattern with chain-of-thought reasoning before scoring
> - **Faithfulness:** Does the answer only contain claims supported by the retrieved context?
> - **Answer Relevancy:** Does the answer actually address the question asked?
> - **Context Recall:** Did the retrieval find the chunks needed to answer the question?
> - **Hallucination Rate:** What fraction of claims in the output are not grounded in the context?
> - **Online Monitoring:** Sampling live production traffic to detect score degradation over time

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

### 🔷 CONCEPT OVERVIEW: Industry Benchmarks

> **What:** Industry benchmarks are standardised test sets used to measure and compare LLM capabilities — from general knowledge (MMLU) to coding (HumanEval) to math (GSM8K) to multi-turn conversation (MT-Bench).

> **Why:** Benchmarks provide a common language for comparing models objectively. In interviews, knowing benchmark names and scores signals that you make model-selection decisions based on evidence, not hype.

> **How (Using Benchmarks for Model Selection):**
> 1. Identify the primary capability needed (coding? math? conversation?)
> 2. Find the benchmark that best matches that capability (HumanEval for code, GSM8K for math)
> 3. Look up current scores for candidate models on that benchmark
> 4. Supplement with LMSYS Chatbot Arena for real-world human preference data
> 5. Run your own task-specific eval on a golden set from your domain

> **Benefits:**
> - Standardised comparison across models without running each yourself
> - Catches cases where a model excels in general but fails in specific domains
> - Enables informed upgrade decisions (is the new model actually better for my use case?)

> **Key Terms:**
> - **MMLU:** Massive Multitask Language Understanding — 57 academic subjects, multiple choice
> - **HumanEval:** 164 Python coding problems; measures pass@k (did any of k samples pass tests?)
> - **GSM8K:** Grade School Math — 8,500 word problems; CoT significantly helps
> - **MT-Bench:** Multi-turn conversation benchmark; scored 1–10 by GPT-4 as judge
> - **LMSYS Chatbot Arena:** Live ELO ranking from human pairwise preferences — most realistic signal
> - **SWE-Bench:** Real GitHub issues as tasks; measures actual software engineering ability
> - **pass@k:** Probability that at least 1 of k generated samples passes all unit tests

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

---

### 🔷 CONCEPT OVERVIEW: Quantization

> **What:** Quantization is the process of reducing the numerical precision of model weights from 32-bit or 16-bit floating point to lower precision formats (8-bit integers, 4-bit integers, etc.), making models smaller and faster to run.

> **Why:** A 70B parameter model in FP32 requires ~280 GB of VRAM — impossible on any single consumer GPU. Quantization shrinks it to fit on available hardware with only a small accuracy tradeoff. It's the primary technique enabling local and on-device LLM deployment.

> **How (Post-Training Quantization Flow):**
> 1. Start with a trained FP16 or FP32 model
> 2. Run a small calibration dataset through the model to observe activation ranges
> 3. Map each weight value to the nearest value in the lower-precision format (e.g., INT4)
> 4. Store the compressed weights; load them at inference time
> 5. Dequantize on-the-fly during matrix multiplication (compute still happens in FP16)

> **Benefits:**
> - 4-bit quantization reduces memory by ~4x vs FP16 with moderate quality loss
> - Enables 70B models on a single A100 GPU; 7B models on consumer GPUs
> - Faster inference due to smaller memory bandwidth requirements
> - Makes local deployment viable (GGUF format on CPU via llama.cpp)

> **Key Terms:**
> - **FP32:** 32-bit floating point; full precision; used only for training
> - **FP16/BF16:** 16-bit floating point; standard for GPU inference
> - **INT8:** 8-bit integer quantization; ~2x memory reduction, minimal quality loss
> - **INT4:** 4-bit integer quantization; ~4x memory reduction, moderate quality loss
> - **GPTQ:** Post-training quantization via layer-wise error minimization on a calibration set
> - **AWQ (Activation-Aware Quantization):** Protects the ~1% of "salient" weights; best INT4 quality
> - **GGUF:** llama.cpp's quantization format for CPU/hybrid inference
> - **QLoRA:** Fine-tuning with a 4-bit base model + FP16 LoRA adapters; fits on consumer GPU
> - **NF4 (NormalFloat4):** Optimised 4-bit format for normally-distributed weights; used in QLoRA

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

### 🔷 CONCEPT OVERVIEW: Inference Optimization

> **What:** Inference optimization is a collection of techniques — KV caching, speculative decoding, batching strategies, and attention optimizations — that reduce latency, increase throughput, and lower cost when serving LLMs in production.

> **Why:** Serving a 70B model naively can cost $10+/hour on high-end GPUs with poor throughput. Inference optimization can deliver 10–30x more requests per second from the same hardware, directly impacting product cost and user experience.

> **How (Key Techniques Flow):**
> 1. **KV Cache:** Compute Key/Value matrices for prompt tokens once; reuse on each new token generated
> 2. **Speculative Decoding:** Small draft model proposes 4–8 tokens; large model verifies all in one pass
> 3. **Continuous Batching:** Process requests at different stages simultaneously; don't wait for full batch
> 4. **Flash Attention:** Fused CUDA kernel that avoids materialising the full attention matrix in GPU memory
> 5. **PagedAttention:** Manages KV cache in non-contiguous memory pages — like OS virtual memory

> **Benefits:**
> - Continuous batching delivers 20–30x throughput vs naive static batching
> - Speculative decoding cuts latency 2–3x for predictable outputs
> - Flash Attention reduces attention memory by 10x and speeds it up 2–4x
> - Quantization + PagedAttention together enable fitting much larger models per GPU

> **Key Terms:**
> - **KV Cache:** Stored Key and Value matrices from prior tokens; avoids recomputation on each step
> - **Speculative Decoding:** Draft model generates candidate tokens; target model verifies in one pass
> - **Continuous Batching:** Processing requests asynchronously at different decode stages simultaneously
> - **PagedAttention:** vLLM's OS-inspired memory management for KV cache; reduces waste by ~90%
> - **Flash Attention:** Optimised attention kernel that tiles computation to avoid full matrix materialisation
> - **TTFT (Time To First Token):** Latency metric for how quickly the first output token is generated
> - **Tensor Parallelism:** Splitting weight matrices across multiple GPUs for linear scaling
> - **vLLM:** High-performance LLM serving library; implements PagedAttention + continuous batching

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

---

### 🔷 CONCEPT OVERVIEW: Long-Context Handling

> **What:** Long-context handling refers to strategies for processing documents or conversations that are too long to fit in the model's context window, or where naively stuffing everything in yields poor results due to the "lost-in-the-middle" problem.

> **Why:** Even with models that support 200K+ token windows, research shows LLMs systematically underperform when the relevant fact is in the middle of a long context. Simply "putting it all in" is unreliable and expensive. Smart chunking, retrieval, and summarization strategies are needed.

> **How (Retrieval-First Strategy):**
> 1. Split document into overlapping chunks (e.g., 500 tokens, 50 token overlap)
> 2. Embed each chunk and store in vector DB
> 3. At query time, retrieve only the most relevant 5–10 chunks
> 4. Place retrieved chunks at the beginning or end of the context (not the middle)
> 5. Generate the answer from the well-positioned, relevant chunks

> **Benefits:**
> - Avoids lost-in-the-middle degradation
> - Cheaper than full-document context for every query
> - More precise answers by focusing context on relevant material

> **Key Terms:**
> - **Lost-in-the-Middle:** LLM failure mode where facts in the middle of long contexts are underutilised
> - **Needle-in-a-Haystack Test:** Benchmark inserting a fact at various positions to measure long-context retrieval
> - **Hierarchical Retrieval:** Retrieve summaries first, then drill into relevant sections
> - **Map-Reduce:** Process chunks independently (map), then combine results (reduce)
> - **RAPTOR:** Recursive Abstractive Processing for Tree-Organised Retrieval — builds summary trees
> - **Sliding Window:** Process overlapping windows of text; aggregate answers across windows
> - **Context Utilisation:** How reliably the model uses information from different positions in the context

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

---

### 🔷 CONCEPT OVERVIEW: LLM MLOps

> **What:** MLOps for LLMs is the practice of systematically managing the lifecycle of LLM-powered systems — including versioning prompts, models, and retrieval pipelines; safe deployment patterns; experiment tracking; and continuous improvement loops.

> **Why:** Unlike traditional ML (which deploys a single model binary), LLM systems have four independently-changing components: model, prompt, retrieval pipeline, and tools. Any of these can silently degrade quality. Without disciplined MLOps, production LLM quality degrades unpredictably.

> **How (Safe Change Deployment Flow):**
> 1. Propose a change (prompt edit, model upgrade, embedding model swap)
> 2. Run the eval suite against the new version; compare to stored baseline metrics
> 3. Deploy as a canary to 5% of traffic; monitor LLM judge scores vs control
> 4. If canary scores match or exceed baseline, gradually roll out to 100%
> 5. Log all inputs/outputs; sample for quality monitoring; feed failures back to improve

> **Benefits:**
> - Catch silent quality regressions before they affect all users
> - Enable safe, evidence-based iteration
> - Build a data flywheel: production failures become training/fine-tuning data

> **Key Terms:**
> - **Canary Deployment:** Routing a small percentage of traffic to the new version for risk-limited testing
> - **Blue-Green Deployment:** Running old (blue) and new (green) systems in parallel; instant rollback available
> - **Data Flywheel:** Virtuous cycle where production logs → curated failures → improved model → better logs
> - **Prompt Versioning:** Treating prompt templates as code artifacts with version control and change history
> - **Embedding Index Swap:** Migrating from one embedding model to another by rebuilding the vector index
> - **MLflow:** Open-source experiment tracking; logs parameters, metrics, and artifacts per run
> - **Shadow Eval:** Running the eval pipeline on live production traffic samples asynchronously

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

---

### 🔷 CONCEPT OVERVIEW: Chain-of-Thought (CoT) and Variants

> **What:** Chain-of-Thought (CoT) prompting encourages LLMs to produce intermediate reasoning steps before giving a final answer, rather than jumping directly to the answer. Variants extend this into trees, graphs, parallel sampling, and tool-augmented reasoning.

> **Why:** LLMs are next-token predictors. When asked complex questions directly, they often confabulate answers. By generating reasoning steps, the model conditions its answer on prior correct reasoning — dramatically improving accuracy on multi-step problems.

> **How (Standard CoT):**
> 1. Append "Let's think step by step" (zero-shot) or provide worked examples (few-shot)
> 2. Model generates intermediate reasoning: "First… then… therefore…"
> 3. Model then produces a final answer conditioned on the reasoning chain
> 4. For self-consistency: repeat N times with temperature > 0, take majority vote

> **Benefits:**
> - Zero-shot CoT ("Let's think step by step") alone improves GSM8K from ~56% to ~78% for GPT-3
> - Self-consistency further boosts accuracy by ~10–15% on math benchmarks
> - Program-of-Thought offloads arithmetic to code execution, eliminating calculation errors

> **Key Terms:**
> - **Chain-of-Thought (CoT):** Prompting the model to reason step-by-step before answering
> - **Zero-Shot CoT:** Adding "Let's think step by step" with no examples
> - **Self-Consistency:** Sample N reasoning chains; majority-vote on the final answer
> - **Tree of Thoughts (ToT):** Branch multiple reasoning paths; evaluate and backtrack from dead ends
> - **Program-of-Thought (PoT):** Model writes executable code; code runs to produce the answer
> - **ReAct:** Interleave Reasoning (Thought) with tool Actions and Observations
> - **Reflexion:** Agent reflects on past failures and stores verbal memories to improve future attempts
> - **RLVR:** Reinforcement Learning with Verifiable Rewards — trains reasoning by rewarding correct answers

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

### 🔷 CONCEPT OVERVIEW: Reasoning Models (o1 / o3 / DeepSeek-R1)

> **What:** Reasoning models are a new class of LLMs (OpenAI o1/o3, Claude extended thinking, DeepSeek-R1) that use **test-time compute** — spending additional tokens on internal "thinking" before producing output — trained via reinforcement learning on verifiable tasks rather than human preference.

> **Why:** Standard LLMs are trained to produce human-preferred responses (RLHF), which is great for general tasks but doesn't specifically reward getting hard problems *correct*. Reasoning models are trained with RLVR — only correct answers on math/code problems are rewarded — leading to emergent long chains of internal reasoning that solve harder problems.

> **How:**
> 1. Model receives the user's prompt
> 2. Instead of immediately generating a response, it produces hidden "thinking" tokens
> 3. The thinking process resembles extended CoT — exploring approaches, backtracking, verifying
> 4. After thinking, the model generates the visible final response
> 5. Users are billed for both thinking tokens and output tokens

> **Benefits:**
> - Significantly better on hard math, multi-step code, and complex logical reasoning
> - Less prompt engineering required — reasoning is trained in, not prompted in
> - Scales with compute: `reasoning_effort="high"` thinks longer for harder problems

> **Key Terms:**
> - **Test-Time Compute:** Using extra tokens/computation during inference (not training) to improve answers
> - **RLVR:** Reinforcement Learning with Verifiable Rewards — reward signal is objective correctness
> - **RLHF:** Reinforcement Learning from Human Feedback — reward signal is human preference ratings
> - **Thinking Tokens:** Hidden internal reasoning tokens generated before the visible output
> - **reasoning_effort:** API parameter controlling how long the model thinks (low/medium/high)
> - **DeepSeek-R1:** Open-source reasoning model trained with RLVR; competitive with o1

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

---

### 🔷 CONCEPT OVERVIEW: Multimodal LLMs

> **What:** Multimodal LLMs can process and generate content across multiple modalities — most commonly text and images, but also audio, video, and documents. They combine a vision encoder, a projection layer, and a standard language model backbone.

> **Why:** Real-world information isn't just text — it's charts, diagrams, screenshots, scanned documents, and photos. Multimodal LLMs enable applications that reason across both visual and textual information, like document understanding, visual Q&A, and chart analysis.

> **How (Architecture Flow):**
> 1. Image is split into fixed-size patches (e.g., 16×16 pixels each)
> 2. Vision encoder (e.g., ViT) converts patches into dense embeddings
> 3. A projection layer (linear or MLP) maps vision embeddings into the LLM's token space
> 4. Image embeddings are concatenated with text token embeddings
> 5. The combined sequence passes through the standard transformer decoder
> 6. The model generates text output conditioned on both visual and textual context

> **Benefits:**
> - Single model handles text + image tasks without separate pipelines
> - Enables document understanding without explicit OCR pre-processing
> - Charts, diagrams, and handwritten notes become queryable

> **Key Terms:**
> - **ViT (Vision Transformer):** Splits images into patches; each patch becomes a token-like embedding
> - **Projection Layer:** Maps vision embeddings into the LLM's embedding space (bridges modalities)
> - **CLIP:** OpenAI's model that jointly embeds images and text in the same vector space
> - **Multimodal Embedding:** A vector that encodes the meaning of an image for retrieval
> - **ColPali:** End-to-end multimodal retriever that embeds PDF pages as images
> - **OCR (Optical Character Recognition):** Extracting text from images; a simpler alternative to multimodal LLMs
> - **Page-as-Image Pattern:** Render each PDF page as an image; use vision LLM to describe; embed descriptions

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

---

### 🔷 CONCEPT OVERVIEW: Training Data Memorization & Privacy

> **What:** LLMs can memorize and reproduce verbatim text from their training data — including personally identifiable information (PII), API keys, passwords, and copyrighted content. Fine-tuning on sensitive data amplifies this risk.

> **Why:** Memorization creates real security and legal liability. If a model is fine-tuned on customer support logs and reproduces someone's email or credit card number in response to an unrelated query, that's a GDPR violation and a potential breach. Understanding memorization is essential for any production AI system.

> **How (Memorization Occurs):**
> 1. During training, the model optimizes to predict next tokens in training data
> 2. For repeated or unique sequences, the model "memorizes" — storing patterns strongly enough to reproduce them
> 3. A user can accidentally (or deliberately) trigger reproduction via targeted prompting
> 4. Fine-tuning on new sensitive data concentrates memorization risk on that specific dataset

> **Benefits of Understanding This:**
> - Enables proactive PII scrubbing before training or fine-tuning
> - Informs decisions about what data should never be used for training
> - Guides architecture choices (e.g., using RAG instead of fine-tuning for sensitive knowledge)

> **Key Terms:**
> - **Memorization:** The model's ability to reproduce verbatim sequences from training data
> - **PII (Personally Identifiable Information):** Names, emails, SSNs, phone numbers, addresses
> - **Differential Privacy (DP):** Mathematical privacy guarantee; limits what can be inferred about any single training example
> - **DP-SGD:** Differentially Private Stochastic Gradient Descent — adds calibrated noise during training
> - **Epsilon (ε):** Privacy budget in DP; lower = stronger privacy; ε=8 is commonly used in practice
> - **Delta (δ):** Probability that the DP guarantee fails; typically set to 1e-5
> - **PII Scrubbing:** Automated detection and removal/replacement of personal data before training
> - **Embedding Inversion:** Attack that approximately recovers source text from its embedding vector

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

### 🔷 CONCEPT OVERVIEW: GDPR & AI Compliance

> **What:** GDPR (General Data Protection Regulation) and the EU AI Act impose legal requirements on AI systems that process EU residents' personal data — including rights to erasure, data minimisation, purpose limitation, and documentation of high-risk AI.

> **Why:** Enterprise AI systems routinely process personal data. Non-compliance can result in fines up to 4% of global annual revenue. The right to erasure (Art. 17) is particularly challenging for AI — if someone's data was used to fine-tune a model, "deleting" their data may require retraining.

> **How (Compliance Architecture):**
> 1. Minimise data: strip PII before embedding or storing in vector DBs
> 2. Avoid fine-tuning on user data where possible; use RAG for personalisation instead
> 3. Log all LLM calls with user consent; store in EU region if serving EU users
> 4. Implement audit trails for data access and model usage
> 5. Classify AI system risk level under EU AI Act; document high-risk systems

> **Benefits:**
> - Avoids regulatory fines and reputational damage
> - Forces data hygiene that also improves system reliability
> - Proactive compliance is cheaper than reactive remediation

> **Key Terms:**
> - **Right to Erasure (Art. 17):** User's right to have their personal data deleted
> - **Data Minimisation:** Only collect and store the minimum data required for the purpose
> - **Purpose Limitation:** Data collected for one purpose cannot be repurposed without new consent
> - **Data Residency:** Legal requirement to store data within a specific geographic region
> - **EU AI Act:** 2024 EU regulation classifying AI systems by risk; high-risk systems need documentation
> - **DPA (Data Processing Agreement):** Legal contract required with third-party data processors (e.g., OpenAI, Cohere)
> - **Machine Unlearning:** Research area for removing specific training data influence from a model post-hoc

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

---

### 🔷 CONCEPT OVERVIEW: AI System Design

> **What:** AI system design is the practice of architecting complete, production-ready LLM-powered products — covering data flow, component selection, scaling, cost, security, evaluation, and operational concerns — rather than just writing prompt code.

> **Why:** Building a demo is easy; building a reliable, cost-efficient, secure, and observable product at scale is hard. System design interviews test whether you've thought about the full picture: failure modes, latency budgets, cost at scale, access control, and how you'd know if the system degrades.

> **How (Interview Framework):**
> 1. **Clarify:** query volume, latency SLA, accuracy target, budget, data sensitivity
> 2. **Start simple:** describe the naive solution; identify where it breaks
> 3. **Layer in complexity:** add RAG, caching, agents, re-ranking only where needed
> 4. **Discuss eval:** golden dataset, metrics, canary deployment strategy
> 5. **Discuss production:** monitoring, cost optimisation, graceful degradation, rollback

> **Benefits of This Approach:**
> - Shows end-to-end thinking, not just ML knowledge
> - Demonstrates production experience and cost awareness
> - Signals you've considered security, compliance, and failure modes proactively

> **Key Terms:**
> - **Prompt Caching:** Reusing the KV cache for repeated prefixes (system prompt) to cut token costs
> - **P95 Latency:** The 95th percentile latency — the response time exceeded by only 5% of requests
> - **Rate Limiting:** Capping requests per user/time period to prevent abuse and manage costs
> - **Row-Level Security:** Access control at the data layer — users can only retrieve their own documents
> - **Graceful Degradation:** Fallback behaviour when a component fails (e.g., cache-first, then API)
> - **Multi-tenancy:** Serving multiple organisations or users from one system with data isolation
> - **Audit Log:** Immutable record of all LLM inputs and outputs for compliance and debugging

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

### 🔷 QUICK-REFERENCE: All Concept Overviews at a Glance

| Concept | What (1 line) | Why (1 line) | Key Interview Signal |
|---------|---------------|--------------|---------------------|
| **Tokenization** | Text → numeric token IDs for model input | LLMs process numbers, not text; governs cost & context limits | Know BPE internals; explain digit tokenization |
| **Sampling (Temperature/Top-p)** | Strategy for choosing next token from probability distribution | Balances creativity vs determinism | Temperature reshapes; top-p truncates — complementary |
| **HyDE** | Embed a generated answer instead of the raw query | Bridges the gap between short questions and long documents | Know when it fails (LLM hallucination in hypothesis) |
| **Multi-Query Retrieval** | Generate paraphrases; retrieve for each; deduplicate | One query misses many relevant phrasings | 3–5x retrieval cost; best for ambiguous queries |
| **Re-Ranking** | Cross-encoder rescores top-20 candidates to return top-5 | Bi-encoders are fast but imprecise; cross-encoders are accurate | Single highest-impact RAG improvement |
| **LLM-as-Judge** | Strong LLM scores outputs of application LLM | Human labeling is slow; BLEU/ROUGE fails on open-ended tasks | Know G-Eval pattern; mention evals triangle |
| **Benchmarks** | Standardised test sets (MMLU, HumanEval, GSM8K…) | Common language for comparing models | LMSYS Arena = most realistic; SWE-Bench = agentic |
| **Quantization** | Reduce weight precision (FP16 → INT4) for memory/speed | 70B model won't fit on consumer GPU without it | AWQ = best INT4 quality; GGUF = CPU deployment |
| **KV Cache / PagedAttention** | Cache Key/Value matrices; manage in memory pages | Avoids recomputing attention for prior tokens | PagedAttention reduces waste by ~90% |
| **Speculative Decoding** | Draft model proposes tokens; large model verifies in batch | Large model forward pass is the bottleneck; batch verification is cheap | 2–3x latency improvement on predictable outputs |
| **Lost-in-the-Middle** | LLMs underuse facts in the middle of long contexts | Full-document stuffing is unreliable even within context window | Always cite Liu et al. 2023; recommend retrieval |
| **RAPTOR** | Build summary tree; retrieve at any level | Multi-hop questions need hierarchical context | Expensive to index; best for complex documents |
| **LLM MLOps** | Version prompts/models/indexes; safe deploy patterns | Four components change independently; any can silently break quality | Canary + eval gate before 100% rollout |
| **Data Flywheel** | Logs → curate failures → improve model → better logs | Production failures are the richest training signal | Shows production maturity in interviews |
| **CoT / Self-Consistency** | Generate reasoning steps; majority-vote across N chains | Direct answers on complex problems confabulate | Self-consistency: +15–20% on math benchmarks |
| **Reasoning Models (o1/o3)** | Test-time compute; RLVR-trained; internal thinking tokens | RLHF optimises preference; RLVR optimises correctness | Reasoning is trained in, not prompted in |
| **Multimodal LLMs** | Process text + images via vision encoder + projection layer | Real-world info is charts, docs, screenshots — not just text | Know ViT patch encoding; page-as-image RAG pattern |
| **Memorization & Privacy** | LLMs can reproduce verbatim training data including PII | GDPR liability; security risk; enterprise compliance | DP-SGD with Opacus; avoid fine-tuning on user data |
| **GDPR / EU AI Act** | Legal requirements for data handling and high-risk AI | Fines up to 4% global revenue; right to erasure is hard for fine-tuned models | Know Art. 17; recommend RAG over fine-tuning |
| **AI System Design** | End-to-end product architecture: RAG + cache + auth + eval + monitoring | Demo ≠ production; scale, cost, security, compliance must all be considered | Always address: access control, cost at scale, graceful degradation, eval strategy |

---

*Part 3 of 3  |  2025–2026*
*Read alongside Part 1 (LangChain, LangGraph, Tool Calling, MCP, Vector DBs, RAG, Pinecone) and Part 2 (LLM Fundamentals, Prompt Engineering, Agents, Observability, Fine-tuning, Streaming, Security, Deployment)*
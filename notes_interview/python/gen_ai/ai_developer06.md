# 🤖 AI Developer Interview Notes — Part 6
### DSPy · Guardrails AI · LlamaIndex · TGI · ONNX · Ray Serve · Shadow Testing
### Synthetic Data · ORPO · Unsloth · Axolotl · Chaos Engineering · Triton
### Junior (🟢) → Senior (🔴)

> **Final part of the series. Covers:**
> DSPy (automated prompt optimization) · Guardrails AI · LlamaIndex (full alternative to LangChain) ·
> Text Generation Inference (TGI) · ONNX Runtime · Ray Serve · Shadow Testing/Shadow Mode ·
> Synthetic Data Generation · ORPO Fine-tuning · Unsloth · Axolotl · Chaos Engineering ·
> Triton Inference Server · Load Shedding
>
> **Format:** What | Why | How | Benefits | Key Terms | Code Examples | Interview Tips

---

## 📋 Table of Contents

### SECTION A — Frameworks & Tools
1. [DSPy — Automated Prompt Optimization](#1-dspy--automated-prompt-optimization)
2. [Guardrails AI](#2-guardrails-ai)
3. [LlamaIndex — Full Deep Dive](#3-llamaindex--full-deep-dive)

### SECTION B — Inference & Serving Infrastructure
4. [Text Generation Inference (TGI)](#4-text-generation-inference-tgi)
5. [ONNX Runtime for LLM Inference](#5-onnx-runtime-for-llm-inference)
6. [Ray Serve for LLMs](#6-ray-serve-for-llms)
7. [Triton Inference Server](#7-triton-inference-server)

### SECTION C — Production Reliability
8. [Shadow Testing / Shadow Mode](#8-shadow-testing--shadow-mode)
9. [Load Shedding](#9-load-shedding)
10. [Chaos Engineering for AI Systems](#10-chaos-engineering-for-ai-systems)

### SECTION D — Fine-tuning Ecosystem
11. [Synthetic Data Generation](#11-synthetic-data-generation)
12. [ORPO — Odds Ratio Preference Optimization](#12-orpo--odds-ratio-preference-optimization)
13. [Unsloth — Fast Fine-tuning](#13-unsloth--fast-fine-tuning)
14. [Axolotl — Production Fine-tuning Framework](#14-axolotl--production-fine-tuning-framework)

### SECTION E — Master Summary
15. [Complete Job Readiness Checklist](#15-complete-job-readiness-checklist)

---

# SECTION A — Frameworks & Tools

---

## 1. DSPy — Automated Prompt Optimization

---

### 🔷 CONCEPT OVERVIEW

| Level | Definition |
|-------|-----------|
| 🟢 Junior | Writing the perfect prompt by hand is like tuning a radio by ear — tedious and imprecise. DSPy is a framework that automatically optimizes prompts and few-shot examples by treating prompt engineering like a machine learning problem: define what "good" looks like, give DSPy some examples, and it finds the best prompts automatically. |
| 🔴 Senior | DSPy (Declarative Self-improving Python, Stanford 2023) is a programming model that replaces hand-crafted prompts with declarative Signatures and Modules. A Teleprompter (optimizer) automatically tunes the prompts and few-shot demonstrations by minimizing a metric over a development set using approaches like BootstrapFewShot, MIPRO, and BayesianSignatureOptimizer. This separates program logic from prompt details, making pipelines robust to model and task changes without manual re-prompting. |

---

### 1.1 Core DSPy Concepts

```
DSPy Mental Model:

Traditional:  prompt = "Given {context}, answer {question}. Think step by step..."
              (manual string, brittle, model-specific)

DSPy:         class QA(dspy.Signature):
                  "Answer questions given context."
                  context:  dspy.InputField()
                  question: dspy.InputField()
                  answer:   dspy.OutputField()
              (declarative, auto-optimized, model-agnostic)

The Teleprompter finds the best prompt/examples automatically
by running your pipeline on training data and optimizing a metric.
```

---

### 1.2 DSPy Signatures and Modules

```python
# pip install dspy-ai
import dspy
from dspy.teleprompt import BootstrapFewShot, MIPRO
from dspy.evaluate import Evaluate

# ── Configure the LLM ──
lm = dspy.LM("openai/gpt-4o", api_key="...")
dspy.configure(lm=lm)

# ─────────────────────────────────────────────────
# Step 1: Define Signatures (input/output contracts)
# ─────────────────────────────────────────────────
class ClaimClassification(dspy.Signature):
    """Classify an insurance claim into the correct category."""
    claim_description: str = dspy.InputField(desc="The customer's claim description")
    policy_type:       str = dspy.InputField(desc="Customer's policy type: auto/home/life")
    claim_category: str  = dspy.OutputField(desc="One of: water_damage, fire, theft, accident, liability, other")
    confidence:     float = dspy.OutputField(desc="Confidence score 0.0-1.0")


class RAGSignature(dspy.Signature):
    """Answer insurance questions using retrieved policy documents."""
    context:  list[str] = dspy.InputField(desc="Retrieved policy document chunks")
    question: str       = dspy.InputField(desc="Customer question")
    answer:   str       = dspy.OutputField(desc="Accurate answer based only on context")
    citations: list[str] = dspy.OutputField(desc="Specific policy sections cited")


# ─────────────────────────────────────────────────
# Step 2: Build Modules (composable building blocks)
# ─────────────────────────────────────────────────
class InsuranceQAModule(dspy.Module):
    """Full RAG pipeline as a DSPy module."""

    def __init__(self, retriever):
        super().__init__()
        self.retriever  = retriever
        # Predict: basic chain-of-thought generation
        self.generate   = dspy.ChainOfThought(RAGSignature)

    def forward(self, question: str) -> dspy.Prediction:
        # Retrieve relevant documents
        context = self.retriever(question).passages

        # Generate answer using the signature
        prediction = self.generate(
            context=context,
            question=question
        )
        return prediction


class MultiHopInsuranceQA(dspy.Module):
    """Multi-hop QA: decompose complex questions into sub-questions."""

    def __init__(self, retriever, num_hops: int = 2):
        super().__init__()
        self.retriever  = retriever
        self.num_hops   = num_hops
        # Generate sub-questions
        self.decompose  = dspy.ChainOfThought("question -> sub_question")
        # Answer each sub-question
        self.sub_answer = dspy.ChainOfThought(RAGSignature)
        # Synthesize final answer
        self.synthesize = dspy.ChainOfThought("question, sub_answers -> final_answer")

    def forward(self, question: str) -> dspy.Prediction:
        sub_answers = []

        for hop in range(self.num_hops):
            # Decompose into sub-question
            sub_q   = self.decompose(question=question).sub_question
            context = self.retriever(sub_q).passages

            # Answer sub-question
            sub_ans = self.sub_answer(context=context, question=sub_q)
            sub_answers.append(f"Q: {sub_q}\nA: {sub_ans.answer}")

        # Synthesize
        final = self.synthesize(
            question=question,
            sub_answers="\n\n".join(sub_answers)
        )
        return final


# ─────────────────────────────────────────────────
# Step 3: Define Evaluation Metric
# ─────────────────────────────────────────────────
def answer_correctness_metric(example, prediction, trace=None) -> float:
    """
    Metric function: returns float 0-1.
    DSPy optimizes to maximize this metric.
    """
    # Use LLM-as-judge for open-ended QA
    judge = dspy.ChainOfThought("question, gold_answer, predicted_answer -> score: float")
    result = judge(
        question=example.question,
        gold_answer=example.answer,
        predicted_answer=prediction.answer
    )
    return float(result.score)


def exact_match_metric(example, prediction, trace=None) -> bool:
    """Simple exact match for classification tasks."""
    return example.claim_category.lower() == prediction.claim_category.lower()


# ─────────────────────────────────────────────────
# Step 4: Prepare Training Data
# ─────────────────────────────────────────────────
trainset = [
    dspy.Example(
        question="What is the deductible for water damage?",
        answer="The standard deductible for water damage is €500."
    ).with_inputs("question"),
    dspy.Example(
        question="How do I file a theft claim?",
        answer="File online at the claims portal or call 1-800-IAG within 30 days."
    ).with_inputs("question"),
    # ... more examples
]

devset = [...]  # Held-out evaluation set


# ─────────────────────────────────────────────────
# Step 5: Optimize with Teleprompter
# ─────────────────────────────────────────────────
from dspy.teleprompt import BootstrapFewShot

# BootstrapFewShot: generates few-shot examples by running pipeline on trainset
# then filtering for examples where the pipeline was correct
teleprompter = BootstrapFewShot(
    metric=answer_correctness_metric,
    max_bootstrapped_demos=4,      # Max few-shot examples to add per module
    max_labeled_demos=16,          # Max labeled examples to consider
    max_rounds=1,                  # Optimization rounds
)

# Build the module
retriever  = dspy.ColBERTv2(url="http://localhost:8893/api/search")
qa_program = InsuranceQAModule(retriever)

# Compile: this is where the magic happens
# DSPy automatically finds the best few-shot examples and prompt instructions
optimized_program = teleprompter.compile(
    qa_program,
    trainset=trainset,
)

# Evaluate optimized vs baseline
evaluator = Evaluate(devset=devset, metric=answer_correctness_metric, num_threads=4)

baseline_score  = evaluator(qa_program)
optimized_score = evaluator(optimized_program)

print(f"Baseline:  {baseline_score:.2f}")
print(f"Optimized: {optimized_score:.2f}")
print(f"Improvement: +{optimized_score - baseline_score:.2f}")

# Save and load optimized program
optimized_program.save("insurance_qa_optimized.json")
loaded_program = InsuranceQAModule(retriever)
loaded_program.load("insurance_qa_optimized.json")


# ─────────────────────────────────────────────────
# Advanced: MIPRO — more powerful optimizer
# ─────────────────────────────────────────────────
from dspy.teleprompt import MIPROv2

mipro = MIPROv2(
    metric=answer_correctness_metric,
    auto="medium",     # "light" | "medium" | "heavy"
    # auto="heavy" tries many more configurations — better results, slower
)

heavily_optimized = mipro.compile(
    qa_program,
    trainset=trainset,
    max_bootstrapped_demos=4,
    max_labeled_demos=16,
    requires_permission_to_run=False,
)
```

---

### 1.3 DSPy vs Manual Prompt Engineering

```
Manual Prompt Engineering:
  ✅ Full control over exact wording
  ❌ Brittle: changing the model requires re-prompting
  ❌ Not reproducible: different engineers write differently
  ❌ Doesn't scale: 50 modules = 50 prompts to maintain
  ❌ No principled way to know if prompt is optimal

DSPy:
  ✅ Automatically optimized prompts for your data and model
  ✅ Model-agnostic: swap GPT-4o → Claude, re-optimize automatically
  ✅ Reproducible: program logic is separate from prompt details
  ✅ Measurable: optimization directly maximizes your metric
  ❌ Requires labeled training examples (50-200 ideally)
  ❌ Optimization takes time and API calls
  ❌ Less readable than hand-crafted prompts

When to use DSPy:
  ✅ Complex multi-step pipelines (RAG + classification + generation)
  ✅ When you need to switch between models frequently
  ✅ When you have labeled data and want to maximize performance
  ✅ Research / prototyping where you're exploring architectures
  
When NOT to use DSPy:
  ❌ Simple single-step tasks (just use a good prompt directly)
  ❌ No labeled data available
  ❌ Need very fine-grained control over output format
```

### 💡 Interview Tips — DSPy
- **Core pitch**: "DSPy treats prompt engineering as a machine learning problem — define a metric, provide examples, and the optimizer finds the best prompt automatically."
- The key innovation: **separation of program logic from prompts** — you write the pipeline structure in Python, DSPy handles what the prompts actually say.
- Know the **three optimizer tiers**: BootstrapFewShot (simple, fast), MIPRO (powerful, slower), BayesianSignatureOptimizer (research-grade).
- Senior: DSPy is especially powerful for **multi-hop reasoning pipelines** where manual prompt chains become very complex to optimize. When you have 5+ connected modules, DSPy's joint optimization beats optimizing each module independently.

---

## 2. Guardrails AI

---

### 🔷 CONCEPT OVERVIEW

| Level | Definition |
|-------|-----------|
| 🟢 Junior | Guardrails AI is a library that acts as a safety wrapper around LLM calls. You define rules — "responses must be valid JSON", "no competitor mentions", "no PII in output" — and Guardrails automatically checks every LLM response against these rules, retrying if they're violated. |
| 🔴 Senior | Guardrails AI is a validation framework that wraps LLM inference with declarative input/output validation using a library of pre-built validators (toxic language, PII detection, SQL injection, schema validation, semantic similarity) and a retry/fix loop. When validation fails, it can trigger automatic LLM-based correction (LLM fix) or raise an exception. It separates validation logic from application code, enabling reusable safety constraints across multiple LLM endpoints. |

---

### 2.1 Core Guardrails Concepts

```python
# pip install guardrails-ai
# guardrails hub install hub://guardrails/regex_match
# guardrails hub install hub://guardrails/toxic_language
# guardrails hub install hub://guardrails/detect_pii

import guardrails as gd
from guardrails.hub import ToxicLanguage, DetectPII, ValidJson, RegexMatch
from pydantic import BaseModel, Field
from typing import Optional

# ─────────────────────────────────────────────────
# Basic usage: validate LLM output against a schema
# ─────────────────────────────────────────────────
class ClaimResponse(BaseModel):
    """Structured claim response with validation."""
    decision:        str   = Field(description="approve or deny")
    amount:          float = Field(ge=0, le=100000, description="Claim amount in EUR")
    reason:          str   = Field(min_length=10, max_length=500)
    next_steps:      list[str]
    case_number:     str   = Field(pattern=r"^CASE-\d{6}$")

# Create guard with schema validation
guard = gd.Guard.from_pydantic(ClaimResponse)

# Call LLM with guardrails wrapping
from openai import OpenAI
client = OpenAI()

result = guard(
    client.chat.completions.create,
    prompt="Process this claim: Water damage of €3,500 for policy AIA-2847.",
    model="gpt-4o",
    max_tokens=500,
    # On validation failure: retry up to 3 times with error feedback to model
    num_reasks=3,
)

# result.validated_output is a validated ClaimResponse object
print(result.validated_output.decision)  # "approve"
print(result.validated_output.amount)    # 3500.0


# ─────────────────────────────────────────────────
# Multiple validators with on_fail actions
# ─────────────────────────────────────────────────
from guardrails import Guard, OnFailAction
from guardrails.hub import ToxicLanguage, DetectPII, CompetitorCheck

# Build guard with multiple validators
guard = (
    Guard()
    .use(ToxicLanguage(
        threshold=0.5,
        on_fail=OnFailAction.EXCEPTION  # Raise exception on toxic output
    ))
    .use(DetectPII(
        pii_entities=["EMAIL_ADDRESS", "PHONE_NUMBER", "SSN", "CREDIT_CARD"],
        on_fail=OnFailAction.FIX        # Auto-redact PII from output
    ))
    .use(RegexMatch(
        regex=r"^(?!.*competitor_name).*$",  # No competitor mentions
        on_fail=OnFailAction.REASK          # Ask LLM to regenerate
    ))
)

# Use the guard
validated_response, metadata = guard.parse(
    llm_output=raw_llm_response,
    metadata={"user_id": "user_123"}
)

# Check what validators fired
for log in guard.history[-1].iterations:
    for validation in log.validator_logs:
        if not validation.validation_passed:
            print(f"Failed: {validation.validator_name} — {validation.failure_reason}")


# ─────────────────────────────────────────────────
# Custom validator
# ─────────────────────────────────────────────────
from guardrails.validators import Validator, register_validator, ValidationResult, PassResult, FailResult

@register_validator(name="insurance/no-legal-advice", data_type="string")
class NoLegalAdvice(Validator):
    """Ensure the response doesn't give specific legal advice."""

    LEGAL_ADVICE_PHRASES = [
        "you should sue",
        "file a lawsuit",
        "legal action",
        "you are entitled to",
        "the law requires",
        "your legal rights",
    ]

    def validate(self, value: str, metadata: dict) -> ValidationResult:
        value_lower = value.lower()
        for phrase in self.LEGAL_ADVICE_PHRASES:
            if phrase in value_lower:
                return FailResult(
                    error_message=f"Response contains legal advice: '{phrase}'",
                    fix_value=value.replace(phrase, "[consult a legal professional]")
                )
        return PassResult()


# ─────────────────────────────────────────────────
# Input validation (before LLM call)
# ─────────────────────────────────────────────────
from guardrails.hub import DetectPromptInjection, RestrictToTopic

input_guard = (
    Guard()
    .use(DetectPromptInjection(
        on_fail=OnFailAction.EXCEPTION
    ))
    .use(RestrictToTopic(
        valid_topics=["insurance", "claims", "policies", "coverage"],
        invalid_topics=["politics", "medical_advice", "financial_investments"],
        on_fail=OnFailAction.EXCEPTION
    ))
)

def safe_insurance_chat(user_message: str) -> str:
    """Chat with input AND output guardrails."""
    # Validate input
    try:
        validated_input, _ = input_guard.parse(user_message)
    except gd.errors.ValidationError as e:
        return "I can only help with insurance-related questions."

    # Call LLM
    raw_response = call_llm(validated_input)

    # Validate output
    try:
        validated_output, _ = guard.parse(raw_response)
        return validated_output
    except gd.errors.ValidationError as e:
        return "I'm unable to provide that information. Please contact our support team."


# ─────────────────────────────────────────────────
# Async support for production
# ─────────────────────────────────────────────────
import asyncio

async def async_guarded_call(prompt: str) -> str:
    result = await guard.async_parse(
        llm_api=client.chat.completions.create,
        prompt=prompt,
        model="gpt-4o",
        max_tokens=500,
    )
    return result.validated_output
```

---

### 2.2 Guardrails vs Alternatives

| Feature | Guardrails AI | Custom Validation | Instructor | LangChain Output Parsers |
|---------|--------------|------------------|-----------|------------------------|
| Pre-built validators | 50+ (hub) | None | None | Few |
| Retry loop | ✅ Auto | Manual | ✅ Auto | Manual |
| Input validation | ✅ | Custom | ❌ | ❌ |
| PII detection | ✅ Hub | Custom | ❌ | ❌ |
| Toxicity detection | ✅ Hub | Custom | ❌ | ❌ |
| Schema validation | ✅ Pydantic | Pydantic | ✅ Pydantic | Partial |
| Fix actions | ✅ LLM fix | Manual | Retry only | Manual |
| Async | ✅ | Custom | ✅ | ✅ |
| Best for | Safety-critical apps | Full control | Structured output | LangChain pipelines |

### 💡 Interview Tips — Guardrails AI
- **Key pitch**: "Guardrails separates validation logic from application code — define your safety rules once, reuse across every LLM endpoint."
- Know the **three on_fail actions**: EXCEPTION (stop and raise), FIX (auto-correct the output), REASK (send failure back to LLM with correction instructions).
- For insurance: mention **DetectPII** (never return customer SSNs) and **NoLegalAdvice** (custom validator) as immediate must-haves.
- Senior: compare to Instructor — "Instructor is better for structured data extraction; Guardrails is better for safety validation with diverse validators and fix actions."

---

## 3. LlamaIndex — Full Deep Dive

---

### 🔷 CONCEPT OVERVIEW

| Level | Definition |
|-------|-----------|
| 🟢 Junior | LlamaIndex is an alternative to LangChain for building RAG systems. It specializes in connecting LLMs to your data — documents, databases, APIs — and has very powerful built-in tools for indexing, querying, and reasoning over data. |
| 🔴 Senior | LlamaIndex (formerly GPT Index) is a data framework for building LLM applications over enterprise data. Its core abstractions — Nodes, Indices, Query Engines, and Agent Tools — are optimized for document ingestion and retrieval. It provides more opinionated and feature-rich RAG primitives than LangChain (e.g., SubQuestionQueryEngine, RouterQueryEngine, KnowledgeGraphIndex) at the cost of less flexibility in non-RAG pipelines. |

---

### 3.1 LlamaIndex Core Concepts vs LangChain

```
LangChain Mental Model:          LlamaIndex Mental Model:
  Chain → sequential steps         Index → data structure over docs
  Agent → tool-using loop          Query Engine → smart retriever + synthesizer
  Memory → conversation state      Node Postprocessors → rerank/filter/transform
  Retriever → vector search        SubQuestionQueryEngine → decompose complex queries
  Document → text + metadata       NodeWithScore → retrieved node + relevance score
```

---

### 3.2 Complete LlamaIndex RAG Pipeline

```python
# pip install llama-index llama-index-llms-openai llama-index-embeddings-openai
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    Settings,
    QueryBundle,
)
from llama_index.core.node_parser import (
    SentenceWindowNodeParser,
    HierarchicalNodeParser,
    SemanticSplitterNodeParser,
)
from llama_index.core.postprocessor import (
    MetadataReplacementPostProcessor,
    SentenceTransformerRerank,
    LLMRerank,
)
from llama_index.core.query_engine import (
    SubQuestionQueryEngine,
    RouterQueryEngine,
)
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# ── Global settings ──
Settings.llm       = OpenAI(model="gpt-4o",       temperature=0.0)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")


# ─────────────────────────────────────────────────
# 1. Document Loading
# ─────────────────────────────────────────────────
from llama_index.core import SimpleDirectoryReader
from llama_index.readers.web import SimpleWebPageReader
from llama_index.readers.database import DatabaseReader

# Load from directory (auto-detects PDF, DOCX, TXT, etc.)
documents = SimpleDirectoryReader(
    input_dir="./insurance_docs",
    recursive=True,
    filename_as_id=True,              # Use filename as document ID
    required_exts=[".pdf", ".docx"],  # Only specific extensions
).load_data()

# Load from web
web_docs = SimpleWebPageReader(html_to_text=True).load_data(
    urls=["https://docs.iac-france.fr/policy-terms"]
)


# ─────────────────────────────────────────────────
# 2. Sentence Window Parsing (built-in!)
# ─────────────────────────────────────────────────
# LlamaIndex has SentenceWindowNodeParser built-in
node_parser = SentenceWindowNodeParser.from_defaults(
    window_size=3,            # ±3 sentences context window
    window_metadata_key="window",
    original_text_metadata_key="original_text",
)

nodes = node_parser.get_nodes_from_documents(documents)

# Build index
index = VectorStoreIndex(nodes)

# Query engine with metadata replacement (returns window, not just sentence)
query_engine = index.as_query_engine(
    similarity_top_k=6,
    node_postprocessors=[
        MetadataReplacementPostProcessor(target_metadata_key="window")
        # This replaces the retrieved sentence with its full window context
    ]
)

response = query_engine.query("What documents are needed for a water damage claim?")
print(response)


# ─────────────────────────────────────────────────
# 3. Hierarchical Node Parser (Parent Document Retriever equivalent)
# ─────────────────────────────────────────────────
hierarchical_parser = HierarchicalNodeParser.from_defaults(
    chunk_sizes=[2048, 512, 128]  # Three levels: large → medium → small
    # Retrieval uses small nodes, context uses parent nodes
)

all_nodes = hierarchical_parser.get_nodes_from_documents(documents)

# Use AutoMergingRetriever to merge child nodes back to parents
from llama_index.core.retrievers import AutoMergingRetriever
from llama_index.core.storage.docstore import SimpleDocumentStore

docstore = SimpleDocumentStore()
docstore.add_documents(all_nodes)

storage_context = StorageContext.from_defaults(docstore=docstore)
automerge_index  = VectorStoreIndex(
    all_nodes,
    storage_context=storage_context
)

base_retriever  = automerge_index.as_retriever(similarity_top_k=12)
auto_retriever  = AutoMergingRetriever(
    base_retriever,
    storage_context=storage_context,
    verbose=True,
    simple_ratio_thresh=0.5,  # Merge if >50% of parent's children are retrieved
)


# ─────────────────────────────────────────────────
# 4. Reranking (built-in)
# ─────────────────────────────────────────────────
reranker = SentenceTransformerRerank(
    model="cross-encoder/ms-marco-MiniLM-L-6-v2",
    top_n=3
)

query_engine_with_reranking = index.as_query_engine(
    similarity_top_k=10,   # Retrieve 10 → rerank → return top 3
    node_postprocessors=[reranker]
)


# ─────────────────────────────────────────────────
# 5. SubQuestionQueryEngine — decompose complex questions
# ─────────────────────────────────────────────────
from llama_index.core.tools import QueryEngineTool

# Create specialized query engines for different document types
policy_engine = VectorStoreIndex.from_documents(policy_docs).as_query_engine()
claims_engine = VectorStoreIndex.from_documents(claims_docs).as_query_engine()
rates_engine  = VectorStoreIndex.from_documents(rates_docs).as_query_engine()

# Wrap as tools with descriptions
query_engine_tools = [
    QueryEngineTool.from_defaults(
        query_engine=policy_engine,
        name="policy_qa",
        description="Answers questions about insurance policy terms and coverage details"
    ),
    QueryEngineTool.from_defaults(
        query_engine=claims_engine,
        name="claims_qa",
        description="Answers questions about claim procedures, requirements, and status"
    ),
    QueryEngineTool.from_defaults(
        query_engine=rates_engine,
        name="rates_qa",
        description="Answers questions about premium rates and pricing"
    ),
]

# SubQuestionQueryEngine: decomposes complex question into sub-questions
# routes each to the right tool, then synthesizes a final answer
sub_question_engine = SubQuestionQueryEngine.from_defaults(
    query_engine_tools=query_engine_tools,
    use_async=True,
    verbose=True,
)

# Complex question: automatically decomposed and routed
response = sub_question_engine.query(
    "Compare the deductibles for water damage claims vs theft claims, "
    "and tell me the current premium rate for comprehensive coverage."
)
# Sub-questions generated:
# 1. "What is the deductible for water damage claims?" → claims_qa
# 2. "What is the deductible for theft claims?" → claims_qa
# 3. "What is the premium rate for comprehensive coverage?" → rates_qa
print(response)


# ─────────────────────────────────────────────────
# 6. Router Query Engine — route to right index by topic
# ─────────────────────────────────────────────────
from llama_index.core.selectors import LLMSingleSelector

router_engine = RouterQueryEngine(
    selector=LLMSingleSelector.from_defaults(),
    query_engine_tools=query_engine_tools,
    verbose=True,
)
# Automatically routes "What's the deductible?" → claims_qa
# Routes "What's the premium?" → rates_qa


# ─────────────────────────────────────────────────
# 7. Persist and reload index
# ─────────────────────────────────────────────────
# Save
index.storage_context.persist(persist_dir="./insurance_index")

# Load
from llama_index.core import load_index_from_storage
storage_context = StorageContext.from_defaults(persist_dir="./insurance_index")
loaded_index    = load_index_from_storage(storage_context)
```

---

### 3.3 LlamaIndex Agents

```python
from llama_index.core.agent import ReActAgent, FunctionCallingAgent
from llama_index.core.tools import FunctionTool

# Define tools
def get_policy_details(policy_id: str) -> dict:
    """Get details for a specific insurance policy."""
    return {"policy_id": policy_id, "coverage": "comprehensive", "deductible": 500}

def file_claim(policy_id: str, amount: float, description: str) -> str:
    """File a new insurance claim."""
    return f"Claim filed successfully. Reference: CLAIM-{hash(policy_id)%10000:04d}"

# Create tools
policy_tool = FunctionTool.from_defaults(fn=get_policy_details)
claim_tool  = FunctionTool.from_defaults(fn=file_claim)

# RAG tool from query engine
from llama_index.core.tools import QueryEngineTool
rag_tool = QueryEngineTool.from_defaults(
    query_engine=query_engine,
    name="insurance_knowledge_base",
    description="Search insurance policies, terms, and procedures"
)

# Build agent
agent = ReActAgent.from_tools(
    tools=[policy_tool, claim_tool, rag_tool],
    llm=OpenAI(model="gpt-4o"),
    verbose=True,
    max_iterations=10,
)

response = agent.chat(
    "I need to file a water damage claim for policy AIA-2847. "
    "First check my policy details, then look up what documentation I need, "
    "then file the claim for €3,500."
)
```

---

### 3.4 LangChain vs LlamaIndex: When to Use Which

| Scenario | LangChain | LlamaIndex |
|----------|-----------|-----------|
| Complex multi-step RAG pipelines | ✅ Good | ✅ Better (more RAG primitives) |
| Document-heavy knowledge base | ✅ Good | ✅ Better (optimized for this) |
| Multi-agent orchestration | ✅ LangGraph is best-in-class | ✅ Good but less control |
| Custom chains/non-RAG pipelines | ✅ LCEL is very flexible | ❌ Less suited |
| Streaming | ✅ Strong | ✅ Good |
| Sentence Window Retrieval | Manual | ✅ Built-in |
| Auto-merging (Parent Doc) | Manual | ✅ Built-in |
| Sub-question decomposition | Manual | ✅ Built-in |
| Knowledge graph RAG | Manual | ✅ Built-in |
| Team familiarity | Wider adoption | Growing fast |

### 💡 Interview Tips — LlamaIndex
- Key message: "LlamaIndex has more batteries-included RAG features — Sentence Window, Auto-merging, SubQuestionQueryEngine are all built-in. LangChain is more flexible for non-RAG pipelines."
- **SubQuestionQueryEngine** is the killer feature — automatically decomposes complex multi-part questions and routes them to specialized indexes.
- Know that **both frameworks are converging** — LangChain has adopted many LlamaIndex RAG patterns, and LlamaIndex has added agent capabilities.
- Senior: "In production I've seen teams use **LlamaIndex for the RAG layer** and **LangGraph for the agent orchestration layer** — combining the best of both."

---

# SECTION B — Inference & Serving Infrastructure

---

## 4. Text Generation Inference (TGI)

---

### 🔷 CONCEPT OVERVIEW

| Level | Definition |
|-------|-----------|
| 🟢 Junior | TGI is Hugging Face's tool for running large language models in production. Like vLLM, it makes LLM inference fast and efficient, but it's made by Hugging Face so it works seamlessly with HuggingFace models and has native integration with the HuggingFace ecosystem. |
| 🔴 Senior | TGI (Text Generation Inference) is Hugging Face's production-grade LLM serving toolkit written in Rust + Python. It implements continuous batching, PagedAttention-equivalent memory management, tensor parallelism, quantization (AWQ, GPTQ, BitsAndBytes), speculative decoding, and provides an OpenAI-compatible REST API. TGI is the serving backend behind HuggingFace Inference Endpoints and is widely used in enterprise deployments alongside vLLM. |

---

### 4.1 TGI vs vLLM Comparison

| Feature | TGI (HuggingFace) | vLLM |
|---------|------------------|------|
| **Language** | Rust + Python | Python + CUDA |
| **Ecosystem** | HuggingFace native | OpenAI API compatible |
| **Quantization** | AWQ, GPTQ, BitsAndBytes, EETQ | AWQ, GPTQ, FP8 |
| **Speculative Decoding** | ✅ Medusa, ngram | ✅ Draft models |
| **LoRA serving** | ✅ Multi-LoRA | ✅ Multi-LoRA |
| **Tensor Parallelism** | ✅ | ✅ |
| **Flash Attention** | ✅ | ✅ |
| **Paged Attention** | ✅ (Flash decoding) | ✅ (PagedAttention) |
| **Streaming** | ✅ SSE | ✅ SSE |
| **Model support** | HuggingFace models | HuggingFace + more |
| **Deployment** | Docker, K8s | Docker, K8s |
| **Best for** | HuggingFace ecosystem | OpenAI-compatible drop-in |

---

### 4.2 TGI Deployment

```bash
# Docker deployment (simplest)
docker run --gpus all \
  -p 8080:80 \
  -v $HOME/models:/data \
  ghcr.io/huggingface/text-generation-inference:latest \
  --model-id mistralai/Mistral-7B-Instruct-v0.3 \
  --num-shard 1 \
  --max-input-tokens 4096 \
  --max-total-tokens 8192 \
  --quantize bitsandbytes-nf4 \
  --dtype bfloat16

# Multi-GPU deployment (tensor parallelism across 2 GPUs)
docker run --gpus all \
  -p 8080:80 \
  ghcr.io/huggingface/text-generation-inference:latest \
  --model-id mistralai/Mixtral-8x7B-Instruct-v0.1 \
  --num-shard 2 \          # Shard across 2 GPUs
  --max-batch-prefill-tokens 32000
```

```python
# Python client
from huggingface_hub import InferenceClient

client = InferenceClient(model="http://localhost:8080")

# Text generation
response = client.text_generation(
    "What is comprehensive insurance?",
    max_new_tokens=200,
    temperature=0.7,
    top_p=0.95,
    stream=False,
)
print(response)

# Streaming
for token in client.text_generation(
    "Explain water damage coverage step by step:",
    max_new_tokens=300,
    stream=True,
):
    print(token, end="", flush=True)

# Chat completions (OpenAI-compatible endpoint)
import openai
oa_client = openai.OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="not-needed"
)

chat_response = oa_client.chat.completions.create(
    model="tgi",
    messages=[{"role": "user", "content": "What is the deductible for flood damage?"}],
    max_tokens=200,
)
print(chat_response.choices[0].message.content)


# TGI with Multiple LoRA Adapters (serve many fine-tuned models from one base)
docker_cmd = """
docker run --gpus all -p 8080:80 \
  ghcr.io/huggingface/text-generation-inference:latest \
  --model-id mistralai/Mistral-7B-Instruct-v0.3 \
  --lora-adapters iac-claims-adapter,iac-billing-adapter,iac-support-adapter
"""
# Now switch between LoRA adapters per-request:
response = client.text_generation(
    "Process this claim:",
    adapter_id="iac-claims-adapter",  # Per-request LoRA selection
)
```

---

### 4.3 TGI Production Configuration

```yaml
# tgi-deployment.yaml (Kubernetes)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tgi-llm-server
spec:
  replicas: 2
  template:
    spec:
      containers:
      - name: tgi
        image: ghcr.io/huggingface/text-generation-inference:latest
        args:
          - --model-id=mistralai/Mistral-7B-Instruct-v0.3
          - --num-shard=1
          - --max-input-tokens=4096
          - --max-total-tokens=8192
          - --max-batch-total-tokens=65536   # Max tokens across all concurrent requests
          - --quantize=awq                    # AWQ quantization (best quality)
          - --speculate=4                     # Speculative decoding with 4 candidate tokens
        resources:
          limits:
            nvidia.com/gpu: 1
            memory: "24Gi"
        ports:
          - containerPort: 80
        readinessProbe:
          httpGet:
            path: /health
            port: 80
          initialDelaySeconds: 60    # Model loading takes time
          periodSeconds: 10
```

### 💡 Interview Tips — TGI
- **When to choose TGI vs vLLM**: "TGI when you're already in the HuggingFace ecosystem and want native model hub integration. vLLM when you need OpenAI API compatibility or are using non-HF models."
- Key TGI advantage: **native HuggingFace model hub** — just pass a model ID and TGI downloads, loads, and serves it automatically.
- **Multi-LoRA serving** is a killer feature for organizations with many fine-tuned variants — one base model, many adapters, switched per-request.
- Senior: TGI's Rust core gives it **excellent throughput stability under high load** — Rust's memory safety prevents the garbage collection pauses that can affect Python-based servers.

---

## 5. ONNX Runtime for LLM Inference

---

### 🔷 CONCEPT OVERVIEW

| Level | Definition |
|-------|-----------|
| 🟢 Junior | ONNX is a standard format for saving AI models that can run on many different hardware types — CPUs, GPUs, phones, edge devices. ONNX Runtime is the engine that runs these models. It's perfect when you need to run a smaller LLM on a CPU without a dedicated AI server. |
| 🔴 Senior | ONNX (Open Neural Network Exchange) Runtime provides hardware-accelerated inference across diverse backends (CPU, CUDA, DirectML, CoreML, TensorRT) via a unified API. For LLMs, the ONNX Runtime GenAI extension provides optimized transformer kernels, KV cache management, and beam search/sampling — enabling efficient CPU-only inference of quantized models (INT4, INT8) for edge deployment, on-device inference, and low-cost serving without GPU. |

---

### 5.1 Export and Run LLMs with ONNX

```python
# pip install onnxruntime-genai optimum[onnxruntime]
from optimum.onnxruntime import ORTModelForCausalLM
from transformers import AutoTokenizer
import onnxruntime_genai as og

# ── Export a model to ONNX ──
# Using Optimum (Hugging Face's optimization toolkit)
from optimum.exporters.onnx import main_export

main_export(
    model_name_or_path="microsoft/phi-2",  # Small, fast model good for ONNX
    output="./phi2-onnx",
    task="text-generation",
    optimization_level=99,   # Maximum optimization
    monolith=True,           # Single ONNX file
)

# Export with INT4 quantization (CPU-optimized)
# Command line:
# python -m onnxruntime.tools.quantization.quantize \
#   --input_model phi2-onnx/model.onnx \
#   --output_model phi2-onnx-int4/model.onnx \
#   --quant_format QOperator \
#   --per_channel False \
#   --reduce_range False


# ── Run inference with ONNX Runtime GenAI ──
model     = og.Model("./phi2-onnx-int4")
tokenizer = og.Tokenizer(model)
tokenizer_stream = tokenizer.create_stream()

# Configure generation parameters
params = og.GeneratorParams(model)
params.set_search_options(
    max_length=200,
    temperature=0.7,
    top_p=0.9,
    repetition_penalty=1.1,
)

prompt   = "What is insurance deductible? Explain simply."
input_tokens = tokenizer.encode(prompt)
params.input_ids = input_tokens

# Generate
generator = og.Generator(model, params)

print("Response: ", end="", flush=True)
while not generator.is_done():
    generator.compute_logits()
    generator.generate_next_token()

    new_token = generator.get_next_tokens()[0]
    print(tokenizer_stream.decode(new_token), end="", flush=True)
print()

del generator  # Important: free KV cache memory


# ── Using Optimum ONNX model ──
model     = ORTModelForCausalLM.from_pretrained("./phi2-onnx")
tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2")

inputs = tokenizer("Explain insurance in one sentence:", return_tensors="pt")
output = model.generate(**inputs, max_new_tokens=100)
print(tokenizer.decode(output[0], skip_special_tokens=True))


# ── When ONNX Runtime shines ──
# Scenario 1: On-premise deployment without GPU
# Scenario 2: Edge/embedded systems (factory floor, medical devices)
# Scenario 3: Windows Desktop apps (DirectML backend)
# Scenario 4: Mobile deployment (CoreML for iOS, NNAPI for Android)
# Scenario 5: Very high throughput CPU servers (Phi-3-mini, Gemma 2B)
```

---

### 5.2 ONNX vs Other Serving Options

| Use Case | Recommended Tool |
|----------|----------------|
| GPU server, max throughput | vLLM or TGI |
| CPU server, no GPU | ONNX Runtime or llama.cpp (GGUF) |
| On-device (phone/laptop) | ONNX Runtime GenAI or MLC LLM |
| Windows app | ONNX Runtime (DirectML) |
| Edge IoT device | ONNX Runtime (NNAPI/CoreML) |
| Model portability across frameworks | ONNX format |

### 💡 Interview Tips — ONNX Runtime
- **When it matters**: "ONNX Runtime is the answer when you need to deploy on CPU, edge devices, or Windows desktop — anywhere there's no GPU."
- Know the hardware backends: **CUDA** (NVIDIA GPU), **CoreML** (Apple Silicon), **DirectML** (Windows GPU), **NNAPI** (Android), **CPU** (universal fallback).
- For LLMs, the practical choice is often **ONNX Runtime vs llama.cpp (GGUF)** for CPU inference — GGUF is simpler to use for casual deployment, ONNX Runtime gives more optimization control.
- Senior: ONNX Runtime's **operator fusion** is key — it fuses multiple operations (MatMul + Add + LayerNorm) into a single optimized kernel, giving significant CPU speedups.

---

## 6. Ray Serve for LLMs

---

### 🔷 CONCEPT OVERVIEW

| Level | Definition |
|-------|-----------|
| 🟢 Junior | Ray Serve is a library for deploying machine learning models at scale. It handles the hard parts of serving — auto-scaling, load balancing, batching, and deploying multiple models together — using a Python-native framework that's easy to write but scales to large clusters. |
| 🔴 Senior | Ray Serve is a scalable model serving library built on the Ray distributed computing framework. It provides deployment graphs (composable serving pipelines), autoscaling (CPU/GPU-aware), dynamic request batching, multi-replica serving, and actor-based state management — enabling complex ML serving pipelines (preprocessing → inference → postprocessing) that scale horizontally across multiple nodes. |

---

### 6.1 Ray Serve LLM Deployment

```python
# pip install ray[serve] vllm
import ray
from ray import serve
from ray.serve.llm import LLMConfig, LLMServer, LLMRouter
from vllm import AsyncLLMEngine, SamplingParams
from vllm.engine.arg_utils import AsyncEngineArgs

ray.init()

# ── Simple LLM deployment ──
@serve.deployment(
    num_replicas=2,                     # 2 replicas for redundancy
    ray_actor_options={"num_gpus": 1},  # 1 GPU per replica
    autoscaling_config={
        "min_replicas":         1,
        "max_replicas":         4,
        "target_num_ongoing_requests_per_replica": 5,
    }
)
class LLMDeployment:
    def __init__(self):
        engine_args = AsyncEngineArgs(
            model="mistralai/Mistral-7B-Instruct-v0.3",
            tensor_parallel_size=1,
            gpu_memory_utilization=0.90,
            max_model_len=8192,
        )
        self.engine = AsyncLLMEngine.from_engine_args(engine_args)

    async def __call__(self, request) -> str:
        data    = await request.json()
        prompt  = data["prompt"]
        params  = SamplingParams(temperature=0.7, max_tokens=200)

        async for output in self.engine.generate(prompt, params, request_id=str(id(request))):
            if output.finished:
                return output.outputs[0].text

        return ""


# Deploy
llm_app = LLMDeployment.bind()
serve.run(llm_app, route_prefix="/llm")


# ── Multi-model pipeline ──
@serve.deployment
class Preprocessor:
    def preprocess(self, text: str) -> str:
        return text.strip().lower()[:2000]

@serve.deployment(ray_actor_options={"num_gpus": 1})
class ClassifierModel:
    def __init__(self):
        from transformers import pipeline
        self.classifier = pipeline("text-classification", model="distilbert-base-uncased")

    def classify(self, text: str) -> str:
        result = self.classifier(text)[0]
        return result["label"]

@serve.deployment(ray_actor_options={"num_gpus": 1})
class LLMModel:
    async def generate(self, text: str, intent: str) -> str:
        # Use intent to route to different prompts
        prompt = f"[{intent}] {text}"
        return await self._generate_async(prompt)

@serve.deployment
class InsurancePipeline:
    def __init__(self, preprocessor, classifier, llm):
        self.preprocessor = preprocessor
        self.classifier   = classifier
        self.llm          = llm

    async def __call__(self, request) -> dict:
        data    = await request.json()
        message = data["message"]

        # Pipeline: preprocess → classify → generate
        clean_msg = await self.preprocessor.preprocess.remote(message)
        intent    = await self.classifier.classify.remote(clean_msg)
        response  = await self.llm.generate.remote(clean_msg, intent)

        return {"response": response, "intent": intent}

# Wire together as deployment graph
preprocessor_handle = Preprocessor.bind()
classifier_handle   = ClassifierModel.bind()
llm_handle          = LLMModel.bind()
pipeline            = InsurancePipeline.bind(
    preprocessor_handle,
    classifier_handle,
    llm_handle
)

serve.run(pipeline, route_prefix="/insurance")


# ── Built-in LLM features (Ray 2.7+) ──
from ray.serve.llm import LLMConfig, build_openai_app

llm_config = LLMConfig(
    model_loading_config={
        "model_id": "mistralai/Mistral-7B-Instruct-v0.3",
    },
    accelerator_type="A10G",
    deployment_config={
        "autoscaling_config": {
            "min_replicas": 1,
            "max_replicas": 4,
            "target_ongoing_requests": 10,
        }
    }
)

# Creates an OpenAI-compatible endpoint automatically
app = build_openai_app({"mistral-7b": llm_config})
serve.run(app)
```

### 💡 Interview Tips — Ray Serve
- **When Ray Serve over vLLM**: "Ray Serve is for **complex serving pipelines** — preprocessing + routing + multiple models + postprocessing. vLLM is better for single-model high-throughput serving."
- Key strength: **deployment graphs** — you can define complex DAGs of model calls that Ray handles with automatic distribution and fault tolerance.
- Know that **Ray Serve uses vLLM internally** for LLM inference in its modern versions — they're complementary, not competing.
- Senior: Ray Serve's **autoscaling** is GPU-aware — it can scale up replicas when GPU utilization is high and scale down when idle, unlike simple CPU-based autoscalers.

---

## 7. Triton Inference Server

---

### 🔷 CONCEPT OVERVIEW

| Level | Definition |
|-------|-----------|
| 🟢 Junior | Triton is NVIDIA's tool for running AI models on GPUs in production. It's like a professional-grade GPU model server — very fast, supports many model formats, and handles batching automatically. |
| 🔴 Senior | NVIDIA Triton Inference Server is a production-grade model serving system supporting multiple backends (TensorRT, ONNX Runtime, PyTorch TorchScript, TensorFlow, Python). It provides dynamic batching, concurrent model execution, model ensembles, model versioning, and gRPC/HTTP endpoints. For LLMs, Triton is typically used with TensorRT-LLM backend for maximum GPU throughput — often 5-10x faster than naive PyTorch inference. |

---

### 7.1 Triton + TensorRT-LLM

```python
# TensorRT-LLM: converts HuggingFace model to optimized TensorRT engine
# Then serves via Triton

# Step 1: Convert to TensorRT-LLM (command line)
# python convert_checkpoint.py \
#   --model_dir ./llama-3-8b \
#   --output_dir ./llama-3-8b-trt \
#   --dtype float16 \
#   --tp_size 1         # Tensor parallelism across 1 GPU

# Step 2: Build TensorRT engine
# trtllm-build \
#   --checkpoint_dir ./llama-3-8b-trt \
#   --output_dir ./llama-3-8b-engine \
#   --gemm_plugin float16 \
#   --max_batch_size 32 \
#   --max_input_len 2048 \
#   --max_output_len 512

# Step 3: Deploy with Triton
# tritonserver --model-repository ./triton-model-repo \
#   --backend-config=tensorrtllm,executor_worker_path=/opt/tritonserver/backends/tensorrtllm/trtllmExecutorWorker

# Python client
import tritonclient.grpc as grpcclient
import numpy as np

client = grpcclient.InferenceServerClient(url="localhost:8001")

def triton_generate(prompt: str, max_tokens: int = 200) -> str:
    # Prepare inputs
    input_text   = np.array([[prompt]], dtype=object)
    max_tokens_v = np.array([[max_tokens]], dtype=np.int32)
    bad_words    = np.array([[""]], dtype=object)
    stop_words   = np.array([[""]], dtype=object)

    inputs = [
        grpcclient.InferInput("INPUT_0",  input_text.shape,   "BYTES"),
        grpcclient.InferInput("INPUT_1",  max_tokens_v.shape, "INT32"),
        grpcclient.InferInput("INPUT_2",  bad_words.shape,    "BYTES"),
        grpcclient.InferInput("INPUT_3",  stop_words.shape,   "BYTES"),
    ]
    inputs[0].set_data_from_numpy(input_text)
    inputs[1].set_data_from_numpy(max_tokens_v)
    inputs[2].set_data_from_numpy(bad_words)
    inputs[3].set_data_from_numpy(stop_words)

    outputs = [grpcclient.InferRequestedOutput("OUTPUT_0")]

    response = client.infer(
        model_name="ensemble",
        inputs=inputs,
        outputs=outputs
    )
    return response.as_numpy("OUTPUT_0")[0].decode()


# Performance comparison (Llama 3 8B, A100 GPU):
# PyTorch eager:        ~800 tokens/sec
# vLLM:               ~2,400 tokens/sec
# TensorRT-LLM/Triton: ~4,800 tokens/sec  ← ~6x vs baseline
```

### 💡 Interview Tips — Triton
- **When to use Triton**: "Triton + TensorRT-LLM for maximum GPU throughput — typically 5-10x faster than vLLM for batch inference. The trade-off is much higher setup complexity."
- Know the **use case**: Triton is for organizations with very high throughput requirements (millions of requests/day) and dedicated ML infrastructure teams. vLLM is easier and good enough for most use cases.
- Mention **model ensemble** feature — Triton can chain a preprocessing model → LLM → postprocessing model as a single logical endpoint.

---

# SECTION C — Production Reliability

---

## 8. Shadow Testing / Shadow Mode

---

### 🔷 CONCEPT OVERVIEW

| Level | Definition |
|-------|-----------|
| 🟢 Junior | Shadow testing means running a new model version on real user requests without actually showing users its responses. You compare the new model's answers to the old model's answers in the background, checking for quality differences, before deciding to switch users to the new version. |
| 🔴 Senior | Shadow mode (also called shadow deployment or shadow testing) routes production traffic to both the current (live) model and the new (shadow) model simultaneously. Only the live model's response is returned to users. The shadow model's response is captured, compared to the live response, and evaluated against quality metrics asynchronously. This allows risk-free evaluation of new models on real production traffic distribution before committing to a full rollout. |

---

### 8.1 Shadow Testing Implementation

```python
import asyncio
import time
import uuid
from dataclasses import dataclass, field
from openai import AsyncOpenAI
from typing import Callable, Optional

@dataclass
class ShadowComparison:
    request_id:         str
    user_message:       str
    live_response:      str
    shadow_response:    str
    live_latency_ms:    float
    shadow_latency_ms:  float
    live_model:         str
    shadow_model:       str
    timestamp:          float = field(default_factory=time.time)


class ShadowTestingRouter:
    """
    Routes requests to both live and shadow model simultaneously.
    Returns live response to user, logs shadow for comparison.
    """

    def __init__(
        self,
        live_model:   str,
        shadow_model: str,
        shadow_rate:  float = 1.0,      # 100% of traffic gets shadow-tested
        comparison_callback: Optional[Callable] = None,
    ):
        self.live_model   = live_model
        self.shadow_model = shadow_model
        self.shadow_rate  = shadow_rate
        self.callback     = comparison_callback
        self.client       = AsyncOpenAI()
        self.comparisons  = []

    async def _call_model(self, model: str, messages: list) -> tuple[str, float]:
        """Call a model and return (response, latency_ms)."""
        start    = time.time()
        response = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.0,
            max_tokens=500,
        )
        latency = (time.time() - start) * 1000
        return response.choices[0].message.content, latency

    async def route(self, messages: list) -> str:
        """
        Send to live model (blocking) and shadow model (non-blocking).
        Returns live response immediately.
        """
        import random
        request_id = str(uuid.uuid4())

        if random.random() > self.shadow_rate:
            # Skip shadow for this request
            response, _ = await self._call_model(self.live_model, messages)
            return response

        # Run both models concurrently
        live_task   = asyncio.create_task(self._call_model(self.live_model,   messages))
        shadow_task = asyncio.create_task(self._call_model(self.shadow_model, messages))

        # Wait for LIVE model (return to user immediately)
        live_response, live_latency = await live_task

        # Log shadow comparison asynchronously (don't block user)
        asyncio.create_task(
            self._record_comparison(
                request_id, messages, live_response, live_latency,
                shadow_task
            )
        )

        return live_response  # ← User gets live response immediately

    async def _record_comparison(
        self,
        request_id:    str,
        messages:      list,
        live_response: str,
        live_latency:  float,
        shadow_task:   asyncio.Task,
    ):
        """Background task: wait for shadow, compare, log."""
        try:
            shadow_response, shadow_latency = await shadow_task
        except Exception as e:
            print(f"Shadow model failed: {e}")
            return

        comparison = ShadowComparison(
            request_id=request_id,
            user_message=messages[-1]["content"] if messages else "",
            live_response=live_response,
            shadow_response=shadow_response,
            live_latency_ms=live_latency,
            shadow_latency_ms=shadow_latency,
            live_model=self.live_model,
            shadow_model=self.shadow_model,
        )

        self.comparisons.append(comparison)

        if self.callback:
            await self.callback(comparison)

    def get_shadow_report(self) -> dict:
        """Generate comparison report from shadow results."""
        if not self.comparisons:
            return {"error": "No shadow comparisons yet"}

        n = len(self.comparisons)

        # Latency comparison
        avg_live_latency   = sum(c.live_latency_ms   for c in self.comparisons) / n
        avg_shadow_latency = sum(c.shadow_latency_ms for c in self.comparisons) / n

        return {
            "total_comparisons":    n,
            "avg_live_latency_ms":  f"{avg_live_latency:.1f}",
            "avg_shadow_latency_ms": f"{avg_shadow_latency:.1f}",
            "latency_regression":   avg_shadow_latency > avg_live_latency * 1.2,
            "sample_comparisons":   [
                {
                    "user": c.user_message[:50],
                    "live": c.live_response[:100],
                    "shadow": c.shadow_response[:100],
                }
                for c in self.comparisons[-5:]
            ]
        }


# ── Automated quality comparison using LLM judge ──
async def compare_responses_with_judge(
    comparison: ShadowComparison,
    judge_client: AsyncOpenAI
) -> dict:
    """Use LLM-as-judge to compare live vs shadow quality."""

    judge_prompt = f"""Compare these two AI responses to the same question.
Question: {comparison.user_message}

Response A (from current model):
{comparison.live_response}

Response B (from new model candidate):
{comparison.shadow_response}

Which is better? Rate each 1-5 on: accuracy, helpfulness, safety.
Output JSON: {{"winner": "A" | "B" | "tie", "A_score": 1-5, "B_score": 1-5, "reasoning": "..."}}"""

    response = await judge_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": judge_prompt}],
        temperature=0,
    )
    import json
    return json.loads(response.choices[0].message.content)


# ── Usage ──
async def main():
    router = ShadowTestingRouter(
        live_model="gpt-4o-mini",        # Current production model
        shadow_model="gpt-4o",           # Candidate for upgrade
        shadow_rate=0.10,                # Test on 10% of traffic
    )

    # Simulate production traffic
    test_messages = [
        [{"role": "user", "content": "What is my deductible for water damage?"}],
        [{"role": "user", "content": "How do I file a theft claim?"}],
        [{"role": "user", "content": "What does comprehensive coverage include?"}],
    ]

    for messages in test_messages:
        response = await router.route(messages)
        print(f"User sees: {response[:80]}...")

    await asyncio.sleep(2)  # Wait for async shadow tasks
    report = router.get_shadow_report()
    print(f"\nShadow Report: {report}")

asyncio.run(main())
```

### 💡 Interview Tips — Shadow Testing
- **The key value**: "Shadow testing is the only way to evaluate a new model on the exact distribution of real production traffic without any user impact."
- Unlike A/B testing, shadow testing has **zero user risk** — all users get the live model's response. Only the comparison is internal.
- Real-world use: **before any model upgrade** (GPT-4o-mini → GPT-4o, prompt change, fine-tune deployment) — run shadow for 24-48 hours, confirm shadow quality ≥ live quality, then switch.
- Senior: mention the **async shadow call** pattern — the shadow model call must not block the user's response. Use asyncio.create_task to fire-and-forget the shadow call.

---

## 9. Load Shedding

---

### 🔷 CONCEPT OVERVIEW

| Level | Definition |
|-------|-----------|
| 🟢 Junior | Load shedding means intentionally refusing some requests when your system is overloaded — like a power grid intentionally cutting power to some neighborhoods to prevent a total blackout. It's better to reject 20% of requests gracefully than to crash entirely under overload. |
| 🔴 Senior | Load shedding is a reliability pattern where a service proactively rejects requests when system load exceeds a threshold, rather than allowing the queue to grow unboundedly and causing cascading failures. For LLM services, this is critical because LLM requests are expensive (GPU-bound), latency-sensitive, and can back up catastrophically. Shedding strategies include token bucket limits, priority queues (premium users not shed), and deadline-based rejection (requests waiting too long are dropped). |

---

### 9.1 Load Shedding Implementation

```python
import asyncio
import time
from collections import deque
from enum import Enum
from dataclasses import dataclass

class UserTier(Enum):
    PREMIUM   = 1   # Never shed
    STANDARD  = 2   # Shed when overloaded
    FREE      = 3   # First to be shed

@dataclass
class Request:
    user_id:    str
    message:    str
    tier:       UserTier
    arrival_time: float = 0.0
    max_wait_ms: float = 5000.0  # Drop request if waiting > 5s


class LLMLoadShedder:
    """
    Multi-strategy load shedder for LLM service.
    Prevents overload cascades by rejecting requests early.
    """

    def __init__(
        self,
        max_concurrent:    int   = 50,    # Max simultaneous LLM calls
        queue_size:        int   = 100,   # Max queued requests
        target_latency_ms: float = 2000,  # Target P95 latency
    ):
        self.max_concurrent    = max_concurrent
        self.queue_size        = queue_size
        self.target_latency_ms = target_latency_ms

        self.current_load      = 0         # Active LLM calls
        self.request_queue     = deque()   # Waiting requests
        self.recent_latencies  = deque(maxlen=100)  # P95 tracking
        self._lock             = asyncio.Lock()

    def _compute_p95_latency(self) -> float:
        if not self.recent_latencies:
            return 0
        sorted_latencies = sorted(self.recent_latencies)
        idx = int(len(sorted_latencies) * 0.95)
        return sorted_latencies[idx]

    def _should_shed(self, request: Request) -> tuple[bool, str]:
        """
        Decide whether to shed this request.
        Priority: Premium > Standard > Free
        """
        p95_latency = self._compute_p95_latency()

        # Always accept premium users (up to hard limit)
        if request.tier == UserTier.PREMIUM:
            if self.current_load >= self.max_concurrent * 1.5:  # 50% overflow for premium
                return True, "System critically overloaded"
            return False, "OK"

        # Check deadline: request too old → shed
        wait_ms = (time.time() - request.arrival_time) * 1000
        if wait_ms > request.max_wait_ms:
            return True, f"Request deadline exceeded ({wait_ms:.0f}ms > {request.max_wait_ms}ms)"

        # Queue full → shed free tier first
        if len(self.request_queue) >= self.queue_size:
            if request.tier == UserTier.FREE:
                return True, "Queue full, free tier request shed"
            if request.tier == UserTier.STANDARD and len(self.request_queue) >= self.queue_size * 0.8:
                return True, "Queue 80% full, standard tier shed"

        # P95 latency too high → shed lower tiers
        if p95_latency > self.target_latency_ms * 1.5:
            if request.tier == UserTier.FREE:
                return True, f"High latency ({p95_latency:.0f}ms), shedding free tier"

        if p95_latency > self.target_latency_ms * 2.0:
            if request.tier in (UserTier.FREE, UserTier.STANDARD):
                return True, f"Critical latency ({p95_latency:.0f}ms), shedding standard tier"

        return False, "OK"

    async def handle_request(self, request: Request) -> str:
        """Process or shed a request."""
        request.arrival_time = time.time()

        async with self._lock:
            should_shed, reason = self._should_shed(request)

        if should_shed:
            # Return 503 with retry guidance
            wait_estimate = self._compute_p95_latency() / 1000
            return f"SERVICE_UNAVAILABLE: {reason}. Retry after {wait_estimate:.1f}s"

        # Accept request
        async with self._lock:
            self.current_load += 1

        try:
            start    = time.time()
            response = await self._call_llm(request.message)
            latency  = (time.time() - start) * 1000
            self.recent_latencies.append(latency)
            return response
        finally:
            async with self._lock:
                self.current_load -= 1

    async def _call_llm(self, message: str) -> str:
        """Actual LLM call (placeholder)."""
        await asyncio.sleep(0.5)  # Simulate 500ms LLM latency
        return f"Response to: {message[:50]}"


# ── HTTP middleware for FastAPI ──
from fastapi import FastAPI, Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

class LoadSheddingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, shedder: LLMLoadShedder):
        super().__init__(app)
        self.shedder = shedder

    async def dispatch(self, request: Request, call_next) -> Response:
        # Check if we should shed this request
        user_tier = self._get_user_tier(request)
        req       = Request_(
            user_id=request.headers.get("x-user-id", "anonymous"),
            message="",  # Not available yet
            tier=user_tier,
            arrival_time=time.time(),
        )

        _, reason = self.shedder._should_shed(req)
        if reason != "OK":
            return Response(
                content=f'{{"error": "Too many requests", "reason": "{reason}"}}',
                status_code=503,
                headers={
                    "Content-Type": "application/json",
                    "Retry-After":  "5",
                    "X-Shed-Reason": reason,
                }
            )

        return await call_next(request)

    def _get_user_tier(self, request: Request) -> UserTier:
        tier = request.headers.get("x-user-tier", "free")
        return {"premium": UserTier.PREMIUM, "standard": UserTier.STANDARD}.get(
            tier, UserTier.FREE
        )
```

### 💡 Interview Tips — Load Shedding
- **Why not just queue everything?** Unbounded queues under overload lead to all users waiting forever — everyone gets a bad experience. Load shedding ensures some users get fast responses.
- The **tiering principle** is key for business: premium/paid users should never be shed. Free tier is first to go. This protects revenue while managing capacity.
- Mention **deadline-based shedding** — if a request has been waiting 5 seconds and the LLM takes 2 more, it's better to reject it now (user already left) than waste GPU time.
- Senior: explain the difference between **load shedding** (proactive rejection at entry) and **circuit breaker** (stopping calls to a downstream service that's failing). They're complementary patterns.

---

## 10. Chaos Engineering for AI Systems

---

### 🔷 CONCEPT OVERVIEW

| Level | Definition |
|-------|-----------|
| 🟢 Junior | Chaos engineering means deliberately breaking parts of your system on purpose — like unplugging a server or making an API slow — to find out how your system behaves before a real failure surprises you in production. |
| 🔴 Senior | Chaos engineering for AI systems extends the Netflix Chaos Monkey principle to LLM pipelines. It involves controlled injection of failures (API timeouts, rate limit errors, vector DB unavailability, model degradation, corrupted inputs) to verify that fallbacks, circuit breakers, and degradation paths work as designed — before real failures expose them in production. |

---

### 10.1 Chaos Tests for LLM Systems

```python
import asyncio
import random
from unittest.mock import patch, AsyncMock
from contextlib import asynccontextmanager
import pytest

class AISystemChaosRunner:
    """Inject failures into AI system components to test resilience."""

    def __init__(self, system_under_test):
        self.system = system_under_test
        self.results = []

    # ── Failure injection scenarios ──

    @asynccontextmanager
    async def llm_api_timeout(self, delay_seconds: float = 35.0):
        """Simulate LLM API timeout (exceeds 30s timeout)."""
        original = self.system.llm_client.chat.completions.create

        async def slow_llm(*args, **kwargs):
            await asyncio.sleep(delay_seconds)
            return await original(*args, **kwargs)

        with patch.object(self.system.llm_client.chat.completions, 'create', slow_llm):
            yield

    @asynccontextmanager
    async def llm_rate_limit(self, fail_rate: float = 0.3):
        """Simulate 30% of LLM calls hitting rate limits."""
        from openai import RateLimitError
        original = self.system.llm_client.chat.completions.create

        async def flaky_llm(*args, **kwargs):
            if random.random() < fail_rate:
                raise RateLimitError(
                    message="Rate limit exceeded",
                    response=None,
                    body={"error": {"type": "rate_limit_error"}}
                )
            return await original(*args, **kwargs)

        with patch.object(self.system.llm_client.chat.completions, 'create', flaky_llm):
            yield

    @asynccontextmanager
    async def vector_db_unavailable(self):
        """Simulate vector DB being completely down."""
        async def failing_search(*args, **kwargs):
            raise ConnectionError("Vector DB connection refused")

        with patch.object(self.system.vectorstore, 'similarity_search', failing_search):
            yield

    @asynccontextmanager
    async def corrupt_llm_output(self, corruption_rate: float = 0.2):
        """Simulate LLM returning malformed/unexpected output."""
        original = self.system.llm_client.chat.completions.create

        async def corrupting_llm(*args, **kwargs):
            response = await original(*args, **kwargs)
            if random.random() < corruption_rate:
                # Return garbage instead of valid response
                response.choices[0].message.content = "}{invalid json{{"
            return response

        with patch.object(self.system.llm_client.chat.completions, 'create', corrupting_llm):
            yield

    async def run_chaos_scenario(self, scenario_name: str, chaos_context, test_queries: list):
        """Run queries under a chaos scenario, record outcomes."""
        results = {"scenario": scenario_name, "successes": 0, "failures": 0, "degraded": 0}

        async with chaos_context:
            for query in test_queries:
                try:
                    start    = asyncio.get_event_loop().time()
                    response = await self.system.process(query)
                    latency  = asyncio.get_event_loop().time() - start

                    if response and len(response) > 10:
                        results["successes"] += 1
                    else:
                        results["degraded"] += 1

                except Exception as e:
                    results["failures"] += 1
                    print(f"  Failure in {scenario_name}: {type(e).__name__}: {e}")

        results["success_rate"] = results["successes"] / len(test_queries)
        self.results.append(results)
        return results

    async def run_full_chaos_suite(self, test_queries: list):
        """Run all chaos scenarios."""
        scenarios = [
            ("LLM API Timeout",      self.llm_api_timeout(delay_seconds=35)),
            ("LLM Rate Limits 30%",  self.llm_rate_limit(fail_rate=0.3)),
            ("Vector DB Down",       self.vector_db_unavailable()),
            ("Corrupt LLM Output",   self.corrupt_llm_output(corruption_rate=0.2)),
        ]

        print("🔥 Running Chaos Engineering Suite")
        print("=" * 50)

        for scenario_name, chaos_ctx in scenarios:
            print(f"\n🐒 Scenario: {scenario_name}")
            results = await self.run_chaos_scenario(scenario_name, chaos_ctx, test_queries)
            print(f"  Success rate: {results['success_rate']:.1%}")
            print(f"  Failures: {results['failures']}/{len(test_queries)}")

            # Assert minimum resilience requirements
            assert results["success_rate"] >= 0.7, \
                f"RESILIENCE FAILURE: {scenario_name} success rate {results['success_rate']:.1%} < 70%"

        return self.results


# ── pytest integration ──
@pytest.mark.asyncio
async def test_system_resilience(insurance_bot_system):
    chaos = AISystemChaosRunner(insurance_bot_system)

    test_queries = [
        "What is my deductible?",
        "How do I file a claim?",
        "What does comprehensive cover?",
    ]

    # Test: system should work even when vector DB is down (degraded mode)
    async with chaos.vector_db_unavailable():
        response = await insurance_bot_system.process("What is insurance?")
        # Should return SOMETHING (from LLM knowledge) even without retrieval
        assert response is not None
        assert len(response) > 20
        assert "error" not in response.lower()

    # Test: system should handle LLM rate limits with retry/fallback
    async with chaos.llm_rate_limit(fail_rate=0.5):
        successes = 0
        for _ in range(10):
            try:
                response = await insurance_bot_system.process("Hello")
                if response:
                    successes += 1
            except Exception:
                pass
        assert successes >= 7, "Should succeed ≥70% of time with 50% rate limit error rate"
```

### 💡 Interview Tips — Chaos Engineering
- **GameDay**: formal chaos engineering sessions where the team deliberately breaks prod (or a prod replica) to verify resilience. Netflix, Amazon, and major tech companies run these regularly.
- For AI systems, the unique chaos scenarios are: **LLM API outage** (provider down), **vector DB unavailability** (should still work without RAG), **model version change** (unexpected output format), **context window overflow** (input too long).
- Key principle: **verify fallbacks actually work** — a fallback to a cheaper model during OpenAI outage is useless if nobody has tested that path.
- Senior: the goal isn't to avoid all failures — it's to **understand your failure modes** so you can design graceful degradation that maintains partial functionality.

---

# SECTION D — Fine-tuning Ecosystem

---

## 11. Synthetic Data Generation

---

### 🔷 CONCEPT OVERVIEW

| Level | Definition |
|-------|-----------|
| 🟢 Junior | Synthetic data generation means using a powerful AI (like GPT-4) to create training examples for a smaller, cheaper AI. You write 10-20 examples by hand, ask GPT-4 to generate 1000 more like them, and use all 1000 to fine-tune a faster, cheaper model. |
| 🔴 Senior | Synthetic data generation leverages frontier LLMs (GPT-4, Claude Opus) as data factories to create training datasets for fine-tuning smaller models. Techniques include: Self-Instruct (generate diverse instructions from seed examples), Evol-Instruct (progressively rewrite instructions to be more complex), Constitutional AI (iteratively critique and revise outputs), and distillation (generate (prompt, response) pairs using a teacher model). The key insight: generating data with GPT-4 is ~1000x cheaper than human annotation at scale. |

---

### 11.1 Synthetic Data Pipelines

```python
from openai import OpenAI
import json
import random
from typing import Optional

client = OpenAI()


# ─────────────────────────────────────────────────
# Technique 1: Self-Instruct
# Start with seed examples → generate diverse new examples
# ─────────────────────────────────────────────────
SEED_EXAMPLES = [
    {"instruction": "What is the deductible for water damage?",
     "response": "The deductible for water damage is €500 for standard policies."},
    {"instruction": "How do I file a claim?",
     "response": "File claims online at our portal or call 1-800-IAG within 30 days."},
    {"instruction": "Does comprehensive coverage include theft?",
     "response": "Yes, comprehensive coverage includes theft of the insured item."},
]

def generate_self_instruct_batch(
    seed_examples: list[dict],
    n_to_generate: int = 20,
    domain: str = "insurance customer service"
) -> list[dict]:
    """Generate new instruction-response pairs similar to seeds."""

    seed_text = "\n".join([
        f"Instruction: {ex['instruction']}\nResponse: {ex['response']}"
        for ex in random.sample(seed_examples, min(3, len(seed_examples)))
    ])

    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.9,  # High temperature for diversity
        messages=[{
            "role": "user",
            "content": f"""You are creating training data for a {domain} AI.
Generate {n_to_generate} diverse instruction-response pairs.

Here are example pairs to follow:
{seed_text}

Requirements:
- Cover different aspects: coverage types, claims, billing, policy terms
- Vary question complexity (simple facts to complex scenarios)
- Use realistic insurance terminology
- Keep responses accurate and professional
- Include edge cases and nuanced situations

Output as JSON list:
[{{"instruction": "...", "response": "..."}}]
Only output valid JSON, no markdown."""
        }]
    )

    return json.loads(response.choices[0].message.content)


# ─────────────────────────────────────────────────
# Technique 2: Evol-Instruct (WizardLM approach)
# Progressively make instructions more complex
# ─────────────────────────────────────────────────
EVOL_STRATEGIES = [
    "Add more constraints and requirements to the question",
    "Make the question require multi-step reasoning",
    "Add a specific scenario or context to the question",
    "Combine with a related question into a multi-part question",
    "Add domain-specific technical details that require expertise",
    "Transform into a comparative question requiring analysis",
]

def evolve_instruction(instruction: str, strategy: Optional[str] = None) -> str:
    """Make an instruction more complex using a specific strategy."""
    if strategy is None:
        strategy = random.choice(EVOL_STRATEGIES)

    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.8,
        messages=[{
            "role": "user",
            "content": f"""Rewrite this insurance question to be more complex using this strategy:
Strategy: {strategy}

Original question: {instruction}

Output ONLY the rewritten question, nothing else."""
        }]
    )
    return response.choices[0].message.content.strip()


def generate_evolved_dataset(
    seed_instructions: list[str],
    evolution_rounds: int = 3,
    n_variants_per_seed: int = 3
) -> list[dict]:
    """Generate progressively more complex instruction-response pairs."""
    dataset = []

    for seed in seed_instructions:
        current = seed

        for round_num in range(evolution_rounds):
            # Evolve the instruction
            evolved = evolve_instruction(current)

            # Generate high-quality response
            response = client.chat.completions.create(
                model="gpt-4o",
                temperature=0.3,   # Low temp for accurate responses
                messages=[
                    {"role": "system", "content": "You are an expert insurance advisor. Provide accurate, complete answers."},
                    {"role": "user",   "content": evolved}
                ]
            )

            dataset.append({
                "instruction": evolved,
                "response": response.choices[0].message.content,
                "evolution_round": round_num,
                "original_seed": seed,
            })

            current = evolved  # Use evolved as next seed

    return dataset


# ─────────────────────────────────────────────────
# Technique 3: Constitutional AI data generation
# Generate then critique and improve
# ─────────────────────────────────────────────────
CONSTITUTION = [
    "The response should be accurate and not contain false insurance information.",
    "The response should not give specific legal advice.",
    "The response should be empathetic when dealing with claims.",
    "The response should suggest human support for complex situations.",
    "The response should never share other customers' information.",
]

def constitutional_ai_refine(instruction: str, initial_response: str) -> str:
    """Iteratively improve a response using constitutional principles."""
    current_response = initial_response

    for principle in CONSTITUTION:
        # Critique: does the response violate this principle?
        critique = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            messages=[{
                "role": "user",
                "content": f"""Does this insurance bot response violate this principle?
Principle: {principle}
Response: {current_response}
Answer with: VIOLATION: [explanation] or OK"""
            }]
        )

        if "VIOLATION" in critique.choices[0].message.content:
            # Revise: fix the violation
            revision = client.chat.completions.create(
                model="gpt-4o",
                temperature=0.3,
                messages=[{
                    "role": "user",
                    "content": f"""Revise this insurance bot response to fix this issue:
Issue: {critique.choices[0].message.content}
Original question: {instruction}
Current response: {current_response}
Write only the improved response."""
                }]
            )
            current_response = revision.choices[0].message.content

    return current_response


# ─────────────────────────────────────────────────
# Technique 4: Quality filtering
# Not all generated data is good — filter before training
# ─────────────────────────────────────────────────
def filter_dataset_quality(
    dataset: list[dict],
    min_response_words: int = 20,
    max_response_words: int = 500,
) -> list[dict]:
    """Filter synthetic data for quality before fine-tuning."""
    filtered = []

    for item in dataset:
        instruction = item.get("instruction", "")
        response    = item.get("response", "")

        # Basic length filters
        if len(instruction.split()) < 3:
            continue
        if len(response.split()) < min_response_words:
            continue
        if len(response.split()) > max_response_words:
            continue

        # Check response actually addresses the instruction (LLM judge)
        relevance_check = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            messages=[{
                "role": "user",
                "content": f"""Does this response actually answer the question?
Question: {instruction}
Response: {response[:300]}
Answer only: YES or NO"""
            }]
        )

        if "YES" in relevance_check.choices[0].message.content:
            filtered.append(item)

    print(f"Quality filter: {len(filtered)}/{len(dataset)} kept ({len(filtered)/len(dataset)*100:.1f}%)")
    return filtered


# ── Full pipeline: generate → filter → format for fine-tuning ──
def build_fine_tuning_dataset(
    seed_examples: list[dict],
    target_size: int = 1000,
    output_file: str = "training_data.jsonl"
) -> int:
    """Build a complete fine-tuning dataset from seeds."""
    all_data = []

    # Phase 1: Self-instruct (bulk generation)
    print("Phase 1: Self-instruct generation...")
    batch = generate_self_instruct_batch(seed_examples, n_to_generate=target_size // 2)
    all_data.extend(batch)

    # Phase 2: Evol-instruct (complex examples)
    print("Phase 2: Evol-instruct generation...")
    seeds     = [ex["instruction"] for ex in seed_examples]
    evolved   = generate_evolved_dataset(seeds, evolution_rounds=2)
    all_data.extend(evolved)

    # Phase 3: Quality filter
    print("Phase 3: Quality filtering...")
    filtered = filter_dataset_quality(all_data)

    # Phase 4: Format as JSONL for OpenAI fine-tuning
    with open(output_file, "w") as f:
        for item in filtered[:target_size]:
            training_example = {
                "messages": [
                    {"role": "system", "content": "You are a helpful insurance assistant for IAG France."},
                    {"role": "user",   "content": item["instruction"]},
                    {"role": "assistant", "content": item["response"]},
                ]
            }
            f.write(json.dumps(training_example, ensure_ascii=False) + "\n")

    print(f"Dataset saved: {len(filtered[:target_size])} examples → {output_file}")
    return len(filtered[:target_size])
```

### 💡 Interview Tips — Synthetic Data Generation
- **The business case**: "10 seed examples + GPT-4 generation + quality filtering = 1000 training examples. Cost: ~$5 in API calls. Equivalent human annotation cost: ~$5,000-20,000."
- Key quality concern: **hallucination in training data**. If GPT-4 generates wrong facts in training data, the fine-tuned model learns those wrong facts. Always filter with a quality checker.
- **Evol-Instruct** is what made WizardLM and WizardCoder — the graduated complexity ensures the fine-tuned model handles both simple and complex queries.
- Senior: discuss **data contamination** — if you generate synthetic data using GPT-4 and then fine-tune on it, your model is effectively distilling GPT-4. This raises OpenAI ToS questions for commercial use — know this nuance.

---

## 12. ORPO — Odds Ratio Preference Optimization

---

### 🔷 CONCEPT OVERVIEW

| Level | Definition |
|-------|-----------|
| 🟢 Junior | Normally to align an AI (like ChatGPT), you train it twice: first to follow instructions, then to give preferred responses. ORPO combines both training steps into one by rewarding the model for choosing the preferred response and penalizing it for the rejected response in a single training pass. |
| 🔴 Senior | ORPO (Odds Ratio Preference Optimization, 2024) is a monolithic alignment algorithm that performs supervised fine-tuning (SFT) and preference alignment simultaneously in a single training stage. The loss function combines a standard SFT cross-entropy loss with an odds ratio-based penalty that increases the likelihood of chosen responses relative to rejected responses. Unlike DPO (which requires a pre-trained SFT reference model) and PPO (which requires a reward model), ORPO needs only preference pairs and no reference model. |

---

### 12.1 ORPO vs Other Alignment Methods

```
Training stages comparison:

PPO (RLHF):     SFT → Reward Model Training → PPO RL       (3 stages)
DPO:            SFT → DPO fine-tuning                      (2 stages)
ORPO:           ORPO (SFT + alignment combined)            (1 stage)

ORPO Loss = SFT_loss + λ * OR_loss

SFT_loss = -log P(y_chosen | x)   ← Standard next-token prediction

OR_loss  = -log σ(log(odds_chosen / odds_rejected))
         where odds = P(y|x) / (1 - P(y|x))

Key: No reference model needed — the SFT component IS the reference
```

```python
import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import ORPOTrainer, ORPOConfig
from datasets import Dataset

# ── ORPO Training with TRL ──
model_name = "microsoft/Phi-3-mini-4k-instruct"  # Small model, great for ORPO
model      = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.bfloat16)
tokenizer  = AutoTokenizer.from_pretrained(model_name)

# Preference dataset format: (prompt, chosen, rejected)
preference_data = [
    {
        "prompt":   "How do I file an insurance claim?",
        "chosen":   "To file a claim: 1) Call our 24/7 claims line at 1-800-IAG, "
                    "2) Document the damage with photos, 3) Get repair estimates. "
                    "Our team will guide you through the process.",
        "rejected": "You should call us I think. Or maybe go online. "
                    "I'm not sure of the exact steps.",
    },
    {
        "prompt":   "What is a deductible?",
        "chosen":   "A deductible is the amount you pay out-of-pocket before insurance "
                    "covers the rest. For example, with a €500 deductible on a €3,000 "
                    "claim, you pay €500 and insurance pays €2,500.",
        "rejected": "The deductible is like a fee you pay. It's some amount of money. "
                    "Insurance pays after that.",
    },
]

# Format for ORPO training
def format_orpo_example(example):
    """Format preference pair for ORPO training."""
    prompt  = f"<|user|>\n{example['prompt']}\n<|end|>\n<|assistant|>\n"
    chosen  = prompt + example["chosen"]  + "<|end|>"
    rejected = prompt + example["rejected"] + "<|end|>"
    return {"prompt": prompt, "chosen": chosen, "rejected": rejected}

dataset = Dataset.from_list([format_orpo_example(d) for d in preference_data])

# ORPO configuration
orpo_config = ORPOConfig(
    output_dir="./orpo-insurance-model",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=8e-6,          # Lower LR than SFT — combined objective
    lambda_orpo=0.1,             # λ — weight of odds ratio loss vs SFT loss
    max_length=512,
    max_prompt_length=128,
    beta=0.1,                    # Temperature parameter
    fp16=True,
    logging_steps=10,
    save_steps=100,
    evaluation_strategy="steps",
    eval_steps=100,
)

trainer = ORPOTrainer(
    model=model,
    args=orpo_config,
    train_dataset=dataset,
    tokenizer=tokenizer,
)

trainer.train()
trainer.save_model("./orpo-insurance-final")


# ── ORPO manual implementation (understanding the loss) ──
def orpo_loss(
    model,
    input_ids_chosen:   torch.Tensor,
    input_ids_rejected: torch.Tensor,
    attention_mask_c:   torch.Tensor,
    attention_mask_r:   torch.Tensor,
    prompt_length:      int,
    lambda_orpo:        float = 0.1,
) -> torch.Tensor:
    """
    ORPO loss = SFT cross-entropy + λ * odds ratio penalty
    """
    # ── SFT loss on chosen response ──
    logits_chosen = model(input_ids_chosen, attention_mask=attention_mask_c).logits
    sft_loss = F.cross_entropy(
        logits_chosen[:, prompt_length-1:-1].reshape(-1, logits_chosen.size(-1)),
        input_ids_chosen[:, prompt_length:].reshape(-1),
    )

    # ── Log probabilities for chosen and rejected ──
    def get_log_probs(input_ids, attention_mask):
        logits  = model(input_ids, attention_mask=attention_mask).logits
        log_probs = F.log_softmax(logits, dim=-1)
        # Sum log probs over response tokens only
        response_log_probs = torch.gather(
            log_probs[:, prompt_length-1:-1],
            2,
            input_ids[:, prompt_length:].unsqueeze(-1)
        ).squeeze(-1)
        return response_log_probs.sum(-1)  # Total log prob of response

    log_prob_chosen   = get_log_probs(input_ids_chosen,   attention_mask_c)
    log_prob_rejected = get_log_probs(input_ids_rejected, attention_mask_r)

    # ── Odds ratio ──
    # odds = P / (1 - P) = exp(log_p) / (1 - exp(log_p))
    log_odds_chosen   = log_prob_chosen   - torch.log1p(-torch.exp(log_prob_chosen))
    log_odds_rejected = log_prob_rejected - torch.log1p(-torch.exp(log_prob_rejected))

    # ── Odds ratio loss ──
    # Maximize: chosen odds / rejected odds
    log_odds_ratio = log_odds_chosen - log_odds_rejected
    or_loss = -F.logsigmoid(log_odds_ratio).mean()

    return sft_loss + lambda_orpo * or_loss
```

### 💡 Interview Tips — ORPO
- **Why ORPO over DPO**: "ORPO trains in one stage instead of two — no separate SFT run needed. This saves training time and reduces the risk of forgetting from the SFT stage."
- Key number: ORPO uses **λ=0.1** as the default weight for the odds ratio component — too high and alignment dominates over SFT quality, too low and preferences aren't learned.
- Best models to ORPO fine-tune: **Phi-3-mini, Gemma 2B, Llama 3 8B** — small enough to fine-tune on a single A100 with ORPO.
- Senior: ORPO showed **state-of-the-art results on AlpacaEval** when it was released in 2024, beating DPO on several benchmarks while being simpler to train.

---

## 13. Unsloth — Fast Fine-tuning

---

### 🔷 CONCEPT OVERVIEW

| Level | Definition |
|-------|-----------|
| 🟢 Junior | Unsloth is a tool that makes fine-tuning large language models much faster and uses much less GPU memory — typically 2x faster and using 80% less GPU memory compared to standard approaches. It lets you fine-tune models that wouldn't otherwise fit on your GPU. |
| 🔴 Senior | Unsloth (2024) is a fine-tuning optimization library that reimplements attention, RoPE embeddings, and cross-entropy loss kernels in Triton/CUDA with custom backward passes. It eliminates redundant memory allocations in the LoRA training loop, applies kernel fusion, and uses grouped query attention optimization — achieving 2-5x faster throughput and 60-80% VRAM reduction vs HuggingFace + PEFT baseline, enabling 70B model fine-tuning on a single 24GB GPU. |

---

### 13.1 Unsloth Fine-tuning

```python
# pip install unsloth
from unsloth import FastLanguageModel
from trl import SFTTrainer, TrainingArguments
from datasets import load_dataset
import torch

# ── Load model with Unsloth optimization ──
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Meta-Llama-3.1-8B-Instruct",  # Unsloth-optimized checkpoints
    max_seq_length=2048,
    dtype=None,             # Auto-detect (bfloat16 on Ampere+)
    load_in_4bit=True,      # QLoRA: 4-bit base + fp16 adapters
    # token="hf_...",       # For gated models
)

# ── Add LoRA adapters ──
model = FastLanguageModel.get_peft_model(
    model,
    r=16,                   # LoRA rank
    target_modules=[        # Which layers to fine-tune
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj",  # MLP layers too
    ],
    lora_alpha=16,
    lora_dropout=0,         # Unsloth optimizes for dropout=0
    bias="none",
    use_gradient_checkpointing="unsloth",  # Unsloth's optimized checkpointing
    random_state=42,
    use_rslora=False,       # Rank-stabilized LoRA (optional improvement)
)

# Print trainable parameters
model.print_trainable_parameters()
# trainable params: 41,943,040 || all params: 8,072,802,304 (0.52%)


# ── Dataset preparation ──
def format_insurance_example(example):
    """Format for Llama 3 chat template."""
    return {
        "text": f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are a helpful insurance assistant for IAG France.<|eot_id|>
<|start_header_id|>user<|end_header_id|>
{example['question']}<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
{example['answer']}<|eot_id|><|end_of_text|>"""
    }

dataset = load_dataset("json", data_files="insurance_training.jsonl")["train"]
dataset = dataset.map(format_insurance_example)


# ── Training ──
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=2048,
    dataset_num_proc=2,
    args=TrainingArguments(
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        warmup_steps=5,
        max_steps=100,                     # Or num_train_epochs=3
        learning_rate=2e-4,
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        logging_steps=1,
        optim="adamw_8bit",                # 8-bit Adam — less VRAM
        weight_decay=0.01,
        lr_scheduler_type="linear",
        seed=3407,
        output_dir="outputs",
    ),
)

# Shows memory usage and training speed
trainer_stats = trainer.train()
print(f"Peak VRAM: {torch.cuda.max_memory_reserved() / 1e9:.2f} GB")


# ── Save and export ──
# Save LoRA adapters only (small, ~100MB for 16GB base model)
model.save_pretrained("insurance-lora-adapter")
tokenizer.save_pretrained("insurance-lora-adapter")

# Merge and export as GGUF for local deployment
model.save_pretrained_gguf(
    "insurance-model-gguf",
    tokenizer,
    quantization_method="q4_k_m"   # 4-bit quantized for CPU
)
# Now run with: ollama create insurance-bot -f ./insurance-model-gguf/Modelfile


# ── Inference with fine-tuned model ──
FastLanguageModel.for_inference(model)  # Enable fast inference mode

inputs = tokenizer(
    ["""<|begin_of_text|><|start_header_id|>user<|end_header_id|>
What is the deductible for water damage?<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>"""],
    return_tensors="pt"
).to("cuda")

outputs = model.generate(
    **inputs,
    max_new_tokens=200,
    use_cache=True,
    temperature=0.7,
    do_sample=True,
)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

---

### 13.2 Unsloth Performance Numbers

```
Comparison (Llama 3 8B, A100 40GB, batch_size=2):

                    Speed (tok/s)    VRAM Used    Max Seq Length
HuggingFace + PEFT: ~850             ~22GB        2048
Unsloth (4-bit):   ~2,100           ~8GB         8192
Unsloth speedup:   2.5x faster      64% less     4x longer sequences

For 70B model (requires 2x A100 normally):
Unsloth 4-bit:     Fits on 1x A100 (40GB)  ← game-changer for small teams
```

### 💡 Interview Tips — Unsloth
- **The pitch**: "Unsloth is the fastest practical LoRA fine-tuning library — 2-5x faster, 60-80% less VRAM, same quality as standard PEFT. It's now the default choice for most teams fine-tuning open-source models."
- Key feature: **GGUF export** — go from fine-tuning to a quantized GGUF model ready for Ollama in one step.
- Know the **limitation**: Unsloth focuses on decoder-only models (Llama, Mistral, Phi, Qwen). It doesn't support encoder models (BERT) or encoder-decoder (T5).
- Senior: Unsloth achieves its speed through **Triton kernel reimplementation** — the attention and cross-entropy kernels are custom-written in Triton, eliminating the memory overhead of PyTorch's generic implementations.

---

## 14. Axolotl — Production Fine-tuning Framework

---

### 🔷 CONCEPT OVERVIEW

| Level | Definition |
|-------|-----------|
| 🟢 Junior | Axolotl is a professional fine-tuning toolkit that makes it easy to configure and run fine-tuning jobs using a YAML config file. Instead of writing training code, you describe what you want — model, dataset, LoRA settings — in a config file and Axolotl handles the rest, including distributed training across multiple GPUs. |
| 🔴 Senior | Axolotl is a production-grade LLM fine-tuning framework that abstracts over HuggingFace Transformers, PEFT, DeepSpeed, and FSDP through a unified YAML configuration. It provides battle-tested training recipes for SFT, DPO, ORPO, and RL, supports 50+ base models, handles multi-GPU and multi-node training, and provides prompt template management — making it the go-to for teams that run fine-tuning jobs repeatedly and need reproducibility. |

---

### 14.1 Axolotl Configuration

```yaml
# axolotl_config.yml — Complete fine-tuning configuration
# Run with: axolotl train axolotl_config.yml

# ── Base model ──
base_model: mistralai/Mistral-7B-Instruct-v0.3
model_type: MistralForCausalLM
tokenizer_type: LlamaTokenizer

# ── LoRA configuration ──
adapter: lora
lora_r: 16
lora_alpha: 32
lora_dropout: 0.05
lora_target_modules:
  - q_proj
  - k_proj
  - v_proj
  - o_proj
  - gate_proj
  - up_proj
  - down_proj

# ── Quantization (QLoRA) ──
load_in_4bit: true
bnb_4bit_quant_type: nf4
bnb_4bit_use_double_quant: true
bnb_4bit_compute_dtype: bfloat16

# ── Dataset configuration ──
datasets:
  - path: insurance_training.jsonl
    type: alpaca          # prompt/input/output format
    data_files: training.jsonl
  - path: insurance_eval.jsonl
    type: alpaca
    split: eval

# For conversational data (multi-turn):
# datasets:
#   - path: conversations.jsonl
#     type: sharegpt
#     conversation: mistral  # Uses Mistral chat template

dataset_prepared_path: ./prepared_data   # Cache prepared dataset
val_set_size: 0.05        # 5% validation split

# ── Sequence settings ──
sequence_len: 4096
sample_packing: true       # Bin-pack multiple short examples → faster training
pad_to_sequence_len: true

# ── Training parameters ──
output_dir: ./insurance-mistral-7b-lora
num_epochs: 3
micro_batch_size: 2
gradient_accumulation_steps: 4
learning_rate: 0.0002
train_on_inputs: false     # Only train on outputs (responses), not inputs
group_by_length: true

# ── Optimizer ──
optimizer: paged_adamw_8bit   # 8-bit Adam saves VRAM
lr_scheduler: cosine
warmup_steps: 10

# ── Mixed precision ──
bf16: auto
tf32: false

# ── Logging ──
logging_steps: 10
eval_steps: 100
save_steps: 200
save_total_limit: 3         # Keep last 3 checkpoints

# Weights & Biases integration
wandb_project: insurance-bot-finetuning
wandb_run_name: mistral-7b-lora-run-1

# ── Multi-GPU with DeepSpeed ──
# deepspeed: deepspeed_configs/zero2.json
# To use: deepspeed --num_gpus=4 -m axolotl.cli.train axolotl_config.yml

# ── FSDP (alternative to DeepSpeed) ──
# fsdp:
#   - full_shard
#   - auto_wrap
# fsdp_config:
#   fsdp_transformer_layer_cls_to_wrap: MistralDecoderLayer
```

```bash
# Training commands

# Single GPU
axolotl train axolotl_config.yml

# Multi-GPU (4 GPUs with DeepSpeed ZeRO-2)
accelerate launch --num_processes 4 -m axolotl.cli.train axolotl_config.yml

# Preview dataset (check formatting before training)
axolotl preprocess axolotl_config.yml

# Inference with fine-tuned model
axolotl inference axolotl_config.yml \
  --lora_model_dir ./insurance-mistral-7b-lora \
  --prompt "What is the deductible for water damage?"

# Merge LoRA adapters into base model
axolotl merge_lora axolotl_config.yml \
  --lora_model_dir ./insurance-mistral-7b-lora \
  --output_dir ./insurance-mistral-7b-merged

# Convert to GGUF
python -m llama_cpp.llama_cpp.convert \
  --input ./insurance-mistral-7b-merged \
  --output ./insurance-mistral-7b.gguf \
  --quantization q4_k_m
```

```python
# DPO training with Axolotl
# In config, change:
# rl: dpo
# And dataset format includes prompt/chosen/rejected

dpo_config_addition = """
# Add to axolotl_config.yml for DPO:
rl: dpo
dpo_beta: 0.1

datasets:
  - path: preference_data.jsonl
    type: chatml.intel  # or llama3, mistral, etc.
    # Format: {"system": "...", "prompt": "...", "chosen": "...", "rejected": "..."}
"""

# ORPO training with Axolotl
orpo_config_addition = """
rl: orpo
orpo_alpha: 0.1  # Lambda weight

datasets:
  - path: preference_data.jsonl
    type: orpo.mistral
"""
```

---

### 14.2 Axolotl vs Unsloth vs Direct PEFT

| Feature | Axolotl | Unsloth | Direct PEFT/TRL |
|---------|---------|---------|----------------|
| Config-driven | ✅ YAML | ❌ Python code | ❌ Python code |
| Speed | Standard | 2-5x faster | Baseline |
| VRAM | Standard | 60-80% less | Baseline |
| Multi-GPU | ✅ DeepSpeed/FSDP | Limited | ✅ via Accelerate |
| DPO/ORPO | ✅ Built-in | ✅ via TRL | ✅ via TRL |
| Reproducibility | ✅ YAML config = reproducible | ❌ Code changes | ❌ Code changes |
| Production teams | ✅ Best for teams | ✅ Best for individuals | For custom needs |
| Best for | Reproducible team workflows | Single-GPU fast experiments | Full custom control |

### 💡 Interview Tips — Axolotl
- **The pitch**: "Axolotl is what teams use when they're running fine-tuning jobs repeatedly and need reproducibility. One YAML file describes the entire experiment — version control it alongside your code."
- Know the **sample packing** feature — bins multiple short training examples into one sequence to maximize GPU utilization. Can give 2-3x faster training on short-example datasets.
- Senior: explain when you'd choose **Axolotl (team, reproducibility) vs Unsloth (single GPU, max speed) vs direct TRL (full custom control)**.
- **Checkpoint management**: Axolotl's `save_total_limit` prevents filling disk with checkpoints — always set this in production.

---

# SECTION E — Master Summary

---

## 15. Complete Job Readiness Checklist

---

### 🎯 ARE THESE NOTES ENOUGH TO GET THE JOB?

**Honest Assessment by Role Level:**

```
Junior AI Engineer (1-2 years):
  Your notes cover 95%+ of what will be asked.
  You are OVER-PREPARED for junior roles.
  Focus on: being able to explain concepts clearly in your own words.
  Gap: actual project experience (build something with these tools).

Mid-level AI Engineer (3-5 years):
  Your notes cover 85-90% of interview topics.
  Strong foundation. Remaining 10-15% = depth from real production experience.
  You can get the job; strengthen with hands-on projects.

Senior AI Engineer (6+ years):
  Your notes cover 75-80% of senior interview topics.
  The missing 20-25% is: system design from experience, production incidents,
  team leadership, architectural decisions under uncertainty.
  Notes cannot replace 2-3 years of production AI system experience.
```

---

### 📋 COMPLETE TOPIC COVERAGE ACROSS ALL 6 PARTS

#### ✅ FULLY COVERED (Can answer confidently)

**LLM Fundamentals**
- [ ] Transformer architecture, attention, tokenization
- [ ] Inference parameters (temperature, top-p, top-k)
- [ ] Context window management, KV cache
- [ ] Quantization (INT4, INT8, AWQ, GPTQ, GGUF)
- [ ] Fine-tuning (SFT, LoRA, QLoRA, RLHF, DPO, ORPO)
- [ ] MoE architecture, GQA/MQA, Sliding Window Attention
- [ ] GRPO and reasoning model training (o1, DeepSeek-R1)

**RAG & Retrieval**
- [ ] Naive RAG, all 7 RAG types (Self-RAG, CRAG, Hybrid, Agentic, Modular, Online, Graph)
- [ ] Advanced retrieval: HyDE, multi-query, reranking, FLARE
- [ ] Parent Document Retriever, Sentence Window Retrieval
- [ ] Contextual Retrieval (Anthropic), Microsoft GraphRAG
- [ ] Embedding models: BGE, E5, Nomic, MTEB leaderboard
- [ ] Vector databases: Pinecone, Weaviate, Qdrant, Chroma, FAISS, pgvector

**Agents & Orchestration**
- [ ] ReAct, Plan-and-Execute, Reflexion patterns
- [ ] LangGraph (stateful, checkpointers, human-in-loop)
- [ ] AutoGen, CrewAI, raw tool calling
- [ ] Multi-agent: supervisor, swarm/handoff
- [ ] Memory: MemGPT, Mem0, 4 memory types

**Frameworks & Tools**
- [ ] LangChain (LCEL, chains, agents, memory)
- [ ] LlamaIndex (full RAG primitives, SubQuestionQueryEngine)
- [ ] DSPy (automated prompt optimization)
- [ ] Guardrails AI (validation, validators, fix actions)
- [ ] Instructor (structured output with Pydantic)
- [ ] LiteLLM (multi-provider gateway)

**Inference & Serving**
- [ ] vLLM (PagedAttention, continuous batching)
- [ ] TGI (HuggingFace, multi-LoRA, Rust backend)
- [ ] Ollama (local model serving)
- [ ] ONNX Runtime (CPU/edge inference)
- [ ] Ray Serve (distributed serving pipelines)
- [ ] Triton + TensorRT-LLM (max GPU throughput)
- [ ] Speculative decoding, Flash Attention

**Fine-tuning Ecosystem**
- [ ] Unsloth (2-5x faster, 60-80% less VRAM)
- [ ] Axolotl (config-driven, team workflows)
- [ ] Synthetic data generation (Self-Instruct, Evol-Instruct)
- [ ] ORPO (single-stage alignment)

**Production Engineering**
- [ ] Data pipelines (Unstructured, Docling, chunking strategies)
- [ ] LLM testing (unit, property-based, adversarial, DeepEval)
- [ ] Observability (LangSmith, OpenTelemetry, Prometheus, Grafana)
- [ ] Shadow testing, load shedding, chaos engineering
- [ ] Canary deployment, blue-green, feature flags
- [ ] Cost optimization (model tiering, caching, Batch API, LLMLingua)

**Security & Safety**
- [ ] Prompt injection (direct + indirect/RAG poisoning)
- [ ] Red teaming (manual + automated with LLM-as-attacker)
- [ ] Data poisoning, model extraction, watermarking
- [ ] LLM calibration, reward hacking
- [ ] Responsible AI, fairness metrics, EU AI Act
- [ ] OWASP Top 10 for LLMs

**Evaluation**
- [ ] LLM-as-judge (G-Eval), RAGAS, DeepEval
- [ ] Industry benchmarks (MMLU, HumanEval, GSM8K, LMSYS Arena)
- [ ] Evals pipeline in CI/CD

---

### ⚠️ WHAT YOUR NOTES CANNOT GIVE YOU

These require real experience — not just reading:

**1. System Design from First Principles**
Your notes give you the components. Interviews test whether you can assemble them under pressure:
- "Design a multi-tenant RAG system for 50,000 enterprise users"
- "How would you handle 10x traffic spike during a disaster event?"
- Practice 10+ system design questions from scratch on a whiteboard

**2. Production Incident Experience**
- "Tell me about a time the LLM started giving wrong answers in production"
- "How did you debug a 3x latency regression after a model update?"
- Build something real, break it, fix it — this experience is irreplaceable

**3. Real Numbers**
- "What throughput did your vLLM deployment achieve per GPU?"
- "What was your RAG pipeline's faithfulness score?"
- Build a project, run benchmarks, know your actual numbers

**4. Tradeoff Decision-Making**
- "Should we use RAG or fine-tune for this use case?"
- "LangGraph or AutoGen — defend your choice for this specific scenario"
- Notes give you frameworks; interviews test whether you can apply them to ambiguous situations

---

### 🚀 THE 20 MOST ASKED SENIOR AI ENGINEER INTERVIEW QUESTIONS

Master these and you can handle 90% of interviews:

| # | Question | Key Answer (from your notes) |
|---|---------|------------------------------|
| 1 | Design a RAG system for 100K users | Part 1+3+4: Pipeline + Parent Doc + Reranking + Canary deploy |
| 2 | How do you improve a RAG that gives wrong answers? | Part 3+5: Data pipeline → chunking → contextual retrieval → rerank → eval |
| 3 | RAG vs fine-tuning? | Part 2: RAG for dynamic knowledge, FT for style/format; often both |
| 4 | How does vLLM achieve high throughput? | Part 2+3: PagedAttention + continuous batching |
| 5 | Explain MoE in Mixtral | Part 5: Sparse activation, top-K routing, load balancing loss |
| 6 | How do you test LLM applications? | Part 4: Unit(temp=0) → property → adversarial → DeepEval CI/CD |
| 7 | How do you reduce LLM costs 50%? | Part 4: Model tiering + caching + Batch API + MRL embeddings |
| 8 | What is prompt injection and how to defend? | Part 2+5: Direct/indirect, delimiter+classifier+output validation |
| 9 | Which agent framework and why? | Part 4+6: LangGraph(prod) vs CrewAI(proto) vs raw(max control) |
| 10 | How do you deploy a model change safely? | Part 3+6: Shadow test → canary 5% → eval gate → gradual rollout |
| 11 | What is RLHF vs DPO vs ORPO? | Part 2+6: Stages, reference model requirements, when to use each |
| 12 | How do you handle EU AI Act for insurance AI? | Part 5: High-risk classification, bias audit, human oversight, docs |
| 13 | LangChain vs LlamaIndex? | Part 6: LlamaIndex for RAG primitives, LangGraph for agent control |
| 14 | How does GQA reduce KV cache memory? | Part 5: 32Q/8KV = 4x reduction; critical for long context serving |
| 15 | What is DSPy and why use it? | Part 6: Automated prompt optimization; metric → optimizer → compile |
| 16 | How do you evaluate a RAG system without labels? | Part 3: RAGAS (faithfulness+relevancy) + LLM-as-judge |
| 17 | What is Contextual Retrieval? | Part 5: LLM adds context prefix to each chunk; 49% fewer failures |
| 18 | How does GraphRAG differ from standard RAG? | Part 5: Global queries via community summaries; corpus-wide patterns |
| 19 | How do you generate synthetic training data? | Part 6: Self-Instruct + Evol-Instruct + Constitutional AI + filtering |
| 20 | What is reward hacking and how to prevent it? | Part 5: Goodhart's Law; KL penalty + verifiable rewards + GRPO |

---

### 🎯 FINAL INTERVIEW CONFIDENCE RATING

```
After completing all 6 parts, your readiness by interview type:

Technical screening (60 min, concepts):        ████████████ 95% ready
System design interview (45 min):              ████████░░░░ 70% ready
Coding + ML fundamentals (90 min):             ████████████ 90% ready
Behavioral + production experience (60 min):   ██████░░░░░░ 55% ready
Take-home project (1 week):                    ████████████ 95% ready
Whiteboard architecture (30 min):              ████████░░░░ 75% ready

Overall readiness: ~82% (Junior/Mid: 95%, Senior: 75%)

The remaining 18% gap = real project experience.
BUILD SOMETHING. Deploy it. Break it. Fix it.
```

---

### 🛠️ RECOMMENDED PROJECTS TO CLOSE THE GAP

Build these to get real numbers and stories for interviews:

**Project 1 — Production RAG System (2 weeks)**
- Ingest 100+ PDFs with Unstructured, chunk with Parent Document Retriever
- Index with BGE-M3 embeddings in Qdrant
- Add contextual retrieval, hybrid BM25+dense search, Cohere reranking
- Evaluate with RAGAS — target faithfulness > 0.85
- Deploy with FastAPI + LiteLLM + Redis cache
- Add LangSmith observability
- **Result**: Real latency, cost, and quality numbers to cite in interviews

**Project 2 — Fine-tuned Specialist Model (1 week)**
- Generate 500 synthetic examples with Evol-Instruct
- Fine-tune Mistral-7B with Axolotl + LoRA
- Evaluate before/after on a test set
- Deploy with vLLM or TGI
- **Result**: "I fine-tuned a 7B model that improved task accuracy from 72% to 89%"

**Project 3 — LangGraph Agent (1 week)**
- Build a multi-step agent with 3+ tools and human-in-loop
- Add LangSmith tracing
- Write adversarial tests with DeepEval
- Add Guardrails AI validation
- **Result**: Full agent development experience with all production patterns

---

### 📚 STUDY PLAN — Last 2 Weeks Before Interview

```
Week 1: Review & Reinforce
  Day 1: Part 1 (LangChain, LangGraph, RAG) — review key code patterns
  Day 2: Part 2 (LLM Fundamentals, Prompt Engineering, Agents)
  Day 3: Part 3 (Tokenization, Advanced Retrieval, Quantization, Evaluation)
  Day 4: Part 4 (Data Pipelines, Testing, APIs, Memory, Cost)
  Day 5: Part 5 (MoE, GQA, GRPO, Advanced RAG, Security)
  Day 6: Part 6 (DSPy, Guardrails, LlamaIndex, TGI, ORPO, Unsloth)
  Day 7: System design practice — design 3 systems from scratch

Week 2: Practice & Simulate
  Day 1-2: Mock technical screens — explain each major concept out loud
  Day 3-4: System design whiteboard practice
  Day 5: Coding practice (RAG pipeline, agent loop, eval metric)
  Day 6: Behavioral questions — map your experiences to the frameworks
  Day 7: Rest and review your own project's numbers
```

---

*Part 6 of 6 — COMPLETE SERIES*

*All 6 Parts Together Cover:*
- *Part 1: LangChain, LangGraph, Tool Calling, MCP, Vector DBs, Embeddings, RAG, Persistence, Pinecone*
- *Part 2: LLM Fundamentals, Prompt Engineering, Agents, Observability, Fine-tuning, Streaming, Security, Deployment*
- *Part 3: Tokenization, Advanced Retrieval, Evaluation, Quantization, Long-Context, MLOps, Reasoning Models, Multimodal, Privacy*
- *Part 4: Data Pipelines, LLM Testing, Managed APIs, LLM Gateways, Responsible AI, Agentic Frameworks, Computer Use, Instructor, Memory, Embedding Models, Cost Optimization*
- *Part 5: MoE, GQA, GRPO, Sliding Window Attention, Parent Doc Retriever, Sentence Window, Contextual Retrieval, GraphRAG, FLARE, Red Teaming, Data Poisoning, Model Extraction, Watermarking, Calibration, Reward Hacking*
- *Part 6: DSPy, Guardrails AI, LlamaIndex, TGI, ONNX Runtime, Ray Serve, Triton, Shadow Testing, Load Shedding, Chaos Engineering, Synthetic Data, ORPO, Unsloth, Axolotl*

*Total: ~6 complete reference guides | 2025–2026 | Abhishek's AI Interview Series*
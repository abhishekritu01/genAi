# GenAI and AI Terminology: Quick Notes (Interview Edition)

> Short, sorted notes built from your cheat sheet, with the blank "25 terms" section filled in and extra market terms added.
> **⭐ = high priority for the RingCentral Agentic Systems Engineer JD.** Learn ⭐ terms first.
> Rule: use a term only where it describes a real engineering decision, not as decoration.

## Contents
1. Core AI and LLM
2. Prompting and output control
3. RAG, embeddings, retrieval
4. Agents and agentic workflows
5. LangChain, LangGraph, orchestration
6. Tools, APIs, MCP, integrations
7. Evaluation and testing
8. LLMOps, observability, production
9. Training, fine-tuning, optimization
10. Security, safety, governance
11. Advanced and emerging terms
12. Business and market buzzwords
13. The 25 terms to memorize first (with definitions)
14. Confusable pairs (interviewers love these)
15. Acronym decoder
16. How terms connect in one production agent
17. Sounding natural in the interview

---

## 1. Core AI and LLM

| Term | Short meaning |
|---|---|
| **GenAI** ⭐ | AI that generates new content: text, images, audio, code |
| **LLM** ⭐ | Large Language Model: predicts next tokens; processes and generates language |
| **Foundation model** | Broadly trained model adaptable to many tasks |
| **Transformer** | Neural architecture (attention-based) behind most LLMs |
| **Token** ⭐ | Unit of text a model processes (word or word fragment); cost and limits are measured in tokens |
| **Tokenization** | Converting text into tokens |
| **Context window** ⭐ | Max tokens (input + output) a model can handle in one request |
| **Inference** | Running a trained model to get output |
| **Multimodal** | Handles several data types (text, image, audio) |
| **SLM** | Small Language Model: cheaper/faster for narrow tasks |
| **Frontier model** | Leading-edge, most capable model at the time |
| **Open-weight model** | Weights publicly available (subject to license), e.g. Llama-style models |
| **Hallucination** ⭐ | Fluent output that is unsupported or false |
| **Knowledge cutoff** | Date after which the model has no training data |

---

## 2. Prompting and output control

| Term | Short meaning |
|---|---|
| **Prompt engineering** ⭐ | Designing instructions and context to get reliable outputs |
| **System prompt** ⭐ | Highest-level instructions defining role and rules |
| **Zero-shot / Few-shot** ⭐ | No examples vs examples in the prompt |
| **Chain-of-thought (CoT)** | Prompting the model to reason step by step |
| **Prompt template** | Reusable prompt with variables |
| **Structured output** ⭐ | Output in a defined format (JSON) |
| **JSON Schema** ⭐ | Spec of valid fields, types, constraints |
| **Constrained decoding** | Restricting generation to a valid structure |
| **Temperature** | Controls randomness (low = more deterministic) |
| **Top-p** | Nucleus sampling cutoff for token choice |
| **Prompt chaining** | Output of one call feeds the next |
| **Context engineering** ⭐ | Choosing and organizing everything the model sees: instructions, history, retrieved data, tools |
| **Prompt versioning** | Tracking prompt changes so behavior is testable and reproducible |

**Interview phrase:** "I use structured outputs with schema validation so downstream services don't blindly trust free-form model responses."

---

## 3. RAG, embeddings, retrieval

| Term | Short meaning |
|---|---|
| **RAG** ⭐ | Retrieval-Augmented Generation: retrieve external info, give it to the LLM |
| **Embedding** ⭐ | Vector representing meaning; similar meaning = nearby vectors |
| **Vector database** ⭐ | Stores vectors, does fast nearest-neighbor search (pgvector, Pinecone, Qdrant, etc.) |
| **Semantic search** | Search by meaning, not only keywords |
| **Chunking** ⭐ | Splitting documents into retrieval units |
| **Chunk overlap** | Repeated text between chunks to keep context |
| **Similarity search / ANN** | Finding nearest vectors (approximate nearest neighbor, e.g. HNSW) |
| **Cosine similarity** | Angle-based similarity between vectors |
| **Hybrid search** ⭐ | Vector + keyword (BM25) search combined |
| **BM25** | Classic keyword-ranking algorithm |
| **Reranking** ⭐ | Re-scoring retrieved results with a relevance model (cross-encoder) |
| **Metadata filtering** ⭐ | Restricting retrieval by tenant, date, ACL, type |
| **Query rewriting** | Reformulating the question for better retrieval |
| **HyDE** | Embedding a hypothetical answer instead of the raw query |
| **Grounding** ⭐ | Tying answers to evidence or trusted data |
| **Citations / attribution** | Pointing to the source of each claim |
| **GraphRAG** | Retrieval using entity relationships (knowledge graph) |
| **Retrieval precision / recall** ⭐ | Relevant share of retrieved / share of relevant that was found |
| **MMR** | Diversifies results to reduce redundancy |
| **Lost in the middle** | Models use start/end of long context better than the middle |

**Interview phrase:** "I'd evaluate retrieval quality separately from generation quality, then tune chunking, metadata filters, hybrid search, and reranking based on the failure patterns."

---

## 4. Agents and agentic workflows

| Term | Short meaning |
|---|---|
| **AI agent** ⭐ | Model + tools pursuing a goal |
| **Agentic AI** ⭐ | Systems that plan and act with some autonomy |
| **Agentic workflow** ⭐ | Multi-step process where the agent decides or adapts next steps |
| **Agent loop** ⭐ | Decide → act → observe → continue or stop |
| **Tool calling / Function calling** ⭐ | Model requests a registered function with structured args; your code runs it |
| **Tool registry** ⭐ | Catalog of tools with descriptions/schemas |
| **Orchestration** ⭐ | Coordinating model calls, tools, state, steps |
| **Planner / Executor** | Decides steps / carries them out |
| **ReAct** ⭐ | Reason → Act → Observe loop pattern |
| **Plan-and-execute** | Plan first, then run the steps |
| **Reflection** | Model reviews and corrects its own output |
| **Multi-agent system** ⭐ | Several agents collaborating |
| **Supervisor agent / Sub-agent** | Delegating manager / specialized worker |
| **Handoff** | Passing control between agents/components |
| **Human-in-the-loop (HITL)** ⭐ | Human review/approval at a step |
| **Autonomy boundary** | Limit of what the agent can do without approval |
| **Stopping condition** | Rule that ends a run (success, failure, step cap) |
| **Deterministic workflow** ⭐ | Fixed steps/routing, not model-chosen |
| **Router** | Sends a request to the right path/agent/tool set |
| **A2A (agent-to-agent)** | Protocols/patterns for agents to communicate |

> Strong line: "I use the least autonomy that solves the problem: deterministic workflow where steps are known, agent autonomy only where the path is genuinely uncertain."

---

## 5. LangChain, LangGraph, orchestration

| Term | Short meaning |
|---|---|
| **LangChain** ⭐ | Framework of components (models, prompts, parsers, retrievers, tools) |
| **LangGraph** ⭐ | Stateful graph-based orchestration (cycles, branching, persistence, HITL) |
| **LCEL** | LangChain Expression Language: `prompt | model | parser` composition |
| **Chain** | Connected sequence of steps |
| **Node / Edge / Conditional edge** ⭐ | Processing unit / connection / route chosen by condition |
| **State** ⭐ | Data shared across workflow steps |
| **State reducer** | Rule for merging updates into state (e.g. append messages) |
| **Checkpointing** ⭐ | Saving state per step so work can resume |
| **Thread ID** | Key identifying a conversation/run's checkpoints |
| **Persistence / Durable execution** ⭐ | State survives restarts; workflows resume reliably |
| **Workflow interrupt** | Pause until human/external event |
| **Recursion limit** | Safety cap on graph steps |
| **Subgraph** | A graph used as a node (modularity) |
| **LangSmith** | LangChain's tracing/evaluation platform |
| **Other frameworks (know names)** | LlamaIndex (data/RAG), CrewAI, AutoGen, Semantic Kernel |

---

## 6. Tools, APIs, MCP, integrations

| Term | Short meaning |
|---|---|
| **REST API** | HTTP interface for resources |
| **API contract** | Agreed requests, responses, errors |
| **MCP** ⭐ | Model Context Protocol: standard for connecting AI apps to tools/context |
| **MCP client / server** ⭐ | Client in the host app discovers/calls; server exposes tools, resources, prompts |
| **Connector** ⭐ | Integration with an external service or data source |
| **OAuth 2.0** ⭐ | Framework for scoped, delegated access |
| **Least privilege** ⭐ | Only the permissions needed |
| **Schema validation** ⭐ | Check data against required fields/types |
| **Idempotency** ⭐ | Repeating an operation doesn't repeat its effect |
| **Idempotency key** | Unique key making a create/write safe to retry |
| **Retry policy / Exponential backoff / Jitter** ⭐ | When to retry / growing delays / randomized delays |
| **Rate limiting** | Caps request frequency |
| **Circuit breaker** ⭐ | Stops calling a failing dependency temporarily |
| **Compensating action / Saga** | Undo of an earlier step when a multi-step operation fails |
| **Side effect** ⭐ | Change outside the return value (e.g. CRM update) |
| **Tool allowlist** | Explicit list of permitted tools |
| **Capability-based access** | Access granted per action/resource, not broadly |
| **Webhook** | Event-driven callback from a service |
| **Pagination** | Fetching large results in pages |

**Interview phrase:** "The model can request a tool call, but the backend remains responsible for authentication, authorization, validation, and safe execution."

---

## 7. Evaluation and testing

| Term | Short meaning |
|---|---|
| **Evals** ⭐ | Systematic measurement of LLM app quality |
| **Evaluation harness** ⭐ | Code that runs test cases and computes results |
| **Golden dataset** ⭐ | Curated cases with trusted expected outcomes |
| **LLM-as-a-judge** ⭐ | Using an LLM to score/compare outputs |
| **Task success rate** ⭐ | Share of tasks completed per defined criteria |
| **Tool-call accuracy** ⭐ | Correct tool choice + correct arguments |
| **Faithfulness / Groundedness** ⭐ | Answer supported by provided evidence |
| **Hallucination rate** ⭐ | Unsupported answers ÷ total answers |
| **Regression testing** ⭐ | Confirm changes didn't break existing behavior |
| **Benchmark** | Standard tasks to compare systems |
| **A/B testing** | Compare two variants under an experiment |
| **Pairwise evaluation** | Judge which of two outputs is better |
| **Human evaluation** | People rate quality/correctness |
| **Adversarial testing / Red teaming** ⭐ | Probing with hard or malicious inputs |
| **Evaluation leakage** | Eval data influencing development, inflating results |
| **False positive / False negative** | Flagged but not true / missed but true |
| **Evaluation threshold (gate)** | Minimum score to release |
| **Trajectory evaluation** | Scoring the path of steps, not only the final answer |
| **pass@k / multi-trial** | Handling non-determinism by repeated runs |
| **Calibration** | Aligning judge scores with human labels |

---

## 8. LLMOps, observability, production

| Term | Short meaning |
|---|---|
| **LLMOps** ⭐ | Deploying, evaluating, monitoring, maintaining LLM apps |
| **AI observability** ⭐ | Understanding behavior via traces, logs, metrics, evals |
| **Tracing / Span** ⭐ | Follow a request across steps / one timed unit of work |
| **Structured logging** | Machine-readable log fields |
| **Latency (p50/p95/p99)** ⭐ | Response time percentiles |
| **TTFT** | Time to first token |
| **Throughput** | Work done per unit time |
| **Token usage / Cost per task** ⭐ | Tokens processed / total cost to complete a task |
| **Streaming** ⭐ | Incremental output delivery |
| **Caching / Prompt caching** ⭐ | Reuse results / reuse processed prompt prefix |
| **Semantic cache** | Cache keyed by meaning of query (use carefully) |
| **Graceful degradation** ⭐ | Reduced function instead of total failure |
| **Fallback model** | Alternate model when primary fails |
| **Canary release / Rollback** ⭐ | Small-traffic rollout / revert |
| **Feature flag** | Toggle behavior without redeploying |
| **SLO / SLA / Error budget** | Reliability target / formal commitment / tolerated unreliability |
| **Dead-letter queue (DLQ)** | Holds jobs that repeatedly failed |
| **Drift** | Inputs or behavior shifting over time |
| **Observability tools (know names)** | LangSmith, Langfuse, Arize Phoenix, OpenTelemetry |

---

## 9. Training, fine-tuning, optimization

| Term | Short meaning |
|---|---|
| **Pre-training** | Large-scale initial training |
| **Fine-tuning** | Further training for a task/domain |
| **Instruction tuning** | Training to follow instructions |
| **Transfer learning** | Reusing learned knowledge on a new task |
| **PEFT / LoRA / QLoRA** | Train few parameters / low-rank adapters / LoRA + quantization |
| **Quantization** | Lower numeric precision to save memory/speed |
| **Distillation** | Small student model learns from large teacher |
| **RLHF / DPO** | Human-preference alignment / direct preference training |
| **Synthetic data** | Generated data for training/testing/evals |
| **Model routing** ⭐ | Choose model by task, cost, latency, quality |
| **Model cascading** ⭐ | Cheap model first, escalate hard cases |
| **Inference optimization** | Speed/cost/resource improvements when serving |

> **RAG vs fine-tuning:** RAG gives external context at inference time (good for changing facts, citations, access control). Fine-tuning changes model parameters (good for style/behavior/format). Different problems; can be combined.

---

## 10. Security, safety, governance

| Term | Short meaning |
|---|---|
| **Guardrails** ⭐ | Controls on model inputs, outputs, and actions |
| **Prompt injection** ⭐ | Malicious instructions in user input or retrieved/tool content |
| **Direct vs indirect injection** ⭐ | From the user vs hidden in data the agent reads |
| **Jailbreak** | Attempt to bypass model restrictions |
| **Data leakage / exfiltration** ⭐ | Unauthorized exposure of sensitive data |
| **PII / Redaction** ⭐ | Identifying personal data / masking it |
| **Tenant isolation** ⭐ | One customer's data never reaches another |
| **Audit trail / Audit log** ⭐ | Record of who/what did what and when |
| **Provenance** | Where data/answers came from |
| **Content filtering / Policy enforcement** | Block violating content / apply allow-deny rules |
| **Runtime validation** | Checks during execution |
| **Human approval gate** ⭐ | Explicit authorization before an action proceeds |
| **Blast radius** | Scope of damage if something fails or is breached |
| **Data poisoning** | Corrupting training/knowledge data |
| **Supply chain security** | Protecting dependencies, models, artifacts |
| **Threat modeling** | Identify attackers, threats, mitigations |
| **Excessive agency** | Agent has more power than needed |
| **Confused deputy** | Agent uses its own privileges for a user who lacks them |
| **Tool poisoning** | Malicious tool/MCP descriptions that steer the model |
| **Responsible AI / AI governance** | Safety, fairness, privacy, accountability; policies and oversight |

> **Lethal trifecta:** private data + untrusted content + external communication in one agent = high risk. Break at least one leg.

---

## 11. Advanced and emerging terms

| Term | Short meaning |
|---|---|
| **Reasoning model** | Model optimized for multi-step problem solving |
| **Test-time compute** | Extra computation at inference to improve results |
| **Agentic retrieval** | Agent adapts search strategy, multiple retrieval calls |
| **Semantic router** | Routes requests by meaning/intent |
| **Short-term / Long-term memory** | Context in the current interaction / info kept across sessions |
| **Memory retrieval** | Selecting relevant stored memory for the prompt |
| **Knowledge graph / Graph database** | Entities and relationships / database storing them |
| **Multimodal embedding** | Vectors across modalities |
| **VLM** | Vision-Language Model |
| **OCR** | Extract text from images/scans |
| **STT / TTS** | Speech-to-text / text-to-speech (important for voice/communications products) |
| **Real-time inference** | Responses under tight latency |
| **Speculative decoding** | Draft model proposes tokens, big model verifies |
| **Mixture of Experts (MoE)** | Routes inputs to specialized sub-networks |
| **AI gateway** | Central layer for routing, access control, observability, policy across providers |
| **Computer use / browser agents** | Agents operating UIs through screenshots/clicks |

---

## 12. Business and market buzzwords

| Term | Short meaning |
|---|---|
| **AI-native** | Product designed around AI as the core |
| **Copilot** | AI assistant that helps a human do the task |
| **Autonomous automation** | Decisions and actions with limited human involvement |
| **Workflow automation** | Automating business steps and decisions |
| **Intelligent document processing (IDP)** | AI extraction/classification of document info |
| **Enterprise AI** | AI with security, integration, reliability, governance |
| **AI transformation** | Reworking processes/operating model using AI |
| **Human-AI collaboration / Human oversight** | Complementary work / ability to monitor and intervene |
| **Vertical / Horizontal AI** | Industry-specific / cross-industry |
| **AIaaS** | AI delivered as a managed service |
| **Production-ready AI** | Deployed with monitoring, testing, security, recovery |
| **Scalable AI** | Handles growth within cost/performance limits |
| **AI ROI** | Business value relative to cost |
| **Contact center AI / agent assist** | AI helping service reps live (relevant to RingCentral-style products) |
| **Conversation intelligence** | Analyzing calls/chats for insights, summaries, sentiment |

---

## 13. The 25 terms to memorize first (with definitions)

1. **Agentic workflow:** multi-step process where an LLM-driven agent decides or adapts next steps using tools, within limits.
2. **Orchestration:** coordinating model calls, tools, state and steps so the system behaves reliably.
3. **LangGraph:** framework for stateful graph workflows: nodes, edges, conditional routing, checkpoints, human interrupts.
4. **RAG:** retrieve relevant external data at query time and give it to the LLM so answers are grounded.
5. **Embeddings:** vectors where similar meaning sits close together; the basis of semantic search.
6. **Hybrid search:** vector search plus keyword (BM25) search, fused; best of meaning and exact terms.
7. **Reranking:** re-scoring the retrieved candidates with a more precise model to put the best first.
8. **Function calling:** the model returns a structured request (function name + args); your code validates and executes it.
9. **MCP:** open protocol so AI apps discover and use tools/resources/prompts from servers through a standard interface.
10. **Structured output:** model output constrained/validated to a schema (e.g. JSON) so code can trust it.
11. **Context engineering:** deciding what goes into the model's context (instructions, history, retrieved data, tools) and in what form.
12. **State management:** holding and updating shared data across workflow steps and conversation turns.
13. **Checkpointing:** saving workflow state at each step so runs can resume, replay, or pause for approval.
14. **Human-in-the-loop:** requiring human review or approval at defined steps, especially for risky actions.
15. **Idempotency:** repeating an operation yields the same effect as doing it once, making retries safe.
16. **LLM-as-a-judge:** using an LLM with a rubric to grade outputs; needs calibration against human labels.
17. **Evaluation harness:** code and data that automatically run test cases and compute quality metrics.
18. **Groundedness:** whether each claim in an answer is supported by the provided sources.
19. **LLMOps:** practices to deploy, evaluate, monitor and maintain LLM apps in production.
20. **Observability:** understanding system behavior from traces, logs, metrics and eval results.
21. **Prompt injection:** malicious instructions in user input or retrieved/tool content meant to hijack the model.
22. **Least privilege:** giving each component only the minimum permissions required.
23. **Guardrails:** controls on inputs, outputs and actions (validators, classifiers, policies, approvals).
24. **Model routing:** choosing which model handles a request based on task, cost, latency and quality needs.
25. **Graceful degradation:** keeping reduced functionality when a dependency fails instead of failing completely.

---

## 14. Confusable pairs (quick contrasts)

| Pair | Difference in one line |
|---|---|
| **Agent vs chain** | Agent chooses steps at runtime; chain follows a fixed sequence |
| **Agent vs workflow** | Workflow = predefined path (deterministic); agent = model-directed path |
| **LangChain vs LangGraph** | Components and linear pipelines vs stateful graphs with loops, persistence, HITL |
| **RAG vs fine-tuning** | Adds knowledge at inference time vs changes model behavior via training |
| **RAG vs long context** | Retrieve only what's needed vs stuff everything in (cost, lost-in-the-middle) |
| **Function calling vs MCP** | How the model requests a call vs a standard for packaging/discovering tools |
| **Dense vs sparse retrieval** | Meaning-based vectors vs exact-term keyword matching |
| **Retrieval vs reranking** | Fast broad candidate fetch vs slower precise reordering |
| **Precision vs recall** | Accuracy of what was returned vs coverage of what should be returned |
| **Faithfulness vs correctness** | Supported by the given context vs true in the world |
| **Hallucination vs error** | Unsupported fabrication vs wrong but grounded (e.g. bad source) |
| **Guardrails vs authorization** | Probabilistic checks vs deterministic access control in code |
| **Direct vs indirect prompt injection** | User attacks the prompt vs attack hidden in data the agent reads |
| **Retry vs fallback** | Same operation again vs a different path |
| **Short-term vs long-term memory** | Current interaction context vs persisted across sessions |
| **Checkpoint vs memory** | Workflow execution state vs facts retained for future conversations |
| **Streaming vs batch** | Incremental output (low perceived latency) vs full response (easier validation) |
| **SLO vs SLA** | Internal target vs formal commitment |
| **Latency vs throughput** | Time per request vs requests per time |
| **Model routing vs cascading** | Pick one model up front vs try cheap first, escalate if needed |
| **Prompt caching vs semantic caching** | Reuse processed prompt prefix vs reuse answers for similar queries |
| **Evals vs unit tests** | Statistical quality measurement on non-deterministic output vs deterministic pass/fail |
| **Online vs offline evals** | Live traffic monitoring vs fixed datasets before release |
| **Copilot vs agent** | Assists a human in the loop vs acts more autonomously |

---

## 15. Acronym decoder

| Acronym | Meaning |
|---|---|
| LLM | Large Language Model |
| SLM | Small Language Model |
| RAG | Retrieval-Augmented Generation |
| HITL | Human-in-the-loop |
| MCP | Model Context Protocol |
| ANN | Approximate Nearest Neighbor |
| HNSW | Hierarchical Navigable Small World (graph index) |
| BM25 | Best Matching 25 (keyword ranking) |
| RRF | Reciprocal Rank Fusion |
| LCEL | LangChain Expression Language |
| TTFT | Time To First Token |
| p95 / p99 | 95th / 99th percentile latency |
| SLO / SLA | Service Level Objective / Agreement |
| PEFT / LoRA / QLoRA | Parameter-Efficient Fine-Tuning / Low-Rank Adaptation / Quantized LoRA |
| RLHF / DPO | Reinforcement Learning from Human Feedback / Direct Preference Optimization |
| MoE | Mixture of Experts |
| VLM | Vision-Language Model |
| OCR | Optical Character Recognition |
| STT / TTS | Speech-to-Text / Text-to-Speech |
| PII | Personally Identifiable Information |
| RBAC / ABAC | Role-based / Attribute-based Access Control |
| OAuth | Open Authorization (delegated access) |
| IDP | Intelligent Document Processing (or Identity Provider, depending on context) |
| DLQ | Dead-Letter Queue |
| CDC | Change Data Capture |
| CI/CD | Continuous Integration / Continuous Delivery |
| SSE | Server-Sent Events (one-way streaming) |
| RLS | Row-Level Security |
| ROI | Return on Investment |

---

## 16. How the terms connect in one production agent (say this story)

> "A user request hits an **API**, where we authenticate and apply **tenant isolation**. An **orchestrator** built on **LangGraph** manages **state** with **checkpointing**. **Context engineering** assembles the instructions and history. A **router** picks the workflow and **model** (**model routing**). If knowledge is needed, **RAG** runs **hybrid search** with **metadata filtering**, then **reranking**, returning **grounded** context with citations. For actions, the model uses **function calling** through a **tool registry** (possibly **MCP**); the backend does **schema validation**, **authorization** (**least privilege**), and executes **idempotent** calls with **timeouts**, **retries with backoff**, and a **circuit breaker**. Risky writes pass a **human approval gate**. **Guardrails** check inputs and outputs. Everything is **traced** and **audit-logged**. Offline, an **evaluation harness** with a **golden dataset** measures **task success, tool-call accuracy and faithfulness**, gated in CI; online we watch **latency, cost per task and failures**, rolling out changes by **canary release** with **rollback**."

Practice saying this in about 60-90 seconds. It covers most of the JD.

---

## 17. Sounding natural in the interview

**Don't say:**
> "I use AI and LLMs to make the application intelligent."

**Say (only if true for you; otherwise phrase it as "here's how I would design it"):**
> "I use a RAG pipeline to ground responses in enterprise data, LangGraph to orchestrate multi-step workflows, and structured tool calling to integrate backend services. I evaluate task success and tool-call accuracy, while tracing latency, failures, and token costs in production."

**Tips**
- Define a term in one plain sentence before going deep.
- Attach each term to a decision or trade-off ("I chose hybrid search because our data has product codes").
- If you haven't used a term hands-on, say "I understand it conceptually and here's how I'd apply it."
- Prefer measurement language: "I'd measure it with…".
- Don't stack more than 2-3 buzzwords in one sentence.

**Final reminder:** Learn definitions first, then practise explaining how 5-6 of these concepts work together in one agent (Section 16). That beats memorizing hundreds of disconnected terms.














---

---

# GenAI and AI Terminology: Comprehensive Production Playbook (Interview Edition)

> The definitive master glossary of GenAI, Agentic LLM Architecture, and LLMOps terms compiled for Senior Systems Engineering interviews. 
> **⭐ = Core High-Priority Terminology.** Focus heavily on these choices during technical architectural discussions.

---

## Contents
1. Core AI and LLM Foundations
2. Prompting, Context Control, and Output Constraints
3. Retrieval-Augmented Generation (RAG) and Vector Search
4. Advanced Retrieval Optimization
5. Autonomous Agents and Agentic Workflows
6. Enterprise Tool Governance and API Integration
7. Frameworks, State Management, and Orchestration
8. LLMOps, Observability, and Production Monitoring
9. Training, Fine-Tuning, and Model Optimization
10. Security, Safety, and Governance
11. Advanced Architecture and Emerging Paradigms
12. Enterprise Readiness and Market Dynamics
13. The 35 Master Terms to Memorize First
14. High-Stakes Confusable Pairs (Interview Traps)
15. Complete Acronym Decoder
16. Production-Grade Agentic Architecture Blueprint
17. Interview Communication Strategy: Speaking Like a Lead Architect

---

## 1. Core AI and LLM Foundations

| Term | Engineering Definition & Production Context |
|---|---|
| **GenAI** ⭐ | Generative Artificial Intelligence: Deep learning architectures optimized to construct brand-new, high-dimensional content vectors (text, images, audio, source code) by sampling learned probability distributions rather than analyzing or classifying existing datasets. |
| **LLM** ⭐ | Large Language Model: Massively parameterized transformer-based neural network variants designed to process sequence-to-sequence tokens, predicting the most statistically probable subsequent token based on billions of parameters. |
| **Foundation Model** | A highly scaled, foundational model checkpoint pre-trained on diverse, non-specific corpora at massive compute scale, acting as an adaptable base for downstream specializations or specialized context framing. |
| **Transformer** | The ubiquitous neural architecture utilizing self-attention mechanisms to weigh the dynamic mathematical relationships of non-contiguous tokens across an entire sequence concurrently, replacing historical recurrent models (RNNs/LSTMs). |
| **Token** ⭐ | The atomic unit of text processing (a character string, word fragment, or full word) mapped to a specific numerical index within a model's embedding dictionary. In production, API expenditures, performance speed, and hard context bounds are tracked and billed purely via token quantities. |
| **Tokenization** | The deterministic pre-processing execution stage where raw string inputs are parsed, segmented, and mapped via an encoder (e.g., Byte-Pair Encoding) into a structured array of token identifiers digestible by the neural network layers. |
| **Context Window** ⭐ | The physical maximum token threshold (encompassing the collective sum of system prompts, chat histories, retrieved context segments, and the final output payload) that an LLM architecture can ingest and process during a single mathematical inference loop. |
| **Inference** | The operational execution runtime phase where a compiled, frozen model checkpoint evaluates a prompt matrix through its hidden layers to generate an output distribution without altering its underlying weights. |
| **Multimodal** | Neural architectures possessing distinct input encoders or unified token spaces capable of natively ingesting and cross-referencing multiple diverse data types (e.g., interleaving text strings, structural images, audio streams, and video files) inside a single inference cycle. |
| **SLM** | Small Language Model: A deliberately compact model checkpoint (typically sub-10 billion parameters) distilled to execute highly narrow tasks with minimal VRAM footprints, drastically decreasing operational inference costs. |
| **Frontier Model** | An industry-standard designation for the latest, highly capable generation of foundational models pushing the absolute technical boundaries of multi-step logical reasoning and capability at the current point in time. |
| **Open-Weight Model** | A model distribution pattern where the trained neural network parameter weights are publicly downloadable and self-hostable, subject to specific commercial usage licensing agreements (e.g., Meta's Llama family). |
| **Hallucination** ⭐ | The generation of syntactically fluent and structurally cohesive token sequences that possess no factual anchoring or statistical correlation to either the provided context window or valid external reference realities. |
| **Knowledge Cutoff** | The fixed chronological timestamp marking the exact boundaries of a foundational model’s pre-training corpus, after which the model possesses zero structural memory of historical occurrences unless explicitly supplemented via external data streams. |

---

## 2. Prompting, Context Control, and Output Constraints

| Term | Engineering Definition & Production Context |
|---|---|
| **Prompt Engineering** ⭐ | The programmatic discipline of structuring, sequencing, and optimizing instruction blocks, environmental variables, and programmatic instructions to minimize behavioral stochasticity and guide the LLM toward dependable outputs. |
| **System Prompt** ⭐ | The highest-priority, structural instruction wrapper injected at the root of an inference sequence to hardcode the agent's core role, behavioral boundaries, error paths, tool usage paradigms, and execution constraints. |
| **Zero-Shot / Few-Shot** ⭐ | *Zero-Shot:* Prompting a model to complete an execution relying entirely on its underlying weights without structural target examples. *Few-Shot:* Embedding explicit target input-output pairs inside the prompt payload to align the model with complex formatting or specific tonal patterns. |
| **Chain-of-Thought (CoT)** | An instruction methodology forcing the model to emit an explicit, step-by-step logical decomposition of its reasoning process within a hidden text block or visible scratchpad prior to generating its final answer token. |
| **Prompt Template** | A reusable, parameterized string structure containing static instruction sets interspersed with dynamic variable placeholders, managed programmatically within orchestration pipelines to standardize runtime user inputs. |
| **Structured Output** ⭐ | Forcing an LLM to generate its response payload in absolute alignment with a predetermined software schema (such as a rigorous JSON blueprint or Pydantic class) to ensure seamless parsing by downstream application logic. |
| **JSON Schema** ⭐ | The formal, declarative validation specification detailing the precise object properties, data types, required fields, and structural array boundaries that an LLM's generated payload must strictly comply with. |
| **Constrained Decoding** | A low-level inference technique that dynamically masks the model's token selection probability distribution at the logit level during generation, ensuring that only tokens fulfilling an active JSON schema or grammar can be legally chosen. |
| **Temperature** | A hyperparameter scaling the model's logit outputs prior to token selection; low settings (approaching 0) yield deterministic, highly repetitive token choices, while high settings increase generation diversity and randomness. |
| **Top-p (Nucleus Sampling)** | An inference parameter that restricts the model's token selection pool to the smallest collective subset of high-probability tokens whose cumulative percentage sum reaches the target threshold `p`, smoothing out erratic tail-end generations. |
| **Prompt Chaining** | An architectural pipeline pattern where a complex objective is split into separate, sequential model requests, where the validated structured output of step `N` is dynamically injected into the system template of step `N+1`. |
| **Context Engineering** ⭐ | The strategic management, curation, and dynamic formatting of the entire runtime token payload sent to an LLM, including systemic constraints, historical conversation segments, active tool parameters, and highly ranked RAG outputs. |
| **Prompt Versioning** | The infrastructure practice of checking prompt templates into version control systems (e.g., Git or specialized prompt registries) alongside rigorous semantic tags to ensure application behavior remains testable, deterministic, and auditable across model upgrades. |

---

## 3. Retrieval-Augmented Generation (RAG) and Vector Search

| Term | Engineering Definition & Production Context |
|---|---|
| **RAG** ⭐ | Retrieval-Augmented Generation: An architecture that intercepts a user query, fetches relevant factual documents from an external indexing engine at runtime, and injects those documents directly into the LLM's active context window to ground its generation in verifiable facts. |
| **Embedding** ⭐ | The dense, low-dimensional mathematical vector representation of a textual asset within a continuous multi-dimensional space, where the spatial proximity (geometric distance) between vectors reflects the underlying semantic meaning of the tokens. |
| **Vector Database** ⭐ | A highly specialized storage layer custom-built to index, manage, and perform multi-dimensional spatial calculations (e.g., Cosine, Dot Product, or Euclidean distances) across millions of embedding vectors at sub-millisecond latencies. |
| **Semantic Search** | An information-retrieval pattern that uncovers matching documents based on conceptual intent and context alignment through vector space proximity, successfully bypassing the rigid constraints of exact keyword matching. |
| **Chunking** ⭐ | The deterministic data pipeline stage where expansive, unstructured text resources are systematically split into smaller, cohesive blocks (chunks) based on token counts, structural markdown boundaries, or semantic splitters to fit within retrieval windows. |
| **Chunk Overlap** | A sliding window parameter specifying the deliberate number of identical tokens preserved across consecutive text chunks to prevent the fragmentation of critical contextual facts at boundary lines. |
| **Similarity Search / ANN** | Approximate Nearest Neighbor: A class of highly optimized geometric search algorithms (such as Hierarchical Navigable Small World - HNSW) designed to traverse complex high-dimensional vector spaces and find nearest matches rapidly by balancing a negligible trade-off in mathematical precision. |
| **Cosine Similarity** | A geometric metric measuring the cosine of the angle between two multi-dimensional vectors, quantifying semantic equivalence independent of the total raw length of the documents being compared. |
| **Hybrid Search** ⭐ | An enterprise retrieval pattern that runs an exact keyword-based match (e.g., BM25) and an abstract semantic vector search concurrently, blending the divergent scoring outputs into a single, comprehensive results stream. |
| **BM25** | A classic, probabilistic keyword ranking algorithm that calculates document relevance based on the term frequency and inverse document frequency of specific query strings within a given corpus. |
| **Reranking** ⭐ | A secondary, high-fidelity optimization stage that passes the top candidate documents retrieved from an initial search through a specialized cross-encoder neural model to calculate absolute relevance scores and filter out noise before context injection. |
| **Metadata Filtering** ⭐ | The execution of relational boolean queries (e.g., `WHERE tenant_id == 'XYZ'`) directly against a vector store's indexed attributes, shrinking the mathematical vector calculation pool to enforce security isolation and absolute multi-tenant bounds. |
| **Query Rewriting** | Utilizing a fast LLM node at the ingress point of a retrieval pipeline to analyze a conversational user query, strip out conversational filler, correct ambiguities, and re-architect the prompt into multiple optimized search keys. |
| **HyDE** | Hypothetical Document Embeddings: An advanced retrieval pattern that instructs an LLM to generate a fake, ideal answer to a user's question, using the embedding vector of *that generated response* to run the vector database query instead of using the raw user question. |
| **Grounding** ⭐ | The engineering process of ensuring that an LLM's conversational output is structurally anchored to and justified by validated reference facts provided within its active prompt context, eliminating speculative internal extrapolation. |
| **Citations / Attribution** | Programmatically appending verified metadata pointers (e.g., file paths, document IDs, or exact chunk hyperlinks) directly alongside generated text blocks to allow human operators to audit the exact source of a claim. |
| **GraphRAG** | An advanced retrieval topology that extracts structured entity networks and relationship nodes (knowledge graphs) from an unstructured corpus, allowing an agent to traverse relational links and understand complex, distributed enterprise knowledge bases. |
| **Retrieval Precision / Recall** ⭐ | *Precision:* The ratio of highly relevant chunks retrieved to the total number of chunks returned. *Recall:* The ratio of relevant chunks successfully discovered to the absolute volume of relevant data buried across the entire database. |
| **MMR** | Maximal Marginal Relevance: A vector query refinement algorithm designed to optimize for both high document relevance and low data redundancy, deliberately diversifying the retrieved chunks to maximize informational variance within the prompt. |
| **Lost in the Middle** | A known transformer behavioral phenomenon where models exhibit high contextual awareness for tokens situated at the absolute beginning or end of a massive prompt context, but fail to compute or reason over facts located in the center. |

---

## 4. Advanced Retrieval Optimization

| Term | Engineering Definition & Production Context |
|---|---|
| **Parent-Child Chunking** | An elegant RAG configuration where documents are sliced into very small, granular fragments (children) to optimize mathematical vector searches, but upon matching, the system pulls a broader enclosing text frame (the parent) to pass to the LLM for rich context. |
| **Query Deconstruction / Sub-Queries** | The practice of programmatically parsing a compound user request into separate, independent sub-questions that are executed in parallel across distinct vector stores, databases, or API integrations, aggregating the outputs at the end. |
| **Reciprocal Rank Fusion (RRF)** ⭐ | A standard algorithm used to merge multiple distinct information retrieval result sets (such as combining a BM25 keyword list with an ANN vector list) by scoring documents purely based on their relative positional ranks within each individual stream. |
| **Self-RAG / Self-Correction** | An active agent loop pattern where an intermediate model node evaluates the semantic utility of its own retrieved chunks; if the data fails an internal relevance evaluation, the agent loops back, rewrites its search query, and tries again. |

---

## 5. Autonomous Agents and Agentic Workflows

| Term | Engineering Definition & Production Context |
|---|---|
| **AI Agent** ⭐ | An autonomous software entity composed of a core language model acting as the cognitive engine, integrated with runtime state containers, external memory banks, and a formal registry of tools to fulfill long-term objectives without static coding. |
| **Agentic AI** ⭐ | Software architectures that transcend simple prompt-response patterns, displaying systemic capability to plan execution vectors, select variable external applications, react to runtime feedback, and loop until goals are met. |
| **Agentic Workflow** ⭐ | An architectural design pattern that structures execution into multi-step, iterative loops where the specific path of the application is dynamically adjusted by the model’s internal reasoning rather than hardcoded logic. |
| **Agent Loop** ⭐ | The foundational execution cycle of autonomous systems: evaluate active state $
ightarrow$ decide on a tool or text action $
ightarrow$ execute the choice $
ightarrow$ observe the environmental feedback $
ightarrow$ determine whether to stop or repeat. |
| **Tool Calling / Function Calling** ⭐ | The native capability of an LLM to parse a natural language query against a selection of code functions, outputting a precise JSON payload matching the arguments of a specific function rather than standard conversational text. |
| **Tool Registry** ⭐ | A declarative centralized library exposing all available code execution tools, microservices, and API schemas to an agent, complete with explicit, natural language docstrings that the model evaluates to understand *when* and *how* to use them. |
| **Orchestration** ⭐ | The systematic coordination of models, data structures, state changes, human approval breaks, and tool loops across an enterprise application lifecycle. |
| **Planner / Executor** | An agentic design pattern that decouples the architecture into two roles: a high-capability **Planner** model that builds an explicit execution roadmap, and a fast, low-cost **Executor** model that invokes the requested tools in sequence. |
| **ReAct** ⭐ | Reason and Act: A standardized agent prompting loop pattern that instructs the model to iteratively output a "Thought" line detailing its logical deduction, an "Action" line executing a tool call, and an "Observation" line consuming the tool's raw result. |
| **Plan-and-Execute** | An execution strategy where the agent explicitly constructs a multi-step checklist upfront, then systematically steps through each node sequentially, minimizing recursive overhead and erratic path-switching. |
| **Reflection** | An iterative optimization node where an agent is forced to ingest its own completed draft output, check it against a strict rubric or compiler log, and write an improved version before finalizing the payload. |
| **Multi-Agent System** ⭐ | An enterprise system topology consisting of multiple, distinct agent nodes collaborating within a structured network, where each node possesses localized tools, custom system instructions, and specialized domain expertise. |
| **Supervisor Agent / Sub-Agent** | A hierarchical multi-agent pattern where a central **Supervisor Agent** evaluates user goals, dynamically routes tasks to specialized **Sub-Agents**, handles task aggregation, and maintains overall system state. |
| **Handoff** | The transactional mechanism of transferring the active execution state, session variables, and conversation routing control from one specific agent to a completely different specialized agent node. |
| **Human-in-the-Loop (HITL)** ⭐ | The intentional placement of a hard programmatic break at a high-risk node within an autonomous graph, forcing the runtime thread to pause and wait for explicit human modification or approval before executing downstream changes. |
| **Autonomy Boundary** | The hard-coded operational parameter defining the absolute limits of an agent's self-directed execution capabilities (e.g., restricting financial actions to a fixed monetary cap) before triggering a forced human approval check. |
| **Stopping Condition** | A set of strict deterministic constraints (e.g., reaching maximum step counts, hitting tool error thresholds, or detecting success tags) that force an agentic loop to terminate immediately to avoid infinite runtime billing. |
| **Deterministic Workflow** ⭐ | A rigid application pipeline where routing paths, data formatting, and business rules are completely hard-coded via traditional source code, utilizing LLM nodes purely for isolated data transformations. |
| **Router** | A classification node (either programmatic or a rapid model call) that analyzes an incoming payload and instantly directs the request down a specific conditional edge within the application graph. |
| **A2A (Agent-to-Agent)** | The emerging network protocols, data exchange formats, and communication schemas allowing heterogeneous autonomous agent nodes to negotiate goals and exchange payloads across network boundaries. |

---

## 6. Enterprise Tool Governance and API Integration

| Term | Engineering Definition & Production Context |
|---|---|
| **MCP (Model Context Protocol)** ⭐ | An open, standard protocol establishing uniform client-server communication paradigms for exposing secure data inputs, prompt layouts, and tool invocation hooks to language models. |
| **Tool Execution Environment** | The highly isolated, sandboxed runtime container (e.g., gRPC microservice, ephemeral Docker workspace, or secure Lambda instance) where agent-requested tool code executes safely away from core application infrastructure. |
| **Idempotency Key** ⭐ | A unique transactional identifier passed alongside an agent's tool call ensuring that recursive loops or automatic framework retries never trigger accidental, duplicate side-effects on state-changing external APIs (e.g., making dual phone calls or charges). |
| **Rate Limiting / Throttling** ⭐ | Traffic control mechanisms applied to agentic tool calls to ensure that autonomous loops do not overwhelm downstream internal microservices or exhaust external API quotas during highly recursive execution paths. |
| **Circuit Breaker Pattern** ⭐ | An automated stability pattern that monitors tool failures; if a tool exceeds an error threshold, the system trips the breaker, bypassing future calls to protect overall agent response times. |
| **Semantic API Description** | High-precision descriptions (e.g., OpenAPI specs with detailed docstrings) that the LLM uses to understand *when* and *how* to call an API. |
| **Tool RAG / Dynamic Tool Selection** ⭐ | Storing hundreds of tool definitions in a vector database and retrieving only the top 5 relevant schemas to inject into the prompt, avoiding context bloat. |
| **Token Buckets for Agents** | Client-side tracking logic that enforces severe rate-limiting constraints on autonomous loops, preventing runaway agents from consuming too many tokens. |
| **Asynchronous Tool Execution** | Allowing an agent to invoke a long-running external job, yielding the thread, and letting a webhook wake the agent graph back up when complete. |
| **Human-in-the-loop (HITL) Injection** | The reverse of standard HITL: allowing a human supervisor to dynamically inject a tool correction payload into an active, paused graph state before it resumes. |

---

## 7. Frameworks, State Management, and Orchestration

| Term | Engineering Definition & Production Context |
|---|---|
| **LangChain** ⭐ | An open-source development ecosystem providing standardized abstractions for chaining prompt templates, model connectors, parsing utilities, and RAG components into structured pipelines. |
| **LangGraph** ⭐ | A stateful, graph-centric orchestration library built on top of LangChain, explicitly designed to model cyclical agent paths, handle multi-agent routing, enforce persistent state tracking, and manage complex human approval loops. |
| **LCEL** | LangChain Expression Language: A declarative, functional syntax enabling engineers to compose complex, multi-component LLM sequences with built-in support for streaming, batching, and async handling out-of-the-box. |
| **Chain** | A linear, directional sequence of connected execution blocks where data flows strictly forward from a prompt component to a model call, and finally through an output parser. |
| **Node / Edge / Conditional Edge** ⭐ | *Node:* An explicit function or processing step in a LangGraph graph. *Edge:* A static directional connection between steps. *Conditional Edge:* A dynamic routing path selected at runtime based on the evaluation of active state data. |
| **State** ⭐ | The centralized, single-source-of-truth data object shared across an entire orchestration graph, accessible by all active nodes and tracking execution history across a session. |
| **State Reducer** | An explicit, deterministic function that defines exactly how new outputs generated by a node are merged into the graph's overarching **State** object (e.g., appending a message to an existing list without overwriting history). |
| **Checkpointing** ⭐ | The automated serialization and database persistence of an agentic graph's complete state vector at every step boundary, enabling transaction rollbacks, multi-session resilience, and long-term memory retrieval. |
| **Thread ID** | A unique execution partition key used by checkpointers to map, track, isolate, and recover specific user conversation sessions across stateless distributed compute networks. |
| **Persistence / Durable Execution** ⭐ | An architectural guarantee that an agentic workflow's operational memory survives mid-run compute drops or backend restarts by reading from a non-volatile checkpoint database to resume gracefully. |
| **Workflow Interrupt** | A scheduled, intentional pause built into an orchestration graph that serializes state and halts execution until an external API call or human approval event signs off on continuation. |
| **Recursion Limit** | A hard safety rail configured on an orchestration engine that counts graph node transitions and violently terminates execution if a loop exceeds a set limit, preventing infinite loops. |
| **Subgraph** | A fully contained orchestration graph nested completely within an individual node of a parent graph, promoting architectural modularity and clean multi-agent isolation. |
| **LangSmith** | A specialized cloud platform built for testing, optimizing, logging, and running analytics on LLM applications by tracing every single step of an orchestration pipeline. |

---

## 8. LLMOps, Observability, and Production Monitoring

| Term | Engineering Definition & Production Context |
|---|---|
| **Tracing** ⭐ | The end-to-end logging of an asynchronous agent's tree of operations—capturing inputs, intermediate thoughts, precise API payloads, latencies, and token costs for every step. |
| **Semantic Caching** ⭐ | An optimization strategy that uses vector databases to intercept user queries, returning cached responses if the input matches a past request's semantic intent closely enough. |
| **Streaming (SSEs)** ⭐ | Delivering generated tokens to the client in real-time via Server-Sent Events, hiding latency and improving user experience. |
| **Cost Tracking / Attribution** | Programmatically calculating token consumption per user, team, or specific component to monitor margins and budget compliance. |
| **Fallback Strategy** ⭐ | An automated backup plan (e.g., switching to an alternative model or entering a graceful degradation mode) when the primary LLM fails or times out. |
| **Prompt Drift** | A shift in application behavior or performance when a foundational model provider updates their underlying weights behind a static API endpoint. |
| **Semantic Monitoring** | Tracking production logs using embeddings or clustering to detect new patterns of user queries or system failures in real-time. |
| **Cold Start / Time to First Token (TTFT)** | The latency measured from the user's initial request to the moment the LLM emits its very first output token. |
| **Semantic Drift / Concept Drift** | The erosion of embedding or classification accuracy over time as production data characteristics shift away from the baseline training data. |
| **Synthetic Data Generation** | Using frontier models to generate thousands of realistic user edge-cases, failure modes, and conversations to build your **Golden Dataset**. |
| **Cost-to-Resolution (CTR)** ⭐ | A business-critical engineering metric tracking the cumulative token spend across an entire multi-step agent loop required to successfully close a user's task. |

---

## 9. Training, Fine-Tuning, and Model Optimization

| Term | Engineering Definition & Production Context |
|---|---|
| **Fine-Tuning** | Training a pre-trained model on a specific dataset to adapt its style, tone, or compliance with specialized structural syntax. |
| **LoRA / QLoRA** | Low-Rank Adaptation: An optimization technique that freezes base model weights and trains a small set of adapter layers, slashing VRAM needs. |
| **PEFT** | Parameter-Efficient Fine-Tuning: Methods (like LoRA) that fine-tune models by updating only a tiny fraction of total parameters. |
| **Distillation** | Transferring knowledge from a massive "teacher" model to a smaller, faster "student" model to reduce latency and infrastructure costs. |
| **Quantization** ⭐ | Reducing the numerical precision of model weights (e.g., from 16-bit floats to 8-bit or 4-bit integers) to minimize memory footprint and boost inference speed. |
| **RLHF / RLAIF** | Reinforcement Learning from Human (or AI) Feedback: Post-training alignment techniques used to make models safer and more helpful. |
| **Context Window Extension** | Engineering methods (like RoPE scaling) used to stretch a model’s operational context capacity beyond its initial training configuration. |

---

## 10. Security, Safety, and Governance

| Term | Engineering Definition & Production Context |
|---|---|
| **Prompt Injection** ⭐ | A vulnerability where malicious user inputs trick the LLM into ignoring system instructions and executing unauthorized actions. |
| **Indirect Prompt Injection** ⭐ | When an agent processes untrusted external data (like an email or web page) containing hidden instructions meant to hijack the agentic loop. |
| **PII Redaction / Masking** ⭐ | The automated stripping or obfuscating of Personally Identifiable Information before it is sent to external LLM provider endpoints. |
| **Guardrails** ⭐ | Programmable validation layers (e.g., NeMo Guardrails, Llama Guard) acting between the user, the model, and the tools to block unsafe inputs/outputs. |
| **Data Leakage** | Accidentally introducing sensitive proprietary or user data into the model’s context or training sets, exposing it to unauthorized third parties. |
| **Jailbreaking** | The art of crafting prompts that bypass the safety alignments embedded inside an LLM, forcing it to generate prohibited content. |
| **Model Lineage / Provenance** | The formal auditing trail documenting the exact dataset versions, base weights, and fine-tuning steps used to deploy a model. |
| **RBAC for Agents** ⭐ | Role-Based Access Control explicitly mapped to agent tools, ensuring an agent cannot execute a function its current user isn't cleared for. |
| **Prompt Leakage** | A security failure where an attacker tricks the model into spitting out its internal **System Prompt**, exposing proprietary business logic or tool schemas. |

---

## 11. Advanced Architecture and Emerging Paradigms

| Term | Engineering Definition & Production Context |
|---|---|
| **Time-Travel / Forking** ⭐ | The ability to rewind an agentic workflow to a past checkpoint, modify the state variable or user intent, and branch a new execution path forward. |
| **Map-Reduce (Agentic)** | Branching a single state array into multiple concurrent tool/agent executions and aggregating the results back into a single state object. |
| **Short-Term vs. Long-Term Memory** | *Short-term:* Session state inside the current context window or thread graph. *Long-term:* Persisted user preferences/historical facts saved across weeks/months in an external DB and pulled via RAG. |
| **Token Eviction / Dynamic Truncation** ⭐ | A memory-management strategy that programmatically drops old conversation history or lower-priority tool logs when the graph state approaches the model's **Context Window** limit. |
| **Stateful Agents** ⭐ | Agents designed to preserve session memory, intermediate variables, and environmental state indefinitely across distinct interactions. |
| **Long-Context Reasoning** | The specific capability of models to maintain high retrieval and logical fidelity when evaluating hundreds of thousands of context tokens at once. |
| **Agentic Mesh / Fabric** | A decentralized infrastructure pattern where multiple specialized agents communicate dynamically across network boundaries using unified protocols. |
| **Cognitive Architecture** ⭐ | The structural design of an AI system's thinking process—governing how state, memory, planning models, and tools interact over time. |
| **Self-Correction Loop** | An autonomous sequence where an agent validates its own execution errors (e.g., a database syntax error) and refines its next step to fix it. |
| **Liquid / Dynamic Prompts** | Prompts that alter their own structural composition in real-time based on live context, user intent analysis, and system states. |
| **Air-Gapped LLM Execution** | Hosting open-weight frontier models entirely on internal corporate private clusters with absolute isolation from the public internet. |

---

## 12. Enterprise Readiness and Market Dynamics

| Term | Engineering Definition & Production Context |
|---|---|
| **Agentic ROI** ⭐ | The quantifiable business value generated by replacing manual work with autonomous agent workflows. |
| **Time-to-Value (TTV)** | The velocity with which an engineering team can move a GenAI concept from initial prototype into a stable, value-generating production state. |
| **Enterprise Readiness** | The benchmark status of an AI application meeting corporate compliance, high availability, strict security, and operational scaling targets. |
| **Sovereign AI** | The strategic deployment of AI infrastructure, models, and data fully localized within a specific nation's borders or a company's private cloud. |
| **Human-AI Co-pilot** | A collaboration paradigm where an AI assists a professional in real-time but leaves ultimate decision-making authority to the human operator. |
| **Shadow AI** | The unauthorized, unmonitored use of public consumer AI tools or third-party APIs by employees within an organization's corporate network. |

---

## 13. The 35 Master Terms to Memorize First

If you get squeezed on time during prep, prioritize these 35 terms. They form the foundational lexicon of production system architecture.

1. **Agentic Workflow** ⭐
2. **Context Window** ⭐
3. **Tool Calling / Function Calling** ⭐
4. **Structured Output** ⭐
5. **Persistence / Durable Execution** ⭐
6. **RAG (Retrieval-Augmented Generation)** ⭐
7. **Embedding** ⭐
8. **Vector Database** ⭐
9. **Hybrid Search** ⭐
10. **Reranking** ⭐
11. **Metadata Filtering** ⭐
12. **Groundedness** ⭐
13. **Human-in-the-Loop (HITL)** ⭐
14. **Deterministic Workflow** ⭐
15. **State / State Reducer** ⭐
16. **Checkpointing** ⭐
17. **Model Context Protocol (MCP)** ⭐
18. **Idempotency Key** ⭐
19. **Circuit Breaker Pattern** ⭐
20. **LLM-as-a-Judge** ⭐
21. **Golden Dataset** ⭐
22. **Tracing** ⭐
23. **Semantic Caching** ⭐
24. **Prompt Injection / Indirect Injection** ⭐
25. **RBAC for Agents** ⭐
26. **Time-Travel / Forking** ⭐
27. **Token Eviction / Dynamic Truncation** ⭐
28. **Tool RAG / Dynamic Tool Selection** ⭐
29. **Reciprocal Rank Fusion (RRF)** ⭐
30. **Cost-to-Resolution (CTR)** ⭐
31. **PII Redaction / Masking** ⭐
32. **Guardrails** ⭐
33. **Token** ⭐
34. **LangGraph** ⭐
35. **Streaming (SSEs)** ⭐

---

## 14. High-Stakes Confusable Pairs (Interview Traps)

* **Fine-Tuning vs. RAG**
  * *Fine-Tuning:* Alters internal model weights to master formatting, stylistic tone, or distinct domain syntax. It **cannot** be trusted for real-time fact recall and suffers from static knowledge cutoffs.
  * *RAG:* Injects real-time, external data dynamically into a frozen model's context window. It provides immediate fact accuracy and auditability but does not teach the model new stylistic capabilities.
* **Tool Calling vs. Agentic Workflow**
  * *Tool Calling:* The isolated act of an LLM inspecting a schema and outputting a single structured request for an external function. It is a single capability.
  * *Agentic Workflow:* The overarching cognitive framework that wraps tool calling inside loops, evaluations, and stateful decisions to execute multi-step objectives over time.
* **State vs. Context Window**
  * *State:* The total database record of variables, history, and system flags managed by your application orchestration layer.
  * *Context Window:* The strict operational hardware limit of tokens that can actually be sent to the LLM API endpoint for a single calculation pass.
* **Semantic Search vs. Keyword Search**
  * *Semantic Search:* Utilizes vector embeddings to match concepts based on absolute meaning, abstracting away the exact words used.
  * *Keyword Search (BM25):* Matches exact text strings, structural characters, and specific product names. It excels at parsing technical identifiers where concept matching fails.
* **Deterministic Routing vs. LLM Routing**
  * *Deterministic Routing:* Traditional code logic (`if/else` statements or edge conditions based on programmatic variables) directing the system path with absolute certainty.
  * *LLM Routing:* Relying on the model's internal reasoning to select the ideal next node or agent out of a group of possibilities.
* **Prompt Injection vs. Jailbreaking**
  * *Prompt Injection:* Hijacking an agent's functional path by tricking it into ignoring system rules to perform an unauthorized task.
  * *Jailbreaking:* Tricking the underlying LLM into entirely breaking past its core safety alignments to discuss prohibited topics or generate dangerous content.
* **Zero-Shot vs. Few-Shot**
  * *Zero-Shot:* Presenting a task to the LLM with instructions alone, relying completely on its pre-trained understanding to deduce the execution style.
  * *Few-Shot:* Including several structured examples of inputs paired with correct outputs inside the prompt text, guiding the model on the exact pattern expected.

---

## 15. Complete Acronym Decoder

* **LCEL:** *LangChain Expression Language* — A declarative syntax pattern engineered to compose distinct software chains cleanly with native streaming and batch support.
* **MCP:** *Model Context Protocol* — An open-source architecture defining how client hosts provide secure access to tools, resources, and prompt building blocks.
* **RAG:** *Retrieval-Augmented Generation* — The process of bolstering an LLM prompt with targeted snippets extracted from an external indexing engine.
* **HITL:** *Human-in-the-Loop* — An explicit application break point where human validation must occur before critical downstream system state changes can run.
* **TTFT:** *Time to First Token* — The concrete latency metric measuring the duration between shipping an API payload and receiving the first generated piece of output.
* **LoRA:** *Low-Rank Adaptation* — A parameter-efficient fine-tuning approach that injects low-rank matrices into transformer layers to optimize models at low hardware costs.
* **PEFT:** *Parameter-Efficient Fine-Tuning* — The collective family of optimization strategies that adjust a minimum threshold of model weights to save time and compute.
* **JSON:** *JavaScript Object Notation* — The ubiquitous data exchange language used for structured output definitions in agent tool communication.
* **SSE:** *Server-Sent Events* — A lightweight, unidirectional push technology enabling agents to stream token blocks down to frontend interfaces over long-lived HTTP connections.
* **ANN:** *Approximate Nearest Neighbor* — The class of mathematical algorithms used to query high-dimensional vector spaces rapidly by sacrificing minimal accuracy for speed.
* **MMR:** *Maximal Marginal Relevance* — A selection algorithm that penalizes redundant information during vector retrieval stages to maximize data variety within the prompt context window.
* **HyDE:** *Hypothetical Document Embeddings* — An advanced RAG pattern that prompts an LLM to generate a theoretical answer string, using *that* generated string's vector to perform the database search rather than the raw question.
* **RBAC:** *Role-Based Access Control* — A security architecture that maps user roles to specific permissions, used in agent design to govern access to tool registries.
* **RRF:** *Reciprocal Rank Fusion* — A sorting routine that balances search hits from multi-source indexes by treating positions as primary scoring factors.
* **CTR:** *Cost-to-Resolution* — The absolute financial measurement of API token depletion calculated from user query onset to final workflow exit.

---

## 16. Production-Grade Agentic Architecture Blueprint

```
                     [User Input Transactional Ingress]
                                     │
                                     ▼
                      ┌─────────────────────────────┐
                      │    API Gateway / Firewall   │ ◄───► [PII Masking & Injection Shield]
                      └─────────────────────────────┘
                                     │
                                     ▼
           ┌───────────────────────────────────────────────────┐
           │ LangGraph Stateful Orchestration Graph Framework  │ ◄──► [Durable Checkpointer DB]
           └───────────────────────────────────────────────────┘
             │                                               ▲
             │ (Dynamic Context Token Packing)               │ (Return Validated JSON Schema)
             ▼                                               │
     ┌───────────────┐                               ┌───────────────┐
     │System Template│ ──► [Token Eviction Layer] ──►│ LLM Engine API│
     └───────────────┘                               └───────────────┘
            ▲                                                │
            │ (Context Enrichment Context)                   │ (Emits Tool Calling Intention)
            │                                                ▼
   ┌─────────────────┐                               ┌───────────────┐
   │  Reranking Node │                               │ Tool Registry │ ◄───► [RBAC / Scope Verification]
   └─────────────────┘                               └───────────────┘
            ▲                                                │
            │ (Reciprocal Rank Fusion)                       │ (Isolated Environment Execution)
   ┌─────────────────┐                                       ▼
   │  Hybrid Search  │                               ┌───────────────┐
   │ (Vector + BM25) │                               │ Tool Executor │ ◄───► [Idempotency Key & Circuit Breakers]
   └─────────────────┘                               └───────────────┘
            ▲                                                │
            │                                                ▼
     [Vector Data Store]                        [Downstream Microservices]
```

---

## 17. Interview Communication Strategy: Speaking Like a Lead Architect

Instead of dryly reciting definitions, position these concepts as engineering strategic choices designed to manage real-world production trade-offs.

### Talk About State with Authority
* **Weak formulation:** *"I like LangGraph because it uses a graph with nodes to track state data easily."*
* **Architect formulation:** *"When architecting high-concurrency enterprise workflows, I implement graph-based orchestration centered around **durable execution**. By checking state updates into a persistent **state reducer** model at every node boundary, we isolate session states, handle infrastructure disconnects cleanly, and implement dependable **Human-in-the-loop** routing rails for high-risk transactional nodes without data corruption."*

### Frame API Integrations Defensively
* **Weak formulation:** *"I configure function calling to let the LLM execute tools on our network."*
* **Architect formulation:** *"I decouple execution completely. **Tool calling** is utilized purely as a semantic intent parser. The model emits structured arguments matching our strict **JSON Schema**, which is subsequently picked up by an isolated **tool execution environment**. We wrap every execution block in **idempotency keys** and **circuit breaker patterns** to protect our underlying microservices from recursive runaway loops."*

### Justify RAG Strategy via Mechanics
* **Weak formulation:** *"I chunk documents and save them in a vector database to search them later."*
* **Architect formulation:** *"We employ a **hybrid search** paradigm to solve retrieval limits. We evaluate user inputs across dense semantic **embeddings** and keyword-based **BM25 indexes**, combining raw relevance scores through **Reciprocal Rank Fusion (RRF)**. We leverage **parent-child chunking** topologies to pass full structural contexts to the LLM, passing results through a **reranking** tier to counter **lost-in-the-middle** degradations."*

### Elevate Security Beyond Simple Prompts
* **Weak formulation:** *"I tell the model in the prompt not to share secrets or follow bad user instructions."*
* **Architect formulation:** *"We assume all unstructured data interfaces are vulnerable to **indirect prompt injection**. We enforce hard **autonomy boundaries** through rigorous **deterministic workflows** instead of relying on fragile prompt engineering. Furthermore, we decouple user access control completely, mapping system credentials via runtime **RBAC for agents** to ensure a model cannot invoke a tool scope beyond the current authenticated user's profile."*
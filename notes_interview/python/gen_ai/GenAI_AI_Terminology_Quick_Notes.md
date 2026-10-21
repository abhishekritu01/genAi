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

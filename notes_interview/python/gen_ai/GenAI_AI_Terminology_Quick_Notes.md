# GenAI & Agentic AI: Quick Revision Notes (Interview Edition)

> Merged from two glossaries, duplicates removed, missing topics added (marked 🆕).
> **⭐ = high priority** (Agentic Systems Engineer JD). Learn ⭐ first.
> Rule: use a term only where it describes a real engineering decision, not as decoration.

## Contents
1. Core AI & LLM
2. Prompting & output control
3. RAG, embeddings, retrieval
4. Agents & agentic workflows
5. Memory & context management 🆕
6. LangChain, LangGraph, orchestration
7. Tools, APIs, MCP, integrations
8. Evaluation & testing
9. LLMOps, observability, production
10. Training, fine-tuning, optimization
11. Security, safety, governance
12. Voice, contact center & communications AI 🆕
13. Advanced & emerging
14. Business & market buzzwords
15. Top 40 terms to memorize first
16. Confusable pairs
17. Acronym decoder
18. Production agent architecture (diagram + 90-sec story)
19. Common interview questions & answer skeletons 🆕
20. Speaking like an architect
21. Agent SDKs, skills & protocols 🆕
22. Advanced RAG, structured output & tool-call details 🆕
23. Backend & system design basics 🆕
24. Compliance, governance & agent safety controls 🆕
25. Model behavior & failure modes 🆕

---

## 1. Core AI & LLM

| Term | Meaning |
|---|---|
| **GenAI** ⭐ | AI that generates new content (text, image, audio, code) by sampling learned distributions |
| **LLM** ⭐ | Large Language Model; transformer that predicts the next token |
| **Foundation model** | Broadly pre-trained base model, adaptable to many tasks |
| **Transformer** | Self-attention architecture behind modern LLMs (replaced RNN/LSTM) |
| **Token** ⭐ | Unit of text (word/fragment). Cost, speed, and limits are all measured in tokens |
| **Tokenization** | Text → token IDs (e.g. Byte-Pair Encoding) |
| **Context window** ⭐ | Max tokens (system prompt + history + retrieved data + output) per request |
| **Inference** | Running a trained, frozen model to produce output |
| **Multimodal** | Handles text, image, audio, video together |
| **SLM** | Small Language Model (<~10B params); cheap/fast for narrow tasks |
| **Frontier model** | Most capable model at the current time |
| **Open-weight model** | Downloadable/self-hostable weights under a license (e.g. Llama) |
| **Hallucination** ⭐ | Fluent output that is unsupported or false |
| **Knowledge cutoff** | Date after which the model has no training data |
| **Reasoning model** 🆕 | Model trained to think through multi-step problems before answering |
| **KV cache** 🆕 | Stored attention keys/values so earlier tokens aren't recomputed (speeds decoding) |

---

## 2. Prompting & output control

| Term | Meaning |
|---|---|
| **Prompt engineering** ⭐ | Designing instructions/context for reliable outputs |
| **System prompt** ⭐ | Highest-priority instructions: role, rules, tool usage, constraints |
| **Zero-shot / Few-shot** ⭐ | No examples vs examples in the prompt |
| **Chain-of-thought (CoT)** | Step-by-step reasoning before the answer |
| **Prompt template** | Reusable prompt with variables |
| **Structured output** ⭐ | Output forced into a schema (JSON / Pydantic) so code can trust it |
| **JSON Schema** ⭐ | Spec of valid fields, types, required keys |
| **Constrained decoding** | Masks invalid tokens at logit level so output always matches schema/grammar |
| **Temperature** | Randomness (low = deterministic) |
| **Top-p (nucleus)** | Sample only from smallest token set whose cumulative prob ≥ p |
| **Prompt chaining** | Output of call N feeds call N+1 |
| **Context engineering** ⭐ | Choosing/organizing everything the model sees: instructions, history, retrieved data, tools |
| **Prompt versioning** | Prompts in Git/registry so behavior is testable and reproducible |
| **Prompt caching** | Reuse the processed prompt prefix to cut cost/latency (put static content first) |

**Say:** "I use structured outputs with schema validation so downstream services don't blindly trust free-form model responses."

---

## 3. RAG, embeddings, retrieval

| Term | Meaning |
|---|---|
| **RAG** ⭐ | Retrieve external data at query time and inject into the prompt to ground answers |
| **Embedding** ⭐ | Vector of meaning; similar meaning = nearby vectors |
| **Vector database** ⭐ | Stores vectors, fast nearest-neighbor search (pgvector, Pinecone, Qdrant, Weaviate) |
| **Semantic search** | Search by meaning, not exact words |
| **Chunking** ⭐ | Splitting docs into retrieval units (by tokens, structure, or semantics) |
| **Chunk overlap** | Repeated tokens between chunks to avoid cutting facts at boundaries |
| **Parent-child chunking** | Search small child chunks, return the larger parent for context |
| **ANN / HNSW** | Approximate nearest neighbor search; HNSW is a graph index (speed vs tiny accuracy loss) |
| **Cosine similarity** | Angle-based vector similarity (ignores length) |
| **BM25** | Classic keyword ranking (TF-IDF family); great for IDs, product codes |
| **Hybrid search** ⭐ | Vector + BM25 combined |
| **RRF** ⭐ | Reciprocal Rank Fusion: merges ranked lists using rank positions only |
| **Reranking** ⭐ | Cross-encoder re-scores top candidates for precision |
| **Metadata filtering** ⭐ | Filter by tenant, date, ACL, type (also enforces multi-tenant isolation) |
| **Query rewriting** | LLM reformulates the question for better retrieval |
| **Sub-queries / decomposition** | Split a compound question into parallel searches |
| **HyDE** | Embed a hypothetical answer instead of the raw query |
| **Self-RAG / corrective RAG** | Agent grades its retrieved chunks, rewrites query and retries if poor |
| **Agentic retrieval** | Agent chooses sources/strategy, multiple retrieval calls |
| **GraphRAG** | Retrieval over a knowledge graph of entities/relations |
| **Grounding** ⭐ | Tying answers to provided evidence |
| **Citations / attribution** | Pointers to the source of each claim |
| **Precision / Recall** ⭐ | Relevant share of retrieved / share of all relevant that was found |
| **MMR** | Maximal Marginal Relevance: balances relevance and diversity |
| **Lost in the middle** | Models use start/end of long context better than the middle |
| **Embedding model choice** 🆕 | Trade-off of dimension, cost, language/domain fit; re-embed everything if you change it |
| **Index freshness / re-indexing** 🆕 | Keeping the vector index in sync with changing source data (CDC, webhooks) |
| **Text-to-SQL** 🆕 | LLM generates SQL for structured data; needs read-only creds, schema context, validation |

**Say:** "I'd evaluate retrieval separately from generation, then tune chunking, metadata filters, hybrid search, and reranking based on failure patterns."

---

## 4. Agents & agentic workflows

| Term | Meaning |
|---|---|
| **AI agent** ⭐ | LLM + tools + state/memory pursuing a goal |
| **Agentic AI** ⭐ | Systems that plan, act, react to feedback with some autonomy |
| **Agentic workflow** ⭐ | Multi-step process where the model adapts the next step |
| **Agent loop** ⭐ | Decide → act → observe → continue or stop |
| **Tool / Function calling** ⭐ | Model emits function name + JSON args; **your code** validates and executes |
| **Tool registry** ⭐ | Catalog of tools with schemas and clear descriptions |
| **Orchestration** ⭐ | Coordinating model calls, tools, state, approvals |
| **ReAct** ⭐ | Thought → Action → Observation loop |
| **Plan-and-execute / Planner-Executor** | Plan up front (strong model), execute steps (cheap model) |
| **Reflection** | Model critiques and improves its own output |
| **Self-correction loop** | Agent reads an error (e.g. SQL syntax) and fixes its next step |
| **Multi-agent system** ⭐ | Several specialized agents collaborating |
| **Supervisor / Sub-agent** | Manager routes/aggregates; workers specialize |
| **Handoff** | Passing control/state from one agent to another |
| **Router** | Sends request to the right path/agent/tool set (code or small LLM) |
| **Human-in-the-loop (HITL)** ⭐ | Human review/approval at a step |
| **Autonomy boundary** | What the agent may do without approval (e.g. spend cap) |
| **Stopping condition** | Max steps, error threshold, success flag; prevents runaway loops/cost |
| **Deterministic workflow** ⭐ | Fixed code-defined path; LLM only for isolated steps |
| **A2A** | Agent-to-agent communication protocols |
| **Map-reduce (agentic)** | Fan out parallel agent/tool runs, aggregate into one state |
| **Cognitive architecture** | Overall design of how state, memory, planning, tools interact |

> **Strong line:** "I use the least autonomy that solves the problem: deterministic workflow where steps are known, agent autonomy only where the path is genuinely uncertain."

**Anthropic-style workflow patterns** 🆕: prompt chaining, routing, parallelization (sectioning/voting), orchestrator-workers, evaluator-optimizer. Start simple; add agents only when needed.

---

## 5. Memory & context management 🆕

| Term | Meaning |
|---|---|
| **Short-term memory** | Current thread/context window state |
| **Long-term memory** | Facts/preferences persisted across sessions in an external store, retrieved when relevant |
| **Memory retrieval** | Selecting relevant stored memory for the prompt |
| **Checkpoint vs memory** | Checkpoint = workflow execution state; memory = facts for future conversations |
| **Context compaction / summarization** | Summarize old history to free tokens |
| **Token eviction / truncation** ⭐ | Drop old/low-priority content near the context limit |
| **Scratchpad / notes** | Agent writes intermediate findings outside the window, re-reads later |
| **Context isolation** | Sub-agents get their own clean context; return only a summary |
| **Stateful agent** | Preserves state across interactions |
| **Context rot / bloat** | Quality drops as irrelevant tokens pile up; fewer, better tokens win |
| **Tool RAG / dynamic tool selection** ⭐ | Retrieve only the top few relevant tool schemas instead of loading hundreds |

---

## 6. LangChain, LangGraph, orchestration

| Term | Meaning |
|---|---|
| **LangChain** ⭐ | Components: models, prompts, parsers, retrievers, tools |
| **LangGraph** ⭐ | Stateful graph orchestration: cycles, branching, persistence, HITL |
| **LCEL** | `prompt \| model \| parser` declarative composition (streaming/batch/async built in) |
| **Chain** | Fixed linear sequence of steps |
| **Node / Edge / Conditional edge** ⭐ | Step / fixed link / route chosen from state at runtime |
| **State** ⭐ | Shared data object across steps |
| **State reducer** | Rule to merge node output into state (e.g. append messages) |
| **Checkpointing** ⭐ | Save state at each step: resume, replay, pause |
| **Thread ID** | Key identifying a conversation/run's checkpoints |
| **Persistence / Durable execution** ⭐ | Workflow survives crashes/restarts and resumes |
| **Interrupt** | Pause for human/external event (LangGraph `interrupt`) |
| **Time-travel / forking** ⭐ | Rewind to a checkpoint, edit state, branch a new run |
| **Recursion limit** | Cap on graph steps (stops infinite loops) |
| **Subgraph** | A graph used as a node (modularity, agent isolation) |
| **Send / Command** 🆕 | LangGraph primitives: dynamic fan-out (map-reduce) / combine state update + routing |
| **LangSmith** | LangChain tracing + evals |
| **Other frameworks** | LlamaIndex (data/RAG), CrewAI, AutoGen, Semantic Kernel, OpenAI Agents SDK |

---

## 7. Tools, APIs, MCP, integrations

| Term | Meaning |
|---|---|
| **REST API / API contract** | HTTP resources / agreed requests, responses, errors |
| **MCP** ⭐ | Model Context Protocol: standard way for AI apps to connect to tools/context |
| **MCP client / server** ⭐ | Host-side client discovers/calls; server exposes **tools, resources, prompts** |
| **MCP transports** 🆕 | stdio (local) and streamable HTTP (remote) |
| **Connector** ⭐ | Integration with an external service/data source |
| **OAuth 2.0** ⭐ | Scoped, delegated access |
| **Least privilege** ⭐ | Minimum permissions needed |
| **RBAC / ABAC for agents** ⭐ | Tool access mapped to the *user's* role/attributes |
| **Schema validation** ⭐ | Check args/outputs against required fields and types |
| **Semantic API description** | Clear docstrings/OpenAPI text so the model knows *when/how* to call |
| **Idempotency / Idempotency key** ⭐ | Repeating an op has no extra effect / unique key making retries safe |
| **Retry / Exponential backoff / Jitter** ⭐ | When to retry / growing delay / random delay |
| **Timeouts** 🆕 | Bound every external call |
| **Rate limiting / Throttling** | Cap request frequency; protect downstream and quotas |
| **Circuit breaker** ⭐ | Stop calling a failing dependency temporarily |
| **Compensating action / Saga** | Undo earlier steps when a multi-step op fails |
| **Side effect** ⭐ | Change outside the return value (CRM update, email, call) |
| **Tool allowlist** | Explicit permitted tools |
| **Sandboxed execution** | Tool code runs in isolated container/lambda |
| **Async tool execution** | Long job runs elsewhere; webhook resumes the agent |
| **Webhook / Pagination / Queue** | Event callback / large results in pages / decouple work (Kafka, SQS, Redis) |

**Say:** "The model can request a tool call, but the backend stays responsible for authentication, authorization, validation, and safe execution."

---

## 8. Evaluation & testing

| Term | Meaning |
|---|---|
| **Evals** ⭐ | Systematic quality measurement of an LLM app |
| **Evaluation harness** ⭐ | Code + data that runs cases and computes metrics (gate in CI) |
| **Golden dataset** ⭐ | Curated cases with trusted expected outcomes |
| **Synthetic data** | Generated edge cases to grow the golden set |
| **LLM-as-a-judge** ⭐ | LLM scores outputs with a rubric; **calibrate** against human labels |
| **Task success rate** ⭐ | % tasks completed per defined criteria |
| **Tool-call accuracy** ⭐ | Right tool + right arguments |
| **Trajectory evaluation** | Score the path of steps, not just the final answer |
| **Faithfulness / Groundedness** ⭐ | Answer supported by provided evidence |
| **Answer relevance / Context precision & recall** 🆕 | RAG metrics (e.g. RAGAS): is it on-topic, is retrieved context useful and complete |
| **Hallucination rate** ⭐ | Unsupported answers ÷ total |
| **Regression testing** ⭐ | Changes didn't break existing behavior |
| **pass@k / multi-trial** | Handle non-determinism by repeated runs |
| **Pairwise evaluation** | Judge which of two outputs is better |
| **A/B testing** | Compare variants on live traffic |
| **Online vs offline evals** | Live monitoring vs fixed pre-release datasets |
| **Human evaluation** | People rate quality |
| **Red teaming / Adversarial testing** ⭐ | Probe with hard/malicious inputs |
| **Evaluation leakage** | Eval data influences development → inflated scores |
| **False positive / negative** | Flagged but not true / missed but true |
| **Evaluation gate / threshold** | Minimum score to release |
| **Benchmark** | Standard tasks to compare systems |

---

## 9. LLMOps, observability, production

| Term | Meaning |
|---|---|
| **LLMOps** ⭐ | Deploy, evaluate, monitor, maintain LLM apps |
| **AI observability** ⭐ | Understand behavior via traces, logs, metrics, evals |
| **Tracing / Span** ⭐ | End-to-end request tree / one timed unit of work |
| **Structured logging** | Machine-readable log fields |
| **Latency p50/p95/p99** ⭐ | Response-time percentiles (watch the tail) |
| **TTFT** | Time to first token |
| **Throughput** | Work per unit time |
| **Token usage / Cost per task** ⭐ | Tokens consumed / total cost to finish a task |
| **Cost-to-resolution (CTR)** | Cumulative token spend across an entire agent run to close a task |
| **Cost attribution** | Spend per user/team/component |
| **Streaming (SSE)** ⭐ | Incremental token delivery; hides latency |
| **Prompt caching** | Reuse processed prompt prefix |
| **Semantic cache** | Cache by meaning of query (risky: wrong hits, stale, cross-tenant) |
| **Graceful degradation** ⭐ | Reduced function instead of total failure |
| **Fallback model/strategy** | Alternate model/path when primary fails |
| **AI gateway / LLM gateway** | Central layer for routing, auth, rate limits, logging across providers |
| **Canary release / Rollback** ⭐ | Small-traffic rollout / revert |
| **Feature flag** | Toggle behavior without redeploy |
| **SLO / SLA / Error budget** | Target / commitment / tolerated unreliability |
| **DLQ** | Dead-letter queue for repeatedly failed jobs |
| **Drift (data / concept / prompt)** | Inputs or behavior shift; **prompt drift** = provider silently updates model behind same endpoint |
| **Semantic monitoring** | Cluster/embedding-based detection of new query or failure patterns |
| **Tools (know names)** | LangSmith, Langfuse, Arize Phoenix, OpenTelemetry |

---

## 10. Training, fine-tuning, optimization

| Term | Meaning |
|---|---|
| **Pre-training** | Large-scale initial training |
| **Fine-tuning** | Further training for a domain/style/format |
| **Instruction tuning** | Training to follow instructions |
| **Transfer learning** | Reuse learned knowledge on a new task |
| **PEFT / LoRA / QLoRA** | Train few params / low-rank adapters / LoRA on a quantized base |
| **Quantization** ⭐ | Lower precision (16→8/4-bit) to save memory, speed up |
| **Distillation** | Small student learns from large teacher |
| **RLHF / RLAIF / DPO** | Alignment from human / AI feedback / direct preference optimization |
| **Context extension (RoPE scaling)** | Stretch context beyond training length |
| **Model routing** ⭐ | Pick a model per request by task, cost, latency, quality |
| **Model cascading** ⭐ | Cheap model first, escalate hard cases |
| **Inference optimization** | Batching, KV cache, speculative decoding, quantization |

> **RAG vs fine-tuning:** RAG = fresh facts, citations, access control at inference time. Fine-tuning = style, format, behavior. Different problems; can combine.

---

## 11. Security, safety, governance

| Term | Meaning |
|---|---|
| **Guardrails** ⭐ | Controls on inputs, outputs, actions (NeMo Guardrails, Llama Guard) |
| **Prompt injection** ⭐ | Malicious instructions override the model's task |
| **Direct vs indirect injection** ⭐ | From the user vs hidden in data the agent reads (email, web, tool output) |
| **Jailbreak** | Bypass the model's safety alignment |
| **Prompt leakage** | Attacker extracts the system prompt |
| **Data leakage / exfiltration** ⭐ | Unauthorized exposure of sensitive data |
| **PII redaction / masking** ⭐ | Strip personal data before sending to providers/logs |
| **Tenant isolation** ⭐ | One customer's data never reaches another |
| **Audit trail** ⭐ | Who/what did what, when |
| **Provenance / lineage** | Source of data, answers, model versions |
| **Human approval gate** ⭐ | Explicit authorization before risky actions |
| **Blast radius** | Damage scope if something fails/is breached |
| **Excessive agency** | Agent has more power than needed |
| **Confused deputy** | Agent uses its own privileges for a user who lacks them |
| **Tool poisoning** | Malicious tool/MCP descriptions steer the model |
| **Data poisoning** | Corrupted training/knowledge data |
| **Supply chain security** | Protect dependencies, models, artifacts |
| **Threat modeling** | Identify attackers, threats, mitigations |
| **Runtime validation / Policy enforcement** | Checks during execution / allow-deny rules |
| **OWASP Top 10 for LLM Apps** 🆕 | Standard checklist: injection, insecure output handling, excessive agency, etc. |
| **Shadow AI** | Unmonitored use of public AI tools by employees |
| **Responsible AI / AI governance** | Safety, fairness, privacy, accountability, oversight |

> **Lethal trifecta:** private data + untrusted content + external communication in one agent = high risk. Break at least one leg.
> **Guardrails are probabilistic; authorization is deterministic code.** Never rely on the prompt for access control.

---

## 12. Voice, contact center & communications AI 🆕

(Relevant for RingCentral-style products.)

| Term | Meaning |
|---|---|
| **STT / ASR** | Speech-to-text (metric: **WER**, word error rate) |
| **TTS** | Text-to-speech |
| **Voice agent** | STT → LLM → TTS pipeline (or native speech-to-speech model) |
| **Barge-in** | User interrupts the agent mid-speech; must stop TTS and handle gracefully |
| **Endpointing / VAD** | Detect when the user finished speaking / voice activity detection |
| **End-to-end voice latency** | Target sub-second; TTFT + STT + TTS all count |
| **Real-time inference** | Responses under tight latency budgets |
| **Agent assist** | Live suggestions/summaries for human reps |
| **Conversation intelligence** | Analyze calls/chats: summaries, sentiment, topics, compliance |
| **Call summarization / action items** | Typical high-value GenAI use case |
| **Intent detection / routing** | Classify caller need, route to queue/agent/bot |
| **Escalation to human** | Warm handoff with context when confidence is low |
| **Telephony basics** | SIP, WebRTC, PSTN; know they exist |
| **Compliance** | Call recording consent, PCI/PII redaction in transcripts |

---

## 13. Advanced & emerging

| Term | Meaning |
|---|---|
| **Test-time compute** | Extra inference computation to improve answers |
| **Semantic router** | Route by meaning/intent via embeddings |
| **Long-context reasoning** | Fidelity over very large contexts |
| **Knowledge graph / Graph DB** | Entities and relations / storage for them |
| **VLM / Multimodal embedding / OCR** | Vision-language model / cross-modal vectors / text from images |
| **Speculative decoding** | Draft model proposes tokens, big model verifies |
| **Mixture of Experts (MoE)** | Routes inputs to specialized sub-networks |
| **Computer use / browser agents** | Agents operating UIs via screenshots/clicks |
| **Agentic mesh / fabric** | Decentralized network of agents using shared protocols |
| **Air-gapped LLM / Sovereign AI** | Fully private/local hosting / data and models within a jurisdiction |
| **Dynamic prompts** | Prompt structure adapts to live context/intent |

---

## 14. Business & market buzzwords

| Term | Meaning |
|---|---|
| **AI-native** | Designed around AI as the core |
| **Copilot vs autonomous agent** | Assists a human vs acts with limited oversight |
| **Workflow automation** | Automating business steps/decisions |
| **IDP** | Intelligent Document Processing: extract/classify info from documents |
| **Enterprise AI / Enterprise readiness** | Security, integration, reliability, governance, compliance |
| **Production-ready AI** | Monitoring, testing, security, recovery in place |
| **Vertical / Horizontal AI** | Industry-specific / cross-industry |
| **AIaaS** | AI as a managed service |
| **Human oversight** | Ability to monitor and intervene |
| **AI ROI / Agentic ROI** | Business value vs cost |
| **Time-to-value (TTV)** | Speed from prototype to stable value |
| **AI transformation** | Reworking processes using AI |

---

## 15. Top 40 terms to memorize first

**Foundations**
1. **Token / Context window:** unit of cost and the hard input+output limit.
2. **Hallucination:** fluent but unsupported output; fix with grounding.
3. **Context engineering:** deciding what the model sees and in what form.
4. **Structured output:** schema-validated output so code can trust it.

**Retrieval**
5. **RAG:** retrieve at query time, inject, ground the answer.
6. **Embeddings:** meaning as vectors.
7. **Vector DB:** nearest-neighbor storage.
8. **Chunking:** splitting docs into retrieval units.
9. **Hybrid search:** vector + BM25.
10. **RRF:** merge ranked lists by rank position.
11. **Reranking:** cross-encoder re-scores top candidates.
12. **Metadata filtering:** tenant/ACL/date filters.
13. **Groundedness / faithfulness:** claims supported by sources.

**Agents & orchestration**
14. **Agentic workflow:** model adapts next steps within limits.
15. **Orchestration:** coordinating calls, tools, state.
16. **LangGraph:** stateful graph with cycles, checkpoints, interrupts.
17. **State / reducer:** shared data and how updates merge.
18. **Checkpointing / durable execution:** resume after failure or pause.
19. **Human-in-the-loop:** approval for risky steps.
20. **Deterministic workflow:** fixed path; least autonomy needed.
21. **Function/tool calling:** model requests, your code executes.
22. **MCP:** standard protocol for tools/resources/prompts.
23. **Tool RAG:** retrieve only relevant tool schemas.
24. **Token eviction / compaction:** manage context growth.

**Reliability & integrations**
25. **Idempotency key:** safe retries on side-effecting calls.
26. **Retry + backoff + jitter; timeouts.**
27. **Circuit breaker:** stop hitting a failing dependency.
28. **Graceful degradation:** reduced function, not total failure.
29. **Streaming (SSE):** lower perceived latency.

**Eval & ops**
30. **Evals / harness / golden dataset:** measure quality in CI.
31. **LLM-as-a-judge:** rubric grading, calibrated to humans.
32. **Tool-call accuracy / task success:** core agent metrics.
33. **LLMOps / observability / tracing:** run it in production.
34. **Cost per task / latency p95:** the numbers you track.
35. **Model routing / cascading:** match model to task.

**Security**
36. **Prompt injection (direct/indirect):** hijacking via input or data.
37. **Least privilege / RBAC for agents:** deterministic access control.
38. **Guardrails:** input/output/action checks (probabilistic).
39. **PII redaction & tenant isolation.**
40. **Audit trail:** record of every action.

---

## 16. Confusable pairs

| Pair | One-line difference |
|---|---|
| **Agent vs chain** | Agent picks steps at runtime; chain is fixed |
| **Agent vs workflow** | Model-directed path vs predefined path |
| **Tool calling vs agentic workflow** | One capability vs the loop/state wrapped around it |
| **Function calling vs MCP** | How the model requests a call vs standard for packaging/discovering tools |
| **LangChain vs LangGraph** | Components/linear pipelines vs stateful graphs with loops, persistence, HITL |
| **RAG vs fine-tuning** | Facts at inference time vs behavior via training |
| **RAG vs long context** | Retrieve what's needed vs stuff everything (cost, lost-in-the-middle) |
| **Dense vs sparse retrieval** | Vectors (meaning) vs keywords (exact terms) |
| **Retrieval vs reranking** | Fast broad fetch vs slower precise reorder |
| **Precision vs recall** | Accuracy of results vs coverage of relevant items |
| **Faithfulness vs correctness** | Supported by context vs true in the world |
| **Hallucination vs error** | Fabrication vs wrong-but-grounded (bad source) |
| **State vs context window** | Everything your app stores vs what fits in one LLM call |
| **Checkpoint vs memory** | Execution state vs facts retained for future conversations |
| **Short- vs long-term memory** | Current interaction vs persisted across sessions |
| **Deterministic vs LLM routing** | Code `if/else` vs model chooses next node |
| **Guardrails vs authorization** | Probabilistic checks vs deterministic access control |
| **Prompt injection vs jailbreak** | Hijack the task/agent vs break safety alignment |
| **Direct vs indirect injection** | User attacks vs attack hidden in data read by agent |
| **Zero-shot vs few-shot** | No examples vs examples in prompt |
| **Retry vs fallback** | Same operation again vs different path |
| **Streaming vs batch** | Incremental (low perceived latency) vs full response (easier validation) |
| **Latency vs throughput** | Time per request vs requests per time |
| **SLO vs SLA** | Internal target vs formal commitment |
| **Model routing vs cascading** | Pick one up front vs cheap first, escalate if needed |
| **Prompt caching vs semantic caching** | Reuse processed prefix vs reuse answers for similar queries |
| **Evals vs unit tests** | Statistical quality on non-deterministic output vs deterministic pass/fail |
| **Online vs offline evals** | Live traffic monitoring vs fixed pre-release datasets |
| **Copilot vs agent** | Assists a human vs acts more autonomously |
| **Planner vs executor** | Builds the roadmap vs runs the steps |

---

## 17. Acronym decoder

| Acronym | Meaning |
|---|---|
| LLM / SLM | Large / Small Language Model |
| RAG | Retrieval-Augmented Generation |
| HITL | Human-in-the-loop |
| MCP | Model Context Protocol |
| A2A | Agent-to-Agent |
| ReAct | Reason + Act |
| CoT | Chain-of-Thought |
| ANN / HNSW | Approximate Nearest Neighbor / Hierarchical Navigable Small World |
| BM25 | Best Matching 25 (keyword ranking) |
| RRF | Reciprocal Rank Fusion |
| MMR | Maximal Marginal Relevance |
| HyDE | Hypothetical Document Embeddings |
| LCEL | LangChain Expression Language |
| TTFT | Time To First Token |
| p95 / p99 | 95th / 99th percentile latency |
| SLO / SLA | Service Level Objective / Agreement |
| CTR | Cost-to-Resolution |
| TTV | Time-to-Value |
| PEFT / LoRA / QLoRA | Parameter-Efficient Fine-Tuning / Low-Rank Adaptation / Quantized LoRA |
| RLHF / RLAIF / DPO | RL from Human / AI Feedback / Direct Preference Optimization |
| MoE | Mixture of Experts |
| VLM | Vision-Language Model |
| OCR | Optical Character Recognition |
| STT / TTS / ASR | Speech-to-Text / Text-to-Speech / Automatic Speech Recognition |
| WER | Word Error Rate |
| VAD | Voice Activity Detection |
| PII | Personally Identifiable Information |
| RBAC / ABAC | Role- / Attribute-based Access Control |
| OAuth | Open Authorization |
| IDP | Intelligent Document Processing (or Identity Provider) |
| DLQ | Dead-Letter Queue |
| CDC | Change Data Capture |
| CI/CD | Continuous Integration / Delivery |
| SSE | Server-Sent Events (one-way streaming) |
| RLS | Row-Level Security |
| JSON | JavaScript Object Notation |
| ROI | Return on Investment |
| OWASP | Open Worldwide Application Security Project |

---

## 18. Production agent architecture

```
User request
   │
   ▼
API gateway ── auth, tenant isolation, PII masking, injection shield
   │
   ▼
LangGraph orchestrator ◄──► checkpointer DB (durable state)
   │        │
   │        ├─ Router → workflow + model (model routing)
   │        │
   │        ├─ Context assembly (system prompt, history, eviction)
   │        │
   │        ├─ RAG: hybrid search (vector+BM25) → RRF → rerank → grounded context + citations
   │        │
   │        └─ LLM ──► tool call (structured JSON)
   │                      │
   │                      ▼
   │              Tool registry ── RBAC / least privilege, schema validation
   │                      │
   │                      ▼
   │              Executor ── idempotency key, timeout, retry+backoff, circuit breaker
   │                      │         (risky writes → human approval gate)
   │                      ▼
   │              Downstream services
   ▼
Guardrails on input/output → response (streamed)
Everything traced + audit-logged
```

**90-second story (practice this):**

> "A request hits the **API**, where we authenticate and enforce **tenant isolation** and mask **PII**. A **LangGraph** orchestrator manages **state** with **checkpointing**. **Context engineering** assembles instructions and history, and a **router** picks the workflow and model (**model routing**). If knowledge is needed, **RAG** runs **hybrid search** with **metadata filtering**, fuses with **RRF**, **reranks**, and returns **grounded** context with citations. For actions the model uses **function calling** through a **tool registry** (possibly **MCP**); the backend does **schema validation** and **authorization** (**least privilege**), then executes **idempotent** calls with **timeouts, retries with backoff**, and a **circuit breaker**. Risky writes pass a **human approval gate**. **Guardrails** check inputs and outputs. Everything is **traced** and **audit-logged**. Offline, an **evaluation harness** with a **golden dataset** measures **task success, tool-call accuracy and faithfulness**, gated in CI; online we watch **latency, cost per task and failures**, shipping via **canary release** with **rollback**."

---

## 19. Common interview questions & answer skeletons 🆕

| Question | Skeleton answer |
|---|---|
| **Agent or workflow?** | Default to deterministic workflow; use agent autonomy only where the path is uncertain; cap steps, add stopping conditions |
| **How do you reduce hallucinations?** | Grounding via RAG + citations, structured output, "say I don't know" instructions, faithfulness evals, HITL for high stakes |
| **RAG quality is poor. Debug?** | Separate retrieval vs generation; check recall@k first; tune chunking, hybrid search, reranking, metadata filters, query rewriting |
| **How do you make tool calls safe?** | Schema validation, authz in code, least privilege, idempotency keys, timeouts, retries, approval gates for writes |
| **How do you evaluate an agent?** | Golden dataset, task success, tool-call accuracy, trajectory eval, LLM-judge calibrated to humans, multi-trial for non-determinism, CI gates |
| **How do you handle prompt injection?** | Assume retrieved/tool content is untrusted; break the lethal trifecta; least privilege; approval for sensitive actions; output validation; red teaming |
| **How do you control cost/latency?** | Model routing/cascading, prompt caching, streaming, smaller context via retrieval/compaction, parallel tool calls, track cost per task and p95 |
| **How do you handle long-running workflows?** | Durable execution, checkpoints, async tools + webhooks, interrupts for approval, idempotent resume |
| **Multi-tenant concerns?** | Tenant ID in metadata filters and every query, per-tenant keys/quotas, no cross-tenant cache, audit logs |
| **Fine-tune or RAG?** | RAG for changing facts/access control/citations; fine-tune for style/format/behavior; often both |
| **What do you monitor in production?** | Traces, latency percentiles, token cost per task, failure/fallback rates, eval scores on sampled traffic, drift |
| **How do you roll out a prompt/model change?** | Version it, run regression evals, canary release, feature flag, rollback plan |

---

## 20. Speaking like an architect

**Rules**
- Define a term in one plain sentence before going deep.
- Attach each term to a decision or trade-off ("I chose hybrid search because our data has product codes").
- Not used it hands-on? Say "I understand it conceptually, and here's how I'd apply it."
- Prefer measurement language: "I'd measure it with…".
- Max 2-3 buzzwords per sentence.

| Topic | Weak | Strong |
|---|---|---|
| **State** | "LangGraph tracks state with nodes." | "I use graph orchestration with durable execution: state is checkpointed at each node boundary, so we survive restarts and can pause for human approval." |
| **Tools** | "Function calling lets the LLM run tools." | "Tool calling is only an intent parser. The model emits schema-valid args; our backend authorizes, validates, and executes with idempotency keys and circuit breakers." |
| **RAG** | "I chunk docs and put them in a vector DB." | "Hybrid search (embeddings + BM25) fused with RRF, parent-child chunking for context, and a reranker to counter lost-in-the-middle; retrieval evaluated separately from generation." |
| **Security** | "I tell the model not to leak secrets." | "We treat all external data as untrusted, enforce autonomy boundaries in deterministic code, and map runtime RBAC to the authenticated user so the model can never exceed their permissions." |

**Final reminder:** learn definitions first, then practise explaining how 5-6 of these concepts work together in one agent (Section 18). That beats memorizing hundreds of disconnected terms.

---

# Part 2: Added Topics

## 21. Agent SDKs, skills & protocols 🆕

| Term | Meaning |
|---|---|
| **OpenAI Agents SDK** | Lightweight framework: agents, tools, handoffs, guardrails, tracing built in |
| **Claude Agent SDK** | Anthropic's SDK for building agents with the same loop, tools, and context management as Claude Code |
| **MCP vs A2A** | MCP = agent ↔ tools/data. A2A = agent ↔ agent. Complementary, not competing |
| **Agent skills** | Folders of instructions/scripts an agent loads on demand |
| **Progressive disclosure** | Load only skill/tool name+description first; load full instructions only when relevant (saves context) |
| **Sub-agent vs single agent** | Sub-agents: parallel work, context isolation, specialized prompts. Cost: more tokens, coordination overhead. Use a single agent unless context or parallelism demands more |
| **Orchestrator-workers** | Lead agent decomposes dynamically, workers run subtasks, lead synthesizes |
| **Agent identity** | Each agent has its own credentials/scopes, not a shared super-key |

---

## 22. Advanced RAG, structured output & tool-call details 🆕

| Term | Meaning |
|---|---|
| **Contextual retrieval** | Prepend a short LLM-generated context line to each chunk before embedding/BM25 so chunks stand alone |
| **Late chunking** | Embed the whole doc first, then pool per chunk, preserving cross-chunk context |
| **Multi-vector / ColBERT (late interaction)** | Store per-token vectors, score by fine-grained matching; more accurate, more storage |
| **Sparse embeddings (SPLADE)** | Learned sparse vectors: keyword-like but with semantic term expansion |
| **Pydantic / Zod validation** | Typed schema validation for Python / TypeScript model outputs |
| **Invalid JSON handling** | Constrained decoding or native structured outputs first; else validate → repair → retry with error message → fallback/escalate |
| **Parallel tool calling** | Model emits several independent calls at once; run concurrently, return all results together |
| **Streaming tool arguments** | Partial tool-call JSON arrives incrementally; don't execute until complete and validated |
| **Tool result truncation** | Cap/summarize large tool outputs so they don't bloat context |
| **Tool design** | Few, clearly named, non-overlapping tools; precise descriptions; helpful error messages the model can act on |
| **Eval tools** | RAGAS (RAG metrics), DeepEval, Promptfoo (prompt/regression tests), LangSmith/Langfuse evals |
| **CI eval gate** | Run golden dataset on every PR/prompt change; fail the build if scores drop below threshold |

---

## 23. Backend & system design basics 🆕

| Term | Meaning |
|---|---|
| **FastAPI / asyncio** | Async Python web framework / concurrency for I/O-bound LLM and tool calls |
| **Docker / Kubernetes** | Containers / orchestration, autoscaling, rolling deploys |
| **Stateless workers** | Keep state in DB/checkpointer so any worker can serve any request; scale horizontally |
| **Queues / event-driven (Kafka, SQS, Redis Streams)** | Decouple work, absorb spikes, enable retries and DLQ |
| **Postgres + pgvector** | Relational data and vectors in one store; simpler ops, transactional consistency |
| **Redis** | Caching, rate limiting, locks, short-term session state |
| **Row-level security (RLS)** | DB-enforced per-tenant row access; defense in depth for tenant isolation |
| **Multi-tenant design** | Tenant ID everywhere: filters, caches, keys, quotas, logs |
| **Blue/green deployment** | Two environments; switch traffic atomically; instant rollback |
| **Secrets management** | Vault / cloud secret manager; never in prompts, code, or logs |
| **Backpressure / load shedding** | Slow or reject work when overloaded instead of collapsing |
| **Distributed locks / dedupe** | Prevent two workers from performing the same side effect |
| **Observability stack** | OpenTelemetry traces + metrics + logs; correlation ID per request |

---

## 24. Compliance, governance & agent safety controls 🆕

| Term | Meaning |
|---|---|
| **EU AI Act** | Risk-tiered EU regulation (unacceptable, high, limited, minimal risk) with transparency/documentation duties |
| **NIST AI RMF** | US framework: Govern, Map, Measure, Manage |
| **SOC 2 / GDPR / HIPAA basics** | Security controls audit / EU data protection / US health data rules |
| **Data residency & retention** | Where data is stored and how long; relevant for transcripts and logs |
| **Zero data retention (ZDR)** | Provider doesn't store prompts/outputs |
| **Sandboxing & egress controls** | Run agent code isolated; allowlist outbound network to block exfiltration |
| **Per-agent credentials** | Scoped, short-lived tokens per agent/task |
| **Kill switch** | Instant global way to disable an agent or tool |
| **Action logging & replay** | Reconstruct exactly what an agent did and why |
| **Spend / step budgets** | Hard caps on tokens, cost, tool calls per run |
| **Model cards / AI inventory** | Documented model purpose, limits, owners; know which models you run |

---

## 25. Model behavior & failure modes 🆕

| Term | Meaning |
|---|---|
| **Sycophancy** | Model agrees with the user instead of being accurate; counter with neutral prompts and evals |
| **Non-determinism at temp 0** | Outputs can still vary (batching, hardware, provider updates); use multi-trial evals |
| **Tokenizer quirks** | Numbers, rare words, non-English text tokenize poorly; affects cost and accuracy |
| **Over-refusal / under-refusal** | Blocks valid requests / allows harmful ones; tune with evals |
| **Context rot / distraction** | Long, noisy context degrades reasoning |
| **Tool overuse / underuse** | Agent calls tools needlessly or fails to call when needed; fix descriptions and examples |
| **Looping / thrashing** | Agent repeats failed actions; use stopping conditions and error-aware prompts |
| **Reward hacking / spec gaming** | Agent satisfies the metric but not the intent; design robust success criteria |
| **Model selection criteria** | Quality on *your* evals, cost, latency, context length, tool-use reliability, data policy, rate limits |
| **Model deprecation risk** | Pin versions, run regression evals before migrating |

**Quick answer to "how do you choose a model?":** "I benchmark candidates on my own golden dataset for task success and tool-call accuracy, compare cost and p95 latency, then route: a cheap model for easy steps, a stronger one for hard ones, with a fallback if the primary fails."

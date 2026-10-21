# Agentic Systems Engineer: 220 Interview Questions with Short Answers (Quick Revision)

**Goal:** Prepare for an Agentic Systems Engineer interview with a concise question bank and short answers based on the job description.

## How to use this guide
1. Read the short answer, then say it aloud **in your own words** in 30-60 seconds.
2. Mark each question: ✅ Easy · 🔁 Needs Revision · ❌ Can't Answer.
3. For important topics, prepare a real example, architecture sketch, or small code exercise.
4. Be accurate about your experience: distinguish what you **personally implemented** from what you understand **conceptually**.
5. Questions marked **(Personal)** need *your own real story*. A framework is given, but do not invent details.

**Universal answer pattern:** Definition → How it works → Where it fails → What you do about it → Your example (if true).

## Contents
1. Agentic AI Fundamentals (1-20)
2. LangChain and LangGraph (21-40)
3. RAG and Retrieval (41-65)
4. Prompts, Models, Context, and Structured Outputs (66-85)
5. Tool Calling, APIs, SaaS, and MCP (86-110)
6. LLM Evaluation and Testing (111-135)
7. Observability, Reliability, and Production (136-155)
8. Security, Permissions, and Guardrails (156-175)
9. Python, Node.js, Databases, and Backend Engineering (176-190)
10. System Design and Experience-Based Questions (191-200)
11. Advanced Enterprise Architecture and Production Questions (201-220)
12. Final Revision Checklist

---

## 1. Agentic AI Fundamentals (1-20)

**1. What is an AI agent?**
**A:** An LLM-driven system that pursues a goal by repeatedly deciding on an action (usually a tool call), observing the result, and updating its state until the task is done.

**2. How is an agent different from a normal LLM chatbot?**
**A:** A chatbot only generates text from a prompt. An agent can take actions on external systems through tools, works over multiple steps, keeps state, and decides its own next step.

**3. What are the core components of an agentic system?**
**A:** The model, instructions/prompt, tools, memory/state, an orchestrator (loop or graph), guardrails/permissions, and observability plus evaluation.

**4. What is an agent loop?**
**A:** LLM → does it want a tool? → validate and authorize → execute → append result → call the LLM again, repeating until a final answer or a step/time/cost budget is hit.

**5. How does an agent decide which action to take next?**
**A:** The model reasons over the goal, conversation, tool descriptions and previous results, then picks a tool or answers. The orchestrator constrains this with allowed tools, routing and state.

**6. What is the difference between planning and execution?**
**A:** Planning decides the steps; execution carries them out with tools. Plan-and-execute separates them, while ReAct interleaves reasoning and acting.

**7. What is tool calling?**
**A:** The model emits a structured request to call a named function with arguments. Your code runs it and returns the result; the model never executes anything itself.

**8. What is function calling, and how does it work?**
**A:** You pass function schemas (name, description, JSON-schema parameters). The model returns a call with arguments, your code validates and runs it, and the result goes back to the model.

**9. What is the difference between an agent and a chain?**
**A:** A chain is a fixed, predefined sequence of steps. An agent lets the model decide control flow dynamically (which tool, how many loops).

**10. When should you avoid using an agent?**
**A:** When steps are known and deterministic, when latency/cost/predictability matter, when actions are high-risk, or when plain code or a simple chain solves it. Use the least autonomy that works.

**11. What are common agent design patterns?**
**A:** ReAct, plan-and-execute, router, reflection/critic, supervisor-worker, human-in-the-loop, and parallel fan-out/fan-in.

**12. What is a ReAct-style agent?**
**A:** It alternates Thought → Action (tool call) → Observation, reasoning about what to do, acting, reading the result, and continuing until done.

**13. What is reflection or self-critique in an agent?**
**A:** The model (or a second model) reviews its output against criteria and revises it. It improves quality but costs latency and tokens, so bound the iterations.

**14. What is a multi-agent system?**
**A:** Several specialized agents (e.g., researcher, SQL agent, writer, reviewer) coordinated by a supervisor, router, or handoffs.

**15. When is a multi-agent design useful?**
**A:** When domains need different tools or permissions, a single prompt gets too large, subtasks can run in parallel, or you want independent verification. Otherwise a single agent is simpler.

**16. What problems can arise in multi-agent coordination?**
**A:** Context loss, miscommunication, duplicated work, ping-pong loops, error amplification, conflicting actions, higher cost and latency, and harder debugging.

**17. How should an agent know when to stop?**
**A:** When the goal is satisfied (final answer), a max step/time/cost budget is reached, no progress is detected, or it must escalate to a human.

**18. How do you prevent an agent from looping indefinitely?**
**A:** Max iterations/recursion limit, time and token budgets, repeated-identical-call detection, informative tool results, clear stop criteria, and a fallback/escalation path.

**19. How do you handle an agent that repeatedly chooses the wrong tool?**
**A:** Inspect traces, then sharpen tool names/descriptions (including when *not* to use), reduce or scope the tool set, add examples, use a router, and add tool-selection evals.

**20. How would you explain an agentic workflow you built? (Personal)**
**A:** Structure: problem → architecture (state, nodes, tools) → key decisions and trade-offs → safety/guardrails → evaluation/monitoring → results → what you'd improve. Use only your real project.

---

## 2. LangChain and LangGraph (21-40)

**21. What problems does LangChain solve?**
**A:** It gives standard abstractions for models, prompts, output parsers, retrievers and tools, plus composition, reducing boilerplate and provider lock-in.

**22. What is a LangChain chain?**
**A:** A composable sequence of steps (e.g., `prompt | model | parser` via LCEL) where each step's output feeds the next.

**23. What is the difference between a chain and an agent?**
**A:** A chain follows a predetermined flow; an agent lets the LLM choose tools and steps at runtime.

**24. What is LangGraph, and when would you use it?**
**A:** A library for stateful, graph-based workflows with cycles, branching, persistence and human-in-the-loop. Use it when control flow, durable state, and resumability matter.

**25. What is a graph node in LangGraph?**
**A:** A function that takes the current state and returns state updates: an LLM call, tool execution, or plain logic.

**26. What is an edge in LangGraph?**
**A:** A fixed transition from one node to the next.

**27. What is a conditional edge?**
**A:** An edge whose next node is chosen by a function that reads state (e.g., tool call present → tools node, otherwise END).

**28. How is state represented and updated in LangGraph?**
**A:** As a typed schema (TypedDict/Pydantic). Nodes return partial updates that are merged by reducers, e.g., `add_messages` appends to the message list.

**29. Why is shared state important in a workflow?**
**A:** It's the single source of truth across steps, enabling inspection, resume, testing and decoupled nodes.

**30. How do you route execution based on a tool result?**
**A:** A conditional edge inspects the latest message/state (tool calls present? error flag? approval needed?) and returns the next node name.

**31. How do you implement loops in LangGraph safely?**
**A:** Cycle back with a conditional exit, keep a step counter in state, set a recursion limit, detect repeated calls, and route to a fallback node when the budget is spent.

**32. What are checkpoints, and why are they useful?**
**A:** Saved state snapshots per step, keyed by `thread_id`. They enable resume, replay/time-travel debugging, human-in-the-loop, memory and fault tolerance.

**33. How can a workflow resume after interruption?**
**A:** Reload the latest checkpoint with the same `thread_id` and continue. With a durable store (Postgres/SQLite) it survives restarts; side effects must be idempotent.

**34. How would you add human approval to a graph?**
**A:** Add an interrupt before the sensitive node, persist state, show the proposed action, then resume with approve/edit/reject, logging who approved.

**35. How do you handle exceptions inside a node?**
**A:** Catch and classify, write the error into state, and use conditional edges to retry (bounded), fall back, or escalate. Add timeouts and keep side effects idempotent.

**36. How do you test an individual node?**
**A:** Call the node function with crafted state, mock the LLM/tools, and assert the returned state updates.

**37. How do you test the complete graph?**
**A:** Use a fake LLM with scripted responses to assert routing and final state, then run LLM-in-the-loop evals for real behavior.

**38. How do you persist conversation state?**
**A:** A checkpointer (Postgres/Redis/SQLite) keyed by `thread_id`, plus an application DB for messages and metadata.

**39. How would you choose between LangChain and LangGraph?**
**A:** LangChain for simple linear pipelines and components; LangGraph for loops, branching, durable state, human approval, or multi-agent coordination.

**40. Describe a workflow you would implement with LangGraph.**
**A:** Support triage: classify intent → retrieve KB (RAG) → draft reply → conditional approval for risky actions → update CRM → END, with checkpointing and a step limit.

---

## 3. RAG and Retrieval (41-65)

**41. What is Retrieval-Augmented Generation (RAG)?**
**A:** At query time, retrieve relevant external data and put it in the prompt so the model's answer is grounded in it (with citations).

**42. When is RAG preferable to fine-tuning?**
**A:** For private or frequently changing knowledge, when you need citations and access control, and for cheap updates. Fine-tuning is for style/behavior, not reliable facts.

**43. What are the main stages of a RAG pipeline?**
**A:** Ingest/parse → chunk → embed → index; then at query time: rewrite → retrieve → rerank → build prompt → generate → verify/cite.

**44. What is an embedding?**
**A:** A vector representation of text in which similar meaning means nearby vectors.

**45. How do embedding models represent semantic meaning?**
**A:** They're trained on large corpora so that semantically similar texts map close together in a high-dimensional space.

**46. How do you choose an embedding model?**
**A:** Evaluate candidates on your own data (recall@k, MRR), and weigh language/domain fit, dimension, cost, latency and max input length.

**47. What is chunking, and why does it matter?**
**A:** Splitting documents into pieces to embed and retrieve. It determines retrieval precision and the quality of context given to the LLM.

**48. How do you choose chunk size and overlap?**
**A:** Start around 300-800 tokens with 10-20% overlap, preferably structure-aware, then tune by experiment on recall@k and answer quality.

**49. What are the trade-offs of small versus large chunks?**
**A:** Small chunks are precise but lose context; large chunks carry context but dilute embeddings and add noise and cost. Parent-child retrieval balances both.

**50. What is a vector database?**
**A:** A database optimized for storing embeddings and doing fast nearest-neighbor search with metadata filtering.

**51. How does vector similarity search work?**
**A:** Embed the query, compare it to stored vectors with a similarity metric (using ANN indexes like HNSW for speed), and return the top-k.

**52. What is cosine similarity?**
**A:** The cosine of the angle between two vectors; it measures directional similarity on a -1 to 1 scale.

**53. What is metadata filtering in retrieval?**
**A:** Restricting search by attributes like tenant, permissions, date or product at query time.

**54. What is hybrid search?**
**A:** Combining dense vector search with keyword/BM25 search and fusing results (e.g., Reciprocal Rank Fusion).

**55. When would you combine keyword and vector search?**
**A:** When queries mix meaning with exact terms (IDs, names, error codes), which is typical in enterprise data.

**56. What is reranking, and when should you use it?**
**A:** A cross-encoder rescoring of retrieved candidates for higher precision. Use it when top-k results are noisy and you can afford the extra latency.

**57. What is query rewriting?**
**A:** Transforming the user query (resolving "it/that", expanding, decomposing) before retrieval to improve recall.

**58. How can you improve retrieval for vague questions?**
**A:** Query rewriting/expansion, multi-query, HyDE, conversation context, or asking a clarifying question.

**59. How do you handle PDFs, tables, and structured documents?**
**A:** Use layout-aware parsing/OCR, preserve headings and tables (e.g., as markdown/rows), chunk by structure, and attach metadata.

**60. How do you keep a RAG index up to date?**
**A:** Incremental ingestion with change detection (webhooks/CDC/hash), upsert by stable IDs, delete removed docs, and periodic reconciliation.

**61. How do you prevent duplicate or stale documents?**
**A:** Stable IDs and content hashes, dedupe at ingestion, version/`updated_at` metadata, delete stale entries, and prefer the latest version.

**62. How should the model respond when retrieval returns no useful evidence?**
**A:** Say it doesn't know (abstain) rather than guess, optionally ask a clarifying question or escalate. Use a retrieval-score threshold to trigger this.

**63. How do you reduce hallucinations in RAG?**
**A:** Improve retrieval (hybrid + rerank), instruct "answer only from context", require citations, allow abstention, use low temperature, add a verification pass, and measure faithfulness.

**64. How do you evaluate retrieval quality separately from answer quality?**
**A:** Retrieval: recall@k, precision, MRR, nDCG against labeled relevant chunks. Generation: faithfulness and relevance with fixed gold context.

**65. How would you debug a RAG answer that cites the wrong source?**
**A:** Check what was retrieved, then check citation mapping (chunk ID/metadata mismatch), reranking, and whether the model cites provided IDs. Validate that the citation actually supports the claim.

---

## 4. Prompts, Models, Context, and Structured Outputs (66-85)

**66. What makes a prompt effective and reliable?**
**A:** Clear role and task, explicit constraints, defined output format, examples, only relevant context, an "I don't know" escape hatch, delimiters, and testing against an eval set.

**67. What is the difference between system, developer, and user instructions?**
**A:** System: highest-priority rules and role. Developer: app-level instructions (provider-dependent). User: end-user input, treated as untrusted.

**68. What are few-shot examples?**
**A:** Input-output example pairs in the prompt that show the desired format and behavior.

**69. When would you use zero-shot versus few-shot prompting?**
**A:** Zero-shot for simple, well-known tasks; few-shot when format, edge cases or style matter.

**70. How do temperature and token limits affect output?**
**A:** Temperature controls randomness (low for extraction and tool calls). Max tokens caps length, and too low a cap truncates output (e.g., broken JSON).

**71. What is structured output?**
**A:** Model output constrained to a machine-readable format such as a JSON schema.

**72. Why use JSON Schema or typed output models?**
**A:** They enforce shape, enable automatic validation, and make downstream parsing reliable.

**73. How do you validate model-generated JSON?**
**A:** Parse and validate with Pydantic/Zod/JSON Schema, then check semantic constraints (ranges, enums, business rules).

**74. What should happen when structured output is invalid?**
**A:** Retry with the validation error fed back (bounded), then fall back to a default or human queue, and log it as a metric.

**75. What is a prompt template?**
**A:** A parameterized prompt with variables, for reuse, consistency and testability.

**76. How do you manage and version prompts?**
**A:** Keep them in the repo or a registry, version and review them, link each version to eval results, and deploy via feature flags.

**77. How do you select between OpenAI and Anthropic models?**
**A:** Benchmark on your own eval set for quality, latency, cost, tool-call reliability and context size, and keep the model choice config-driven.

**78. How do you manage provider-specific API differences?**
**A:** An adapter layer that normalizes messages, tools and responses, isolating provider-specific code and covering it with contract tests.

**79. What is a context window?**
**A:** The maximum number of tokens (input plus output) a model can consider in one request.

**80. How do you manage long conversations within a context window?**
**A:** Sliding window, summarization, retrieval of relevant history, trimming tool outputs, and token budgets per section.

**81. What is conversation summarization, and what can it lose?**
**A:** Compressing old turns into a summary. It can lose IDs, constraints and nuance, so pin key facts in structured state.

**82. How do you separate persistent memory from temporary context?**
**A:** Persistent memory (facts, preferences) lives in a database and is retrieved on demand; temporary context is the current messages and working state.

**83. What is prompt injection?**
**A:** Untrusted text containing instructions that the model may follow, overriding the intended behavior.

**84. How do you distinguish trusted instructions from untrusted retrieved content?**
**A:** Keep instructions in the system prompt, delimit and label retrieved content as data, but enforce safety with code-level permissions and validation, not the prompt alone.

**85. How would you debug a model whose responses suddenly become inconsistent?**
**A:** Check for model/provider version changes, prompt or template changes, temperature, context or retrieval changes; compare traces; pin versions; run regression evals.

---

## 5. Tool Calling, APIs, SaaS, and MCP (86-110)

**86. How does an LLM select a tool?**
**A:** It sees tool names, descriptions and schemas plus the conversation, and predicts which tool (if any) fits. Description quality drives accuracy.

**87. How do you define a tool's name, description, and schema?**
**A:** Verb-noun name, a description saying when and when not to use it, and typed parameters with enums, constraints and per-field descriptions.

**88. Why should tool arguments be validated server-side?**
**A:** Model output is untrusted; validate type, range and authorization before executing.

**89. How do you handle malformed tool arguments?**
**A:** Return a specific validation error to the model for a bounded retry; otherwise fall back or escalate.

**90. How do you handle a tool timeout?**
**A:** Set per-tool timeouts, return a structured error, never assume a write succeeded (verify state), and retry only if idempotent.

**91. How should an agent recover from a failed API call?**
**A:** Classify the error, retry transient ones with backoff, return actionable errors for non-retryable ones, try an alternative tool or fallback, and tell the user honestly.

**92. What is the difference between a retry and a fallback?**
**A:** Retry repeats the same operation; fallback switches to a different path (another tool/model, cached result, or human).

**93. How do you prevent duplicate actions when a tool call is retried?**
**A:** Idempotency keys, upserts or check-before-create, dedupe by natural key, and recording completed steps.

**94. What is idempotency, and why does it matter?**
**A:** Repeating a request has the same effect as doing it once. It makes retries and resumes safe.

**95. How do you integrate an agent with a REST API?**
**A:** Wrap endpoints in typed tools with auth, timeouts, error mapping, pagination handling and schema validation.

**96. How do you handle pagination and rate limits?**
**A:** Cursor pagination with server-side filters and summarized results; respect `Retry-After`, use backoff, a token bucket and queues.

**97. How do you manage OAuth tokens and API credentials securely?**
**A:** Secrets manager or vault, OAuth with refresh tokens, least-privilege scopes, short-lived tokens, and never in prompts, code or logs.

**98. How do you integrate an agent with an enterprise SaaS application?**
**A:** OAuth with delegated user identity, a few task-level tools, sandbox testing, pagination and rate-limit handling, error mapping, audit logs and contract tests.

**99. What is MCP (Model Context Protocol)?**
**A:** An open standard for exposing tools, resources and prompts to AI applications through a client-server architecture.

**100. What roles do MCP clients and servers play?**
**A:** The client (inside the host app) discovers and calls capabilities; the server exposes the tools, resources and prompts.

**101. How is MCP different from a direct REST integration?**
**A:** MCP standardizes discovery and invocation across AI apps; a REST integration is service-specific and needs custom glue code per app.

**102. When would you choose MCP over a custom connector?**
**A:** MCP when many clients need to reuse tools, you want standard discovery, or a server already exists. A custom connector when you need tight control, special auth/performance, or no server exists.

**103. How would you register and discover tools safely?**
**A:** A registry with schemas, versions, scopes, risk levels and owners; vetted servers; per-agent/user scoping; sanitized tool descriptions.

**104. How do you stop a model from calling unauthorized tools?**
**A:** Expose only allowed tools per user/agent, enforce authorization in code at execution, deny by default, and log denials.

**105. How do you validate an API response before returning it to the model?**
**A:** Schema validation, strip unneeded or sensitive fields, enforce size limits, sanitize for injection, and normalize errors.

**106. How should an agent handle partial success across multiple tools?**
**A:** Track per-step status, don't claim full success, retry or resume failed steps, compensate if needed, and report the true state clearly.

**107. How do you design compensating actions for a failed multi-step operation?**
**A:** Saga pattern: each step has an undo (cancel/refund/delete); on failure run compensations in reverse, idempotently, with logging.

**108. How do you test a tool integration without calling a real external service?**
**A:** Mocks/stubs, recorded fixtures, sandbox accounts, fake servers and contract tests.

**109. How would you debug an agent that calls the correct tool with wrong arguments?**
**A:** Inspect the trace and schema, improve parameter descriptions and examples, constrain with enums, validate and return clear errors, and add argument-accuracy evals.

**110. Describe an enterprise integration you could build with an agent.**
**A:** Example: read a Zendesk ticket, retrieve KB articles, draft a reply, and update the CRM after approval, using OAuth, idempotent writes and audit logs. Adapt to your real experience.

---

## 6. LLM Evaluation and Testing (111-135)

**111. Why do LLM applications need more than ordinary unit tests?**
**A:** Outputs are non-deterministic and quality is subjective, and behavior depends on prompts, models and data, so you need datasets, metrics and multi-trial evals.

**112. What is an evaluation dataset?**
**A:** A set of inputs with expected outputs or criteria used to score the system.

**113. How do you create representative test cases?**
**A:** Use anonymized real traffic, SME-written cases, edge cases, adversarial inputs and past failures, balanced across categories.

**114. What is task-success rate?**
**A:** The percentage of tasks where the goal was actually achieved, verified through outcome or system state.

**115. How do you measure tool-call accuracy?**
**A:** Compare the chosen tool and arguments against labeled expectations, reporting tool-selection accuracy and argument accuracy.

**116. What is hallucination rate, and how might you estimate it?**
**A:** Unsupported answers divided by total answers. Estimate by checking claims against evidence (LLM judge plus human audit) on a sample.

**117. What is groundedness or faithfulness?**
**A:** Whether the answer's claims are supported by the provided context or evidence.

**118. What is LLM-as-a-judge?**
**A:** Using an LLM to grade outputs against a rubric.

**119. What are the limitations of LLM-as-a-judge?**
**A:** Position, verbosity and self-preference biases, sensitivity to rubric wording, being fooled by fluent errors, and cost. It needs calibration.

**120. How do you calibrate a judge model against human ratings?**
**A:** Have humans label a sample, measure agreement (accuracy/kappa), refine the rubric, and spot-check regularly.

**121. What is a golden dataset?**
**A:** A curated, verified set of high-quality cases with trusted expected results.

**122. What is regression testing for prompts and agents?**
**A:** Re-running the eval suite after any change to confirm quality didn't drop versus a baseline, with pass thresholds.

**123. How do you evaluate retrieval separately from generation?**
**A:** Retrieval metrics against labeled relevant docs for fixed queries; generation metrics with fixed gold context.

**124. What are precision and recall in retrieval?**
**A:** Precision: the fraction of retrieved items that are relevant. Recall: the fraction of relevant items that were retrieved.

**125. How do you test multi-step agent workflows?**
**A:** Use mock tools or a sandbox, assert the trajectory and final state, run multiple trials, and check the step budget.

**126. How do you test edge cases and failure paths?**
**A:** Add invalid inputs, tool errors, timeouts, empty results, ambiguous requests and adversarial cases, and assert graceful handling.

**127. How do you evaluate structured-output validity?**
**A:** Track schema-valid rate, semantic validity and retry rate.

**128. How do you measure whether an agent completed the user's actual goal?**
**A:** Verify the final system state or user-confirmed resolution rather than just the text, using a goal-based rubric.

**129. How do you test safety and policy compliance?**
**A:** An adversarial and injection test set, policy rubrics, refusal tests and PII-leakage tests, automated in CI.

**130. How do you compare two prompts or models fairly?**
**A:** Same dataset and settings, multiple trials, pairwise judging with randomized order, statistical significance, a category breakdown, and cost/latency alongside quality.

**131. How do you detect a quality regression after deployment?**
**A:** Online monitoring: sampled judge scores, user feedback, escalation rate, canary probe sets, and alerts versus baseline.

**132. What is the role of human evaluation?**
**A:** It calibrates automated judges, covers subjective or high-stakes cases, and uncovers new failure modes.

**133. How do you prevent evaluation-data leakage?**
**A:** Keep a held-out set, don't tune prompts on the test set, dedupe, and keep eval cases out of few-shot examples and training data.

**134. Which evaluation metrics would you track in production?**
**A:** Task success, tool accuracy, hallucination/faithfulness, escalation rate, user feedback, latency, cost, error rates and safety triggers.

**135. Design a small evaluation harness for a customer-support agent.**
**A:** A versioned dataset of tickets with expected tool/answer, a mock CRM, a runner with multiple trials, metrics (tool accuracy, task success, faithfulness, safety), baseline diffs, and a CI gate.

---

## 7. Observability, Reliability, and Production (136-155)

**136. What should you log for an agent run?**
**A:** Trace ID, hashed user/tenant, model and prompt version, LLM inputs/outputs, tool calls and results (redacted), retrieval chunks and scores, latency, tokens, cost, errors and guardrail decisions.

**137. What is distributed tracing?**
**A:** Following one request across services and steps using correlated spans.

**138. How do traces help debug multi-step workflows?**
**A:** They show each step's input, output and timing, so you can find the first wrong step and the bottlenecks.

**139. Which latency metrics matter for LLM applications?**
**A:** Time-to-first-token, total latency (p50/p95/p99), and per-step and per-tool latency.

**140. How do you reduce end-to-end response time?**
**A:** Stream, parallelize independent calls, use smaller models where possible, cache (including prompt caching), cut steps, trim context, and cap output.

**141. What is the trade-off between streaming and waiting for a full response?**
**A:** Streaming improves perceived latency but complicates output validation, guardrails and error handling; waiting allows full validation first.

**142. How do you track token usage and model cost?**
**A:** Log usage per call, tag by tenant/feature, aggregate tokens × price, build dashboards, and set budgets and alerts.

**143. How do you set timeouts for model and tool calls?**
**A:** Base them on observed p95/p99 per step with an overall deadline, with shorter limits for tools and longer for LLM calls, and propagate the deadline.

**144. When should a request be retried?**
**A:** On transient failures (timeouts, 429, 5xx) and only if the operation is idempotent; not for 4xx logic errors.

**145. How do exponential backoff and jitter help?**
**A:** Backoff spaces retries out progressively, and jitter randomizes timing to avoid synchronized retry storms.

**146. How do you handle provider rate limits?**
**A:** Respect `Retry-After`, use backoff, queues or token buckets, concurrency limits, fallback models, and request quota increases.

**147. What is a circuit breaker?**
**A:** It stops calling a failing dependency after a failure threshold, then probes it periodically (half-open) to recover.

**148. How do you degrade gracefully when a model provider is unavailable?**
**A:** Fall back to another model/provider, a cached or simpler response, reduced features, or human escalation, with honest user messaging.

**149. How do you detect stalled or runaway agent runs?**
**A:** Max duration/step/token budgets, heartbeats, a watchdog, alerts on stuck runs, and cancellation support.

**150. How do you make background agent jobs reliable?**
**A:** A queue with workers, job IDs, retries with a dead-letter queue, idempotent steps, checkpoints, visibility timeouts and status tracking.

**151. How do you correlate logs across API, workflow, and tool services?**
**A:** Propagate a correlation/trace ID through headers and context, and use structured logging.

**152. What should an operational dashboard show?**
**A:** Request rate, error rate, latency percentiles, cost and tokens, tool failures, loop/budget hits, quality scores and queue depth.

**153. How do you roll out a new prompt or model safely?**
**A:** Offline evals versus baseline, a feature flag, canary traffic with monitoring, and a rollback plan.

**154. How do you investigate a sudden increase in latency or cost?**
**A:** Break it down by trace (step, tool, model), then check context length, retries or loops, traffic changes, prompt/model changes and provider status.

**155. What would you alert on for a production agent platform?**
**A:** Error rate, p95 latency, cost spikes, validation failures, loop/budget hits, guardrail triggers, quality drops, queue backlog and provider errors.

---

## 8. Security, Permissions, and Guardrails (156-175)

**156. What are the main security risks in agentic systems?**
**A:** Prompt injection (direct and indirect), data leakage, excessive agency, privilege escalation, tool misuse or poisoning, cross-tenant leakage, insecure output handling and cost abuse.

**157. What is the principle of least privilege?**
**A:** Grant only the minimum permissions needed for the task.

**158. How do you enforce user-level permissions for tool calls?**
**A:** Pass the user's identity/token to tools and check scopes and ACLs in code before executing, ideally with delegated OAuth.

**159. Why must authorization be enforced outside the prompt?**
**A:** Prompts can be bypassed or injected; code-level checks are deterministic.

**160. How do you prevent cross-tenant data leakage?**
**A:** Enforce tenant filters at the data layer, namespace memory and caches, use scoped tokens and row-level security, and run leakage tests.

**161. How do you defend against prompt injection in retrieved documents?**
**A:** Treat documents as data, delimit them, don't give the content-reading step privileged tools, apply least privilege, require approval for actions, and scan outputs.

**162. How do you treat tool outputs as untrusted input?**
**A:** Validate and sanitize, limit size, never follow instructions inside them, and label them as data.

**163. What is the difference between input validation and output validation?**
**A:** Input validation checks what goes into the system or model; output validation checks what the model produces (schema, PII, policy) before it is used or shown.

**164. How do you protect secrets and credentials?**
**A:** Secrets manager, short-lived credentials, runtime injection, rotation, and never in prompts, code or logs.

**165. What should never be included in application logs?**
**A:** Secrets, tokens, passwords, raw PII and full sensitive payloads.

**166. What is audit logging, and what events should be recorded?**
**A:** An immutable record of who did what and when: tool calls, approvals, denials, config changes and sensitive data access.

**167. How do you trace which user and agent initiated an action?**
**A:** Include user ID, agent ID and session/trace ID in every tool call and log entry.

**168. How do you safely handle tools that change data or trigger payments?**
**A:** Approval gates, amount limits, idempotency keys, dry-run/preview, audit logging, reversibility, and a separate privileged executor.

**169. When should human approval be required?**
**A:** For high-impact, irreversible, financial or external-communication actions, low-confidence cases, and policy-sensitive operations.

**170. How do you limit an agent's available tools and action scope?**
**A:** Per-agent allowlists, scoped permissions, parameter bounds, deny by default, and step budgets.

**171. What are guardrails, and where should they be applied?**
**A:** Checks that constrain behavior, applied at input, output, and tool/action levels.

**172. How do you detect and handle unsafe model outputs?**
**A:** Classifiers and rules, schema/PII checks and groundedness checks; then block, redact, regenerate or escalate.

**173. How do you protect against excessive tool calls and cost abuse?**
**A:** Rate limits, per-user budgets, max steps, token caps, quotas and anomaly alerts.

**174. What security gaps should be escalated to an architecture team?**
**A:** Unaudited tool calls, missing permission checks, shared credentials, no tenant isolation, unvetted tools and PII in logs: document each with evidence and impact, then escalate.

**175. Design a secure approval flow for an agent that updates CRM records.**
**A:** The agent proposes the change (as a diff) → an approval request goes to an authorized user → on approval a privileged service executes it with an idempotency key → everything is audit-logged; stale approvals expire.

---

## 9. Python, Node.js, Databases, and Backend Engineering (176-190)

**176. How would you structure a Python service that exposes an agent workflow?**
**A:** An API layer (FastAPI) → service/orchestration layer (the graph) → tool layer → data layer, with dependency injection, config and typed models.

**177. How do async/await and concurrency help with I/O-bound workloads?**
**A:** They overlap waiting on I/O (LLM and API calls), so one process serves many requests and tool calls can run in parallel.

**178. What can go wrong when blocking code runs in an async service?**
**A:** It blocks the event loop and stalls every request; use async libraries, thread pools or process pools.

**179. How do you validate request and response models in an API?**
**A:** Pydantic (FastAPI) or Zod (Node) to reject invalid data and document the contract via OpenAPI.

**180. How do you design clean interfaces between API, orchestration, and tools?**
**A:** Define interfaces/protocols, keep the API layer thin, keep orchestration transport-independent, and make tools isolated modules.

**181. When would you choose SQL versus NoSQL?**
**A:** SQL for relational data, transactions and joins; NoSQL for flexible schema, horizontal scale or key/document access. Decide by access patterns.

**182. How would you store conversations, messages, and workflow state?**
**A:** Tables for conversations, messages, workflow runs/checkpoints and tool calls, JSONB for flexible parts, indexed by thread and user.

**183. What belongs in a relational database versus a vector store?**
**A:** Relational: business entities, transactions and workflow state. Vector store: embeddings for semantic search (can be co-located using pgvector).

**184. How do transactions help maintain consistency?**
**A:** They make multi-step updates atomic, so they either all apply or all roll back.

**185. How do you design indexes for common query patterns?**
**A:** Index columns used in filters, joins and sorts, order composite indexes to match queries, and verify with `EXPLAIN`.

**186. How do you handle schema migrations safely?**
**A:** Backward-compatible expand/contract migrations, versioned scripts, staging tests and a rollback plan.

**187. What is connection pooling, and why is it important?**
**A:** It reuses database connections to avoid connection overhead and exhaustion, with a limited pool size.

**188. How do you process large document ingestion jobs reliably?**
**A:** Queue plus workers, batching, idempotent processing, checkpointing, retries with a dead-letter queue and progress tracking.

**189. How would you use queues for slow or long-running agent tasks?**
**A:** Enqueue the job, return a job ID, have workers process it, expose status via polling or webhook, and add retries and timeouts.

**190. How do you test and debug a backend endpoint that invokes an LLM?**
**A:** Mock the LLM for unit tests, use recorded responses for integration tests, read trace logs, replay inputs, and add contract tests.

---

## 10. System Design and Experience-Based Questions (191-200)

**191. Design an enterprise agent platform that supports multiple business use cases.**
**A:** Gateway/auth → orchestrator (LangGraph) → tool registry and connectors → RAG service → state store → guardrails → observability and evals, with tenant isolation throughout.

**192. How would you design a customer-support agent with RAG and CRM tools?**
**A:** A router sends requests to RAG on the KB (hybrid + rerank, ACL filters) and CRM tools (OAuth, read/write split) → draft → guardrail check → approval for writes → audit, evaluated end to end.

**193. How would you isolate tenants, permissions, data, and usage limits?**
**A:** Tenant ID at every layer: row-level security, vector filters, namespaced cache and memory, per-tenant quotas and rate limits, scoped credentials and per-tenant audit.

**194. How would you design a workflow that can pause, resume, and recover?**
**A:** LangGraph with a durable checkpointer, interrupts, idempotent steps, a job queue, resume by `thread_id`, and timeouts for pending approvals.

**195. How would you scale document ingestion and retrieval?**
**A:** Queue-based ingestion workers, batched embeddings, a sharded ANN index, caching, incremental updates and autoscaling.

**196. How would you balance quality, latency, reliability, and cost?**
**A:** Model cascade, caching, parallelization, step caps, streaming and fallbacks; make trade-offs explicit and measure with evals and SLOs.

**197. Describe a full-stack AI feature you personally delivered end to end. (Personal)**
**A:** Framework: problem → your contribution → stack → key decisions → testing → outcome → lessons. Be honest about what was yours versus the team's.

**198. Describe an AI-generated change that looked correct but had a defect. How did you find it? (Personal)**
**A:** Framework: what it looked like → how it was detected (tests, evals, review, monitoring) → root cause → fix → safeguard you added. Be honest.

**199. How have you tested, evaluated, or monitored an LLM feature in practice? (Personal)**
**A:** Mention only what you really did (eval set, tracing, feedback, regression tests). If something is missing, say how you would add it.

**200. What would you do in your first 30 days working within an established agent platform?**
**A:** Learn the architecture, patterns and runbooks; read the code; ship a small, well-tested change; understand evals and observability; document gaps and raise them through the proper channels.

---

## 11. Advanced Enterprise Architecture and Production Questions (201-220)

### Enterprise Architecture (201-204)

**201. How would you add a new agent capability without disrupting existing platform services?**
**A:** Use the existing extension points (registry/plugins), a feature flag, backward-compatible contracts, contract tests and a canary rollout.

**202. When would you choose a deterministic workflow over an autonomous agent?**
**A:** When steps are known, predictability or compliance matters, or latency/cost is tight; use agent autonomy only where the path is genuinely uncertain.

**203. How do you decide whether a capability belongs in the agent, backend service, or tool?**
**A:** Agent: reasoning and routing. Tool: a single schema-defined, side-effecting capability. Backend service: deterministic business logic, security and reusable logic.

**204. What would you do if the existing architecture lacked a required permission or audit mechanism?**
**A:** Don't bypass or redesign it alone. Document the gap with evidence and risk, escalate to the architecture/security team with a proposed fix, apply a safe interim mitigation (limit or disable the tool), and follow up.

### Debugging and Recovery (205-208)

**205. How would you debug an agent that selects the correct tool but produces incorrect arguments?**
**A:** Review the trace and schema, improve descriptions, examples and enums, add server-side validation with helpful errors, and add argument-accuracy evals.

**206. How would you investigate a workflow that works locally but fails in production?**
**A:** Compare config, environment, secrets, network egress, data scale and versions; check logs and traces; reproduce with production-like data; improve staging parity.

**207. How do you resume a failed workflow without repeating completed side effects?**
**A:** Checkpoints plus idempotency keys and step-completion records; resume from the last successful step and skip steps already done.

**208. How would you diagnose whether a failure originates from the model, prompt, retrieval, tool, or application?**
**A:** Use traces to isolate each layer: check retrieved context, the prompt, the model output, tool args and results, then application logic; replay each layer separately.

### State and Concurrency (209-212)

**209. How would you manage concurrent updates to shared workflow state?**
**A:** Optimistic concurrency with versioning, reducers for merging, per-thread locks or serialized processing via a queue, and no shared mutable state.

**210. How would you persist and recover agent execution across service restarts?**
**A:** A durable checkpointer, stateless workers, resume by `thread_id`/job ID, idempotent steps, and queue visibility timeouts.

**211. How would you prevent duplicate external actions after a timeout?**
**A:** Idempotency keys, treat a timeout as "unknown" and verify state before retrying, reconcile, and dedupe by natural key.

**212. How would you handle a human approval step that remains pending for several hours?**
**A:** Persist state and pause (no held resources), notify the approver, add reminders/escalation and a TTL, resume on approval, and re-validate state on resume or expire if stale.

### Cost and Performance (213-215)

**213. How would you reduce LLM latency while preserving answer quality?**
**A:** Stream, use a model cascade, trim context and use prompt caching, parallelize, cut steps and tune retrieval, then confirm quality with evals.

**214. When is caching safe for LLM responses and retrieval results?**
**A:** For deterministic, non-personalized, non-sensitive and stable data, with a TTL, keyed by tenant/user/permissions and versioned. Avoid caching permission-dependent, personalized or time-sensitive answers.

**215. How would you set per-user token budgets, timeouts, and tool-call limits?**
**A:** Per-user and per-tenant quotas in Redis/DB, max tokens per request, max steps, timeouts and rate limits, with alerts and graceful user messaging.

### Security and Enterprise Integration (216-218)

**216. How would you enforce user-specific permissions when an agent accesses a CRM?**
**A:** Use a delegated OAuth user token so the CRM enforces its own ACLs, scoped permissions, tool-level checks, no shared admin account, and audit logging.

**217. What should an audit record contain for a tool that modifies business data?**
**A:** Who (user and agent), when, tool, resource ID, parameters and before/after values (redacted), result, approval info, trace ID, model/prompt versions and idempotency key.

**218. How would you safely roll out a new tool integration to a subset of users?**
**A:** Feature flag or allowlist, a canary percentage, monitoring, a kill switch, starting in shadow or read-only mode, and a rollback plan.

### Practical Implementation (219-220)

**219. How would you write unit and integration tests for an agent without making real LLM calls in every test?**
**A:** A fake LLM with scripted responses, unit tests per tool and node, integration tests with recorded fixtures, and a small separate live-eval smoke suite.

**220. How would you deploy a prompt or model change with evaluation gates and a rollback plan?**
**A:** Eval gates in CI (thresholds versus baseline), staging, then a feature-flagged canary with monitoring and automatic rollback; prompts and models are versioned artifacts.

---

## 12. Final Revision Checklist

### Core concepts
- [ ] Explain an agent loop, tool selection, and stopping conditions.
- [ ] Explain chains versus agents and when not to use an agent.
- [ ] Explain LangGraph state, nodes, edges, conditional routing, checkpoints, and recovery.
- [ ] Explain RAG from ingestion through chunking, embeddings, retrieval, reranking, and evaluation.
- [ ] Explain tool schemas, server-side validation, retries, idempotency, and API security.
- [ ] Explain MCP clients, servers, tools, and when to use a connector.

### Evaluation and production
- [ ] Explain evaluation datasets, task success, tool accuracy, LLM-as-a-judge, and regression tests.
- [ ] Explain tracing, latency, token cost, failure analysis, and production alerts.
- [ ] Explain timeouts, retries, backoff, circuit breakers, and graceful degradation.
- [ ] Explain how to test workflows without calling real model APIs in every test.

### Security and architecture
- [ ] Explain least privilege, tenant isolation, prompt injection, approval gates, and audit logging.
- [ ] Explain how you would extend an existing platform without unnecessary redesign.
- [ ] Explain how to identify and escalate an architectural gap.

### Coding and personal examples
- [ ] Practise a Python API endpoint that calls an LLM and validates structured output.
- [ ] Practise a tool with validation, timeout, retry, and mocked tests.
- [ ] Prepare one real project story: problem, your contribution, architecture, trade-offs, tests, outcome, and lessons.
- [ ] Prepare one debugging story and explain the evidence you used to find the root cause.
- [ ] Prepare one example of a production failure, safety control, or evaluation improvement.

---

## Suggested Revision Plan

- **Pass 1: Broad coverage.** Read all 220 short answers and mark weak areas.
- **Pass 2: High-priority topics.** Agentic AI, LangGraph, RAG, tools and APIs, evaluation, security, and production debugging.
- **Pass 3: Practical interview.** Draw an agent architecture, solve a small Python exercise, and practise explaining one project end to end.

## 20 one-liners to memorize
1. **Agent** = LLM + tools + loop + state, with limits.
2. **Least autonomy:** use a workflow when steps are known.
3. **Authorization lives in code, not in the prompt.**
4. **Tool output is untrusted data.**
5. **Validate every model-produced argument server-side.**
6. **Idempotency keys make retries safe.**
7. **RAG debugging:** was the right chunk retrieved? Then was it used correctly?
8. **Hybrid search + rerank** is the enterprise default.
9. **Hallucination fix #1 is better retrieval,** then grounding, abstention and verification.
10. **LangGraph = state + nodes + conditional edges + checkpointer.**
11. **Checkpoints enable resume, replay and human approval.**
12. **Evals:** dataset + metrics + automated runner + CI gate.
13. **Tool accuracy, task success, faithfulness** are the headline agent metrics.
14. **LLM-as-judge needs calibration** against human labels.
15. **Every production failure becomes a regression test.**
16. **Trace everything** (prompt, tool, retrieval), with redaction.
17. **Timeouts, retry with backoff + jitter, circuit breaker, fallback.**
18. **Break the lethal trifecta:** private data + untrusted content + external communication.
19. **Spot an architecture gap?** Document it, escalate it, apply a safe interim mitigation, and don't redesign alone.
20. **Be honest:** say what you built, what you tested, and what you only know conceptually.

**Final reminder:** Do not claim experience you do not have. Explain what you personally built, what you have tested, what you understand conceptually, and how you would approach unfamiliar parts.
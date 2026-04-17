# AgentUp — Complete Interview Preparation Guide

---

## SECTION 1 — How the App Works

---

**Q: Can you walk me through the overall architecture of AgentUp?**

AgentUp is a Next.js 16 full-stack application with three layers. The frontend has three pages — Daily Training, My Cases, and Dashboard — built with React and Tailwind CSS. The backend is Next.js Route Handlers which act as REST API endpoints, replacing the need for a separate Express server. The database is Turso, a hosted SQLite-compatible database accessed via the `@libsql/client` library. The AI layer uses OpenAI API for two separate tasks — simulating the customer and scoring the agent.

---

**Q: Why did you choose Next.js instead of a separate frontend and backend?**

For an MVP with a single user and moderate complexity, Next.js is the cleanest choice. Route Handlers give you all the API functionality of Express inside the same project. One repo, one deployment, one set of environment variables. It reduces infrastructure overhead significantly while keeping the code organized and readable.

---

**Q: How does a Daily Training session work end to end?**

When the agent clicks Start Session, the frontend calls `POST /api/session/start`. The backend picks 3 random cases from the database with varied topics and creates a session row. The frontend then shows the first case — the scenario description and the customer's opening message. The agent types or speaks their reply. That reply goes to `POST /api/session/turn` which calls OpenAI with a customer persona system prompt. OpenAI responds as the customer. This repeats for up to 5 turns. After turn 5 the agent clicks Get My Score, which calls `POST /api/session/score`. OpenAI now acts as a QA evaluator and scores the full transcript across 4 criteria. After all 3 cases are scored, `POST /api/session/complete` saves everything to the database and updates the streak.

---

**Q: How does the AI know how to behave as a customer?**

There are two separate OpenAI calls with completely different system prompts. The first is the Customer AI — its system prompt tells it to stay in character as a customer, gives it the scenario, and maps the difficulty level to a tone. Beginner cases get a polite cooperative customer, Intermediate gets a mildly frustrated one, and Advanced gets an angry adversarial one. The second is the Scorer AI — its system prompt tells it to act as a QA evaluator, gives it the full transcript, and asks it to return a JSON object with scores and feedback.

---

**Q: How is the scoring calculated?**

After 5 turns the full conversation transcript is sent to OpenAI with a scoring prompt. OpenAI evaluates the agent across 4 criteria each worth 25 points:

| Criterion | Weight |
|---|---|
| Empathy & Tone | 25% |
| Accuracy of Information | 25% |
| Resolution / Next Step | 25% |
| Professionalism & Clarity | 25% |

The total is the sum of all four giving a score out of 100. OpenAI also returns one strength sentence and one improvement tip. The response is strictly JSON so it can be parsed and saved directly.

---

**Q: How does the Call channel work? Did you use any paid voice API?**

No paid voice API at all. The Call channel uses two completely free browser-native APIs:

- **SpeechRecognition** — converts the agent's microphone input into text in real time. You can see your words appearing as you speak. Once you stop speaking, that text is sent to OpenAI exactly like a chat message.
- **SpeechSynthesis** — when OpenAI returns the customer reply, the browser reads it aloud using built-in text-to-speech.

The entire voice layer is browser-native, zero cost, zero extra dependencies.

---

**Q: Why did you use Turso instead of a traditional database?**

Turso is SQLite-compatible which keeps the schema simple and matches the assignment requirement. The reason for Turso specifically over local SQLite is Vercel. Vercel's serverless functions have a read-only filesystem so you cannot write a local `.db` file. Turso provides a hosted SQLite database accessible over HTTP that works perfectly in serverless environments. The code uses the same SQL queries you would write for any SQLite database — the only difference is the connection method.

---

**Q: How does the streak system work?**

Every time a session is completed, the backend checks the `last_session_date` in the `user_stats` table:

- If it was **yesterday** → streak increments by 1
- If it was **today already** → streak stays the same (two sessions in one day don't double count)
- If it was **any earlier date** → streak resets to 1

This logic runs in `POST /api/session/complete` and the streak is immediately shown on the summary screen and dashboard.

---

**Q: How are custom cases immediately available in training?**

When an agent creates a case on the My Cases page, it is saved to Turso via `POST /api/cases`. The session start endpoint queries all cases with:

```sql
SELECT * FROM cases ORDER BY RANDOM()
```

It has no filter for default cases only — so the new custom case is in the pool immediately on the next session start.

---

**Q: How does the Both channel work?**

When a case has channel set to Both, the training page detects this and shows a channel picker screen before the conversation starts. The agent sees two buttons — Chat and Call — and picks whichever they want to practice with. This choice is stored in local state and determines whether ChatWindow or CallWindow loads.

---

**Q: How does the Dashboard get its data?**

The dashboard makes three parallel API calls on load using `Promise.all`:

| Endpoint | Returns |
|---|---|
| `/api/dashboard/stats` | Streak, sessions this week, top skill, skill to improve, last 10 sessions |
| `/api/dashboard/scores` | Daily average scores for last 30 days (line chart) |
| `/api/dashboard/by-topic` | Average scores grouped by topic and channel (bar charts) |

All three are SQL aggregate queries on the `sessions` and `session_cases` tables joined with `cases`.

---

## SECTION 2 — Technical Deep Dives

---

**Q: Why did you use Zustand for state management instead of Redux or Context?**

Zustand is significantly lighter than Redux — no boilerplate, no reducers, no providers. For this app the state is straightforward — current session, current case index, chat history, session results, and loading flags. Zustand handles all of this in one file with simple get and set functions. Context would have caused unnecessary re-renders across the whole tree. Redux would have been massive overkill for a single-user MVP.

---

**Q: How do you handle the stale closure problem in the Call window?**

This was a real bug I fixed. The Web Speech API's `onend` callback is set up once on mount. If you read React state directly inside that callback, you always get the initial value because the closure captures the value at the time it was created — not the current value. The fix is to use `useRef` alongside `useState`. Every time the state updates, a `useEffect` syncs the new value into the ref. The `onend` callback reads from the ref, which always has the latest value. I used three refs to fix three separate stale closure bugs:

```js
const phaseRef      = useRef('idle');  // fixes: onend couldn't see current phase
const transcriptRef = useRef('');      // fixes: onend always sent empty transcript
const turnCountRef  = useRef(0);       // fixes: turn counter never reached max
```

---

**Q: How do you prevent the AI from returning invalid JSON for scoring?**

The scorer system prompt says explicitly to return only valid JSON with no markdown backticks and no explanation. The response is then wrapped in a try-catch. If `JSON.parse` fails, the code strips any markdown fences before parsing. If it still fails, a fallback object with default scores of 15 each is returned so the app never crashes on a scoring failure.

---

**Q: How is conversation history maintained across turns?**

Each turn the frontend sends the full conversation history as a messages array to the API. OpenAI's chat completion API requires the full history every call because it is stateless — it has no memory between calls. The history is built from the messages already displayed in the chat window, mapped to OpenAI format with roles of `user` and `assistant`. This is the standard pattern for multi-turn conversations with OpenAI.

---

**Q: What is the database schema?**

| Table | Purpose |
|---|---|
| `cases` | All training scenarios — title, scenario, opening message, channel, topic, difficulty, default flag |
| `sessions` | Each completed session — date, average score, streak at time |
| `session_cases` | Join table — links sessions to 3 cases, stores score, feedback JSON, turns JSON |
| `user_stats` | Single row — current streak, best streak, last session date |

---

## SECTION 3 — Extra Features Added Beyond MVP

---

**Q: What did you build beyond the basic PRD requirements?**

**7 default cases instead of 5**
The PRD asked for at least 5. I seeded 7 covering Billing, De-escalation, Retention, Technical, Refunds, Security, and a second Billing case. This gives more variety immediately out of the box.

**Varied topic selection**
The session start logic first tries to pick cases with different topics so every session feels varied. Only if there are not enough unique topics does it fill remaining slots with repeats.

**Best streak tracking**
The `user_stats` table stores both `current_streak` and `best_streak` so the dashboard can show your personal best, not just your current run.

**Score colour coding**
Scores above 75 show in green, 50–75 in amber, below 50 in red throughout the app — in the score ring, score card, and dashboard charts. Instant visual feedback without reading a number.

**Live transcript preview**
In Call mode, as you speak, your words appear in a dashed blue bubble in real time before you have finished speaking. Gives confidence that the mic is working.

**Microphone permission error handling**
If the browser blocks mic access, the app shows a specific helpful message explaining how to fix it, rather than silently failing.

**Custom topic creation**
The form has a dropdown with existing topics and a "+ New topic" option that reveals a text input. A small but complete UX detail that the PRD required.

**Channel picker for Both cases**
A deliberate picker screen so the agent consciously chooses Chat or Call for Both-channel cases rather than it defaulting silently.

---

## SECTION 4 — Enhancements for the Future

---

**Q: If you had more time, what would you improve first?**

**Past session replay** — The full conversation transcript is already saved in the database in `turns_json`. Building a screen where agents can go back and read any past conversation, see exactly what they said, and compare it to their score would be very valuable for learning. The data is there — it just needs a UI.

---

**Q: What other enhancements would make this production-ready?**

| Enhancement | Value |
|---|---|
| **Authentication** | Multi-user support via NextAuth with Google or email login |
| **Manager dashboard** | Team lead view — compare agent scores, identify who needs coaching |
| **Leaderboard** | Weekly score ranking across all agents — drives daily habit |
| **Push notifications** | Daily reminder with current streak — biggest driver of habit formation |
| **AI case generation** | Describe a situation in plain English, AI generates the full scenario automatically |
| **Difficulty progression** | Auto-increase difficulty as scores improve consistently |
| **Voice selection** | Let agent choose customer voice — different voice per difficulty level |
| **Detailed score history** | Per-criterion chart over time — is Empathy improving separately from Accuracy? |
| **Session scheduling** | Block training time in calendar — makes it a fixed part of the workday |
| **Export report** | PDF summary of an agent's monthly progress for manager 1-on-1 reviews |

---

**Q: What would you change about the technical architecture for scale?**

For a team of hundreds of agents:

- **Database** → Move from Turso to PostgreSQL (Neon or Supabase) with Prisma as the ORM for type safety and migration management
- **Queue** → Add BullMQ for OpenAI scoring calls to handle concurrent requests without hitting rate limits
- **Frontend state** → Add React Query alongside Zustand for server state (cases list, dashboard data) to get caching and background refetching for free
- **Auth** → NextAuth with role-based access for agents vs managers

---

## SECTION 5 — Prompt Engineering

---

**Q: How did you write the system prompt for the customer AI?**

The customer prompt has four parts. First it sets the role — "You are roleplaying as a customer contacting a company's support centre." Second it injects the scenario text so the AI knows exactly what the customer's problem is. Third it sets the tone based on difficulty — polite for Beginner, mildly frustrated for Intermediate, angry and adversarial for Advanced. Fourth it gives hard rules — respond in 1 to 3 sentences only, never break character, never offer solutions yourself, never mention being an AI. The short sentence limit is critical — without it the AI gives long essays instead of realistic customer replies.

---

**Q: How does the difficulty level actually change the customer's behaviour?**

The difficulty maps to a tone instruction injected into the system prompt:

| Difficulty | Tone Instruction |
|---|---|
| Beginner | Polite, patient, cooperative. You respond calmly and are open to help. |
| Intermediate | Mildly frustrated and want clear answers quickly. You may sigh or express impatience but remain civil. |
| Advanced | Very angry, stressed and adversarial. You interrupt, challenge answers and may threaten to cancel or escalate. Do NOT become satisfied easily. |

The AI reads this instruction and genuinely adjusts its replies. An Advanced customer will push back even on good answers, making it harder for the agent to score well.

---

**Q: How did you write the scoring prompt to get consistent results?**

The scoring prompt is designed to be deterministic. It tells the model it is a QA evaluator, gives it the full transcript, defines exactly what each criterion means in one sentence, specifies the exact score range (0 to 25 per criterion), and ends with the exact JSON format to return. The key line is "Respond ONLY with this JSON, no backticks, no markdown, no explanation." Giving the model the exact output format with field names and types eliminates ambiguity and gets consistent parseable responses.

---

**Q: What happens if the AI goes off script and breaks character?**

The system prompt has an explicit rule — "Never mention that you are an AI" and "Stay strictly in character as the customer." In practice GPT-4 class models follow this reliably. If an edge case ever caused a break in character, the impact is just a slightly odd customer reply — it does not crash the app. The scoring happens on the transcript regardless of what was said, and the agent can still complete the session.

---

**Q: Why do you send the full conversation history every turn instead of just the latest message?**

OpenAI's API is completely stateless — it has no memory of previous calls. If you only send the latest message, the model has no context and gives a generic reply unrelated to what was said before. Sending the full history as a messages array lets the model understand the entire conversation and respond appropriately — if the customer was angry in turn 2, they should still be somewhat frustrated in turn 4 unless the agent genuinely resolved the issue.

---

## SECTION 6 — Error Handling & Edge Cases

---

**Q: What happens if the OpenAI API call fails during a session?**

For the customer turn, the `catch` block sets the phase back to idle and logs the error. The user sees no crash — the chat just stops and they can try again. For the scoring call, the catch block returns a fallback score object with 15 points per criterion and a generic feedback message. This means the session always completes even if scoring fails. The fallback is clearly a safety net — a real production app would show an error state and offer a retry button.

---

**Q: What if the user closes the browser mid-session?**

The session row is created in the database when the session starts. If the user closes the browser before completing, that session row stays in the database with an average score of 0 and no session_cases rows. It will appear in dashboard queries but with a 0 score. In a production app you would add a `status` column to the sessions table — `in_progress` vs `completed` — and filter out incomplete sessions from all dashboard queries.

---

**Q: What happens if the microphone stops working mid-call?**

The `onerror` handler on SpeechRecognition catches this. If the error is `not-allowed` it sets a `permissionDenied` state and shows a specific message explaining how to allow microphone access. For other errors it just resets the phase back to idle so the user can tap the mic button again. The call log is not lost — everything already said is still on screen and the session can continue if the mic issue is resolved.

---

**Q: How do you handle the case where Turso is down or unreachable?**

Every API route is wrapped in a try-catch. If the Turso connection fails, the route returns a 500 response with the error message. On the frontend, loading states and error boundaries prevent blank screens. In practice Turso has very high uptime and the connection is over HTTPS. For a production app you would add retry logic with exponential backoff for transient connection failures.

---

**Q: What if someone submits the case creation form with empty fields?**

The frontend validates that title, scenario, opening message, and topic are all non-empty before making the API call. The backend also validates these fields and returns a 400 error with the message "All fields are required" if any are missing. Both layers of validation mean you cannot save an incomplete case through the UI or directly via the API.

---

## SECTION 7 — React & Frontend Patterns

---

**Q: Why did you use useCallback for handleAgentSpoke in CallWindow?**

`handleAgentSpoke` is an async function that is referenced inside the `useEffect` that sets up SpeechRecognition. Without `useCallback`, a new function reference would be created on every render, which would trigger the `useEffect` to re-run and reinitialize the SpeechRecognition instance on every render. Wrapping it in `useCallback` with a stable dependency array means the function reference only changes when its dependencies genuinely change.

---

**Q: Why do you use a ref for the SpeechRecognition instance instead of state?**

SpeechRecognition is an external imperative API — you call `.start()` and `.stop()` on it directly. It is not React-managed data that should trigger re-renders. Storing it in a ref with `useRef` gives you a stable reference to the instance across renders without causing any re-renders when it is updated. Putting it in state would cause unnecessary re-renders every time the component updated.

---

**Q: How does the live transcript preview work in the Call window?**

SpeechRecognition has an `interimResults: true` option. This means it fires the `onresult` event continuously as you speak, not just when you stop. Each `onresult` event contains all recognized words so far. The component stores this in the `transcript` state and renders it in a dashed blue bubble while `phase === 'listening'`. When the recognition ends, the final transcript is sent to the API and the bubble disappears.

---

**Q: Why does the chat window scroll to the bottom automatically?**

There is a `bottomRef` attached to an empty `div` at the end of the messages list. A `useEffect` watches the `messages` array and calls `bottomRef.current?.scrollIntoView({ behavior: 'smooth' })` whenever a new message is added. This ensures the latest message is always visible without the user having to scroll manually, which is standard behaviour for any chat interface.

---

**Q: How do you prevent the agent from sending an empty message?**

The send button is disabled when `input.trim()` is falsy or when a request is already loading. The `handleSend` function also returns early if `input.trim()` is empty as a second safety check. This prevents blank messages from being sent to OpenAI which would waste API calls and give meaningless customer responses.

---

## SECTION 8 — Deployment & Infrastructure

---

**Q: Why did you choose Vercel for deployment?**

Vercel is the natural deployment platform for Next.js — it was built by the same team. Zero configuration deployment, automatic HTTPS, environment variable management, and preview deployments on every push. For a hiring exercise it is the fastest way to get a working live URL. The free tier is sufficient for a demo app with low traffic.

---

**Q: What environment variables does the app need to run?**

Three variables:

| Variable | Purpose |
|---|---|
| `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` | AI customer simulation and scoring |
| `TURSO_DATABASE_URL` | Turso database connection URL |
| `TURSO_AUTH_TOKEN` | Turso authentication token |

Without the AI key the session turn and score endpoints return 500 errors. Without the Turso credentials the database connection fails and no data can be read or written.

---

**Q: How does the app behave differently in local development vs production?**

In local development `npm run dev` starts the Next.js dev server with hot reload. The app connects to the same Turso cloud database as production because both environments use the same `.env.local` values. This means data created locally is visible on the live site and vice versa. If you want separate databases for local and production you would set a `file:./data/agentup.db` URL in `.env.local` for local development and keep the Turso cloud URL only in Vercel environment variables.

---

**Q: Why can't you use better-sqlite3 on Vercel?**

`better-sqlite3` is a native Node.js addon — it requires compilation during `npm install` using node-gyp. Vercel's serverless function environment does not support native addons because the functions are packaged and deployed as zip archives without a build environment. Additionally Vercel's filesystem is read-only except for `/tmp`, so even if you could install it, you cannot write a persistent `.db` file. Turso solves both problems — it is a pure JavaScript HTTP client with no native deps, connecting to a database hosted elsewhere.

---

**Q: How would you add CI/CD to this project?**

Add a GitHub Actions workflow that runs on every push to main. The workflow would install dependencies, run a build check with `npm run build`, and if successful trigger a Vercel deployment via the Vercel CLI or the Vercel GitHub integration. The Vercel GitHub integration actually does this automatically when you connect the repo — every push to main deploys to production and every pull request gets a preview URL.

---

## SECTION 9 — Product & Design Thinking

---

**Q: Why is a daily streak important for this kind of app?**

A streak is a habit-forming mechanism. Call centre agents have busy shifts and training can easily be deprioritized. Showing a streak counter creates a loss-aversion effect — agents do not want to break their streak. This is the same psychology used by Duolingo. It costs nothing to implement and meaningfully increases daily engagement. The PRD explicitly asked for it because IAG understands this motivational mechanic.

---

**Q: Why are there 3 cases per session instead of more?**

Three cases takes roughly 15 to 20 minutes to complete — short enough to do before a shift starts. More cases would make it feel like a chore rather than a quick daily habit. The PRD was explicit about this: "short daily AI-powered training sessions." The constraint of 3 cases with 5 turns each is a deliberate product decision to maximize completion rate.

---

**Q: Why does difficulty matter for the AI customer's tone?**

A new agent needs to build confidence first — a polite cooperative customer lets them practice the basics of listening, empathy, and resolution without being overwhelmed. An experienced agent needs to be challenged — an angry adversarial customer tests whether their skills hold up under pressure, which is closer to the real high-stress situations in a call centre. The difficulty setting lets the training match where the agent actually is in their development.

---

**Q: What is the product value of the Dashboard page?**

The dashboard turns raw training data into actionable insight. Without it agents complete sessions and get scores but have no way to see trends or patterns. The dashboard shows whether scores are improving over time, which topics the agent struggles with most, whether Chat or Call is weaker, and how consistent their training habit is. This self-awareness is what converts practice into genuine skill improvement.

---

**Q: Why does the app support custom cases and not just default ones?**

Every call centre is different. An insurance company handles claims and policy disputes. A telecom handles outages and billing. A bank handles fraud and account issues. The 7 default cases are generic starting points. Custom cases let agents practice the exact scenarios they face in their actual job, making the training directly relevant to their daily work. This is the difference between generic training and personalised training.

---

**Q: How would you measure if this app is actually improving agent performance?**

You would track two types of metrics. In-app metrics: average score trend over time, streak consistency, most improved topic, time to reach 80+ average score. Real-world metrics (outside the app): call handle time before and after using AgentUp, customer satisfaction scores, first call resolution rate, number of escalations. The in-app scores are a proxy — the real test is whether those scores correlate with better performance on actual calls.

---

## SECTION 10 — Tricky Follow-up Questions

---

**Q: How do you know the AI scoring is fair and consistent?**

Honestly, it is not perfectly consistent — LLMs have some variability. Two identical transcripts might score 78 and 82 on different runs. For an MVP this is acceptable. To make it more consistent in production you would set `temperature: 0` on the scoring call, which makes the model more deterministic. You could also run each transcript through scoring twice and average the results, or build a calibration set of known-good and known-bad transcripts to test scoring drift over time.

---

**Q: What stops an agent from just typing nonsense to get through the session quickly?**

Nothing technically prevents it in the current MVP — an agent could type "aaa" five times and complete the session. The AI customer would react oddly and the score would be very low. In a production app with managers you would add minimum response length validation, flag sessions where scores are below 20 as suspicious, and the manager dashboard would make it obvious who is gaming the system.

---

**Q: The app has no authentication. Is that a security risk?**

For this MVP with a single mocked user it is not a concern. The API routes are open but they only read and write training data — there is no sensitive personal data, no payments, no PII. In production with real agents you would add NextAuth which takes about an hour to implement. Every API route would check the session token and scope all database queries to the authenticated user's ID.

---

**Q: How would you handle multiple agents using the same deployment right now?**

Right now all agents share the same `user_stats` row and the same session history — there is only one mocked user. If two people used the app simultaneously, their sessions would mix together in the database. The fix is adding a `user_id` column to `sessions`, `session_cases`, and `user_stats`, and passing the user ID through every query. This is the most important production change — everything else is already structured correctly for multi-user with just this one addition.

---

**Q: Why did you store turns_json as a JSON string in SQLite instead of a separate table?**

The turns for a session case are always read and written together — you never need to query individual turns in isolation. Storing them as a JSON string in one column is simpler, faster to read, and avoids a join. SQLite handles JSON strings efficiently. The tradeoff is you cannot query inside the turns with SQL — but since the app never needs to filter or aggregate by turn content, this tradeoff is correct for this use case.

---

**Q: What is the biggest technical risk in this project?**

The biggest risk is OpenAI API latency. Each customer turn waits for an OpenAI response which typically takes 1 to 3 seconds. In a chat interface this is fine — users expect some delay. In the Call interface it feels more awkward because real phone calls have no 2-second processing pause between responses. The mitigation would be streaming the OpenAI response token by token and starting TTS as soon as the first sentence arrives, rather than waiting for the complete reply.

---

## SECTION 11 — Quick Reference

---

### Tech Stack

| Layer | Technology |
|---|---|
| Framework | Next.js 16 (App Router) |
| Styling | Tailwind CSS v4 + CSS variables |
| AI | OpenAI API |
| Database | Turso (hosted SQLite) |
| State | Zustand |
| Charts | Recharts |
| Icons | Lucide React |
| Voice | Web Speech API (browser-native) |
| Deployment | Vercel |

---

### API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/session/start` | Pick 3 cases, create session |
| POST | `/api/session/turn` | OpenAI customer AI response |
| POST | `/api/session/score` | OpenAI scoring after 5 turns |
| POST | `/api/session/complete` | Save results, update streak |
| GET | `/api/cases` | List all cases with filters |
| POST | `/api/cases` | Create new case |
| GET | `/api/cases/[id]` | Get single case |
| DELETE | `/api/cases/[id]` | Delete custom case |
| GET | `/api/dashboard/stats` | Streak, skills, recent sessions |
| GET | `/api/dashboard/scores` | 30-day score history |
| GET | `/api/dashboard/by-topic` | Score by topic and channel |

---

### PRD Coverage

| Requirement | Status |
|---|---|
| 3 scenarios per session | ✅ |
| Up to 5 turns per case | ✅ |
| AI customer in character | ✅ |
| Difficulty affects customer tone | ✅ |
| Score 0–100 with 4 criteria | ✅ |
| Written strength + tip feedback | ✅ |
| Session summary with streak | ✅ |
| At least 5 default cases | ✅ 7 seeded |
| Agent can create custom cases | ✅ |
| Custom cases in training immediately | ✅ |
| Chat channel | ✅ |
| Call channel with mic + TTS | ✅ |
| Both channel with picker | ✅ |
| Filter cases by topic/channel/difficulty | ✅ |
| Score over time chart (30 days) | ✅ |
| Score by topic and channel charts | ✅ |
| Streak, sessions this week, top skill | ✅ |
| Last 10 sessions with score + case title | ✅ |
| Responsive web (no native mobile app) | ✅ |
| Single mocked user (no auth) | ✅ |

---

*Good luck with the interview! You built a complete working product — answer confidently.* 🎯

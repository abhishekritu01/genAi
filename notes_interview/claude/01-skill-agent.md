# Claude Code Skills — Complete Notes

---

## 1. What Are Skills?

Skills are **reusable Markdown files** that teach Claude Code how to handle specific tasks automatically — without repeating instructions every session.

> **Analogy:** Instead of telling Claude "here's how I want PR reviews done" every single time, you write it once as a skill and Claude applies it automatically whenever relevant.

### Key Properties
- Stored in a `SKILL.md` file inside a named directory
- Have a **name** and **description** in frontmatter (YAML header)
- Load **on demand** — only when Claude matches a request to the skill
- Do **not** consume context window unless activated

---

## 2. Anatomy of a Skill

Every skill has two parts:

```
~/.claude/skills/
└── pr-review/           ← named directory (matches skill name)
    └── SKILL.md         ← the skill file (exactly this name, case-sensitive)
```

### SKILL.md Structure

```markdown
---
name: pr-review
description: Reviews pull requests for code quality. Use when reviewing PRs or checking code changes.
allowed-tools: Read, Grep, Glob, Bash
model: sonnet
---

## Instructions go here

1. Check for code smells
2. Verify test coverage
3. Review naming conventions
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | ✅ Yes | Lowercase, hyphens only, max 64 chars. Must match directory name. |
| `description` | ✅ Yes | Tells Claude *when* to use the skill. Max 1,024 chars. **Most important field.** |
| `allowed-tools` | ❌ Optional | Restricts which tools Claude can use when the skill is active. |
| `model` | ❌ Optional | Specifies which Claude model to use for the skill. |

---

## 3. Where Skills Live

```
# Personal skills (follow you across ALL projects)
~/.claude/skills/skill-name/SKILL.md

# Project skills (shared with everyone who clones the repo)
<repo-root>/.claude/skills/skill-name/SKILL.md

# Windows personal path
C:/Users/<your-user>/.claude/skills/skill-name/SKILL.md
```

| Location | Scope | Use Case |
|----------|-------|----------|
| `~/.claude/skills/` | Personal | Your commit style, doc format, how you like code explained |
| `.claude/skills/` | Project/Team | Team coding standards, brand guidelines, project-specific workflows |

---

## 4. How Skill Matching Works

1. Claude Code **scans** all skill locations at startup — loads only `name` + `description` (not full content)
2. When you send a request, Claude **semantically matches** it against all skill descriptions
3. A **confirmation prompt** appears before loading the full skill into context
4. After confirmation, Claude reads the complete `SKILL.md` and follows its instructions

```
You: "write a PR description for my changes"
         ↓
Claude scans descriptions → finds "pr-description" skill → asks to confirm
         ↓
You confirm → full SKILL.md loads → Claude follows instructions
```

> **Tip:** If a skill isn't triggering, the description language doesn't overlap enough with how you phrase requests. Add trigger phrases like "help me profile this", "why is this slow?", "make this faster".

---

## 5. Skill Priority (Conflict Resolution)

When two skills share the same name, this hierarchy decides which wins:

```
Enterprise  (highest priority — always wins)
    ↓
Personal    (~/.claude/skills/)
    ↓
Project     (.claude/skills/ in repo)
    ↓
Plugins     (lowest priority)
```

**Example conflict:** If your company has an enterprise `code-review` skill and you have a personal `code-review` skill → the enterprise one always wins.

**Fix:** Use descriptive, unique names like `frontend-review` or `backend-review` instead of generic names.

---

## 6. Skills vs. Other Claude Code Features

| Feature | When It Loads | Best For |
|---------|--------------|----------|
| **Skills** | On demand, when request matches | Task-specific expertise that's only sometimes relevant |
| **CLAUDE.md** | Every conversation, always | Always-on project standards, constraints, framework prefs |
| **Subagents** | Explicit delegation | Isolated task execution in a separate context |
| **Hooks** | Event-driven (file save, tool call) | Automated side effects, validation, linting on events |
| **MCP Servers** | External tools/integrations | Connecting Claude to external APIs and services |

### Decision Guide

```
Always applies to the project?          → CLAUDE.md
Task-specific, loads when needed?       → Skill
Fires on file save / tool call events?  → Hook
Isolated delegated work?                → Subagent
External API / tool integration?        → MCP Server
```

---

## 7. Writing Effective Descriptions

A good description answers **two questions**:
1. What does the skill do?
2. When should Claude use it?

### Bad Description ❌
```yaml
description: Helps with docs
```

### Good Description ✅
```yaml
description: Writes and improves technical documentation. Use when creating README files,
API docs, inline code comments, or when the user asks to document a function, module, or project.
```

> **Rule of thumb:** Include the exact phrases users would say when they need this skill.

---

## 8. Restricting Tools with `allowed-tools`

Use `allowed-tools` to limit what Claude can do when a skill is active — great for **read-only** or **security-sensitive** workflows.

```yaml
---
name: codebase-onboarding
description: Helps new developers understand how the system works.
allowed-tools: Read, Grep, Glob, Bash
model: sonnet
---
```

With this, Claude can only *read* the codebase — no editing, no writing files.

If `allowed-tools` is **omitted**, Claude uses its normal permission model (no restrictions).

---

## 9. Multi-File Skills (Progressive Disclosure)

For complex skills, avoid cramming everything into one huge `SKILL.md`. Instead:

```
.claude/skills/
└── architecture-guide/
    ├── SKILL.md              ← core instructions (keep under 500 lines)
    ├── references/
    │   └── architecture.md   ← loaded only when needed
    ├── scripts/
    │   └── validate.sh       ← runs without loading content into context
    └── assets/
        └── diagram.png
```

### In SKILL.md, link conditionally:
```markdown
## Instructions

For general questions, follow the steps below.
For system design questions, read `references/architecture.md` first.
```

**Benefits:**
- Context window stays clean — references load only when relevant
- Easier to maintain (modular structure)
- Scripts run and only their *output* consumes tokens (not the script itself)

> **Rule:** Keep `SKILL.md` under **500 lines**. If longer, split into reference files.

---

## 10. Sharing Skills

### Method 1: Git Repository (Team)
Commit skills to `.claude/skills/` — anyone who clones the repo gets them automatically.
```
repo-root/
└── .claude/
    └── skills/
        └── pr-review/
            └── SKILL.md
```

### Method 2: Plugins (Community)
Create a plugin with a `skills/` directory and distribute via a marketplace.

### Method 3: Enterprise Managed Settings (Organization-wide)
Admins deploy skills org-wide via managed settings. These take **highest priority**.

```json
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/approved-plugins" },
    { "source": "npm", "package": "@acme-corp/compliance-plugins" }
  ]
}
```

Use enterprise deployment for: mandatory standards, compliance, security requirements.

---

## 11. Skills + Subagents

> ⚠️ **Gotcha:** Subagents do **NOT** automatically inherit your skills.

- **Built-in agents** (Explorer, Plan, Verify) → cannot access skills at all
- **Custom subagents** → can use skills, but only if explicitly listed in frontmatter

### Custom Subagent with Skills

Create a file in `.claude/agents/`:

```markdown
---
name: frontend-security-reviewer
description: "Use this agent to review frontend code for accessibility and security issues."
tools: Bash, Glob, Grep, Read, WebFetch, WebSearch
model: sonnet
color: blue
skills: accessibility-audit, performance-check
---

Review the provided frontend code for accessibility (WCAG 2.1) and security issues.
```

Skills are **loaded at subagent startup**, not on demand like in the main conversation.

---

## 12. Troubleshooting Checklists

### Skill Doesn't Trigger
- [ ] Check your description — does it overlap with how you're phrasing requests?
- [ ] Add more trigger phrases users would actually say
- [ ] Test variations: "help me profile this", "why is this slow?", "optimize this"

### Skill Doesn't Load
- [ ] Is `SKILL.md` inside a **named directory** (not at the `skills/` root)?
- [ ] Is the file named exactly `SKILL.md` (all caps `SKILL`, lowercase `md`)?
- [ ] Run `claude --debug` and look for error messages mentioning your skill name
- [ ] Validate YAML frontmatter syntax

### Wrong Skill Gets Used
- [ ] Are two skill descriptions too similar? Make them more distinct
- [ ] Be more specific in both descriptions

### Priority Conflict (Personal Skill Ignored)
- [ ] Check if an enterprise/higher-priority skill has the same name
- [ ] Rename your skill to something more unique

### Plugin Skills Not Appearing
- [ ] Clear the cache
- [ ] Restart Claude Code
- [ ] Reinstall the plugin
- [ ] Validate plugin structure with the skills validator tool

### Runtime Errors
- [ ] Are all dependencies installed? Document them in the skill description
- [ ] Do scripts have execute permission? Run `chmod +x script.sh`
- [ ] Are path separators forward slashes `/` (even on Windows)?

---

## 13. Quick Reference

```
# Create a personal skill
mkdir -p ~/.claude/skills/my-skill
touch ~/.claude/skills/my-skill/SKILL.md

# Create a project skill
mkdir -p .claude/skills/my-skill
touch .claude/skills/my-skill/SKILL.md

# Restart Claude Code after any changes to skills
```

### Minimal Skill Template
```markdown
---
name: my-skill-name
description: Does X. Use when the user asks to Y or Z.
---

## Instructions

1. Step one
2. Step two
3. Step three
```

### Full Skill Template
```markdown
---
name: my-skill-name
description: Does X. Use when the user asks to Y, Z, or mentions keywords A and B.
allowed-tools: Read, Grep, Glob, Bash
model: sonnet
---

## Instructions

Core instructions here (keep this file under 500 lines).

For detailed reference on topic X, read `references/topic-x.md`.
For validation, run `scripts/validate.sh` (do not read it, just run it).
```

---

> **Golden Rule:** If you find yourself explaining the same thing to Claude repeatedly — that's a skill waiting to be written.
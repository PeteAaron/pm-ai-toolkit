# pm-ai-toolkit

Shared foundation for building reusable AI-powered product management tools and workflows.

---

## Overview

`pm-ai-toolkit` is the core toolkit layer in a wider PM AI ecosystem.

It is not a standalone application. It is the **foundation** — a set of shared components that
other repos import, extend and build on top of. Think of it as the standard library for this
system: model adapters, prompt templates, structured output schemas and utility functions that
would otherwise be duplicated across every project.

---

## Why This Exists

Most LLM usage in practice starts the same way: a one-off prompt in a chat interface, a
hardcoded API call, a script that only works for one specific case.

That approach breaks down quickly. Prompts become inconsistent. Outputs are hard to validate.
Switching models means rewriting integration code. Nothing is reusable.

This toolkit exists to solve that problem by providing a **structured, repeatable base** for
building AI-powered PM workflows:

- **Reusable prompts** — templates that work across projects, not just one script
- **Model abstraction** — swap Claude for OpenAI (or vice versa) without touching workflow code
- **Structured outputs** — Pydantic schemas enforce what the model returns, making outputs
  reliable and programmatically usable
- **Shared utilities** — file loading, text cleaning, env config — handled once, used everywhere
- **Evaluation scaffolding** — test prompt quality systematically, not just by eyeballing results

The goal is to build AI tools that are **consistent, maintainable and scalable** — not just
functional in the moment.

---

## How It Fits Into the System

This repo is the base layer. Other repos in the ecosystem depend on it.

```text
pm-ai-toolkit           → shared foundation (this repo)
pm-ai-studio            → main app — Streamlit interface for PM workflows
pm-ai-claude-workflows  → prompt-first workflows and automation scripts
pm-ai-labs              → experiments, prototypes and research
```

**pm-ai-toolkit** provides the building blocks.
**pm-ai-studio** assembles those blocks into a usable product.
**pm-ai-claude-workflows** uses them to run structured, repeatable workflows.
**pm-ai-labs** uses them as a base for experimentation without duplicating infrastructure.

Every repo in the system benefits from improvements made here — to adapters, schemas, or
prompts — without needing to maintain their own versions.

---

## What This Repo Provides

| Component   | Purpose                                                               |
| ----------- | --------------------------------------------------------------------- |
| `adapters/` | Model abstraction layer — call Claude or OpenAI through one interface |
| `prompts/`  | Reusable prompt templates for common PM tasks                         |
| `schemas/`  | Pydantic models for structured, validated LLM outputs                 |
| `utils/`    | File loading, text processing and environment config helpers          |
| `evals/`    | Evaluation runner, test cases and scoring rubric                      |
| `examples/` | End-to-end working demos                                              |
| `tests/`    | Unit and smoke tests                                                  |

---

## How It's Used

The core flow is simple:

```text
input → prompt template → adapter → model → structured output → schema validation
```

A downstream app or script:

1. Loads a prompt template from `prompts/`
2. Injects its input (meeting notes, a brief, a feature request)
3. Calls `generate()` from `adapters/llm` with a model choice
4. Validates the response against a Pydantic schema from `schemas/`
5. Uses the structured result — saves it, displays it, or passes it to the next step

The adapter layer means the same workflow code runs against Claude or OpenAI. The schema layer
means outputs are predictable and parseable, not raw strings.

---

## Example Usage

The `examples/` folder contains working end-to-end demos.

**Meeting summarisation** — takes raw meeting notes, returns a structured summary with decisions
and action items.

**PRD generation** — takes a product brief, returns a structured PRD with goals, requirements,
and success metrics.

**Quickstart:**

```bash
cp .env.example .env
# Add your ANTHROPIC_API_KEY and/or OPENAI_API_KEY

pip install -e .

python examples/meeting_summary_demo.py
python examples/prd_demo.py
```

Sample inputs are in `examples/sample_inputs/`. Outputs are written to `examples/sample_outputs/`.

---

## Design Principles

- **Start with real PM problems** — every component exists because a real workflow needs it
- **Prefer simple, useful systems** — no unnecessary abstraction; solve the actual problem
- **Design for reuse** — components should work across projects, not just one use case
- **Support multiple modes** — the same toolkit works in scripts, apps, APIs and experiments
- **Build → use → refine** — ship working tools, use them in practice, improve from real feedback

---

## Current Status

- Foundation complete — adapters, schemas, prompts, utils, evals all in place
- Examples implemented — meeting summarisation and PRD generation working end-to-end
- Tests passing — unit and smoke coverage across core modules
- Ready to support the application layer

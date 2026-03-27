# pm-ai-toolkit

Shared foundation for reusable AI-powered PM tools, workflows and experiments.

## Overview

`pm-ai-toolkit` is the core toolkit layer in a wider PM AI ecosystem.

It provides the shared building blocks used across apps, prompt-first workflows and experiments, including:

- model adapters
- prompt templates
- structured output schemas
- utility functions
- reusable evaluation patterns

The purpose of this repo is to create a consistent, reusable base for building practical AI-powered workflows that support real-world product management work.

This is not a standalone end-user product. It is the foundation layer that other repos and tools will build on top of.

---

## Why this exists

Most LLM usage starts as ad-hoc prompting.

This toolkit is designed to move beyond that by creating a more structured and repeatable approach to building AI-powered PM workflows.

The goal is to make it easier to:

- reuse prompt and workflow patterns
- switch between model providers
- validate and structure outputs
- handle common file and text processing tasks
- test and improve prompt quality over time

---

## Scope

This repository is intended to support workflows such as:

- PRD generation
- meeting summarisation and action extraction
- roadmap prioritisation
- stakeholder update generation
- document Q&A and retrieval workflows
- future experiments in evaluation, RAG and agentic patterns

---

## Repository Structure

```text
pm-ai-toolkit/
  adapters/    # model/provider abstraction (Claude, OpenAI)
  prompts/     # reusable prompt templates and examples
  schemas/     # structured output definitions (Pydantic)
  utils/       # file handling, text processing, env config
  evals/       # evaluation test cases, rubric, and runner
  tests/       # unit and smoke tests
  ui/          # reserved for future UI helpers/components
  templates/   # reserved for future project/workflow templates
```

---

## Setup

**1. Install dependencies**

```bash
pip install -e ".[dev]"
```

**2. Configure API keys**

```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY and/or OPENAI_API_KEY
```

**3. Run tests**

```bash
pytest
```

---

## Usage

```python
from utils.files import load_file
from utils.text import clean_text
from adapters.llm import generate
from schemas.prd import PRDOutput
import json

# Load and clean a brief
brief = clean_text(load_file("my_brief.md"))

# Build the prompt and call the LLM
prompt_template = load_file("prompts/prd_generator.md")
prompt = prompt_template.replace("{{INPUT}}", brief)
result = generate(prompt, model="claude")

# Validate structured output with Pydantic
prd = PRDOutput(**json.loads(result["content"]))
print(prd.title)
```

`generate()` accepts `model="claude"` (default), `model="openai"`, or any full model ID
such as `"claude-3-5-sonnet-20241022"` or `"gpt-4-turbo"`. It always returns:

```python
{
    "provider": "anthropic" | "openai",
    "model": "...",     # exact model ID used
    "content": "...",   # text response
    "raw": ...,         # original SDK response object
}
```

---

## Running Evals

```bash
python evals/runner.py
```

Loads test cases from `evals/test_cases/`, calls the LLM, and prints PASS/FAIL for each case.
Score outputs manually using the criteria in `evals/rubric.md`.

---

## Related Repos

This toolkit is the shared dependency for other repos in the PM AI system. Specific tools
(Slack bots, Notion integrations, CLIs) import from here rather than re-implementing adapter
or schema logic independently.

# Changelog

## v0.1.0 — 2026-03-27

Initial release. Foundation layer complete and ready to support the application layer.

### Added

**Adapters**
- `adapters/llm.py` — `generate()` function with unified interface for Claude and OpenAI
- Model shorthand resolution (`"claude"`, `"openai"`) and full model ID passthrough
- Normalised response shape: `{provider, model, content, raw}`

**Schemas**
- `schemas/prd.py` — `PRDOutput` Pydantic model for structured PRD generation
- `schemas/meeting.py` — `MeetingSummary` Pydantic model for meeting summarisation
- `schemas/roadmap.py` — `RoadmapItem` with computed priority score `(impact × confidence) / effort`

**Prompts**
- `prompts/prd_generator.md` — PRD generation prompt with structured JSON output
- `prompts/meeting_summariser.md` — Meeting summariser prompt with structured JSON output
- `prompts/base_template.md` — Standard prompt template structure and authoring guide

**Utils**
- `utils/files.py` — `load_file()` for `.txt`, `.md`, and `.pdf` files
- `utils/text.py` — `clean_text()`, `chunk_text()`, `extract_json()`
- `utils/config.py` — `load_env()` and `get_api_key()` with clear error messages

**Evals**
- `evals/runner.py` — eval runner that loads test cases, calls the LLM, and prints PASS/FAIL
- `evals/test_cases/prd_sample.json` — sample PRD eval case
- `evals/rubric.md` — scoring rubric for PRD and meeting summarisation quality

**Examples**
- `examples/meeting_summary_demo.py` — end-to-end meeting summarisation demo
- `examples/prd_demo.py` — end-to-end PRD generation demo
- `examples/sample_inputs/` — realistic sample meeting notes and product brief
- `examples/sample_outputs/` — representative sample outputs aligned with schemas

**Tests**
- Unit and smoke tests across adapters, schemas, and utils (`pytest`)

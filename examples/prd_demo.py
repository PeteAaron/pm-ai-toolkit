"""
PRD generator demo.

Loads rough product notes, sends them through the PRD prompt template and LLM adapter,
validates the output against the PRDOutput schema, and prints a rendered result.

Usage:
    python examples/prd_demo.py
    python examples/prd_demo.py --model openai
    python examples/prd_demo.py --input path/to/notes.md
"""
import argparse
import json
import sys
from pathlib import Path

# Allow running from repo root or from examples/
REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))

from adapters.llm import generate
from schemas.prd import PRDOutput
from utils.files import load_file
from utils.text import clean_text

PROMPT_FILE = REPO_ROOT / "prompts" / "prd_generator.md"
DEFAULT_INPUT = REPO_ROOT / "examples" / "sample_inputs" / "prd_notes.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a PRD from rough product notes.")
    parser.add_argument("--model", default="claude", help="Model to use: claude or openai")
    parser.add_argument("--input", default=str(DEFAULT_INPUT), help="Path to product notes file")
    parser.add_argument("--save", action="store_true", help="Save output to sample_outputs/")
    return parser.parse_args()


def extract_json(text: str) -> str:
    """Strip markdown code fences if the model wrapped the JSON."""
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        text = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])
    return text.strip()


def render(prd: PRDOutput) -> str:
    def section(title: str, items: list[str]) -> list[str]:
        if not items:
            return []
        lines = [title]
        for item in items:
            lines.append(f"  • {item}")
        return lines + [""]

    lines = ["=" * 60, f"PRD: {prd.title}", "=" * 60, ""]
    lines += ["PROBLEM STATEMENT", f"  {prd.problem_statement}", ""]
    lines += section("USER SEGMENTS", prd.user_segments)
    lines += section("GOALS", prd.goals)
    lines += section("ASSUMPTIONS", prd.assumptions)
    lines += section("RISKS", prd.risks)
    lines += section("OPEN QUESTIONS", prd.open_questions)
    return "\n".join(lines)


def main() -> None:
    args = parse_args()

    # Load and clean the product notes
    print(f"Loading product notes: {args.input}")
    notes = clean_text(load_file(args.input))

    # Build the prompt
    prompt_template = load_file(PROMPT_FILE)
    prompt = prompt_template.replace("{{INPUT}}", notes)

    # Call the LLM
    print(f"Calling model: {args.model} ...")
    result = generate(prompt, model=args.model)
    print(f"Provider: {result['provider']} / Model: {result['model']}")

    # Parse and validate
    try:
        parsed = json.loads(extract_json(result["content"]))
        prd = PRDOutput(**parsed)
    except (json.JSONDecodeError, Exception) as exc:
        print(f"\nFailed to parse output: {exc}")
        print("\nRaw response:\n", result["content"])
        sys.exit(1)

    # Render and print
    output = render(prd)
    print()
    print(output)

    # Optionally save
    if args.save:
        out_path = REPO_ROOT / "examples" / "sample_outputs" / "prd_output.json"
        out_path.write_text(
            json.dumps(parsed, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(f"Saved to: {out_path}")


if __name__ == "__main__":
    main()

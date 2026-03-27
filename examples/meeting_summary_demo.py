"""
Meeting summariser demo.

Loads a meeting transcript, sends it through the prompt template and LLM adapter,
validates the output against the MeetingSummary schema, and prints a rendered result.

Usage:
    python examples/meeting_summary_demo.py
    python examples/meeting_summary_demo.py --model openai
    python examples/meeting_summary_demo.py --input path/to/transcript.txt
"""
import argparse
import json
import sys
from pathlib import Path

# Allow running from repo root or from examples/
REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))

from adapters.llm import generate
from schemas.meeting import MeetingSummary
from utils.files import load_file
from utils.text import clean_text, extract_json

PROMPT_FILE = REPO_ROOT / "prompts" / "meeting_summariser.md"
DEFAULT_INPUT = REPO_ROOT / "examples" / "sample_inputs" / "meeting_notes.txt"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarise a meeting transcript.")
    parser.add_argument("--model", default="claude", help="Model to use: claude or openai")
    parser.add_argument("--input", default=str(DEFAULT_INPUT), help="Path to transcript file")
    parser.add_argument("--save", action="store_true", help="Save output to sample_outputs/")
    return parser.parse_args()


def render(summary: MeetingSummary) -> str:
    lines = ["=" * 60, "MEETING SUMMARY", "=" * 60, ""]
    lines.append(summary.summary)
    lines.append("")
    if summary.decisions:
        lines.append("DECISIONS")
        for d in summary.decisions:
            lines.append(f"  • {d}")
        lines.append("")
    if summary.action_items:
        lines.append("ACTION ITEMS")
        for i, item in enumerate(summary.action_items):
            owner = summary.owners[i] if i < len(summary.owners) else "Unassigned"
            lines.append(f"  • {item}  [{owner}]")
        lines.append("")
    if summary.risks:
        lines.append("RISKS")
        for r in summary.risks:
            lines.append(f"  • {r}")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    args = parse_args()

    # Load and clean the transcript
    print(f"Loading transcript: {args.input}")
    transcript = clean_text(load_file(args.input))

    # Build the prompt
    prompt_template = load_file(PROMPT_FILE)
    prompt = prompt_template.replace("{{TRANSCRIPT}}", transcript)

    # Call the LLM
    print(f"Calling model: {args.model} ...")
    result = generate(prompt, model=args.model)
    print(f"Provider: {result['provider']} / Model: {result['model']}")

    # Parse and validate
    try:
        parsed = json.loads(extract_json(result["content"]))
        summary = MeetingSummary(**parsed)
    except (json.JSONDecodeError, Exception) as exc:
        print(f"\nFailed to parse output: {exc}")
        print("\nRaw response:\n", result["content"])
        sys.exit(1)

    # Render and print
    output = render(summary)
    print()
    print(output)

    # Optionally save
    if args.save:
        out_path = REPO_ROOT / "examples" / "sample_outputs" / "meeting_summary.json"
        out_path.write_text(
            json.dumps(parsed, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(f"Saved to: {out_path}")


if __name__ == "__main__":
    main()

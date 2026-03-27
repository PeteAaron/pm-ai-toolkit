"""
Simple eval runner. Loads test cases from evals/test_cases/, sends each to the LLM,
validates the output against the relevant schema, and prints a pass/fail result.

Usage:
    python evals/runner.py
"""
import json
import sys
from pathlib import Path

# Allow running directly from repo root or from evals/
sys.path.insert(0, str(Path(__file__).parent.parent))

from adapters.llm import generate
from schemas.prd import PRDOutput
from utils.files import load_file

CASES_DIR = Path(__file__).parent / "test_cases"
PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def run_prd_eval(case_path: Path) -> dict:
    case = json.loads(case_path.read_text(encoding="utf-8"))
    prompt_template = load_file(PROMPTS_DIR / "prd_generator.md")
    prompt = prompt_template.replace("{{INPUT}}", case["input"])

    result = generate(prompt, model="claude")

    try:
        parsed = json.loads(result["content"])
        prd = PRDOutput(**parsed)
        missing = [f for f in case["expected_fields"] if not getattr(prd, f, None)]
        status = "PASS" if not missing else f"PARTIAL (missing: {missing})"
    except json.JSONDecodeError as exc:
        status = f"FAIL (invalid JSON: {exc})"
    except Exception as exc:
        status = f"FAIL ({exc})"

    return {"case_id": case["id"], "status": status}


def main() -> None:
    prd_cases = sorted(CASES_DIR.glob("prd_*.json"))
    if not prd_cases:
        print("No test cases found in evals/test_cases/")
        return

    results = [run_prd_eval(case_file) for case_file in prd_cases]
    for r in results:
        print(f"[{r['status']}] {r['case_id']}")


if __name__ == "__main__":
    main()

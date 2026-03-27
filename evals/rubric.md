# Evaluation Rubric

Use this rubric to score prompt outputs consistently. Score each criterion 1–5.

---

## prd_quality

Applies to outputs from `prompts/prd_generator.md`.

| Criterion                | Score 1                | Score 3                            | Score 5                                       |
| ------------------------ | ---------------------- | ---------------------------------- | --------------------------------------------- |
| **Problem clarity**      | Vague or missing       | Partially clear, reader must infer | Specific, user-focused, no ambiguity          |
| **Goals specificity**    | No measurable goals    | Goals stated but vague             | Measurable, outcome-oriented                  |
| **Assumptions captured** | None listed            | 1–2 obvious ones                   | Substantive, non-obvious assumptions surfaced |
| **Risks identified**     | None listed            | Generic risks ("might be slow")    | Domain-specific, actionable risks             |
| **No hallucination**     | Invented facts present | Minor extrapolation beyond input   | Grounded entirely in input                    |

**Scoring guide:**

- 23–25: Strong — ready to share with engineering
- 18–22: Acceptable — minor revision needed
- Below 18: Weak — prompt or input needs improvement

---

## meeting_quality

Applies to outputs from `prompts/meeting_summariser.md`.

| Criterion             | Score 1                            | Score 3                 | Score 5                                       |
| --------------------- | ---------------------------------- | ----------------------- | --------------------------------------------- |
| **Summary accuracy**  | Misses key topics or is inaccurate | Covers most topics      | Complete and concise, nothing missing         |
| **Action items**      | Missing or incorrect               | Mostly captured         | All items captured                            |
| **Owner attribution** | Owners missing or wrong            | Most owners correct     | All items have correct owners or "Unassigned" |
| **Decisions**         | Vague or missing                   | Most decisions captured | All decisions, clearly stated                 |
| **No hallucination**  | Added context not in transcript    | Minor inference         | Strictly grounded in transcript               |

**Scoring guide:**

- 23–25: Strong — reliable for async follow-up
- 18–22: Acceptable — worth a quick review
- Below 18: Weak — not suitable for distribution

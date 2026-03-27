# Prompt Template Structure

All prompts in this toolkit follow this structure.
Sections marked [REQUIRED] must be present. Others are optional depending on the use case.

---

## Role [REQUIRED]

You are [role description].

Define the model's persona and domain expertise. Be specific — "a senior product manager" is
more effective than "an AI assistant".

---

## Task / Objective [REQUIRED]

[Clear single-sentence statement of what the model must produce.]

One sentence. Imperative form. No ambiguity.

---

## Context

[Background information the model needs to understand the situation.]

Omit this section if there is no stable background context. Do not repeat what is in the Input.

---

## Input

[Description of what the user will supply at runtime.]

Use a placeholder like `{{INPUT}}` or `{{TRANSCRIPT}}` for variable content that will be
substituted before sending the prompt.

---

## Constraints

- [Constraint 1 — what the model must NOT do]
- [Constraint 2 — what the model must stay within]

Use constraints to prevent hallucination, scope creep, or format drift.

---

## Output Format [REQUIRED]

[Exact specification of the output format.]

If JSON: include a complete example JSON block with field names and expected types.
If markdown: specify the heading structure.
If prose: specify length and register.

Example (JSON):

```json
{
  "field_name": "string",
  "list_field": ["string"],
  "numeric_field": 0
}
```

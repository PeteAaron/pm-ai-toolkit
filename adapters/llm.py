from utils.config import get_api_key, load_env

CLAUDE_DEFAULT_MODEL = "claude-haiku-4-5"
OPENAI_DEFAULT_MODEL = "gpt-5.4-nano"


def generate(
    prompt: str,
    model: str = "claude",
    temperature: float = 0.2,
) -> dict:
    """
    Send a prompt to an LLM and return a normalised response dict.

    model can be:
      - "claude"  → uses Claude 3.5 Sonnet via Anthropic SDK
      - "openai"  → uses gpt-5.4-nano via OpenAI SDK
      - a full model ID like "claude-haiku-4-5" or "gpt-5.4-nano"

    Returns:
        {
            "provider": "anthropic" | "openai",
            "model": str,       # exact model ID used
            "content": str,     # extracted text content
            "raw": object,      # raw SDK response for inspection
        }

    Raises:
        ValueError: missing API key, unsupported provider
    """
    load_env()
    provider, model_id = _resolve_model(model)
    if provider == "anthropic":
        return _call_anthropic(prompt, model_id, temperature)
    if provider == "openai":
        return _call_openai(prompt, model_id, temperature)
    raise ValueError(f"Unsupported provider resolved from model='{model}'")


def _resolve_model(model: str) -> tuple[str, str]:
    """Map a shorthand or full model ID to (provider, model_id)."""
    lower = model.lower()
    if lower == "claude":
        return "anthropic", CLAUDE_DEFAULT_MODEL
    if lower in ("openai", "gpt"):
        return "openai", OPENAI_DEFAULT_MODEL
    if lower.startswith("claude"):
        return "anthropic", model
    if lower.startswith("gpt") or lower.startswith("o1") or lower.startswith("o3"):
        return "openai", model
    raise ValueError(
        f"Cannot determine provider for model='{model}'. "
        "Use 'claude', 'openai', or a full model ID like 'claude-haiku-4-5'."
    )


def _call_anthropic(prompt: str, model_id: str, temperature: float) -> dict:
    import anthropic  # lazy import

    api_key = get_api_key("anthropic")
    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model=model_id,
        max_tokens=4096,
        temperature=temperature,
        messages=[{"role": "user", "content": prompt}],
    )
    content = response.content[0].text
    return {"provider": "anthropic", "model": model_id, "content": content, "raw": response}


def _call_openai(prompt: str, model_id: str, temperature: float) -> dict:
    import openai  # lazy import

    api_key = get_api_key("openai")
    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model_id,
        temperature=temperature,
        messages=[{"role": "user", "content": prompt}],
    )
    content = response.choices[0].message.content
    return {"provider": "openai", "model": model_id, "content": content, "raw": response}

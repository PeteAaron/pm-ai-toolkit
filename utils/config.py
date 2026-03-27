import os

from dotenv import load_dotenv


def load_env() -> None:
    """Load .env file into environment. Safe to call multiple times."""
    load_dotenv()


def get_api_key(provider: str) -> str:
    """
    Return the API key for a given provider name.
    Raises ValueError with a clear message if the key is missing or provider is unknown.
    """
    key_map = {
        "claude": "ANTHROPIC_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "openai": "OPENAI_API_KEY",
    }
    env_var = key_map.get(provider.lower())
    if env_var is None:
        raise ValueError(
            f"Unsupported provider: '{provider}'. Choose from: claude, anthropic, openai."
        )
    value = os.environ.get(env_var)
    if not value:
        raise ValueError(
            f"Missing API key. Set {env_var} in your .env file or environment."
        )
    return value

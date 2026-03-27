from unittest.mock import MagicMock, patch

import pytest

from adapters.llm import _resolve_model, generate
from utils.config import get_api_key

# --- _resolve_model ---

def test_resolve_model_claude_shorthand():
    provider, model_id = _resolve_model("claude")
    assert provider == "anthropic"
    assert "claude" in model_id


def test_resolve_model_openai_shorthand():
    provider, model_id = _resolve_model("openai")
    assert provider == "openai"
    assert "gpt" in model_id


def test_resolve_model_full_claude_id():
    provider, model_id = _resolve_model("claude-haiku-4-5")
    assert provider == "anthropic"
    assert model_id == "claude-haiku-4-5"


def test_resolve_model_full_gpt_id():
    provider, model_id = _resolve_model("gpt-5.4-nano")
    assert provider == "openai"
    assert model_id == "gpt-5.4-nano"


def test_resolve_model_unsupported_raises():
    with pytest.raises(ValueError, match="Cannot determine provider"):
        _resolve_model("llama-3-70b")


# --- generate with mocked Anthropic ---

def test_generate_claude_returns_normalised_dict():
    mock_text_block = MagicMock()
    mock_text_block.text = "Generated PRD content"
    mock_response = MagicMock()
    mock_response.content = [mock_text_block]

    with (
        patch("adapters.llm.load_env"),
        patch("adapters.llm.get_api_key", return_value="fake-key"),
        patch("anthropic.Anthropic") as mock_client_class,
    ):
        mock_client = mock_client_class.return_value
        mock_client.messages.create.return_value = mock_response
        result = generate("Test prompt", model="claude")

    assert result["provider"] == "anthropic"
    assert result["content"] == "Generated PRD content"
    assert "model" in result
    assert "raw" in result


# --- generate with mocked OpenAI ---

def test_generate_openai_returns_normalised_dict():
    mock_choice = MagicMock()
    mock_choice.message.content = "OpenAI response text"
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]

    with (
        patch("adapters.llm.load_env"),
        patch("adapters.llm.get_api_key", return_value="fake-key"),
        patch("openai.OpenAI") as mock_client_class,
    ):
        mock_client = mock_client_class.return_value
        mock_client.chat.completions.create.return_value = mock_response
        result = generate("Test prompt", model="openai")

    assert result["provider"] == "openai"
    assert result["content"] == "OpenAI response text"
    assert "raw" in result


# --- get_api_key error handling ---

def test_get_api_key_missing_raises_clear_error():
    with patch.dict("os.environ", {}, clear=True), patch("utils.config.load_env"):
        with pytest.raises(ValueError, match="Missing API key"):
            get_api_key("anthropic")


def test_get_api_key_unsupported_provider_raises():
    with pytest.raises(ValueError, match="Unsupported provider"):
        get_api_key("cohere")

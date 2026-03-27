import pytest

from utils.files import load_file
from utils.text import chunk_text, clean_text

# --- clean_text ---

def test_clean_text_collapses_spaces():
    assert clean_text("hello   world") == "hello world"


def test_clean_text_strips_edges():
    assert clean_text("  hello  ") == "hello"


def test_clean_text_normalises_crlf():
    result = clean_text("line one\r\nline two")
    assert "\r" not in result
    assert "line one\nline two" == result


def test_clean_text_collapses_blank_lines():
    result = clean_text("para one\n\n\n\npara two")
    assert result == "para one\n\npara two"


def test_clean_text_collapses_tabs():
    assert clean_text("col1\t\tcol2") == "col1 col2"


# --- chunk_text ---

def test_chunk_text_short_input_is_unchanged():
    text = "Short text."
    assert chunk_text(text, max_chars=4000) == ["Short text."]


def test_chunk_text_splits_long_input():
    para = "A" * 100
    long_text = "\n\n".join([para] * 50)  # ~5100 chars
    chunks = chunk_text(long_text, max_chars=1000)
    assert len(chunks) > 1


def test_chunk_text_chunks_are_within_limit():
    para = "B" * 100
    long_text = "\n\n".join([para] * 50)
    chunks = chunk_text(long_text, max_chars=500, overlap=50)
    # Each chunk should not massively exceed max_chars (overlap can push slightly over)
    for chunk in chunks:
        assert len(chunk) <= 700


def test_chunk_text_single_large_paragraph():
    # A single paragraph larger than max_chars should be returned as-is
    big_para = "X" * 5000
    chunks = chunk_text(big_para, max_chars=1000)
    assert len(chunks) == 1
    assert chunks[0] == big_para


# --- load_file ---

def test_load_file_txt(tmp_path):
    f = tmp_path / "test.txt"
    f.write_text("hello world", encoding="utf-8")
    assert load_file(f) == "hello world"


def test_load_file_md(tmp_path):
    f = tmp_path / "test.md"
    f.write_text("# Title\n\nContent.", encoding="utf-8")
    assert load_file(f) == "# Title\n\nContent."


def test_load_file_unsupported_extension(tmp_path):
    f = tmp_path / "document.docx"
    f.write_bytes(b"fake content")
    with pytest.raises(ValueError, match="Unsupported file type"):
        load_file(f)


def test_load_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_file("/nonexistent/path/file.txt")

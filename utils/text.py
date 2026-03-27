import re


def extract_json(text: str) -> str:
    """Strip markdown code fences if the model wrapped the JSON output."""
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        text = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])
    return text.strip()


def clean_text(text: str) -> str:
    """
    Normalise whitespace: collapse multiple spaces/tabs to single space,
    normalise line endings, collapse 3+ blank lines to 2, strip edges.
    """
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk_text(text: str, max_chars: int = 4000, overlap: int = 200) -> list[str]:
    """
    Split text into overlapping chunks of at most max_chars characters.
    Splits on paragraph boundaries where possible to avoid cutting mid-sentence.
    Overlap ensures context is not lost at chunk boundaries.
    """
    if len(text) <= max_chars:
        return [text]

    paragraphs = text.split("\n\n")
    chunks: list[str] = []
    current = ""

    for para in paragraphs:
        candidate = (current + "\n\n" + para) if current else para
        if len(candidate) > max_chars:
            if current:
                chunks.append(current.strip())
                # Start next chunk with overlap from end of previous
                tail = current[-overlap:] if len(current) > overlap else current
                current = tail + "\n\n" + para
            else:
                # Single paragraph exceeds max_chars — include as-is
                chunks.append(para.strip())
                current = ""
        else:
            current = candidate

    if current.strip():
        chunks.append(current.strip())

    return chunks

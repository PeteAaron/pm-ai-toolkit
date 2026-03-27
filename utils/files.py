from pathlib import Path


def load_file(path: str | Path) -> str:
    """
    Load text content from .txt, .md, or .pdf files.
    Returns the content as a plain string.
    Raises ValueError for unsupported extensions.
    Raises FileNotFoundError if the file does not exist.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")
    suffix = p.suffix.lower()
    if suffix in (".txt", ".md"):
        return p.read_text(encoding="utf-8")
    if suffix == ".pdf":
        return _load_pdf(p)
    raise ValueError(f"Unsupported file type: '{suffix}'. Supported: .txt, .md, .pdf")


def _load_pdf(path: Path) -> str:
    from pypdf import PdfReader  # lazy import — only needed when PDFs are used

    reader = PdfReader(str(path))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages)

from pathlib import Path

def read_file_with_fallback(file_path: str) -> str:
    """Read file with UTF-8 encoding, fallback to latin-1 and cp1252."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    for encoding in ["utf-8", "latin-1", "cp1252"]:
        try:
            with open(file_path, "r", encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    
    raise ValueError(f"Could not decode file {file_path} with any supported encoding")

def write_file_with_encoding(file_path: str, content: str, encoding: str = "utf-8"):
    """Write file with specified encoding."""
    with open(file_path, "w", encoding=encoding) as f:
        f.write(content)

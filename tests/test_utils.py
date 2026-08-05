import pytest
from pathlib import Path
import tempfile
from mcp_server.utils import read_file_with_fallback

def test_read_utf8_file():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write("Conteúdo em UTF-8: ãõç")
        temp_path = f.name
    
    try:
        content = read_file_with_fallback(temp_path)
        assert "ãõç" in content
    finally:
        Path(temp_path).unlink()

def test_read_latin1_file():
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.txt', delete=False) as f:
        f.write("Conteúdo em Latin-1: ãõç".encode('latin-1'))
        temp_path = f.name
    
    try:
        content = read_file_with_fallback(temp_path)
        assert "ãõç" in content
    finally:
        Path(temp_path).unlink()

def test_read_nonexistent_file():
    with pytest.raises(FileNotFoundError):
        read_file_with_fallback("/nonexistent/file.txt")

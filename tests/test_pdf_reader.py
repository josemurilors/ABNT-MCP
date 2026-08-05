import pytest
from pathlib import Path
import tempfile
from pypdf import PdfWriter
from mcp_server.tools.pdf_reader import read_pdf_paper

def test_read_pdf_all_pages():
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
        temp_path = f.name
    
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    writer.add_blank_page(width=200, height=200)
    with open(temp_path, 'wb') as f:
        writer.write(f)
    
    try:
        result = read_pdf_paper(temp_path)
        assert result["status"] == "success"
        assert result["total_pages"] == 2
    finally:
        Path(temp_path).unlink()

def test_read_pdf_specific_pages():
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
        temp_path = f.name
    
    writer = PdfWriter()
    for i in range(5):
        writer.add_blank_page(width=200, height=200)
    with open(temp_path, 'wb') as f:
        writer.write(f)
    
    try:
        result = read_pdf_paper(temp_path, pages=[0, 2, 4])
        assert result["status"] == "success"
        assert result["extracted_pages"] == [0, 2, 4]
    finally:
        Path(temp_path).unlink()

def test_read_nonexistent_pdf():
    result = read_pdf_paper("/nonexistent/file.pdf")
    assert result["status"] == "error"
    assert "not found" in result["message"].lower()

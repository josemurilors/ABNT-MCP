import pytest
from unittest.mock import patch, Mock
from pathlib import Path
import tempfile
from mcp_server.tools.bibtex_fetcher import get_bibtex_by_doi, clean_bibtex

@patch('mcp_server.tools.bibtex_fetcher.requests.get')
def test_get_bibtex_by_doi(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "@article{doe2023, author={Doe, John}, title={Test}, year={2023}}"
    mock_get.return_value = mock_response
    
    result = get_bibtex_by_doi("10.1234/test")
    
    assert result["status"] == "fetched"
    assert "@article{doe2023" in result["bibtex"]

@patch('mcp_server.tools.bibtex_fetcher.requests.get')
def test_get_bibtex_with_insert(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "@article{doe2023, author={Doe, John}, title={Test}, year={2023}}"
    mock_get.return_value = mock_response
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.bib', delete=False) as f:
        f.write("")
        temp_path = f.name
    
    try:
        result = get_bibtex_by_doi("10.1234/test", bib_path=temp_path)
        assert result["status"] == "added"
        
        content = Path(temp_path).read_text()
        assert "@article{doe2023" in content
    finally:
        Path(temp_path).unlink()

@patch('mcp_server.tools.bibtex_fetcher.requests.get')
def test_get_bibtex_anti_duplication(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "@article{doe2023, author={Doe, John}, title={Test}, year={2023}}"
    mock_get.return_value = mock_response
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.bib', delete=False) as f:
        f.write("@article{doe2023, author={Doe, John}, title={Test}, year={2023}}")
        temp_path = f.name
    
    try:
        result = get_bibtex_by_doi("10.1234/test", bib_path=temp_path)
        assert result["status"] == "duplicate"
    finally:
        Path(temp_path).unlink()

def test_clean_bibtex():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.bib', delete=False, encoding='utf-8') as f:
        f.write("@article{DOE2023, author={SILVA, JOAO}, title={Testão}, year={2023}}")
        temp_path = f.name
    
    try:
        result = clean_bibtex(temp_path)
        assert result["status"] == "cleaned"
        assert "doe2023" in result["cleaned_bibtex"].lower()
    finally:
        Path(temp_path).unlink()

import pytest
from unittest.mock import patch, Mock
from mcp_server.tools.academic_search import search_papers

@patch('mcp_server.tools.academic_search.requests.get')
def test_search_papers_crossref(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "message": {
            "items": [
                {
                    "DOI": "10.1234/test",
                    "title": ["Test Article"],
                    "author": [{"given": "John", "family": "Doe"}],
                    "issued": {"date-parts": [[2023]]}
                }
            ]
        }
    }
    mock_get.return_value = mock_response
    
    result = search_papers("machine learning", limit=1, source="crossref")
    
    assert result["status"] == "success"
    assert len(result["papers"]) == 1
    assert result["papers"][0]["doi"] == "10.1234/test"
    assert result["papers"][0]["title"] == "Test Article"

@patch('mcp_server.tools.academic_search.requests.get')
def test_search_papers_with_email(mock_get):
    import os
    os.environ["TCC_MCP_EMAIL"] = "test@example.com"
    
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": {"items": []}}
    mock_get.return_value = mock_response
    
    search_papers("test", limit=1)
    
    call_args = mock_get.call_args
    assert "mailto:test@example.com" in call_args[1]["headers"]["User-Agent"]
    
    del os.environ["TCC_MCP_EMAIL"]

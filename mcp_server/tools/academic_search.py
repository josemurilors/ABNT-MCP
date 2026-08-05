import os
import requests
from typing import Optional

def get_user_agent() -> str:
    """Get User-Agent with configured email."""
    email = os.getenv("TCC_MCP_EMAIL", "usuario-tcc@academico.local")
    return f"TCC-MCP/1.0 (https://github.com/usuario/tcc-mcp; mailto:{email})"

def search_papers(query: str, limit: int = 10, source: str = "crossref") -> dict:
    """Search academic papers via Crossref or Semantic Scholar."""
    headers = {
        "User-Agent": get_user_agent(),
        "Accept": "application/json"
    }
    
    try:
        if source == "crossref":
            return _search_crossref(query, limit, headers)
        elif source == "semantic_scholar":
            return _search_semantic_scholar(query, limit, headers)
        else:
            return {"status": "error", "message": f"Unknown source: {source}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def _search_crossref(query: str, limit: int, headers: dict) -> dict:
    """Search via Crossref API."""
    url = "https://api.crossref.org/works"
    params = {
        "query": query,
        "rows": limit,
        "select": "DOI,title,author,issued,abstract"
    }
    
    response = requests.get(url, params=params, headers=headers, timeout=10)
    response.raise_for_status()
    
    data = response.json()
    papers = []
    
    for item in data.get("message", {}).get("items", []):
        paper = {
            "doi": item.get("DOI", ""),
            "title": item.get("title", [""])[0] if item.get("title") else "",
            "authors": _format_authors(item.get("author", [])),
            "year": _extract_year(item.get("issued", {})),
            "abstract": item.get("abstract", "")
        }
        papers.append(paper)
    
    return {"status": "success", "papers": papers}

def _search_semantic_scholar(query: str, limit: int, headers: dict) -> dict:
    """Search via Semantic Scholar API."""
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,authors,year,abstract,externalIds"
    }
    
    response = requests.get(url, params=params, headers=headers, timeout=10)
    response.raise_for_status()
    
    data = response.json()
    papers = []
    
    for item in data.get("data", []):
        paper = {
            "doi": item.get("externalIds", {}).get("DOI", ""),
            "title": item.get("title", ""),
            "authors": ", ".join([a.get("name", "") for a in item.get("authors", [])]),
            "year": item.get("year", 0),
            "abstract": item.get("abstract", "")
        }
        papers.append(paper)
    
    return {"status": "success", "papers": papers}

def _format_authors(authors: list) -> str:
    """Format author list to string."""
    names = []
    for author in authors:
        given = author.get("given", "")
        family = author.get("family", "")
        names.append(f"{given} {family}".strip())
    return ", ".join(names)

def _extract_year(issued: dict) -> int:
    """Extract year from issued date."""
    date_parts = issued.get("date-parts", [[]])
    if date_parts and date_parts[0]:
        return date_parts[0][0]
    return 0

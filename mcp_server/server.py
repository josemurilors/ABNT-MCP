from fastmcp import FastMCP
from mcp_server.tools.academic_search import search_papers
from mcp_server.tools.bibtex_fetcher import get_bibtex_by_doi, clean_bibtex
from mcp_server.tools.pdf_reader import read_pdf_paper
from mcp_server.tools.citation_validator import validate_citations
from mcp_server.tools.structure_checker import check_tcc_structure
from mcp_server.tools.compiler import compile_document

mcp = FastMCP("TCC-MCP")

@mcp.tool()
def tool_search_papers(query: str, limit: int = 10, source: str = "crossref") -> dict:
    """Search academic papers via Crossref or Semantic Scholar."""
    return search_papers(query, limit, source)

@mcp.tool()
def tool_get_bibtex_by_doi(doi: str, bib_path: str = None) -> dict:
    """Fetch BibTeX by DOI and optionally insert into .bib file."""
    return get_bibtex_by_doi(doi, bib_path)

@mcp.tool()
def tool_clean_bibtex(bib_path: str) -> dict:
    """Clean and standardize BibTeX file for ABNT."""
    return clean_bibtex(bib_path)

@mcp.tool()
def tool_read_pdf_paper(file_path: str, pages: list[int] = None) -> dict:
    """Extract text from PDF file."""
    return read_pdf_paper(file_path, pages)

@mcp.tool()
def tool_validate_citations(project_path: str) -> dict:
    """Validate citations in LaTeX project."""
    return validate_citations(project_path)

@mcp.tool()
def tool_check_tcc_structure(project_path: str) -> dict:
    """Check TCC structure according to NBR 14724."""
    return check_tcc_structure(project_path)

@mcp.tool()
def tool_compile_document(project_path: str, engine: str = "auto") -> dict:
    """Compile document with preflight check."""
    return compile_document(project_path, engine)

if __name__ == "__main__":
    mcp.run()

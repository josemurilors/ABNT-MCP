import pytest
from pathlib import Path
import tempfile
import shutil
from mcp_server.tools.citation_validator import validate_citations

def test_validate_citations_no_orphans():
    with tempfile.TemporaryDirectory() as tmpdir:
        main_tex = Path(tmpdir) / "main.tex"
        main_tex.write_text(r"\documentclass{article} \begin{document} \cite{doe2023} \end{document}", encoding='utf-8')
        
        bib_file = Path(tmpdir) / "referencias.bib"
        bib_file.write_text("@article{doe2023, author={Doe}, title={Test}, year={2023}}", encoding='utf-8')
        
        result = validate_citations(tmpdir)
        
        assert result["status"] == "success"
        assert len(result["orphan_citations"]) == 0
        assert len(result["uncited_references"]) == 0

def test_validate_citations_with_orphans():
    with tempfile.TemporaryDirectory() as tmpdir:
        main_tex = Path(tmpdir) / "main.tex"
        main_tex.write_text(r"\cite{doe2023} \cite{missing2024}", encoding='utf-8')
        
        bib_file = Path(tmpdir) / "referencias.bib"
        bib_file.write_text("@article{doe2023, author={Doe}, title={Test}, year={2023}}", encoding='utf-8')
        
        result = validate_citations(tmpdir)
        
        assert "missing2024" in result["orphan_citations"]

def test_validate_citations_recursive():
    with tempfile.TemporaryDirectory() as tmpdir:
        main_tex = Path(tmpdir) / "main.tex"
        main_tex.write_text(r"\input{capitulo1}", encoding='utf-8')
        
        cap1 = Path(tmpdir) / "capitulo1.tex"
        cap1.write_text(r"\cite{doe2023}", encoding='utf-8')
        
        bib_file = Path(tmpdir) / "referencias.bib"
        bib_file.write_text("@article{doe2023, author={Doe}, title={Test}, year={2023}}", encoding='utf-8')
        
        result = validate_citations(tmpdir)
        
        assert result["status"] == "success"
        assert len(result["orphan_citations"]) == 0

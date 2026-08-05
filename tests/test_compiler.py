import pytest
from pathlib import Path
import tempfile
from mcp_server.tools.compiler import compile_document

def test_compile_document_auto_detect_latex():
    with tempfile.TemporaryDirectory() as tmpdir:
        project = Path(tmpdir)
        main_tex = project / "main.tex"
        main_tex.write_text(r"\documentclass{article} \begin{document} Hello \end{document}", encoding='utf-8')
        
        result = compile_document(tmpdir, engine="auto")
        
        assert result["status"] in ["success", "error"]
        if result["status"] == "error":
            assert "not found" in result["message"].lower() or "not available" in result["message"].lower()

def test_compile_document_preflight_check():
    with tempfile.TemporaryDirectory() as tmpdir:
        project = Path(tmpdir)
        main_tex = project / "main.tex"
        main_tex.write_text(r"\documentclass{article} \begin{document} Test \end{document}", encoding='utf-8')
        
        result = compile_document(tmpdir, engine="nonexistent_compiler")
        
        assert result["status"] == "error"
        assert "not found" in result["message"].lower()

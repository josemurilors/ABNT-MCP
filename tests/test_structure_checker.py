import pytest
from pathlib import Path
import tempfile
from mcp_server.tools.structure_checker import check_tcc_structure

def test_check_structure_complete():
    with tempfile.TemporaryDirectory() as tmpdir:
        project = Path(tmpdir)
        
        (project / "capa.tex").write_text("\\chapter{Capa}", encoding='utf-8')
        (project / "folha_rosto.tex").write_text("\\chapter{Folha de Rosto}", encoding='utf-8')
        (project / "resumo.tex").write_text("\\chapter{Resumo}", encoding='utf-8')
        (project / "abstract.tex").write_text("\\chapter{Abstract}", encoding='utf-8')
        (project / "lista_ilustracoes.tex").write_text("\\listoffigures", encoding='utf-8')
        (project / "lista_tabelas.tex").write_text("\\listoftables", encoding='utf-8')
        (project / "lista_abreviaturas.tex").write_text("Lista de abreviaturas", encoding='utf-8')
        (project / "sumario.tex").write_text("\\tableofcontents", encoding='utf-8')
        (project / "introducao.tex").write_text("\\chapter{Introdução}", encoding='utf-8')
        (project / "desenvolvimento.tex").write_text("\\chapter{Fundamentação}", encoding='utf-8')
        (project / "conclusao.tex").write_text("\\chapter{Conclusão}", encoding='utf-8')
        (project / "referencias.tex").write_text("\\bibliography{ref}", encoding='utf-8')
        
        result = check_tcc_structure(tmpdir)
        
        assert result["status"] == "success"
        assert len(result["missing_elements"]) == 0

def test_check_structure_missing_elements():
    with tempfile.TemporaryDirectory() as tmpdir:
        project = Path(tmpdir)
        (project / "introducao.tex").write_text("\\chapter{Intro}", encoding='utf-8')
        
        result = check_tcc_structure(tmpdir)
        
        assert result["status"] == "success"
        assert len(result["missing_elements"]) > 0
        assert "resumo" in result["missing_elements"]

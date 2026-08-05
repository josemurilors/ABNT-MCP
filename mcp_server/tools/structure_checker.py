import re
from pathlib import Path
from ..utils import read_file_with_fallback

REQUIRED_ELEMENTS = {
    "pre-textual": [
        "capa", "folha_de_rosto", "resumo", "abstract",
        "lista_ilustracoes", "lista_tabelas", "lista_abreviaturas", "sumario"
    ],
    "textual": [
        "introducao", "desenvolvimento", "conclusao"
    ],
    "post-textual": [
        "referencias"
    ],
    "optional": [
        "apendices", "anexos"
    ]
}

ELEMENT_PATTERNS = {
    "capa": [r"\\begin\{titlepage\}", r"\\maketitle", r"capa", r"cover"],
    "folha_de_rosto": [r"folha\s+de\s+rosto", r"title\s+page"],
    "resumo": [r"\\begin\{resumo\}", r"\\chapter\*?\{resumo\}", r"resumo"],
    "abstract": [r"\\begin\{abstract\}", r"\\chapter\*?\{abstract\}", r"abstract"],
    "lista_ilustracoes": [r"\\listoffigures", r"lista\s+de\s+ilustrações", r"lista\s+de\s+figuras"],
    "lista_tabelas": [r"\\listoftables", r"lista\s+de\s+tabelas"],
    "lista_abreviaturas": [r"lista\s+de\s+abreviaturas", r"lista\s+de\s+siglas"],
    "sumario": [r"\\tableofcontents", r"sumário", r"sumario"],
    "introducao": [r"\\chapter\*?\{introdução\}", r"\\chapter\*?\{introducao\}", r"introdução"],
    "desenvolvimento": [r"\\chapter", r"fundamentação", r"metodologia", r"resultados"],
    "conclusao": [r"\\chapter\*?\{conclusão\}", r"\\chapter\*?\{considerações\s+finais\}", r"conclusão"],
    "referencias": [r"\\bibliography", r"\\begin\{thebibliography\}", r"referências", r"referencias"],
    "apendices": [r"\\begin\{apendice\}", r"\\chapter\*?\{apêndice\}", r"apêndices"],
    "anexos": [r"\\begin\{anexo\}", r"\\chapter\*?\{anexo\}", r"anexos"]
}

def check_tcc_structure(project_path: str) -> dict:
    """Check TCC structure according to NBR 14724."""
    try:
        project = Path(project_path)
        
        all_content = collect_all_content(project)
        
        found_elements = set()
        for element, patterns in ELEMENT_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, all_content, re.IGNORECASE):
                    found_elements.add(element)
                    break
        
        missing_elements = []
        for category, elements in REQUIRED_ELEMENTS.items():
            if category == "optional":
                continue
            for element in elements:
                if element not in found_elements:
                    missing_elements.append(element)
        
        return {
            "status": "success",
            "found_elements": sorted(list(found_elements)),
            "missing_elements": missing_elements,
            "has_optional_apendices": "apendices" in found_elements,
            "has_optional_anexos": "anexos" in found_elements
        }
    
    except Exception as e:
        return {"status": "error", "message": str(e)}

def collect_all_content(project: Path) -> str:
    """Collect content from all .tex files in project."""
    all_content = []
    
    for tex_file in project.glob("**/*.tex"):
        try:
            content = read_file_with_fallback(str(tex_file))
            all_content.append(content)
        except:
            continue
    
    return "\n".join(all_content)

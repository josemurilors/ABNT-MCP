from __future__ import annotations

import re
from pathlib import Path
from typing import Optional
from ..utils import read_file_with_fallback

def validate_citations(project_path: str) -> dict:
    """Validate citations in LaTeX project (recursive)."""
    try:
        project = Path(project_path)
        
        main_tex = find_main_tex(project)
        if not main_tex:
            return {"status": "error", "message": "No .tex file found"}
        
        tex_files = resolve_tex_files(main_tex)
        
        all_citations = set()
        for tex_file in tex_files:
            content = read_file_with_fallback(str(tex_file))
            citations = extract_citations(content)
            all_citations.update(citations)
        
        bib_file = find_bib_file(project)
        if not bib_file:
            return {"status": "error", "message": "No .bib file found"}
        
        bib_keys = parse_bib_keys(bib_file)
        
        orphan_citations = list(all_citations - bib_keys)
        uncited_references = list(bib_keys - all_citations)
        
        return {
            "status": "success",
            "orphan_citations": orphan_citations,
            "uncited_references": uncited_references,
            "total_citations": len(all_citations),
            "total_references": len(bib_keys)
        }
    
    except Exception as e:
        return {"status": "error", "message": str(e)}

def find_main_tex(project: Path) -> Optional[Path]:
    """Find main .tex file in project."""
    for name in ["main.tex", "tcc.tex", "dissertacao.tex", "tese.tex"]:
        main = project / name
        if main.exists():
            return main
    
    tex_files = list(project.glob("*.tex"))
    return tex_files[0] if tex_files else None

def find_bib_file(project: Path) -> Optional[Path]:
    """Find .bib file in project."""
    for name in ["referencias.bib", "references.bib", "bibliografia.bib"]:
        bib = project / name
        if bib.exists():
            return bib
    
    bib_files = list(project.glob("*.bib"))
    return bib_files[0] if bib_files else None

def resolve_tex_files(main_tex: Path) -> list[Path]:
    """Recursively resolve all .tex files via \\input{} and \\include{}."""
    files = [main_tex]
    content = read_file_with_fallback(str(main_tex))
    
    for match in re.finditer(r'\\(?:input|include)\{([^}]+)\}', content):
        included = match.group(1)
        if not included.endswith('.tex'):
            included += '.tex'
        
        full_path = main_tex.parent / included
        if full_path.exists():
            files.extend(resolve_tex_files(full_path))
    
    return files

def extract_citations(content: str) -> set:
    """Extract all citation keys from LaTeX content."""
    citations = set()
    
    patterns = [
        r'\\cite\{([^}]+)\}',
        r'\\citeauthor\{([^}]+)\}',
        r'\\citeyear\{([^}]+)\}',
        r'\\citet\{([^}]+)\}',
        r'\\citep\{([^}]+)\}'
    ]
    
    for pattern in patterns:
        for match in re.finditer(pattern, content):
            keys = match.group(1).split(',')
            citations.update(key.strip() for key in keys)
    
    return citations

def parse_bib_keys(bib_path: Path) -> set:
    """Parse all citation keys from .bib file."""
    content = read_file_with_fallback(str(bib_path))
    keys = set()
    
    for match in re.finditer(r'@\w+\{([^,]+),', content):
        keys.add(match.group(1).strip())
    
    return keys

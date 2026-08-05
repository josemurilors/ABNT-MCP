import shutil
import subprocess
from pathlib import Path
from ..utils import read_file_with_fallback

def compile_document(project_path: str, engine: str = "auto") -> dict:
    """Compile document with preflight check."""
    try:
        project = Path(project_path)
        
        if engine == "auto":
            engine = detect_engine(project)
            if not engine:
                return {
                    "status": "error",
                    "message": "Compiler not found. Install TeX Live, Pandoc, or Typst."
                }
        
        availability = check_compiler_availability(engine)
        if not availability["available"]:
            return {
                "status": "error",
                "message": availability["message"]
            }
        
        if engine in ["latexmk", "pdflatex"]:
            return compile_latex(project, engine)
        elif engine == "pandoc":
            return compile_pandoc(project)
        elif engine == "typst":
            return compile_typst(project)
        else:
            return {"status": "error", "message": f"Compiler not found for engine: {engine}"}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}

def detect_engine(project: Path) -> str:
    """Detect compilation engine from project files."""
    if (project / "main.tex").exists() or any(project.glob("*.tex")):
        if shutil.which("latexmk"):
            return "latexmk"
        elif shutil.which("pdflatex"):
            return "pdflatex"
    
    if (project / "main.md").exists() and shutil.which("pandoc"):
        return "pandoc"
    
    if (project / "main.typ").exists() and shutil.which("typst"):
        return "typst"
    
    return None

def check_compiler_availability(engine: str) -> dict:
    """Check if compiler binary is available."""
    binary_map = {
        "latexmk": "latexmk",
        "pdflatex": "pdflatex",
        "pandoc": "pandoc",
        "typst": "typst"
    }
    
    binary = binary_map.get(engine)
    if not binary:
        return {"available": False, "message": f"Compiler not found for engine: {engine}"}
    
    if not shutil.which(binary):
        return {
            "available": False,
            "message": f"Compiler '{binary}' not found in PATH. Please install it."
        }
    
    return {"available": True, "engine": binary}

def compile_latex(project: Path, engine: str) -> dict:
    """Compile LaTeX document."""
    main_tex = find_main_tex(project)
    if not main_tex:
        return {"status": "error", "message": "No .tex file found"}
    
    try:
        result = subprocess.run(
            [engine, "-interaction=nonstopmode", str(main_tex)],
            cwd=str(project),
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            pdf_path = main_tex.with_suffix('.pdf')
            return {
                "status": "success",
                "pdf_path": str(pdf_path),
                "message": "Compilation successful"
            }
        else:
            errors = extract_latex_errors(result.stdout)
            return {
                "status": "error",
                "message": "Compilation failed",
                "errors": errors
            }
    
    except subprocess.TimeoutExpired:
        return {"status": "error", "message": "Compilation timeout (60s)"}

def compile_pandoc(project: Path) -> dict:
    """Compile Markdown with Pandoc."""
    main_md = project / "main.md"
    if not main_md.exists():
        return {"status": "error", "message": "main.md not found"}
    
    output_pdf = project / "output.pdf"
    
    try:
        result = subprocess.run(
            ["pandoc", str(main_md), "-o", str(output_pdf)],
            cwd=str(project),
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            return {
                "status": "success",
                "pdf_path": str(output_pdf),
                "message": "Compilation successful"
            }
        else:
            return {
                "status": "error",
                "message": "Pandoc compilation failed",
                "errors": result.stderr
            }
    
    except subprocess.TimeoutExpired:
        return {"status": "error", "message": "Compilation timeout (60s)"}

def compile_typst(project: Path) -> dict:
    """Compile Typst document."""
    main_typ = project / "main.typ"
    if not main_typ.exists():
        return {"status": "error", "message": "main.typ not found"}
    
    output_pdf = project / "output.pdf"
    
    try:
        result = subprocess.run(
            ["typst", "compile", str(main_typ), str(output_pdf)],
            cwd=str(project),
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            return {
                "status": "success",
                "pdf_path": str(output_pdf),
                "message": "Compilation successful"
            }
        else:
            return {
                "status": "error",
                "message": "Typst compilation failed",
                "errors": result.stderr
            }
    
    except subprocess.TimeoutExpired:
        return {"status": "error", "message": "Compilation timeout (60s)"}

def find_main_tex(project: Path) -> Path:
    """Find main .tex file."""
    for name in ["main.tex", "tcc.tex", "dissertacao.tex"]:
        main = project / name
        if main.exists():
            return main
    
    tex_files = list(project.glob("*.tex"))
    return tex_files[0] if tex_files else None

def extract_latex_errors(log: str) -> list:
    """Extract error lines from LaTeX log."""
    errors = []
    for line in log.split('\n'):
        if line.startswith('!') or 'Error' in line:
            errors.append(line)
    return errors[:10]

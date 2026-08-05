import os
import re
import requests
from pathlib import Path
from typing import Optional
import bibtexparser
from ..utils import read_file_with_fallback, write_file_with_encoding

def get_user_agent() -> str:
    email = os.getenv("TCC_MCP_EMAIL", "usuario-tcc@academico.local")
    return f"TCC-MCP/1.0 (https://github.com/usuario/tcc-mcp; mailto:{email})"

def get_bibtex_by_doi(doi: str, bib_path: Optional[str] = None) -> dict:
    """Fetch BibTeX by DOI and optionally insert into .bib file."""
    headers = {
        "User-Agent": get_user_agent(),
        "Accept": "application/x-bibtex"
    }
    
    try:
        url = f"https://doi.org/{doi}"
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        bibtex = response.text
        key = extract_bibtex_key(bibtex)
        
        if bib_path:
            existing_keys = parse_bib_keys(bib_path)
            if key in existing_keys:
                return {"status": "duplicate", "message": f"Key '{key}' already exists", "key": key}
            
            append_to_bib(bib_path, bibtex)
            return {"status": "added", "key": key, "bibtex": bibtex}
        
        return {"status": "fetched", "key": key, "bibtex": bibtex}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}

def extract_bibtex_key(bibtex: str) -> str:
    """Extract the citation key from BibTeX entry."""
    match = re.search(r'@\w+\{([^,]+),', bibtex)
    return match.group(1).strip() if match else ""

def parse_bib_keys(bib_path: str) -> set:
    """Parse all citation keys from .bib file."""
    content = read_file_with_fallback(bib_path)
    keys = set()
    
    for match in re.finditer(r'@\w+\{([^,]+),', content):
        keys.add(match.group(1).strip())
    
    return keys

def append_to_bib(bib_path: str, bibtex: str):
    """Append BibTeX entry to file."""
    content = read_file_with_fallback(bib_path)
    if content and not content.endswith('\n'):
        content += '\n'
    content += bibtex + '\n'
    write_file_with_encoding(bib_path, content)

def clean_bibtex(bib_path: str) -> dict:
    """Clean and standardize BibTeX file for ABNT."""
    try:
        content = read_file_with_fallback(bib_path)
        bib_database = bibtexparser.loads(content)
        
        cleaned_entries = []
        missing_fields_report = []
        
        for entry in bib_database.entries:
            entry_id = entry.get('ID', '')
            
            entry['ID'] = entry_id.lower().replace(' ', '_')
            
            if 'author' in entry:
                entry['author'] = clean_author_names(entry['author'])
            
            if 'title' in entry:
                entry['title'] = escape_tex_accents(entry['title'])
            
            missing = check_abnt_required_fields(entry)
            if missing:
                missing_fields_report.append({
                    "key": entry['ID'],
                    "missing_fields": missing
                })
            
            cleaned_entries.append(entry)
        
        cleaned_db = bibtexparser.bibdatabase.BibDatabase()
        cleaned_db.entries = cleaned_entries
        cleaned_bibtex = bibtexparser.dumps(cleaned_db)
        
        write_file_with_encoding(bib_path, cleaned_bibtex)
        
        return {
            "status": "cleaned",
            "cleaned_bibtex": cleaned_bibtex,
            "missing_fields_report": missing_fields_report
        }
    
    except Exception as e:
        return {"status": "error", "message": str(e)}

def clean_author_names(author_str: str) -> str:
    """Convert UPPERCASE names to Title Case."""
    if author_str.isupper():
        return author_str.title()
    return author_str

def escape_tex_accents(text: str) -> str:
    """Escape accents for TeX."""
    replacements = {
        'ã': r'{\~a}', 'õ': r'{\~o}',
        'á': r'{\'a}', 'é': r'{\'e}', 'í': r'{\'i}', 'ó': r'{\'o}', 'ú': r'{\'u}',
        'â': r'{\^a}', 'ê': r'{\^e}', 'ô': r'{\^o}',
        'ç': r'{\c c}'
    }
    for char, tex in replacements.items():
        text = text.replace(char, tex)
    return text

def check_abnt_required_fields(entry: dict) -> list:
    """Check for ABNT required fields."""
    entry_type = entry.get('ENTRYTYPE', '').lower()
    
    required = {
        'article': ['author', 'title', 'journal', 'year', 'volume', 'number', 'pages'],
        'book': ['author', 'title', 'year', 'publisher', 'address'],
        'inproceedings': ['author', 'title', 'booktitle', 'year'],
        'phdthesis': ['author', 'title', 'year', 'school'],
        'mastersthesis': ['author', 'title', 'year', 'school']
    }
    
    required_fields = required.get(entry_type, ['author', 'title', 'year'])
    missing = [f for f in required_fields if f not in entry or not entry[f]]
    
    return missing

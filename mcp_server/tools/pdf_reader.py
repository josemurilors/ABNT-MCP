from pathlib import Path
from typing import Optional
from pypdf import PdfReader

def read_pdf_paper(file_path: str, pages: Optional[list[int]] = None) -> dict:
    """Extract text from PDF file."""
    path = Path(file_path)
    
    if not path.exists():
        return {"status": "error", "message": f"File not found: {file_path}"}
    
    if not path.suffix.lower() == '.pdf':
        return {"status": "error", "message": "File is not a PDF"}
    
    try:
        reader = PdfReader(file_path)
        total_pages = len(reader.pages)
        
        if pages is None:
            pages_to_extract = list(range(total_pages))
        else:
            pages_to_extract = [p for p in pages if 0 <= p < total_pages]
        
        extracted_text = []
        for page_num in pages_to_extract:
            page = reader.pages[page_num]
            text = page.extract_text()
            extracted_text.append({
                "page": page_num + 1,
                "text": text
            })
        
        return {
            "status": "success",
            "total_pages": total_pages,
            "extracted_pages": pages_to_extract,
            "content": extracted_text
        }
    
    except Exception as e:
        return {"status": "error", "message": str(e)}

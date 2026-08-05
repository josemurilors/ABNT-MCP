# TCC Master Skill

## Purpose
Assist Brazilian students in writing academic papers (TCC) following ABNT standards.

## Commands

### #pesquisar <tema>
Search academic papers and synthesize state of the art.

**Action:** Call `search_papers` MCP tool with query.
**Output:** List of relevant papers with title, authors, year, DOI, abstract.

### #ler <arquivo.pdf>
Extract text from local PDF file.

**Action:** Call `read_pdf_paper` MCP tool.
**Output:** Extracted text from PDF.

### #citar <doi>
Fetch BibTeX by DOI and insert into referencias.bib (with anti-duplication).

**Action:** Call `get_bibtex_by_doi` MCP tool with bib_path="referencias.bib".
**Output:** Confirmation of insertion or duplicate warning.

### #escrever <capítulo>
Write chapter with impersonal tone (3rd person, passive voice, scientific clarity).

**Rules:**
- Use 3rd person singular or plural
- Prefer passive voice: "Foi analisado..." instead of "Analisamos..."
- Maintain scientific clarity and objectivity
- Include citations using \cite{} for LaTeX or [@key] for Markdown

### #revisar
Review text for tone, cohesion, and direct citations.

**Rules:**
- Check for impersonal tone (no 1st person)
- Verify direct citations follow ABNT:
  - Short (up to 3 lines): inline with quotation marks
  - Long (4+ lines): indented block, font size 10, single spacing
- Ensure cohesion between paragraphs

### #limpar-bib
Standardize BibTeX file for ABNT.

**Action:** Call `clean_bibtex` MCP tool.
**Output:** Cleaned BibTeX + report of missing ABNT fields.

### #validar
Verify citations vs references (recursive for LaTeX projects).

**Action:** Call `validate_citations` MCP tool.
**Output:** Report of orphan citations and uncited references.

### #estrutura
Validate pre and post-textual elements (NBR 14724).

**Action:** Call `check_tcc_structure` MCP tool.
**Output:** Report of missing or misplaced elements.

### #compilar
Generate PDF with preflight check.

**Action:** Call `compile_document` MCP tool.
**Output:** Compilation status + PDF path or errors.

## ABNT Standards

### NBR 10520:2023 (Citations)
- **Direct citation (short):** "Text" (AUTHOR, Year, p. X)
- **Direct citation (long):** Indented block, size 10, single spacing
- **Indirect citation:** AUTHOR (Year) or (AUTHOR, Year)

### NBR 6023 (References)
- Author surnames in UPPERCASE
- Title in bold
- Required fields vary by type (article, book, etc.)

### NBR 14724 (Structure)
**Pre-textual:** Capa, Folha de Rosto, Resumo, Abstract, Lista de Ilustrações, Lista de Tabelas, Lista de Abreviaturas, Sumário
**Textual:** Introdução, Desenvolvimento, Conclusão
**Post-textual:** Referências, Apêndices (optional), Anexos (optional)

## Format Detection
Automatically detect format (.tex, .md, .typ) and adapt behavior.

# Spec Document: TCC-MCP

## 1. Visão Geral

**Nome:** TCC-MCP  
**Propósito:** Ferramenta de escrita e revisão acadêmica para TCCs brasileiros seguindo ABNT  
**Público-alvo:** Estudantes de graduação no Brasil  
**Formato suportado:** LaTeX (.tex), Markdown (.md), Typst (.typ)  
**Distribuição:** Repositório público no GitHub com instalação via `uv run`

---

## 2. Arquitetura

```
tcc-mcp/
├── .opencode/
│   └── skills/
│       └── tcc-master.md          # Skill OpenCode (comandos # + ABNT)
├── mcp_server/                    # Pacote Python (underscore)
│   ├── __init__.py                # Torna o diretório um pacote
│   ├── server.py                  # Entry point FastMCP
│   ├── pyproject.toml             # Dependências
│   └── tools/
│       ├── __init__.py            # Permite import de submódulos
│       ├── academic_search.py     # Crossref + Semantic Scholar
│       ├── bibtex_fetcher.py      # Busca, validação, limpeza e inserção de BibTeX
│       ├── citation_validator.py  # Checagem \cite{} vs .bib (recursivo)
│       ├── pdf_reader.py          # Extração de texto de PDFs locais
│       ├── structure_checker.py   # Validação NBR 14724 (recursivo)
│       └── compiler.py            # Compilação (latexmk / pandoc / typst)
├── opencode.json                  # Configuração MCP (com env vars)
├── README.md                      # Instruções cross-platform
├── examples/                      # Projetos de teste
│   ├── latex-example/
│   ├── markdown-example/
│   └── typst-example/
└── .github/
    └── workflows/
        └── test.yml               # CI no GitHub Actions
```

---

## 3. Ferramentas MCP (7 ferramentas)

### 3.1 `search_papers`

**Módulo:** `academic_search.py`  
**Entrada:** `query: str, limit: int = 10, source: str = "crossref"`  
**Saída:** Lista de artigos (título, autores, ano, DOI, abstract)

**Comportamento:**
- Integração com APIs do Crossref e Semantic Scholar
- Injeção automática de User-Agent com email configurado
- Fallback graceful se uma API falhar

**User-Agent:**
```python
USER_EMAIL = os.getenv("TCC_MCP_EMAIL", "usuario-tcc@academico.local")
HEADERS = {
    "User-Agent": f"TCC-MCP/1.0 (https://github.com/usuario/tcc-mcp; mailto:{USER_EMAIL})",
    "Accept": "application/json"
}
```

---

### 3.2 `get_bibtex_by_doi`

**Módulo:** `bibtex_fetcher.py`  
**Entrada:** `doi: str, bib_path: str = None`  
**Saída:** Entrada BibTeX validada + status de inserção (se `bib_path` fornecido)

**Comportamento:**
- Busca BibTeX oficial via DOI (Crossref, DataCite)
- Valida campos obrigatórios
- **Anti-duplicação:** Se `bib_path` fornecido, verifica se a chave já existe no .bib antes de inserir
- Inserção atômica: escreve apenas se a chave não existir

**Lógica de anti-duplicação:**
```python
def add_bibtex_entry(doi: str, bib_path: str = None):
    bibtex = fetch_bibtex_by_doi(doi)
    key = extract_key(bibtex)
    
    if bib_path:
        existing_keys = parse_bib_keys(bib_path)
        if key in existing_keys:
            return {"status": "duplicate", "message": f"Chave '{key}' já existe"}
        
        append_to_bib(bib_path, bibtex)
        return {"status": "added", "key": key}
    
    return {"status": "fetched", "bibtex": bibtex}
```

---

### 3.3 `clean_bibtex`

**Módulo:** `bibtex_fetcher.py`  
**Entrada:** `bib_path: str`  
**Saída:** BibTeX limpo + relatório de campos ABNT ausentes

**Comportamento:**
- Padroniza chaves (lowercase, remove caracteres especiais)
- Corrige nomes em CAIXA ALTA para Title Case
- Escapa acentos TeX (`ã` → `{\~a}`)
- Verifica campos obrigatórios ABNT: `author`, `title`, `year`, `journal/booktitle`, `address` (para livros)
- Retorna relatório de campos ausentes

**Campos ABNT obrigatórios:**
- Artigo: author, title, journal, year, volume, number, pages
- Livro: author, title, year, publisher, address

---

### 3.4 `read_pdf_paper`

**Módulo:** `pdf_reader.py`  
**Entrada:** `file_path: str, pages: list[int] = None`  
**Saída:** Texto extraído do PDF

**Comportamento:**
- Usa `pypdf` para extração
- Se `pages` não fornecido, extrai todas as páginas
- **Encoding resilience:** Tenta UTF-8 primeiro, fallback para latin-1/cp1252

**Tratamento de encoding:**
```python
def read_file_with_fallback(file_path: str) -> str:
    for encoding in ["utf-8", "latin-1", "cp1252"]:
        try:
            with open(file_path, "r", encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Não foi possível decodificar {file_path}")
```

---

### 3.5 `validate_citations`

**Módulo:** `citation_validator.py`  
**Entrada:** `project_path: str`  
**Saída:** Relatório: citações órfãs, referências não citadas

**Comportamento:**
- **Varredura recursiva:** Percorre todos os `.tex` listados em `\input{}` e `\include{}` do arquivo principal
- Extrai todas as citações `\cite{chave}` e `\citeauthor{chave}`
- Compara com chaves no `.bib`
- Retorna:
  - Citações no texto que não existem no .bib
  - Referências no .bib que nunca foram citadas

**Resolução de arquivos modulares:**
```python
def resolve_tex_files(main_tex: str) -> list[str]:
    files = [main_tex]
    content = read_file_with_fallback(main_tex)
    
    # Encontrar \input{} e \include{}
    for match in re.finditer(r'\\(?:input|include)\{([^}]+)\}', content):
        included = match.group(1)
        if not included.endswith('.tex'):
            included += '.tex'
        full_path = Path(main_tex).parent / included
        if full_path.exists():
            files.extend(resolve_tex_files(str(full_path)))
    
    return files
```

---

### 3.6 `check_tcc_structure`

**Módulo:** `structure_checker.py`  
**Entrada:** `project_path: str`  
**Saída:** Relatório de elementos pré/pós-textuais (NBR 14724)

**Comportamento:**
- **Varredura recursiva:** Mesma lógica do `validate_citations`
- Verifica presença de elementos obrigatórios NBR 14724:
  - **Pré-textuais:** Capa, Folha de Rosto, Resumo, Abstract, Lista de Ilustrações, Lista de Tabelas, Lista de Abreviaturas, Sumário
  - **Pós-textuais:** Referências, Apêndices (opcional), Anexos (opcional)
- Verifica ordem dos elementos
- Retorna lista de elementos faltantes ou fora de ordem

**Elementos NBR 14724:**
```python
REQUIRED_ELEMENTS = {
    "pre-textual": [
        "capa", "folha_de_rosto", "resumo", "abstract",
        "lista_ilustracoes", "lista_tabelas", "lista_abreviaturas", "sumario"
    ],
    "post-textual": [
        "referencias", "apendices", "anexos"
    ]
}
```

---

### 3.7 `compile_document`

**Módulo:** `compiler.py`  
**Entrada:** `project_path: str, engine: str = "auto"`  
**Saída:** Status da compilação + erros relevantes

**Comportamento:**
- **Preflight check:** Verifica binários disponíveis (latexmk, pdflatex, pandoc, typst)
- **Detecção automática:** Se `engine="auto"`, detecta formato pelo arquivo principal:
  - `main.tex` → latexmk/pdflatex
  - `main.md` → pandoc
  - `main.typ` → typst
- Captura log de erros e retorna apenas linhas relevantes
- **Encoding resilience:** Lê logs com fallback de encoding

**Preflight check:**
```python
def check_compiler_availability(engine: str) -> dict:
    if engine == "auto":
        for binary in ["latexmk", "pdflatex", "pandoc", "typst"]:
            if shutil.which(binary):
                return {"available": True, "engine": binary}
        return {
            "available": False,
            "message": "Nenhum compilador encontrado. Instale TeX Live, Pandoc ou Typst."
        }
    
    binary_map = {"latexmk": "latexmk", "pdflatex": "pdflatex", "pandoc": "pandoc", "typst": "typst"}
    binary = binary_map.get(engine)
    
    if not shutil.which(binary):
        return {
            "available": False,
            "message": f"Compilador '{binary}' não encontrado no PATH."
        }
    
    return {"available": True, "engine": binary}
```

---

## 4. Skill OpenCode (tcc-master.md)

### 4.1 Comandos Mapeados

| Comando | Ação | Ferramenta MCP |
|---------|------|----------------|
| `#pesquisar <tema>` | Busca artigos e sintetiza estado da arte | `search_papers` |
| `#ler <arquivo.pdf>` | Extrai texto de PDF local | `read_pdf_paper` |
| `#citar <doi>` | Busca BibTeX por DOI e insere no .bib (anti-duplicação) | `get_bibtex_by_doi` |
| `#escrever <capítulo>` | Redige capítulo com tom impessoal (3ª pessoa) | Nenhuma (LLM) |
| `#revisar` | Corrige tom, coesão, citações diretas | Nenhuma (LLM) |
| `#limpar-bib` | Padroniza BibTeX para ABNT | `clean_bibtex` |
| `#validar` | Verifica citações vs referências (recursivo) | `validate_citations` |
| `#estrutura` | Valida elementos NBR 14724 (recursivo) | `check_tcc_structure` |
| `#compilar` | Gera PDF com preflight check | `compile_document` |

### 4.2 Regras Embutidas

- **NBR 10520:2023:** Citações ABNT (diretas/indiretas, curtas/longas)
- **NBR 6023:** Referências
- **NBR 14724:** Estrutura de trabalho acadêmico
- **Tom impessoal:** 3ª pessoa, voz passiva, clareza científica
- **Detecção automática:** Identifica formato (.tex, .md, .typ) e adapta comportamento

---

## 5. Configuração (opencode.json)

```json
{
  "mcpServers": {
    "tcc-mcp": {
      "command": "uv",
      "args": [
        "run",
        "--with", "fastmcp",
        "--with", "bibtexparser",
        "--with", "requests",
        "--with", "pypdf",
        "python", "-m", "mcp_server.server"
      ],
      "env": {
        "TCC_MCP_EMAIL": "seu.email@academico.com"
      }
    }
  }
}
```

---

## 6. Tratamento de Encoding (Transversal)

**Todos os leitores de arquivo** usam fallback de encoding:

```python
def read_file_with_fallback(file_path: str) -> str:
    for encoding in ["utf-8", "latin-1", "cp1252"]:
        try:
            with open(file_path, "r", encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Não foi possível decodificar {file_path}")
```

**Aplicado em:**
- `pdf_reader.py` (metadados do PDF)
- `citation_validator.py` (arquivos .tex)
- `bibtex_fetcher.py` (arquivo .bib)
- `structure_checker.py` (arquivos .tex)
- `compiler.py` (logs de compilação)

---

## 7. Distribuição

- **Repositório público:** GitHub
- **Instalação:** `git clone` + configurar `TCC_MCP_EMAIL` no `opencode.json`
- **Dependências:** `uv run` gerencia automaticamente (cross-platform: Windows, Linux, macOS)
- **CI:** GitHub Actions testa em Ubuntu, Windows, macOS

---

## 8. Exemplos de Uso

### 8.1 LaTeX

```
meu-tcc/
├── main.tex
├── referencias.bib
├── capitulos/
│   ├── 01_introducao.tex
│   ├── 02_fundamentacao.tex
│   └── 03_metodologia.tex
└── opencode.json
```

### 8.2 Markdown

```
meu-tcc/
├── main.md
├── referencias.bib
├── capitulos/
│   ├── 01_introducao.md
│   └── 02_fundamentacao.md
└── opencode.json
```

### 8.3 Typst

```
meu-tcc/
├── main.typ
├── referencias.bib
├── capitulos/
│   ├── 01_introducao.typ
│   └── 02_fundamentacao.typ
└── opencode.json
```

---

## 9. Decisões de Design

### 9.1 Por que Python + FastMCP?

- Ecossistema acadêmico maduro (bibtexparser, pylatexenc, habanero)
- Mais fácil para estudantes contribuírem
- FastMCP é production-ready e bem documentado

### 9.2 Por que uv run?

- Cross-platform (Windows, Linux, macOS)
- Cria ambiente virtual automaticamente
- Instala dependências na primeira execução
- Não precisa de scripts bash

### 9.3 Por que variável de ambiente para email?

- Evita rate limit compartilhado em código aberto
- Não quebra comunicação JSON-RPC do MCP (diferente de prompt interativo)
- Permite reutilização do projeto

### 9.4 Por que varredura recursiva?

- TCCs em LaTeX raramente têm tudo em um único arquivo
- Estrutura modular com `\input{}` e `\include{}` é padrão
- Validação completa exige percorrer todos os arquivos

### 9.5 Por que fallback de encoding?

- Templates acadêmicos legados no Brasil usam latin-1/ISO-8859-1
- UTF-8 é padrão moderno, mas compatibilidade é essencial
- Evita quebras em projetos existentes

---

## 10. Próximos Passos

1. Criar estrutura de diretórios do projeto
2. Implementar server.py com FastMCP
3. Implementar as 7 ferramentas MCP
4. Criar skill tcc-master.md
5. Configurar opencode.json
6. Criar exemplos de teste (LaTeX, Markdown, Typst)
7. Configurar CI no GitHub Actions
8. Escrever README.md com instruções de instalação

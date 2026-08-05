# Changelog

Todas as alteracoes notaveis neste projeto serao documentadas neste arquivo.

O formato e baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/spec/v2.0.0.html).

## [Nao Lancado]

### Adicionado

- Estrutura inicial do projeto
- Suporte a README bilingue (EN/PT-BR)
- Pipeline CI/CD com GitHub Actions
- Validacao de Conventional Commits
- Linting de Markdown e verificacao de links
- Documentacao de regras de protecao de branch
- Codigo de Conduta do Pacto de Contribuidores
- Politica de seguranca e processo de reporte de vulnerabilidades
- Integracao com scan de secrets (Gitleaks)
- Defesa em 4 camadas para Vibe Coding
- Scripts de validacao de .gitignore
- Suporte a modos de idioma (pt-br-first, en-first)

### Alterado

- N/A

### Descontinuado

- N/A

### Removido

- N/A

### Corrigido

- N/A

### Seguranca

- N/A

---

## [0.1.0] - Lancamento Inicial

### Adicionado

- Servidor MCP para assistencia academica
- Pesquisa de artigos academicos
- Leitura de PDFs
- Gerenciamento de citacoes BibTeX
- Escrita assistida com tom impessoal
- Revisao de tom e citacoes
- Validacao ABNT (NBR 14724)
- Compilacao para PDF (LaTeX, Markdown, Typst)

---

## Esquema de Versionamento

Este projeto usa [Semantic Versioning](https://semver.org/):

- Versao **MAJOR**: Mudancas incompativeis ou breaking changes
- Versao **MINOR**: Adicoes de funcionalidades compativeis
- Versao **PATCH**: Correcoes de bugs compativeis

## Processo de Lancamento

Os lancamentos sao feitos manualmente atraves de tags Git:

1. Atualize o CHANGELOG.md
2. Commite as alteracoes
3. Crie uma tag: `git tag v0.2.0`
4. Push a tag: `git push origin v0.2.0`
5. Crie um GitHub Release com notas

---

**Ultima Atualizacao**: 2026-01-XX (Entrada manual para setup inicial)

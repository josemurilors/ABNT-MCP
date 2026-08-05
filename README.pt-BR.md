# TCC-MCP

[![en](https://img.shields.io/badge/lang-en-red.svg)](README.md)
[![pt-br](https://img.shields.io/badge/lang-pt--br-green.svg)](README.pt-BR.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)
[![Secret Scanning](https://img.shields.io/badge/Secret%20Scanning-Gitleaks-brightgreen)](SECURITY.md)

> Ferramenta de escrita e revisao academica para TCCs brasileiros seguindo ABNT.

## Sobre

Servidor MCP (Model Context Protocol) que fornece ferramentas de assistencia academica para Trabalhos de Conclusao de Curso (TCC) no Brasil. Suporta pesquisa de artigos, leitura de PDFs, gerenciamento de citacoes BibTeX, escrita de capitulos com tom impessoal, revisao e compilacao para PDF.

## Funcionalidades

- **Pesquisa Academica** - Busca artigos em bases academicas
- **Leitura de PDFs** - Extrai texto de documentos PDF
- **Gerenciamento de Citacoes** - Adiciona referencias ao arquivo .bib
- **Escrita Assistida** - Redige capitulos com tom impessoal academico
- **Revisao** - Verifica tom e citacoes
- **Validacao ABNT** - Padroniza BibTeX e verifica elementos NBR 14724
- **Compilacao** - Gera PDF a partir de LaTeX, Markdown ou Typst

## Instalacao

### 1. Clone o repositorio

```bash
git clone https://github.com/josemurilors/tcc-mcp.git
cd tcc-mcp
```

### 2. Configure o email no opencode.json

```json
{
  "mcpServers": {
    "tcc-mcp": {
      "env": {
        "TCC_MCP_EMAIL": "seu.email@academico.com"
      }
    }
  }
}
```

### 3. (Opcional) Instale compiladores

- **LaTeX:** TeX Live (Linux), MiKTeX (Windows), MacTeX (macOS)
- **Pandoc:** https://pandoc.org/installing.html
- **Typst:** https://typst.app/

## Uso

### Comandos da Skill

- `#pesquisar <tema>` - Busca artigos academicos
- `#ler <arquivo.pdf>` - Extrai texto de PDF
- `#citar <doi>` - Adiciona referencia ao .bib
- `#escrever <capitulo>` - Redige capitulo com tom impessoal
- `#revisar` - Revisa tom e citacoes
- `#limpar-bib` - Padroniza BibTeX para ABNT
- `#validar` - Verifica citacoes vs referencias
- `#estrutura` - Valida elementos NBR 14724
- `#compilar` - Gera PDF

### Exemplos

Ver pasta `examples/` para projetos de exemplo em LaTeX, Markdown e Typst.

## Desenvolvimento

```bash
pip install -e "mcp_server[dev]"
pytest tests/ -v
```

### Makefile

```bash
make install          # Instalar dependencias
make test             # Executar testes
make lint-md          # Lint Markdown
make lint-secrets     # Escanear secrets
make lint             # Executar todos os lints
make validate         # Validar .gitignore
```

## Seguranca: Defesa em 4 Camadas

Estrategia de **defesa em profundidade** para prevenir vazamento de secrets:

| Camada | Defesa | Ferramenta | Funcao |
|--------|--------|------------|--------|
| 1 | Local | husky + gitleaks | Bloqueia commits com secrets |
| 2 | Repositorio | .gitignore + .env.example | Evita rastreio de arquivos sensiveis |
| 3 | Nuvem | GitHub Push Protection | Bloqueia pushes com secrets |
| 4 | IA | .cursorrules | Instrui IA a nunca gerar codigo inseguro |

Consulte [SECURITY.md](SECURITY.md) para detalhes completos.

## Modos de Idioma

O repositorio suporta documentacao bilingue (PT-BR/EN):

### PT-BR-First (Atual)

- `README.pt-BR.md` e a fonte da verdade (Portugues)
- `README.md` e a traducao (Ingles)

### EN-First

- `README.md` e a fonte da verdade (Ingles)
- `README.pt-BR.md` e a traducao (Portugues)

Alterne modos com:

```bash
./scripts/set-mode.sh pt-br-first
./scripts/set-mode.sh en-first
```

## Convencao de Commits

Todos os commits devem seguir o [Conventional Commits](https://conventionalcommits.org):

```text
<tipo>(<escopo opcional>): <descricao>
```

### Tipos Disponiveis

- `feat` - Nova funcionalidade
- `fix` - Correcao de bug
- `docs` - Alteracoes na documentacao
- `security` - Correcoes de seguranca
- `style` - Alteracoes de estilo de codigo
- `refactor` - Refatoracao de codigo
- `test` - Adicao ou atualizacao de testes
- `chore` - Tarefas de manutencao
- `ci` - Alteracoes na configuracao de CI/CD
- `revert` - Reversao de commits anteriores

## Estrutura do Projeto

```text
.
├── .github/
│   ├── workflows/
│   │   ├── ci.yml              # Validacao CI + scan de secrets
│   │   └── test.yml            # Testes Python multiplataforma
│   ├── dependabot.yml
│   └── mode.json               # Configuracao do modo de idioma
├── .husky/
│   ├── commit-msg              # Validacao de mensagens de commit
│   └── pre-commit              # Gitleaks + linting Markdown
├── scripts/
│   ├── set-mode.sh             # Alternador de modo de idioma
│   └── verify-gitignore.sh     # Verificacao de .gitignore
├── mcp_server/
│   ├── server.py               # Servidor MCP principal
│   └── pyproject.toml          # Configuracao do projeto Python
├── tests/                      # Testes unitarios
├── examples/                   # Projetos de exemplo
├── docs/                       # Documentacao adicional
├── README.md                   # Documentacao em ingles
├── README.pt-BR.md             # Documentacao em portugues
├── CONTRIBUTING.md             # Diretrizes de contribuicao
├── CODE_OF_CONDUCT.md          # Padroes da comunidade
├── SECURITY.md                 # Politica de seguranca
├── CHANGELOG.md                # Historico de versoes
├── .cursorrules                # Regras de seguranca para IA
├── .gitleaks.toml              # Configuracao de deteccao de secrets
├── .env.example                # Template de ambiente
├── Makefile                    # Comandos de desenvolvimento
├── .commitlintrc.json          # Regras de linting de commits
├── .markdownlint.json          # Regras de linting de markdown
└── .lychee.toml                # Configuracao do verificador de links
```

## Contribuindo

Acolhemos contribuicoes! Por favor, leia [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes.

## Seguranca

Consulte [SECURITY.md](SECURITY.md) para:

- Processo de reporte de vulnerabilidades
- Estrategia de protecao de secrets em 4 camadas
- Plano de contingencia para secrets vazados
- Regras de seguranca para IA (.cursorrules)

## Licenca

Este projeto esta licenciado sob a Licenca MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

Se voce encontrar este repositorio util, considere dar uma estrela!

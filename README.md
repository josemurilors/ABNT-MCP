# TCC-MCP

[![en](https://img.shields.io/badge/lang-en-red.svg)](README.md)
[![pt-br](https://img.shields.io/badge/lang-pt--br-green.svg)](README.pt-BR.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)
[![Secret Scanning](https://img.shields.io/badge/Secret%20Scanning-Gitleaks-brightgreen)](SECURITY.md)

> Academic writing and review tool for Brazilian TCCs (undergraduate theses) following ABNT standards.

## About

MCP (Model Context Protocol) server that provides academic assistance tools for undergraduate theses (TCC) in Brazil. Supports article search, PDF reading, BibTeX citation management, chapter writing with impersonal tone, review, and PDF compilation.

## Features

- **Academic Search** - Search articles in academic databases
- **PDF Reading** - Extract text from PDF documents
- **Citation Management** - Add references to .bib file
- **Assisted Writing** - Write chapters with academic impersonal tone
- **Review** - Check tone and citations
- **ABNT Validation** - Standardize BibTeX and verify NBR 14724 elements
- **Compilation** - Generate PDF from LaTeX, Markdown or Typst

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/josemurilors/tcc-mcp.git
cd tcc-mcp
```

### 2. Configure email in opencode.json

```json
{
  "mcpServers": {
    "tcc-mcp": {
      "env": {
        "TCC_MCP_EMAIL": "your.email@academic.com"
      }
    }
  }
}
```

### 3. (Optional) Install compilers

- **LaTeX:** TeX Live (Linux), MiKTeX (Windows), MacTeX (macOS)
- **Pandoc:** https://pandoc.org/installing.html
- **Typst:** https://typst.app/

## Usage

### Skill Commands

- `#pesquisar <tema>` - Search academic articles
- `#ler <arquivo.pdf>` - Extract text from PDF
- `#citar <doi>` - Add reference to .bib
- `#escrever <capitulo>` - Write chapter with impersonal tone
- `#revisar` - Review tone and citations
- `#limpar-bib` - Standardize BibTeX for ABNT
- `#validar` - Verify citations vs references
- `#estrutura` - Validate NBR 14724 elements
- `#compilar` - Generate PDF

### Examples

See `examples/` folder for sample projects in LaTeX, Markdown and Typst.

## Development

```bash
pip install -e "mcp_server[dev]"
pytest tests/ -v
```

### Makefile

```bash
make install          # Install dependencies
make test             # Run tests
make lint-md          # Lint Markdown
make lint-secrets     # Scan secrets
make lint             # Run all lints
make validate         # Validate .gitignore
```

## Security: 4-Layer Defense

**Defense-in-depth** strategy to prevent secret leaks:

| Layer | Defense | Tool | Function |
|-------|---------|------|----------|
| 1 | Local | husky + gitleaks | Blocks commits with secrets |
| 2 | Repository | .gitignore + .env.example | Prevents tracking sensitive files |
| 3 | Cloud | GitHub Push Protection | Blocks pushes with secrets |
| 4 | AI | .cursorrules | Instructs AI to never generate insecure code |

See [SECURITY.md](SECURITY.md) for full details.

## Language Modes

The repository supports bilingual documentation (PT-BR/EN):

### PT-BR-First (Current)

- `README.pt-BR.md` is the source of truth (Portuguese)
- `README.md` is the translation (English)

### EN-First

- `README.md` is the source of truth (English)
- `README.pt-BR.md` is the translation (Portuguese)

Switch modes with:

```bash
./scripts/set-mode.sh pt-br-first
./scripts/set-mode.sh en-first
```

## Commit Convention

All commits must follow the [Conventional Commits](https://conventionalcommits.org) specification:

```text
<type>(<optional scope>): <description>
```

### Available Types

- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation changes
- `security` - Security fixes
- `style` - Code style changes
- `refactor` - Code refactoring
- `test` - Adding or updating tests
- `chore` - Maintenance tasks
- `ci` - CI/CD configuration changes
- `revert` - Revert previous commits

## Project Structure

```text
.
├── .github/
│   ├── workflows/
│   │   ├── ci.yml              # CI validation + secret scanning
│   │   └── test.yml            # Cross-platform Python tests
│   ├── dependabot.yml
│   └── mode.json               # Language mode configuration
├── .husky/
│   ├── commit-msg              # Commit message validation
│   └── pre-commit              # Gitleaks + Markdown linting
├── scripts/
│   ├── set-mode.sh             # Language mode switcher
│   └── verify-gitignore.sh     # .gitignore verification
├── mcp_server/
│   ├── server.py               # Main MCP server
│   └── pyproject.toml          # Python project configuration
├── tests/                      # Unit tests
├── examples/                   # Example projects
├── docs/                       # Additional documentation
├── README.md                   # English documentation
├── README.pt-BR.md             # Portuguese documentation
├── CONTRIBUTING.md             # Contribution guidelines
├── CODE_OF_CONDUCT.md          # Community standards
├── SECURITY.md                 # Security policy
├── CHANGELOG.md                # Version history
├── .cursorrules                # AI security rules
├── .gitleaks.toml              # Secret detection configuration
├── .env.example                # Environment template
├── Makefile                    # Development commands
├── .commitlintrc.json          # Commit linting rules
├── .markdownlint.json          # Markdown linting rules
└── .lychee.toml                # Link checker configuration
```

## Contributing

We welcome contributions! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Security

See [SECURITY.md](SECURITY.md) for:

- Vulnerability reporting process
- 4-layer secret protection strategy
- Contingency plan for leaked secrets
- AI security rules (.cursorrules)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

If you find this repository useful, consider giving it a star!

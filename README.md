# TCC-MCP

Ferramenta de escrita e revisão acadêmica para TCCs brasileiros seguindo ABNT.

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/tcc-mcp.git
cd tcc-mcp
```

2. Configure seu email no `opencode.json`:
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

3. (Opcional) Instale compiladores:
- **LaTeX:** TeX Live (Linux), MiKTeX (Windows), MacTeX (macOS)
- **Pandoc:** https://pandoc.org/installing.html
- **Typst:** https://typst.app/

## Uso

### Comandos da Skill

- `#pesquisar <tema>` - Busca artigos acadêmicos
- `#ler <arquivo.pdf>` - Extrai texto de PDF
- `#citar <doi>` - Adiciona referência ao .bib
- `#escrever <capítulo>` - Redige capítulo com tom impessoal
- `#revisar` - Revisa tom e citações
- `#limpar-bib` - Padroniza BibTeX para ABNT
- `#validar` - Verifica citações vs referências
- `#estrutura` - Valida elementos NBR 14724
- `#compilar` - Gera PDF

### Exemplos

Ver pasta `examples/` para projetos de exemplo em LaTeX, Markdown e Typst.

## Desenvolvimento

```bash
pip install -e ".[dev]"
pytest
```

## Licença

MIT

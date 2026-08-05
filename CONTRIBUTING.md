# Guia de Contribuicao

Obrigado pelo seu interesse em contribuir com este projeto! Este documento fornece diretrizes e informacoes para contribuidores.

## Codigo de Conduta

Ao participar deste projeto, voce concorda em seguir nosso [Codigo de Conduta](CODE_OF_CONDUCT.md).

## Como Contribuir

### Reportando Bugs

Antes de criar relatorios de bug, verifique as issues existentes para evitar duplicatas. Ao criar um relatorio de bug, inclua o maximo de detalhes possivel:

- Use um titulo claro e descritivo
- Descreva os passos exatos para reproduzir o problema
- Forneça exemplos especificos (links, trechos de codigo, capturas de tela)
- Descreva o comportamento observado e o esperado
- Inclua detalhes do ambiente (SO, versao do Python, etc.)

### Sugerindo Melhorias

Sugestoes de melhorias sao acompanhadas como issues do GitHub. Ao criar uma sugestao:

- Use um titulo claro e descritivo
- Forneça uma descricao passo a passo da melhoria sugerida
- Forneça exemplos especificos para demonstrar os passos
- Descreva o comportamento atual e explique o comportamento esperado
- Explique por que esta melhoria seria util

### Pull Requests

1. Faca um fork do repositorio
2. Crie um branch de feature a partir de `main`:

   ```bash
   git checkout -b feat/nome-da-sua-feature
   ```

3. Faca suas alteracoes seguindo as diretrizes abaixo
4. Teste suas alteracoes localmente:

   ```bash
   make lint
   make test
   ```

5. Commite suas alteracoes usando [Conventional Commits](#convencao-de-commits):

   ```bash
   git commit -m "feat: Add new feature"
   ```

6. Push para seu fork:

   ```bash
   git push origin feat/nome-da-sua-feature
   ```

7. Abra um Pull Request

## Convencao de Commits

Todos os commits **devem** seguir a especificacao [Conventional Commits](https://conventionalcommits.org). Isso e validado automaticamente pelo nosso pipeline de CI.

### Formato

```text
<tipo>(<escopo>): <descricao>

[corpo opcional]

[rodape(s) opcional(is)]
```

### Tipos

- `feat`: Nova funcionalidade (incrementa versao MINOR)
- `fix`: Correcao de bug (incrementa versao PATCH)
- `docs`: Alteracoes apenas na documentacao
- `security`: Correcoes de seguranca (incrementa versao PATCH)
- `style`: Alteracoes que nao afetam o significado do codigo (espacos em branco, formatacao)
- `refactor`: Alteracao de codigo que nao corrige bug nem adiciona funcionalidade
- `test`: Adicao ou correcao de testes
- `chore`: Alteracoes no processo de build ou ferramentas auxiliares
- `ci`: Alteracoes em arquivos de configuracao de CI
- `revert`: Reversao de commit anterior

### Exemplos

```bash
# Bons exemplos
git commit -m "feat: Add bilingual README support"
git commit -m "fix: Correct broken links in documentation"
git commit -m "docs: Update CONTRIBUTING.md with branch protection rules"
git commit -m "security: Add gitleaks pre-commit hook"
git commit -m "ci: Add parity-check job to CI workflow"
git commit -m "refactor: Simplify link checker configuration"

# Maus exemplos (serao rejeitados)
git commit -m "Update README"
git commit -m "Fixed stuff"
git commit -m "WIP"
```

## Regras de Protecao de Branch

O branch `main` e protegido e requer:

- **Pull Request**: Minimo 1 aprovacao antes do merge
- **Status Checks**: Workflow CI deve passar
- **Atualizado**: Branches devem estar atualizadas antes do merge
- **Commits Assinados**: Todos os commits devem ser assinados
- **Historico Linear**: Apenas squash ou rebase merge
- **Sem Force Push**: Force pushes nao sao permitidos
- **Sem Exclusoes**: Branch nao pode ser deletado

## Padroes de Documentacao

### Estilo Markdown

Todos os arquivos Markdown devem passar na validacao `markdownlint`:

```bash
make lint-md
```

Regras principais:

- Comprimento de linha nao e forçado (MD013 desabilitado)
- Tags HTML sao permitidas (MD033 desabilitado)
- Use cabecalhos no estilo ATX (`#`, `##`, `###`)
- Use blocos de codigo com delimitadores e especificacao de linguagem
- Use marcadores de lista consistentes (`-` ou `*`)

### Validacao de Links

Todos os links devem ser validos e acessiveis:

```bash
make lint-links
```

- Use HTTPS quando disponivel
- Evite encurtadores de link
- Teste todos os links antes de enviar PR
- Atualize links quebrados imediatamente

## Regras de Seguranca (CRITICO)

### Nunca Commite Secrets

**Esta e uma regra rigida com tolerancia zero.**

#### Padroes Proibidos

```python
# NUNCA FACA ISSO
api_key = 'sk-proj-abc123...'
db_url = 'postgresql://admin:password@prod-db:5432/myapp'
```

#### Padrao Obrigatorio

```python
# SEMPRE FACA ISSO
import os
api_key = os.getenv('OPENAI_API_KEY')
db_url = os.getenv('DATABASE_URL')
```

### Deteccao de Secrets

Antes de commitar, execute:

```bash
make lint-secrets
```

Isso detecta:

- AWS Access Keys (`AKIA*`)
- OpenAI API Keys (`sk-proj-*`)
- GitHub PATs (`ghp_*`)
- Stripe Keys (`sk_live_*`)
- JWT Tokens
- Private Keys (PEM, PFX)
- Database Connection Strings

### Arquivos Protegidos

Estes arquivos sao automaticamente ignorados pelo Git:

- `.env`, `.env.*` (exceto `.env.example`)
- `*.pem`, `*.key`, `*.pfx`, `*.p12`
- `credentials.json`, `service-account*.json`
- `.cursor/`, `.claude/`, `.clinerules`

### Variaveis de Ambiente

Ao adicionar novas variaveis de ambiente:

1. Adicione ao `.env.example` com valor placeholder
2. Documente no README.md e README.pt-BR.md
3. Nunca use credenciais reais em exemplos

**Exemplo**:

```bash
# .env.example
OPENAI_API_KEY=your_openai_key_here
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

### Vibe Coding com IA

Ao usar ferramentas de IA (Cursor, Claude, Copilot):

1. Certifique-se de que `.cursorrules` esta presente na raiz do projeto
2. A IA sera instruida a nunca hardcodar secrets
3. Revise todo o codigo gerado por IA para secrets antes de commitar
4. Se a IA gerar um secret, substitua por `os.getenv('VARIABLE_NAME')`

Consulte [SECURITY.md](SECURITY.md) para a estrategia completa de defesa em 4 camadas.

## Processo de Review

1. **Verificacoes Automaticas**: CI executa automaticamente em todos os PRs
   - Linting de Markdown
   - Validacao de links
   - Validacao de mensagens de commit
   - Verificacao de paridade estrutural (EN <-> PT-BR)
   - Scan de secrets (gitleaks)
   - Auditoria de seguranca (.env files, chaves privadas, secrets hardcoded)

2. **Revisao Humana**: Pelo menos 1 mantenedor deve aprovar
   - Precisão do conteudo
   - Qualidade da documentacao
   - Aderencia aos padroes
   - Conformidade de seguranca

3. **Merge**: Apos aprovacao e todas as verificacoes passarem
   - Mantenedor fara merge usando squash ou rebase

## Setup de Desenvolvimento

### Pre-requisitos

- Python 3.8+
- Git 2.34+ (para Husky hooks)
- Node.js 18+ (para ferramentas de linting)
- Gitleaks (opcional, para scan local de secrets)

### Instalacao

```bash
# Clone seu fork
git clone https://github.com/SEU-USUARIO/tcc-mcp.git
cd tcc-mcp

# Instalar dependencias Python
pip install -e "mcp_server[dev]"

# Instalar dependencias Node (para hooks)
npm install

# Configurar Git hooks
npm run prepare

# (Opcional) Instalar gitleaks para scan local
# https://github.com/gitleaks/gitleaks/releases
```

### Desenvolvimento Local

```bash
# Executar testes
make test

# Lint Markdown
make lint-md

# Verificar links
make lint-links

# Scan de secrets
make lint-secrets

# Executar todas as validacoes
make lint

# Verificar .gitignore
make validate

# Alternar modo de idioma
./scripts/set-mode.sh en-first    # Ingles primeiro
./scripts/set-mode.sh pt-br-first # Portugues primeiro
```

## Duvidas?

Se tiver duvidas sobre contribuicao:

1. Verifique [issues](../../issues) e [discussoes](../../discussions) existentes
2. Abra uma nova issue com o label `question`
3. Entre em contato com os mantenedores

Obrigado por contribuir!

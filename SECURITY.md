# Politica de Seguranca

## Versoes Suportadas

Lancamos patches para vulnerabilidades de seguranca. Quais versoes sao elegiveis para receber tais patches depende da Classificacao CVSS v3.0:

| Versao | Suportada |
|--------|-----------|
| 0.1.x  | :white_check_mark: |

## Reportando uma Vulnerabilidade

**Por favor, nao reporte vulnerabilidades de seguranca atraves de issues publicas do GitHub.**

Em vez disso, reporte-as atraves de um dos seguintes metodos:

### Reporte Privado de Vulnerabilidade (Preferido)

1. Va para a [aba Seguranca](../../security/advisories/new) deste repositorio
2. Clique em "Report a vulnerability"
3. Preencha o formulario com o maximo de detalhes possivel

### Email

Se o reporte privado de vulnerabilidade nao estiver disponivel, envie um email diretamente aos mantenedores:

- **Primario**: josemurilors@gmail.com

## O que Incluir

Por favor, inclua as seguintes informacoes no seu reporte:

- Tipo de problema (ex: buffer overflow, SQL injection, cross-site scripting)
- Caminhos completos do(s) arquivo(s) de origem relacionados a manifestacao do problema
- Localizacao do codigo-fonte afetado (tag/branch/commit ou URL direta)
- Qualquer configuracao especial necessaria para reproduzir o problema
- Instrucoes passo a passo para reproduzir o problema
- Prova de conceito ou codigo de exploit (se possivel)
- Impacto do problema, incluindo como um atacante poderia explora-lo

## Cronograma de Resposta

- **Resposta Inicial**: Dentro de 48 horas apos o envio
- **Atualizacao de Status**: Dentro de 7 dias com detalhes sobre a vulnerabilidade e correcao planejada
- **Resolucao**: O cronograma depende da severidade e complexidade

## Politica de Divulgacao

- Seguimos **Divulgacao Coordenada de Vulnerabilidades**
- Trabalharemos com voce para entender e reproduzir o problema
- Notificaremos voce quando uma correcao for implementada
- Creditaremos voce no advisory de seguranca (a menos que prefira permanecer anonimo)
- A divulgacao publica sera feita apos uma correcao estar disponivel

---

## Vibe Coding Security: Defesa em 4 Camadas

Este repositorio implementa uma estrategia de **defesa em profundidade de 4 camadas** para prevenir vazamento de secrets no desenvolvimento assistido por IA (Vibe Coding).

### Camada 1: Defesa Local (Bloqueio Pre-Commit)

**Objetivo**: Impedir que secrets sejam escritos no historico do Git.

**Ferramentas**:

- **Gitleaks** + **Husky** pre-commit hook

**Como funciona**:

```bash
# Todo git commit dispara scan do gitleaks
git commit -> husky pre-commit -> gitleaks detect -> PASS/FAIL
```

**Configuracao**:

- `.gitleaks.toml` - Regras de deteccao para AWS, OpenAI, Stripe, JWT, etc.
- `.husky/pre-commit` - Hook que executa gitleaks antes de cada commit

**Validacao local**:

```bash
make lint-secrets          # Escanear repositorio inteiro
```

### Camada 2: Defesa do Repositorio (.gitignore & Templates)

**Objetivo**: Impedir que arquivos sensiveis sejam rastreados pelo Git.

**Arquivos**:

- `.gitignore` - Padroes abrangentes de ignore para secrets
- `.env.example` - Template com valores placeholder

**Padroes protegidos**:

```gitignore
# Arquivos de ambiente
.env
.env.*
!.env.example

# Chaves e certificados
*.pem
*.key
*.pfx
*.p12
credentials.json
service-account*.json

# Dados locais de ferramentas de IA
.cursor/
.clinerules
.claude/
```

### Camada 3: Defesa na Nuvem (GitHub Push Protection)

**Objetivo**: Bloquear secrets no nivel do servidor GitHub antes de serem salvos.

**Recursos para habilitar** (Acesso admin necessario):

1. **GitHub Push Protection**:
   - Navegue para: `Settings -> Code security and analysis`
   - Habilite: "Push protection"
   - GitHub rejeitara pushes contendo padroes de secrets conhecidos

2. **Secret Scanning**:
   - Habilite: "Secret scanning"
   - GitHub escaneia continuamente por secrets e alerta admins

3. **Dependabot Alerts**:
   - Habilite: "Dependabot"
   - Notificacoes automaticas para dependencias vulneraveis

**Padroes suportados** (deteccao nativa do GitHub):

- `sk-proj-*` (OpenAI)
- `AKIA*` (AWS Access Keys)
- `ghp_*` (GitHub PATs)
- `sk_live_*` (Stripe)
- E mais de 200 padroes

### Camada 4: Higiene de IA (Regras de Prompt)

**Objetivo**: Instruir ferramentas de IA a nunca gerar codigo inseguro.

**Arquivo**: `.cursorrules`

**Regras principais**:

```text
NUNCA FACA:
- Hardcodar API keys, tokens, senhas em codigo-fonte
- Commitar arquivos .env com credenciais reais
- Logar informacoes sensiveis
- Incluir secrets em mensagens de erro

SEMPRE FAC:
- Usar variaveis de ambiente: os.getenv (Python)
- Referenciar .env.example para variaveis necessarias
- Usar GitHub Secrets para CI/CD
- Usar gerenciadores de secrets em producao (Vault, AWS Secrets Manager)
```

**Comportamento do agente de IA**:

1. Antes de gerar codigo: Verificar se a tarefa requer APIs externas
2. Se sim: Usar variaveis de ambiente exclusivamente
3. Se o usuario fornecer uma chave: Armazenar em .env (nao no codigo)
4. Lembrar o usuario de adicionar a chave ao .env.example

---

## Plano de Contingencia (Se um Secret Vazar)

Se um secret for acidentalmente commitado apesar de todas as defesas:

### Passo 1: Revogar Imediatamente (FACA ISSO PRIMEIRO)

**A primeira acao NUNCA e deletar o commit Git.** A primeira acao e **invalidar a chave no provedor**.

- **OpenAI**: Dashboard -> API Keys -> Revoke
- **AWS**: IAM -> Users -> Security credentials -> Deactivate
- **GitHub**: Settings -> Developer settings -> Personal access tokens -> Delete
- **Stripe**: Dashboard -> Developers -> API keys -> Roll key

### Passo 2: Reescrever Historico Git

Um simples `git rm` NAO remove o secret dos commits anteriores. Voce deve reescrever o historico:

**Opcao A: git-filter-repo (Recomendado)**

```bash
# Instalar
pip install git-filter-repo

# Remover arquivo especifico de todo o historico
git filter-repo --path .env --force

# Remover string especifica de todo o historico
git filter-repo --replace-text expressions.txt --force
# Onde expressions.txt contem:
# literal:sk-proj-abc123...==>REMOVED
```

**Opcao B: BFG Repo-Cleaner**

```bash
# Download BFG
wget https://repo1.maven.org/maven2/com/madgag/bfg/1.14.0/bfg-1.14.0.jar

# Remover arquivo
java -jar bfg.jar --delete-files .env

# Remover senha
java -jar bfg.jar --replace-text passwords.txt
```

**Apos reescrever**:

```bash
# Force push (PERIGOSO - coordenar com a equipe)
git push --force --all
git push --force --tags

# Notificar todos os contribuidores para re-clonar
```

### Passo 3: Rotacionar Todas as Credenciais Relacionadas

Mesmo que voce tenha removido o secret, assuma que esta comprometido:

1. Gere novas credenciais no provedor
2. Atualize arquivos `.env` localmente (nunca commite)
3. Atualize GitHub Secrets se usado em CI/CD
4. Atualize quaisquer sistemas de producao usando as credenciais antigas
5. Audite logs para uso nao autorizado

### Passo 4: Revisao Pos-Incidente

1. Documente o que aconteceu em um advisory de seguranca privado
2. Identifique a causa raiz (qual camada falhou?)
3. Atualize regras de deteccao se necessario
4. Treine a equipe sobre o incidente (sem culpa)

---

## Melhores Praticas de Seguranca

### Gerenciamento de Secrets

- **Nunca** commite secrets, API keys, tokens ou senhas
- Use variaveis de ambiente (arquivos `.env`) para desenvolvimento local
- Adicione arquivos sensiveis ao `.gitignore`
- Use GitHub Secrets para workflows de CI/CD
- Use gerenciadores de secrets em producao (AWS Secrets Manager, HashiCorp Vault, Infisical)

### Dependencias

- Mantenha dependencias atualizadas (Dependabot esta habilitado)
- Revise atualizacoes de dependencias antes do merge
- Use `pip audit` para verificar vulnerabilidades conhecidas

### Revisao de Codigo

- Todas as alteracoes devem passar por revisao de pull request
- Alteracoes sensiveis a seguranca requerem revisao adicional
- CI executa scan de secrets automaticamente

### Autenticacao

- Use OIDC (OpenID Connect) para autenticacao de provedores cloud quando possivel
- Evite credenciais estaticas de longa duracao
- Rotacione secrets regularmente (90 dias recomendado)

---

## Recursos de Seguranca

Este repositorio implementa os seguintes recursos de seguranca:

- **Gitleaks**: Deteccao de secrets em pre-commit hooks e CI
- **Dependabot**: Atualizacoes automatizadas de dependencias
- **Secret Scanning**: Deteccao nativa de secrets do GitHub
- **Push Protection**: Bloqueia secrets antes de serem pushados
- **Branch Protection**: Previne alteracoes nao autorizadas em `main`
- **Code Review**: Aprovacoes necessarias antes do merge
- **Signed Commits**: Garante autenticidade dos commits
- **AI Rules**: .cursorrules para desenvolvimento assistido por IA seguro

## Atualizacoes de Seguranca

Atualizacoes de seguranca sao anunciadas via:

- GitHub Security Advisories
- Notas de lancamento no [CHANGELOG.md](CHANGELOG.md)
- GitHub Releases

## Contato

Para perguntas relacionadas a seguranca:

- **Email**: josemurilors@gmail.com
- **GitHub Security Advisory**: [New Advisory](../../security/advisories/new)

Obrigado por ajudar a manter este projeto seguro!

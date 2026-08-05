.PHONY: install test lint lint-md lint-md-fix lint-links lint-secrets validate mode-en mode-pt help

install:
	pip install -e "mcp_server[dev]"
	npm install
	npx husky init

test:
	pytest tests/ -v

lint: lint-md lint-links lint-secrets

lint-md:
	npx --no -- markdownlint-cli2 '**/*.md' '!node_modules/**/*.md' '!**/.venv/**/*.md'

lint-md-fix:
	npx --no -- markdownlint-cli2 '**/*.md' '!node_modules/**/*.md' '!**/.venv/**/*.md' --fix

lint-links:
	lychee '*.md' '**/*.md'

lint-secrets:
	gitleaks detect --source . -v --config .gitleaks.toml

validate:
	./scripts/verify-gitignore.sh

mode-en:
	./scripts/set-mode.sh en-first

mode-pt:
	./scripts/set-mode.sh pt-br-first

help:
	@echo "Available commands:"
	@echo "  make install        - Install Python and Node dependencies"
	@echo "  make test           - Run pytest"
	@echo "  make lint           - Run all linters (md, links, secrets)"
	@echo "  make lint-md        - Lint Markdown files"
	@echo "  make lint-md-fix    - Fix auto-fixable Markdown issues"
	@echo "  make lint-links     - Check links"
	@echo "  make lint-secrets   - Scan for secrets"
	@echo "  make validate       - Verify .gitignore rules"
	@echo "  make mode-en        - Set English as source of truth"
	@echo "  make mode-pt        - Set Portuguese as source of truth"

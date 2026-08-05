#!/bin/bash

set -e

MODE=$1

if [ -z "$MODE" ]; then
  echo "Erro: Modo nao especificado"
  echo "Uso: ./scripts/set-mode.sh [en-first|pt-br-first]"
  echo ""
  echo "Modos disponiveis:"
  echo "  en-first    - Ingles e a fonte da verdade (padrao)"
  echo "  pt-br-first - Portugues e a fonte da verdade"
  exit 1
fi

if [ "$MODE" != "en-first" ] && [ "$MODE" != "pt-br-first" ]; then
  echo "Erro: Modo invalido: $MODE"
  echo "Modos validos: en-first, pt-br-first"
  exit 1
fi

cat > .github/mode.json << EOF
{
  "mode": "$MODE",
  "description": "Language mode configuration for the repository",
  "primary_language": "$([ "$MODE" = "en-first" ] && echo "en" || echo "pt-BR")",
  "secondary_language": "$([ "$MODE" = "en-first" ] && echo "pt-BR" || echo "en")",
  "source_of_truth": "$([ "$MODE" = "en-first" ] && echo "README.md" || echo "README.pt-BR.md")",
  "translation_file": "$([ "$MODE" = "en-first" ] && echo "README.pt-BR.md" || echo "README.md")",
  "modes": {
    "en-first": {
      "primary": "README.md",
      "secondary": "README.pt-BR.md",
      "description": "English is the source of truth, Portuguese is the translation"
    },
    "pt-br-first": {
      "primary": "README.pt-BR.md",
      "secondary": "README.md",
      "description": "Portuguese is the source of truth, English is the translation"
    }
  }
}
EOF

echo "Modo configurado com sucesso: $MODE"
echo ""
if [ "$MODE" = "en-first" ]; then
  echo "Fonte da verdade: README.md (Ingles)"
  echo "Traducao: README.pt-BR.md (Portugues)"
else
  echo "Fonte da verdade: README.pt-BR.md (Portugues)"
  echo "Traducao: README.md (Ingles)"
fi
echo ""
echo "Lembre-se de fazer commit das alteracoes:"
echo "   git add .github/mode.json"
echo "   git commit -m 'chore: Set language mode to $MODE'"

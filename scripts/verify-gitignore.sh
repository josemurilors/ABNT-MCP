#!/bin/bash

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

PASSED=0
FAILED=0

pass() {
    echo -e "${GREEN}PASS${NC}: $1"
    PASSED=$((PASSED + 1))
}

fail() {
    echo -e "${RED}FAIL${NC}: $1"
    FAILED=$((FAILED + 1))
}

info() {
    echo -e "${YELLOW}INFO${NC}: $1"
}

echo "=========================================="
echo "Git Ignore Verification"
echo "=========================================="
echo ""

info "Creating test directory structure..."

mkdir -p .cursor/rules
mkdir -p .cursor/chats
mkdir -p .cursor/projects
mkdir -p .claude
mkdir -p .windsurf/logs
mkdir -p .vscode
mkdir -p .idea/runConfigurations
mkdir -p .idea/codeStyles
mkdir -p .idea/shelf

touch .cursor/rules/shared-rules.md
touch .cursor/chats/local-chat.json
touch .cursor/projects/local-project.json
touch .cursor/local.json
touch .cursor/test.log
touch .claude/settings.json
touch .claude/local.json
touch .claude/test.log
touch .windsurf/config.local.json
touch .windsurf/logs/test.log
touch .vscode/settings.json
touch .vscode/settings.local.json
touch .vscode/test.log
touch .vscode/launch.json
touch .idea/runConfigurations/App.xml
touch .idea/codeStyles/codeStyleConfig.xml
touch .idea/workspace.xml
touch .idea/usage.statistics.xml
touch .idea/shelf/changes.txt
touch .idea/test.log

echo ""
info "Running verification checks..."
echo ""

if git check-ignore -q .cursor/rules/shared-rules.md 2>/dev/null; then
    fail ".cursor/rules/shared-rules.md is ignored (should be trackable)"
else
    pass ".cursor/rules/shared-rules.md is trackable"
fi

if git check-ignore -q .cursor/chats/local-chat.json 2>/dev/null; then
    pass ".cursor/chats/local-chat.json is ignored"
else
    fail ".cursor/chats/local-chat.json is NOT ignored (should be ignored)"
fi

if git check-ignore -q .cursor/projects/local-project.json 2>/dev/null; then
    pass ".cursor/projects/local-project.json is ignored"
else
    fail ".cursor/projects/local-project.json is NOT ignored (should be ignored)"
fi

if git check-ignore -q .cursor/local.json 2>/dev/null; then
    pass ".cursor/local.json is ignored"
else
    fail ".cursor/local.json is NOT ignored (should be ignored)"
fi

if git check-ignore -q .cursor/test.log 2>/dev/null; then
    pass ".cursor/test.log is ignored"
else
    fail ".cursor/test.log is NOT ignored (should be ignored)"
fi

if git check-ignore -q .claude/settings.json 2>/dev/null; then
    fail ".claude/settings.json is ignored (should be trackable)"
else
    pass ".claude/settings.json is trackable"
fi

if git check-ignore -q .claude/local.json 2>/dev/null; then
    pass ".claude/local.json is ignored"
else
    fail ".claude/local.json is NOT ignored (should be ignored)"
fi

if git check-ignore -q .claude/test.log 2>/dev/null; then
    pass ".claude/test.log is ignored"
else
    fail ".claude/test.log is NOT ignored (should be ignored)"
fi

if git check-ignore -q .windsurf/config.local.json 2>/dev/null; then
    pass ".windsurf/config.local.json is ignored"
else
    fail ".windsurf/config.local.json is NOT ignored (should be ignored)"
fi

if git check-ignore -q .windsurf/logs/test.log 2>/dev/null; then
    pass ".windsurf/logs/test.log is ignored"
else
    fail ".windsurf/logs/test.log is NOT ignored (should be ignored)"
fi

if git check-ignore -q .vscode/settings.json 2>/dev/null; then
    fail ".vscode/settings.json is ignored (should be trackable)"
else
    pass ".vscode/settings.json is trackable"
fi

if git check-ignore -q .vscode/settings.local.json 2>/dev/null; then
    pass ".vscode/settings.local.json is ignored"
else
    fail ".vscode/settings.local.json is NOT ignored (should be ignored)"
fi

if git check-ignore -q .vscode/test.log 2>/dev/null; then
    pass ".vscode/test.log is ignored"
else
    fail ".vscode/test.log is NOT ignored (should be ignored)"
fi

if git check-ignore -q .vscode/launch.json 2>/dev/null; then
    pass ".vscode/launch.json is ignored"
else
    fail ".vscode/launch.json is NOT ignored (should be ignored)"
fi

if git check-ignore -q .idea/runConfigurations/App.xml 2>/dev/null; then
    fail ".idea/runConfigurations/App.xml is ignored (should be trackable)"
else
    pass ".idea/runConfigurations/App.xml is trackable"
fi

if git check-ignore -q .idea/codeStyles/codeStyleConfig.xml 2>/dev/null; then
    fail ".idea/codeStyles/codeStyleConfig.xml is ignored (should be trackable)"
else
    pass ".idea/codeStyles/codeStyleConfig.xml is trackable"
fi

if git check-ignore -q .idea/workspace.xml 2>/dev/null; then
    pass ".idea/workspace.xml is ignored"
else
    fail ".idea/workspace.xml is NOT ignored (should be ignored)"
fi

if git check-ignore -q .idea/usage.statistics.xml 2>/dev/null; then
    pass ".idea/usage.statistics.xml is ignored"
else
    fail ".idea/usage.statistics.xml is NOT ignored (should be ignored)"
fi

if git check-ignore -q .idea/shelf/changes.txt 2>/dev/null; then
    pass ".idea/shelf/changes.txt is ignored"
else
    fail ".idea/shelf/changes.txt is NOT ignored (should be ignored)"
fi

if git check-ignore -q .idea/test.log 2>/dev/null; then
    pass ".idea/test.log is ignored"
else
    fail ".idea/test.log is NOT ignored (should be ignored)"
fi

touch .env.example
if git check-ignore -q .env.example 2>/dev/null; then
    fail ".env.example is ignored (should be trackable)"
else
    pass ".env.example is trackable"
fi

touch .env
if git check-ignore -q .env 2>/dev/null; then
    pass ".env is ignored"
else
    fail ".env is NOT ignored (should be ignored)"
fi

touch test.key
if git check-ignore -q test.key 2>/dev/null; then
    pass "test.key is ignored"
else
    fail "test.key is NOT ignored (should be ignored)"
fi

echo ""
echo "=========================================="
echo "Verification Summary"
echo "=========================================="
echo -e "Passed: ${GREEN}${PASSED}${NC}"
echo -e "Failed: ${RED}${FAILED}${NC}"
echo ""

info "Cleaning up test files..."
rm -rf .cursor .claude .windsurf .vscode .idea .env.example .env test.key

echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}All checks passed!${NC}"
    exit 0
else
    echo -e "${RED}Some checks failed. Please review .gitignore.${NC}"
    exit 1
fi

# Git Commit Message Generator

Generate meaningful commit messages based on git diff analysis.

## Usage

```bash
python git-commit-message-generator.py [options]
```

## Options

- `--staged`: Analyze staged changes (git diff --cached)
- `--branch <branch>`: Compare with specific branch
- `--format <format>`: Message format (conventional/simple/detailed)

## Features

- Analyzes git diff to understand the nature of changes
- Generates conventional commit format messages
- Automatically detects commit type (feat, fix, docs, style, refactor, etc.)
- Determines scope based on changed files
- Creates descriptive commit messages
- No references to automation or AI generation

## Examples

```bash
# Analyze unstaged changes
python git-commit-message-generator.py

# Analyze staged changes
python git-commit-message-generator.py --staged

# Simple format
python git-commit-message-generator.py --format simple

# Compare with main branch
python git-commit-message-generator.py --branch main
```

## Commit Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Test changes
- `chore`: Maintenance tasks
#!/usr/bin/env python3
"""
Git Commit Message Generator - Claude Skill

This skill analyzes git diff output and generates appropriate commit messages
following conventional commit format.
"""

import subprocess
import sys
import re
from typing import List, Dict, Tuple
import argparse


def run_git_command(command: List[str]) -> str:
    """Run a git command and return its output."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {e}", file=sys.stderr)
        sys.exit(1)


def analyze_diff(diff_output: str) -> Dict[str, any]:
    """Analyze git diff output to understand changes."""
    analysis = {
        'files_changed': [],
        'additions': 0,
        'deletions': 0,
        'file_types': set(),
        'change_patterns': []
    }

    # Parse file changes
    file_pattern = r'diff --git a/(.*) b/(.*)'
    for match in re.finditer(file_pattern, diff_output):
        file_path = match.group(1)
        analysis['files_changed'].append(file_path)

        # Determine file type
        if file_path.endswith(('.py', '.pyw')):
            analysis['file_types'].add('python')
        elif file_path.endswith(('.js', '.jsx', '.ts', '.tsx')):
            analysis['file_types'].add('javascript')
        elif file_path.endswith(('.html', '.htm')):
            analysis['file_types'].add('html')
        elif file_path.endswith('.css'):
            analysis['file_types'].add('css')
        elif file_path.endswith(('.yml', '.yaml')):
            analysis['file_types'].add('yaml')
        elif file_path.endswith('.json'):
            analysis['file_types'].add('json')
        elif file_path.endswith('.md'):
            analysis['file_types'].add('markdown')
        elif file_path.endswith(('.sh', '.bash', '.zsh')):
            analysis['file_types'].add('shell')
        elif file_path.endswith('.toml'):
            analysis['file_types'].add('toml')
        elif file_path.endswith('Dockerfile'):
            analysis['file_types'].add('docker')

    # Count additions and deletions
    additions = len(re.findall(r'^\+[^+]', diff_output, re.MULTILINE))
    deletions = len(re.findall(r'^-[^-]', diff_output, re.MULTILINE))
    analysis['additions'] = additions
    analysis['deletions'] = deletions

    # Detect common patterns
    if re.search(r'def test_|class Test|@pytest|@unittest', diff_output):
        analysis['change_patterns'].append('test')
    if re.search(r'README|CHANGELOG|LICENSE|CONTRIBUTING', diff_output, re.IGNORECASE):
        analysis['change_patterns'].append('docs')
    if re.search(r'bug|fix|error|issue|problem|crash|failure', diff_output, re.IGNORECASE):
        analysis['change_patterns'].append('bugfix')
    if re.search(r'feat|feature|add|new|implement', diff_output, re.IGNORECASE):
        analysis['change_patterns'].append('feature')
    if re.search(r'refactor|restructure|reorganize|clean', diff_output, re.IGNORECASE):
        analysis['change_patterns'].append('refactor')
    if re.search(r'style|format|lint|prettier|eslint', diff_output, re.IGNORECASE):
        analysis['change_patterns'].append('style')
    if re.search(r'performance|optimize|speed|faster|cache', diff_output, re.IGNORECASE):
        analysis['change_patterns'].append('perf')
    if re.search(r'config|configuration|settings|env', diff_output, re.IGNORECASE):
        analysis['change_patterns'].append('config')
    if re.search(r'dependency|dependencies|package|npm|pip|yarn|requirements', diff_output, re.IGNORECASE):
        analysis['change_patterns'].append('deps')

    return analysis


def determine_commit_type(analysis: Dict) -> str:
    """Determine the conventional commit type based on analysis."""
    patterns = analysis['change_patterns']

    if 'bugfix' in patterns:
        return 'fix'
    elif 'feature' in patterns:
        return 'feat'
    elif 'docs' in patterns:
        return 'docs'
    elif 'style' in patterns:
        return 'style'
    elif 'refactor' in patterns:
        return 'refactor'
    elif 'perf' in patterns:
        return 'perf'
    elif 'test' in patterns:
        return 'test'
    elif 'config' in patterns:
        return 'chore'
    elif 'deps' in patterns:
        return 'chore'
    elif analysis['deletions'] > analysis['additions'] * 2:
        return 'refactor'
    elif analysis['additions'] > 10:
        return 'feat'
    else:
        return 'chore'


def get_scope(files_changed: List[str]) -> str:
    """Determine scope based on changed files."""
    if not files_changed:
        return ''

    # If all files are in the same directory
    directories = set()
    for file_path in files_changed:
        if '/' in file_path:
            directories.add(file_path.split('/')[0])

    if len(directories) == 1:
        scope = list(directories)[0]
        # Shorten common directory names
        scope_map = {
            'source': 'src',
            'sources': 'src',
            'test': 'test',
            'tests': 'test',
            'documentation': 'docs',
            'config': 'config',
            'configuration': 'config',
        }
        return scope_map.get(scope.lower(), scope)

    # If files have common extensions
    extensions = set()
    for file_path in files_changed:
        if '.' in file_path:
            ext = file_path.split('.')[-1]
            extensions.add(ext)

    if len(extensions) == 1:
        ext = list(extensions)[0]
        if ext in ['py', 'js', 'ts', 'go', 'rs', 'java']:
            return 'core'
        elif ext in ['md', 'txt', 'rst']:
            return 'docs'
        elif ext in ['yml', 'yaml', 'json', 'toml']:
            return 'config'

    # Check for specific files
    for file_path in files_changed:
        base_name = file_path.split('/')[-1].lower()
        if base_name in ['readme.md', 'readme.txt', 'readme.rst']:
            return 'readme'
        elif base_name in ['package.json', 'requirements.txt', 'pyproject.toml', 'cargo.toml', 'go.mod']:
            return 'deps'
        elif base_name.startswith('dockerfile'):
            return 'docker'
        elif base_name in ['.gitignore', '.env', '.env.example']:
            return 'config'

    return ''


def generate_description(analysis: Dict, commit_type: str) -> str:
    """Generate commit message description."""
    files_changed = analysis['files_changed']
    additions = analysis['additions']
    deletions = analysis['deletions']

    if not files_changed:
        return "Update files"

    # Handle single file changes
    if len(files_changed) == 1:
        file_name = files_changed[0].split('/')[-1]

        if commit_type == 'fix':
            return f"Resolve issues in {file_name}"
        elif commit_type == 'feat':
            if additions > deletions * 2:
                return f"Add new functionality to {file_name}"
            else:
                return f"Enhance {file_name}"
        elif commit_type == 'docs':
            return f"Update documentation in {file_name}"
        elif commit_type == 'style':
            return f"Format {file_name}"
        elif commit_type == 'refactor':
            return f"Restructure {file_name}"
        elif commit_type == 'test':
            return f"Add tests for {file_name}"
        elif commit_type == 'perf':
            return f"Optimize {file_name} performance"
        else:
            return f"Update {file_name}"

    # Handle multiple file changes
    if commit_type == 'fix':
        return "Resolve multiple issues"
    elif commit_type == 'feat':
        if len(analysis['file_types']) == 1:
            file_type = list(analysis['file_types'])[0]
            return f"Add new {file_type} features"
        return "Add new functionality"
    elif commit_type == 'docs':
        return "Update documentation"
    elif commit_type == 'style':
        return "Format code"
    elif commit_type == 'refactor':
        if deletions > additions:
            return "Remove unnecessary code"
        return "Restructure codebase"
    elif commit_type == 'test':
        return "Add test coverage"
    elif commit_type == 'perf':
        return "Improve performance"
    elif commit_type == 'chore':
        if 'deps' in analysis['change_patterns']:
            return "Update dependencies"
        elif 'config' in analysis['change_patterns']:
            return "Update configuration"
        return "Update project files"

    return f"Update {len(files_changed)} files"


def generate_body(analysis: Dict) -> str:
    """Generate optional commit body with details."""
    body_lines = []

    files = analysis['files_changed']
    if len(files) > 3:
        body_lines.append("Modified files:")
        for file_path in files[:10]:  # Limit to first 10 files
            body_lines.append(f"  - {file_path}")
        if len(files) > 10:
            body_lines.append(f"  ... and {len(files) - 10} more files")

    # Add statistics if significant
    if analysis['additions'] > 50 or analysis['deletions'] > 50:
        body_lines.append("")
        body_lines.append(f"Changes: +{analysis['additions']} -{analysis['deletions']}")

    return '\n'.join(body_lines)


def main():
    parser = argparse.ArgumentParser(
        description='Generate commit messages based on git diff'
    )
    parser.add_argument(
        '--staged',
        action='store_true',
        help='Analyze staged changes (git diff --cached) instead of unstaged'
    )
    parser.add_argument(
        '--branch',
        type=str,
        help='Compare with specific branch (default: main/master)'
    )
    parser.add_argument(
        '--format',
        choices=['conventional', 'simple', 'detailed'],
        default='conventional',
        help='Commit message format'
    )

    args = parser.parse_args()

    # Get git diff
    if args.staged:
        diff_command = ['git', 'diff', '--cached']
    elif args.branch:
        diff_command = ['git', 'diff', args.branch]
    else:
        # Try to get default branch
        try:
            default_branch = run_git_command(['git', 'symbolic-ref', 'refs/remotes/origin/HEAD']).strip()
            default_branch = default_branch.replace('refs/remotes/origin/', '')
        except:
            default_branch = 'main'

        diff_command = ['git', 'diff']

    diff_output = run_git_command(diff_command)

    if not diff_output.strip():
        print("No changes detected. Make sure you have uncommitted changes or use --staged flag for staged changes.")
        sys.exit(0)

    # Analyze diff
    analysis = analyze_diff(diff_output)

    # Generate commit message
    commit_type = determine_commit_type(analysis)
    scope = get_scope(analysis['files_changed'])
    description = generate_description(analysis, commit_type)
    body = generate_body(analysis)

    # Format message based on style
    if args.format == 'simple':
        commit_message = description.capitalize()
    elif args.format == 'detailed':
        commit_message = f"{description.capitalize()}\n\n{body}" if body else description.capitalize()
    else:  # conventional
        if scope:
            commit_message = f"{commit_type}({scope}): {description.lower()}"
        else:
            commit_message = f"{commit_type}: {description.lower()}"

        if body and args.format == 'conventional':
            commit_message += f"\n\n{body}"

    print("\n" + "="*60)
    print("Generated Commit Message:")
    print("="*60)
    print(commit_message)
    print("="*60)

    # Offer to copy to clipboard if available
    try:
        import pyperclip
        pyperclip.copy(commit_message)
        print("\n✓ Commit message copied to clipboard!")
    except ImportError:
        print("\nTip: Install pyperclip to automatically copy to clipboard:")
        print("  pip install pyperclip")


if __name__ == "__main__":
    main()
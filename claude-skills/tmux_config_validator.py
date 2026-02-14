#!/usr/bin/env python3
"""
tmux Configuration Validator
Validates tmux configuration files for syntax errors and conflicts.
"""

import re
import sys
import os
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class ValidationLevel(Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"

@dataclass
class ValidationIssue:
    level: ValidationLevel
    line_number: int
    message: str
    line_content: str
    suggestion: Optional[str] = None

class TmuxConfigValidator:
    """Validates tmux configuration files."""

    def __init__(self, config_path: str = None):
        """Initialize validator with config file path."""
        if config_path:
            self.config_path = Path(config_path)
        else:
            # Default paths to check
            self.config_path = self._find_config_file()

        self.issues: List[ValidationIssue] = []
        self.keybindings: Dict[str, int] = {}
        self.options: Dict[str, Tuple[str, int]] = {}

    def _find_config_file(self) -> Path:
        """Find tmux config file in standard locations."""
        possible_paths = [
            Path.home() / ".tmux.conf",
            Path.home() / ".config" / "tmux" / "tmux.conf",
            Path("/Users/daisuke.oda/dotfiles/tmux/tmux.conf"),
        ]

        for path in possible_paths:
            if path.exists():
                return path

        raise FileNotFoundError("No tmux configuration file found")

    def validate(self) -> List[ValidationIssue]:
        """Run all validation checks."""
        self.issues = []

        # Read config file
        try:
            with open(self.config_path, 'r') as f:
                lines = f.readlines()
        except Exception as e:
            self.issues.append(ValidationIssue(
                ValidationLevel.ERROR,
                0,
                f"Cannot read config file: {e}",
                "",
                "Check file permissions and path"
            ))
            return self.issues

        # Run validation checks
        self._check_syntax(lines)
        self._check_keybinding_conflicts(lines)
        self._check_deprecated_options(lines)
        self._check_color_values(lines)
        self._check_paths(lines)
        self._validate_with_tmux()

        return self.issues

    def _check_syntax(self, lines: List[str]):
        """Check for common syntax errors."""
        for i, line in enumerate(lines, 1):
            # Skip comments and empty lines
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue

            # Check for unclosed quotes
            if self._has_unclosed_quotes(stripped):
                self.issues.append(ValidationIssue(
                    ValidationLevel.ERROR,
                    i,
                    "Unclosed quotes detected",
                    line.rstrip(),
                    "Ensure all quotes are properly closed"
                ))

            # Check for common typos
            typos = {
                'set-window-opton': 'set-window-option',
                'set-opton': 'set-option',
                'bind-keys': 'bind-key',
                'unbind-keys': 'unbind-key',
                'set-envionment': 'set-environment',
            }

            for typo, correct in typos.items():
                if typo in stripped:
                    self.issues.append(ValidationIssue(
                        ValidationLevel.ERROR,
                        i,
                        f"Possible typo: '{typo}'",
                        line.rstrip(),
                        f"Did you mean '{correct}'?"
                    ))

    def _has_unclosed_quotes(self, line: str) -> bool:
        """Check if line has unclosed quotes."""
        # Remove escaped quotes
        line = line.replace(r'\"', '').replace(r"\'", '')

        # Count quotes
        single_quotes = line.count("'")
        double_quotes = line.count('"')

        return single_quotes % 2 != 0 or double_quotes % 2 != 0

    def _check_keybinding_conflicts(self, lines: List[str]):
        """Check for conflicting key bindings."""
        bind_pattern = re.compile(r'^\s*(bind-key|bind)\s+(-[rnx]+\s+)?(\S+)')

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue

            match = bind_pattern.match(stripped)
            if match:
                key = match.group(3)
                if key in self.keybindings:
                    self.issues.append(ValidationIssue(
                        ValidationLevel.WARNING,
                        i,
                        f"Duplicate key binding '{key}'",
                        line.rstrip(),
                        f"Previously defined at line {self.keybindings[key]}"
                    ))
                else:
                    self.keybindings[key] = i

    def _check_deprecated_options(self, lines: List[str]):
        """Check for deprecated tmux options."""
        deprecated = {
            'mode-mouse': 'mouse',
            'mouse-resize-pane': 'mouse',
            'mouse-select-pane': 'mouse',
            'mouse-select-window': 'mouse',
            'mouse-utf8': None,  # Removed entirely
            'default-command': None,  # Platform specific, often unnecessary
        }

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue

            for old_option, new_option in deprecated.items():
                if old_option in stripped:
                    suggestion = f"Use '{new_option}' instead" if new_option else "This option has been removed"
                    self.issues.append(ValidationIssue(
                        ValidationLevel.WARNING,
                        i,
                        f"Deprecated option '{old_option}'",
                        line.rstrip(),
                        suggestion
                    ))

    def _check_color_values(self, lines: List[str]):
        """Validate color specifications."""
        color_pattern = re.compile(r'(fg|bg|style)=(\S+)')
        valid_colors = {
            'black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white',
            'brightblack', 'brightred', 'brightgreen', 'brightyellow',
            'brightblue', 'brightmagenta', 'brightcyan', 'brightwhite',
            'default', 'terminal'
        }

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue

            matches = color_pattern.findall(stripped)
            for attr, color in matches:
                # Check if it's a valid color name or hex code
                if not (color in valid_colors or
                       color.startswith('colour') or
                       color.startswith('color') or
                       re.match(r'^#[0-9a-fA-F]{6}$', color)):
                    self.issues.append(ValidationIssue(
                        ValidationLevel.WARNING,
                        i,
                        f"Invalid color value '{color}'",
                        line.rstrip(),
                        "Use valid color name, 'colour0-255', or hex code '#RRGGBB'"
                    ))

    def _check_paths(self, lines: List[str]):
        """Check that referenced files exist."""
        source_pattern = re.compile(r'^\s*source(?:-file)?\s+(.+?)(?:\s|$)')

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue

            match = source_pattern.match(stripped)
            if match:
                path_str = match.group(1).strip().strip('"').strip("'")
                # Expand variables
                path_str = os.path.expandvars(path_str)
                path_str = os.path.expanduser(path_str)

                path = Path(path_str)
                if not path.is_absolute():
                    # Relative to config file directory
                    path = self.config_path.parent / path

                if not path.exists():
                    self.issues.append(ValidationIssue(
                        ValidationLevel.ERROR,
                        i,
                        f"Source file not found: {path_str}",
                        line.rstrip(),
                        "Check that the file exists and path is correct"
                    ))

    def _validate_with_tmux(self):
        """Use tmux itself to validate the configuration."""
        try:
            # Test config with tmux
            result = subprocess.run(
                ['tmux', '-f', str(self.config_path), 'start-server', ';', 'kill-server'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode != 0:
                # Parse tmux error output
                error_lines = result.stderr.strip().split('\n')
                for error in error_lines:
                    if error and not error.startswith('server exited'):
                        # Try to extract line number from error
                        line_match = re.search(r'line (\d+):', error)
                        line_num = int(line_match.group(1)) if line_match else 0

                        self.issues.append(ValidationIssue(
                            ValidationLevel.ERROR,
                            line_num,
                            "tmux validation error",
                            "",
                            error
                        ))
        except subprocess.TimeoutExpired:
            self.issues.append(ValidationIssue(
                ValidationLevel.WARNING,
                0,
                "tmux validation timeout",
                "",
                "Config validation took too long, might have blocking commands"
            ))
        except FileNotFoundError:
            self.issues.append(ValidationIssue(
                ValidationLevel.INFO,
                0,
                "tmux not found in PATH",
                "",
                "Install tmux to enable full validation"
            ))
        except Exception as e:
            self.issues.append(ValidationIssue(
                ValidationLevel.WARNING,
                0,
                f"Could not validate with tmux: {e}",
                "",
                "Syntax validation only, runtime validation skipped"
            ))

    def print_report(self):
        """Print validation report."""
        if not self.issues:
            print(f"✅ No issues found in {self.config_path}")
            return

        # Group issues by level
        errors = [i for i in self.issues if i.level == ValidationLevel.ERROR]
        warnings = [i for i in self.issues if i.level == ValidationLevel.WARNING]
        info = [i for i in self.issues if i.level == ValidationLevel.INFO]

        print(f"\n📋 Validation Report for {self.config_path}")
        print("=" * 60)

        if errors:
            print(f"\n❌ {len(errors)} Error(s) found:")
            for issue in errors:
                self._print_issue(issue)

        if warnings:
            print(f"\n⚠️  {len(warnings)} Warning(s) found:")
            for issue in warnings:
                self._print_issue(issue)

        if info:
            print(f"\nℹ️  {len(info)} Info message(s):")
            for issue in info:
                self._print_issue(issue)

        print("\n" + "=" * 60)
        print(f"Summary: {len(errors)} errors, {len(warnings)} warnings, {len(info)} info")

    def _print_issue(self, issue: ValidationIssue):
        """Print a single issue."""
        if issue.line_number > 0:
            print(f"\n  [{issue.level.value}] Line {issue.line_number}: {issue.message}")
        else:
            print(f"\n  [{issue.level.value}] {issue.message}")

        if issue.line_content:
            print(f"    > {issue.line_content}")

        if issue.suggestion:
            print(f"    💡 {issue.suggestion}")

def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Validate tmux configuration')
    parser.add_argument('config', nargs='?', help='Path to tmux config file')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--fix', action='store_true', help='Attempt to fix issues (creates backup)')

    args = parser.parse_args()

    try:
        validator = TmuxConfigValidator(args.config)
        issues = validator.validate()

        if args.json:
            import json
            output = []
            for issue in issues:
                output.append({
                    'level': issue.level.value,
                    'line': issue.line_number,
                    'message': issue.message,
                    'content': issue.line_content,
                    'suggestion': issue.suggestion
                })
            print(json.dumps(output, indent=2))
        else:
            validator.print_report()

        # Exit with error code if errors found
        sys.exit(1 if any(i.level == ValidationLevel.ERROR for i in issues) else 0)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
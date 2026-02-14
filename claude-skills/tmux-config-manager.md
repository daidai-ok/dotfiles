# tmux-config-manager

A Claude skill for managing and validating tmux configuration files.

## Core Responsibilities

1. **Syntax Validation**: Check tmux configuration files for syntax errors
2. **Conflict Detection**: Identify contradictory or conflicting settings
3. **Best Practice Suggestions**: Recommend improvements based on tmux best practices

## Usage

To use this skill, invoke it with one of the following commands:

### Validate Configuration
```
/skill tmux-config-manager validate [config-file-path]
```
Validates the specified tmux configuration file for syntax errors and conflicts.

### Check Conflicts
```
/skill tmux-config-manager check-conflicts
```
Analyzes the configuration for conflicting keybindings or settings.

### Suggest Improvements
```
/skill tmux-config-manager suggest
```
Provides recommendations for improving your tmux configuration.

## Configuration Files

This skill manages the following configuration files:
- `/Users/daisuke.oda/dotfiles/tmux/tmux.conf` (main config)

## Validation Rules

### Syntax Checks
- Valid tmux commands and options
- Correct syntax for key bindings
- Proper quotation and escaping
- Valid color specifications
- Correct option values and types

### Conflict Detection
- Duplicate key bindings
- Conflicting window/pane options
- Incompatible plugin settings
- Circular dependencies in source commands

### Common Issues Detected
- Missing closing quotes or brackets
- Invalid option names
- Deprecated commands or options
- Incorrect path references
- Invalid color codes or names

## Implementation

When invoked, this skill will:

1. Read the specified tmux configuration file
2. Parse the configuration line by line
3. Validate syntax using tmux's built-in checker
4. Identify potential conflicts or issues
5. Provide detailed feedback with line numbers and suggestions

## Error Reporting Format

Errors are reported in the following format:
```
[ERROR] Line <number>: <description>
  > <problematic line>
  Suggestion: <how to fix>
```

## Examples

### Example 1: Syntax Error Detection
```
[ERROR] Line 15: Invalid option 'set-window-opton'
  > set-window-opton -g mode-keys vi
  Suggestion: Change to 'set-window-option'
```

### Example 2: Conflict Detection
```
[WARNING] Line 23: Key binding conflict
  > bind-key -n C-a send-prefix
  Conflicts with line 10: bind-key -n C-a new-window
  Suggestion: Use different key combinations or remove duplicate
```

## Advanced Features

### Auto-fix Mode
```
/skill tmux-config-manager fix
```
Automatically fixes common syntax errors (creates backup first).

### Compatibility Check
```
/skill tmux-config-manager compat [version]
```
Checks configuration compatibility with specific tmux version.

### Plugin Validation
```
/skill tmux-config-manager plugins
```
Validates TPM (Tmux Plugin Manager) plugins and their configurations.

## Best Practices Enforced

1. **Consistent Prefix Key**: Ensure prefix key is set consistently
2. **Color Scheme**: Validate color values are valid
3. **Path Validation**: Check that sourced files exist
4. **Option Scope**: Verify global vs window vs pane options are used correctly
5. **Key Binding Standards**: Check for standard binding conventions

## Integration

This skill integrates with:
- tmux configuration files
- TPM (Tmux Plugin Manager)
- Shell environment variables
- Other dotfile configurations

## Notes

- Always creates backups before making changes
- Respects existing formatting and comments
- Provides non-destructive validation by default
- Can be extended with custom validation rules
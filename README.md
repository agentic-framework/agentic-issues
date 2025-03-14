# agentic-issues

A system for managing issues and tickets for Agentic projects

## Overview

The Agentic Issues system provides a simple, git-style command-line interface for managing issues and tickets within Agentic projects. It allows users to submit, track, and update issues directly from the command line using the familiar `ag` command.

## Features

- Submit issues with title, description, priority, and labels
- List issues with filtering and sorting options
- View detailed issue information
- Add comments to issues
- Update issue status, priority, and assignee
- Project-specific issue tracking

## Installation

To install the Agentic Issues system, follow these steps:

1. Clone the repository:
   ```bash
   cd ~/Agentic/projects
   git clone https://github.com/username/agentic-issues.git
   ```

2. Install the package in development mode:
   ```bash
   cd agentic-issues
   source .venv/bin/activate
   uv pip install -e .
   ```

3. Link the command to the Agentic framework:
   ```bash
   # This step will be implemented in the future
   # For now, you can use the command directly from the package
   ```

## Usage

### Submitting an Issue

To submit a new issue:

```bash
ag issues submit --title "Issue title" --description "Detailed description" --priority high --labels "bug,ui"
```

If you don't provide a description, you'll be prompted to enter one interactively.

### Listing Issues

To list all issues for the current project:

```bash
ag issues list
```

You can filter and sort the issues:

```bash
# Filter by status
ag issues list --status open

# Filter by priority
ag issues list --priority high

# Filter by label
ag issues list --label bug

# Sort by creation date (newest first)
ag issues list --sort created

# Show detailed information
ag issues list --detailed
```

### Viewing an Issue

To view the details of a specific issue:

```bash
ag issues show <issue-id>
```

### Adding a Comment

To add a comment to an issue:

```bash
ag issues comment <issue-id> --content "Your comment here"
```

If you don't provide content, you'll be prompted to enter it interactively.

### Updating an Issue

To update an issue:

```bash
# Update status
ag issues update <issue-id> --status in_progress

# Update priority
ag issues update <issue-id> --priority critical

# Assign to a user
ag issues update <issue-id> --assignee username

# Add a label
ag issues update <issue-id> --add-label documentation
```

## License

See the [LICENSE](LICENSE) file for details.

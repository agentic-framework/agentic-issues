# Agentic Issues - User Manual

This manual provides comprehensive instructions for using the Agentic Issues system.

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Basic Concepts](#basic-concepts)
4. [Command Reference](#command-reference)
5. [Workflows](#workflows)
6. [Tips and Tricks](#tips-and-tricks)
7. [Troubleshooting](#troubleshooting)

## Introduction

Agentic Issues is a command-line issue tracking system designed specifically for the Agentic framework. It provides a simple, git-style interface for managing issues and tickets within Agentic projects.

### Key Features

- Submit issues with title, description, priority, and labels
- List issues with filtering and sorting options
- View detailed issue information
- Add comments to issues
- Update issue status, priority, and assignee
- Project-specific issue tracking

## Installation

### Prerequisites

- Agentic framework installed
- Python 3.8 or higher
- uv package manager (recommended) or pip

### Installation Steps

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

3. Run the installation script to integrate with the Agentic framework:
   ```bash
   python scripts/install_ag_issues.py
   ```

### Verifying Installation

To verify that the installation was successful, run:

```bash
ag issues list
```

If the command runs without errors, the installation was successful.

## Basic Concepts

### Issues

An issue represents a task, bug, feature request, or any other item that needs to be tracked. Each issue has:

- A unique identifier
- A title and description
- A status (open, in_progress, resolved, closed)
- A priority (low, medium, high, critical)
- An author (the user who created the issue)
- An optional assignee (the user responsible for the issue)
- Creation and update timestamps
- Optional labels for categorization
- Optional comments

### Projects

Issues are organized by project. Each project has its own set of issues. The current project is determined by:

1. The `--project` option if specified
2. The current directory if it's an Agentic project
3. A default project if neither of the above applies

### Storage

Issues are stored in JSON files in the Agentic shared directory:

```
~/Agentic/shared/agentic-issues/issues/
```

Each project has its own JSON file containing all issues for that project.

## Command Reference

### Global Options

These options can be used with any command:

- `--project PROJECT`: Specify the project ID (default: current project)
- `--help`: Show help message and exit

### Submit Command

Submit a new issue:

```bash
ag issues submit [options]
```

Options:
- `--title TITLE`: Issue title (required)
- `--description DESC`: Issue description
- `--priority PRIORITY`: Issue priority (low, medium, high, critical)
- `--labels LABELS`: Comma-separated list of labels

If you don't provide a description, you'll be prompted to enter one interactively.

Example:
```bash
ag issues submit --title "Fix login button" --description "The login button doesn't work in Safari" --priority high --labels "bug,ui"
```

### List Command

List issues for the current project:

```bash
ag issues list [options]
```

Options:
- `--status STATUS`: Filter by status (open, in_progress, resolved, closed)
- `--priority PRIORITY`: Filter by priority (low, medium, high, critical)
- `--label LABEL`: Filter by label
- `--sort SORT`: Sort by field (created, updated, priority, status)
- `--detailed`: Show detailed information

Examples:
```bash
# List all open issues
ag issues list --status open

# List high priority issues
ag issues list --priority high

# List issues with the "bug" label
ag issues list --label bug

# List issues sorted by creation date
ag issues list --sort created

# List issues with detailed information
ag issues list --detailed
```

### Show Command

Show details of a specific issue:

```bash
ag issues show ISSUE_ID [options]
```

Example:
```bash
ag issues show f817a888-f1a0-4c61-b319-5d397019154d
```

### Comment Command

Add a comment to an issue:

```bash
ag issues comment ISSUE_ID [options]
```

Options:
- `--content CONTENT`: Comment content

If you don't provide content, you'll be prompted to enter it interactively.

Example:
```bash
ag issues comment f817a888-f1a0-4c61-b319-5d397019154d --content "I've started working on this issue."
```

### Update Command

Update an issue:

```bash
ag issues update ISSUE_ID [options]
```

Options:
- `--status STATUS`: Update status (open, in_progress, resolved, closed)
- `--priority PRIORITY`: Update priority (low, medium, high, critical)
- `--assignee ASSIGNEE`: Assign to a user
- `--add-label LABEL`: Add a label
- `--remove-label LABEL`: Remove a label

Examples:
```bash
# Update status
ag issues update f817a888-f1a0-4c61-b319-5d397019154d --status in_progress

# Update priority
ag issues update f817a888-f1a0-4c61-b319-5d397019154d --priority critical

# Assign to a user
ag issues update f817a888-f1a0-4c61-b319-5d397019154d --assignee username

# Add a label
ag issues update f817a888-f1a0-4c61-b319-5d397019154d --add-label documentation

# Remove a label
ag issues update f817a888-f1a0-4c61-b319-5d397019154d --remove-label bug
```

## Workflows

### Basic Issue Tracking Workflow

1. **Create an issue**:
   ```bash
   ag issues submit --title "Implement feature X" --priority medium
   ```

2. **Start working on the issue**:
   ```bash
   ag issues update ISSUE_ID --status in_progress --assignee your-username
   ```

3. **Add progress updates**:
   ```bash
   ag issues comment ISSUE_ID --content "Implemented the core functionality, still need to add tests."
   ```

4. **Complete the issue**:
   ```bash
   ag issues update ISSUE_ID --status resolved
   ```

5. **Close the issue**:
   ```bash
   ag issues update ISSUE_ID --status closed
   ```

### Bug Tracking Workflow

1. **Report a bug**:
   ```bash
   ag issues submit --title "Bug: Application crashes on startup" --priority high --labels "bug,crash"
   ```

2. **Assign the bug**:
   ```bash
   ag issues update ISSUE_ID --assignee developer-username
   ```

3. **Document investigation**:
   ```bash
   ag issues comment ISSUE_ID --content "Investigated the crash. It appears to be related to the configuration file."
   ```

4. **Fix the bug**:
   ```bash
   ag issues update ISSUE_ID --status in_progress
   ag issues comment ISSUE_ID --content "Fixed the bug by correcting the configuration file parsing."
   ag issues update ISSUE_ID --status resolved
   ```

5. **Verify the fix**:
   ```bash
   ag issues comment ISSUE_ID --content "Verified that the fix works in all test environments."
   ag issues update ISSUE_ID --status closed
   ```

### Project Management Workflow

1. **Create project tasks**:
   ```bash
   ag issues submit --title "Task 1: Design database schema" --priority medium --labels "task,design"
   ag issues submit --title "Task 2: Implement API endpoints" --priority medium --labels "task,implementation"
   ag issues submit --title "Task 3: Create user interface" --priority medium --labels "task,ui"
   ```

2. **Assign tasks to team members**:
   ```bash
   ag issues update TASK1_ID --assignee developer1
   ag issues update TASK2_ID --assignee developer2
   ag issues update TASK3_ID --assignee developer3
   ```

3. **Track progress**:
   ```bash
   ag issues list --label task --detailed
   ```

4. **Update task status**:
   ```bash
   ag issues update TASK1_ID --status in_progress
   ag issues update TASK1_ID --status resolved
   ```

## Tips and Tricks

### Using Short IDs

You can use just the first few characters of an issue ID as long as they uniquely identify the issue:

```bash
ag issues show f817a8
```

### Combining Filters

You can combine multiple filters when listing issues:

```bash
ag issues list --status open --priority high --label bug
```

### Interactive Mode

If you don't provide required options, the system will prompt you for them interactively:

```bash
ag issues submit
# You'll be prompted for title, description, etc.
```

### Scripting

You can use the Agentic Issues system in scripts:

```bash
#!/bin/bash
# Create an issue and capture its ID
ISSUE_ID=$(ag issues submit --title "Automated issue" --description "Created by script" --quiet)
# Update the issue
ag issues update $ISSUE_ID --status in_progress
```

## Troubleshooting

### Common Issues

#### Command Not Found

If you get a "command not found" error when running `ag issues`, make sure:

1. The Agentic framework is installed correctly
2. The Agentic Issues package is installed correctly
3. The installation script was run successfully

Try reinstalling the package:

```bash
cd ~/Agentic/projects/agentic-issues
source .venv/bin/activate
uv pip install -e .
python scripts/install_ag_issues.py
```

#### Issue Not Found

If you get an "issue not found" error, make sure:

1. You're using the correct issue ID
2. You're in the correct project or using the `--project` option
3. The issue exists in the specified project

#### Permission Denied

If you get a "permission denied" error when accessing issue files, make sure:

1. You have the correct permissions for the Agentic shared directory
2. The issue files are not locked by another process

### Getting Help

If you encounter problems not covered in this manual, you can:

1. Check the logs in `~/Agentic/logs/`
2. Run commands with the `--debug` option for more detailed output
3. Submit an issue to the Agentic Issues repository

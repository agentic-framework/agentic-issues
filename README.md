# Agentic Issues

Issue tracking plugin for the Agentic framework.

## Overview

The Agentic Issues plugin provides a simple command-line interface for tracking issues within the Agentic framework. It allows users to create, list, show, update, and close issues directly from the command line using the familiar `ag` command.

## Features

- Create issues with title and description
- List issues with filtering by status, priority, and labels
- View detailed issue information
- Add comments to issues with author information and timestamps
- Update issue status, priority, and assignee
- Add labels to issues
- Close issues

## Installation

To install the Agentic Issues system, follow these steps:

1. Clone the repository:
   ```bash
   cd ~/Agentic/projects
   git clone https://github.com/agentic-framework/agentic-issues.git
   ```

2. Install the package in development mode:
   ```bash
   cd agentic-issues
   source .venv/bin/activate
   uv pip install -e .
   ```

3. Link the command to the Agentic framework:
   ```bash
   # The ag-wrapper.sh script in the Agentic framework provides a convenient way to run the ag command
   # You can use it directly without activating the virtual environment:
   /Users/mingli/Agentic/agentic/ag-wrapper.sh issues list
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

This functionality is fully implemented and allows you to add comments to issues with author information and timestamps. Comments are displayed when viewing the issue details.

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

## Recent Improvements

### Comment Functionality

The comment functionality has been fully implemented, allowing users to:
- Add comments to issues with the `ag issues comment` command
- View comments when displaying issue details with `ag issues show`
- Each comment includes author information and timestamps

### Future Improvements

Based on our experience implementing the comment functionality, we've identified several areas for future improvement:

1. **Unit Tests**: Add comprehensive unit tests for better code quality and confidence
2. **Error Handling**: Improve error handling for robustness
3. **Input Validation**: Add more robust input validation for data integrity
4. **Plugin System**: Implement a plugin system for better code organization
5. **Documentation**: Add comprehensive documentation for classes and functions
6. **Content-File Parameter**: Implement a --content-file parameter for comments to handle longer content
7. **Markdown Support**: Add Markdown support for better formatting
8. **Web Interface**: Consider implementing a web interface for improved usability

## Development

### Git Repository

The Agentic Issues system is maintained in a Git repository. To contribute to the project:

1. Clone the repository:
   ```bash
   git clone https://github.com/agentic-framework/agentic-issues.git
   ```

2. Create a branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. Make your changes and commit them:
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

4. Push your changes to the remote repository:
   ```bash
   git push origin feature/your-feature-name
   ```

5. Create a pull request to merge your changes into the main branch.

## License

See the [LICENSE](LICENSE) file for details.

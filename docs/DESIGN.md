# Agentic Issues - Design Document

This document outlines the technical design and architecture of the Agentic Issues system.

## System Architecture

The Agentic Issues system follows a simple, modular architecture with the following components:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  CLI Interface  │────▶│  Core Business  │────▶│  Storage Layer  │
│                 │     │     Logic       │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                                               │
        │                                               │
        ▼                                               ▼
┌─────────────────┐                           ┌─────────────────┐
│                 │                           │                 │
│  Agentic CLI    │                           │  JSON Files     │
│  Integration    │                           │                 │
└─────────────────┘                           └─────────────────┘
```

### Components

1. **CLI Interface** (`cli.py`):
   - Parses command-line arguments
   - Dispatches to appropriate handlers
   - Formats and displays output

2. **Core Business Logic** (`models.py`):
   - Defines data models (Issue, Comment)
   - Implements business rules and validations
   - Provides methods for manipulating issues

3. **Storage Layer** (`storage.py`):
   - Handles persistence of issues and comments
   - Serializes and deserializes data
   - Manages file operations

4. **Agentic CLI Integration** (`ag_issues.py`):
   - Provides integration with the Agentic framework
   - Handles command routing from the `ag` command

### Data Flow

1. User issues a command via the Agentic CLI (`ag issues ...`)
2. The command is routed to the Agentic Issues system
3. The CLI interface parses the command and dispatches to the appropriate handler
4. The handler uses the core business logic to perform the requested operation
5. The storage layer is used to persist any changes
6. Results are formatted and displayed to the user

## Data Model

### Issue

The core data model is the `Issue` class, which represents an issue or ticket:

```python
@dataclasses.dataclass
class Issue:
    id: str                           # Unique identifier
    project_id: str                   # Project the issue belongs to
    title: str                        # Issue title
    description: str                  # Detailed description
    status: IssueStatus               # Current status (open, in_progress, etc.)
    priority: IssuePriority           # Priority level (low, medium, high, critical)
    author: str                       # User who created the issue
    assignee: Optional[str]           # User assigned to the issue (if any)
    created_at: datetime.datetime     # Creation timestamp
    updated_at: Optional[datetime.datetime]  # Last update timestamp
    comments: List[IssueComment]      # Comments on the issue
    labels: List[str]                 # Labels/tags for categorization
```

### Comment

Comments are represented by the `IssueComment` class:

```python
@dataclasses.dataclass
class IssueComment:
    id: str                           # Unique identifier
    issue_id: str                     # Issue this comment belongs to
    author: str                       # User who wrote the comment
    content: str                      # Comment text
    created_at: datetime.datetime     # Creation timestamp
    updated_at: Optional[datetime.datetime]  # Last update timestamp
```

### Status and Priority

Status and priority are represented as enums:

```python
class IssueStatus(enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

class IssuePriority(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
```

## Storage Design

The storage system uses JSON files to persist issues and comments. Each project has its own JSON file containing all issues for that project.

### File Structure

```
~/Agentic/shared/agentic-issues/
└── issues/
    ├── project-1.json
    ├── project-2.json
    └── ...
```

### JSON Format

Each project file contains an array of issue objects:

```json
[
  {
    "id": "issue-id-1",
    "project_id": "project-1",
    "title": "Issue Title",
    "description": "Issue Description",
    "status": "open",
    "priority": "medium",
    "author": "username",
    "assignee": null,
    "created_at": "2025-03-14T10:00:00.000000",
    "updated_at": null,
    "comments": [
      {
        "id": "comment-id-1",
        "issue_id": "issue-id-1",
        "author": "username",
        "content": "Comment text",
        "created_at": "2025-03-14T10:05:00.000000",
        "updated_at": null
      }
    ],
    "labels": ["bug", "ui"]
  }
]
```

## Design Decisions

### Why JSON Files?

1. **Simplicity**: JSON files are easy to work with and don't require a database server.
2. **Human-readable**: The files can be viewed and edited directly if needed.
3. **Portability**: The system can be easily moved or backed up.
4. **Low overhead**: Minimal dependencies and setup requirements.

For the initial implementation, JSON files provide a good balance of simplicity and functionality. As the system grows, it could be migrated to a database if needed.

### Project-Based Organization

Issues are organized by project, with each project having its own file. This approach:

1. Keeps files to a manageable size
2. Allows for efficient querying of issues for a specific project
3. Aligns with the Agentic framework's project-centric approach

### Command-Line Interface

The system uses a command-line interface to:

1. Integrate seamlessly with the Agentic framework
2. Provide a familiar git-style interface
3. Enable scripting and automation
4. Minimize dependencies

### Extensibility

The modular design allows for easy extension:

1. New commands can be added to the CLI interface
2. Additional data fields can be added to the models
3. The storage layer can be replaced with a different implementation
4. New features can be added without disrupting existing functionality

## Security Considerations

1. **File permissions**: The JSON files are stored in the Agentic shared directory, which has appropriate permissions.
2. **Input validation**: All user input is validated before being processed.
3. **No authentication**: The system relies on the operating system's authentication and does not implement its own.

## Performance Considerations

1. **File size**: As projects grow, the JSON files could become large. The system is designed to handle this by:
   - Loading only the issues for the current project
   - Implementing efficient search and filtering

2. **Concurrency**: The current implementation does not handle concurrent access to the same file. This could be addressed in future versions.

## Future Enhancements

1. **Database storage**: Replace JSON files with a database for improved performance and concurrency.
2. **Web interface**: Add a web-based UI for easier interaction.
3. **Authentication and authorization**: Add user management and access control.
4. **Notifications**: Add email or other notifications for issue updates.
5. **Integration with external systems**: Add support for syncing with GitHub Issues, Jira, etc.

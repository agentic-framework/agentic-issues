"""
Command-line interface for the Agentic Issues system.

This module provides the CLI interface for the `ag issues` command.
"""

import argparse
import datetime
import getpass
import os
import sys
from typing import List, Optional

from agentic_issues.models import Issue, IssuePriority, IssueStatus
from agentic_issues.storage import default_storage


def get_current_project_id() -> Optional[str]:
    """
    Get the ID of the current project.
    
    This function attempts to determine the current project by looking at the
    current working directory. If the current directory is within a project
    directory, it returns the project ID.
    """
    cwd = os.getcwd()
    projects_dir = os.path.expanduser("~/Agentic/projects")
    
    # Check if we're in a project directory
    if cwd.startswith(projects_dir):
        # Extract the project name from the path
        rel_path = os.path.relpath(cwd, projects_dir)
        project_name = rel_path.split(os.path.sep)[0]
        return project_name
    
    # If we're not in a project directory, return None
    return None


def get_current_user() -> str:
    """Get the current user's username."""
    return getpass.getuser()


def format_issue(issue: Issue, detailed: bool = False) -> str:
    """Format an issue for display."""
    status_colors = {
        IssueStatus.OPEN: "\033[92m",  # Green
        IssueStatus.IN_PROGRESS: "\033[93m",  # Yellow
        IssueStatus.RESOLVED: "\033[94m",  # Blue
        IssueStatus.CLOSED: "\033[90m",  # Gray
    }
    
    priority_markers = {
        IssuePriority.LOW: "⬇️",
        IssuePriority.MEDIUM: "⏺️",
        IssuePriority.HIGH: "⬆️",
        IssuePriority.CRITICAL: "🔴",
    }
    
    reset = "\033[0m"
    status_color = status_colors.get(issue.status, "")
    priority_marker = priority_markers.get(issue.priority, "")
    
    # Basic format: ID, status, priority, title
    result = f"{issue.id[:8]} {status_color}{issue.status.value}{reset} {priority_marker} {issue.title}"
    
    if detailed:
        # Add more details for detailed view
        result += f"\n\nDescription:\n{issue.description}\n"
        result += f"\nAuthor: {issue.author}"
        if issue.assignee:
            result += f" | Assignee: {issue.assignee}"
        result += f" | Created: {issue.created_at.strftime('%Y-%m-%d %H:%M')}"
        if issue.updated_at:
            result += f" | Updated: {issue.updated_at.strftime('%Y-%m-%d %H:%M')}"
        
        if issue.labels:
            result += f"\nLabels: {', '.join(issue.labels)}"
        
        if issue.comments:
            result += "\n\nComments:\n"
            for i, comment in enumerate(issue.comments, 1):
                result += f"\n{i}. {comment.author} ({comment.created_at.strftime('%Y-%m-%d %H:%M')}):\n"
                result += f"   {comment.content}\n"
    
    return result


def cmd_submit(args: argparse.Namespace) -> int:
    """Submit a new issue."""
    project_id = args.project or get_current_project_id()
    if not project_id:
        print("Error: Could not determine project ID. Please specify with --project.")
        return 1
    
    # Get issue details
    title = args.title
    if not title:
        print("Error: Title is required.")
        return 1
    
    description = args.description
    if not description:
        # If no description is provided, prompt for one
        print("Please enter a description (press Ctrl+D or Ctrl+Z on a new line to finish):")
        description_lines = []
        try:
            while True:
                line = input()
                description_lines.append(line)
        except EOFError:
            description = "\n".join(description_lines)
    
    # Parse priority
    priority = IssuePriority.MEDIUM
    if args.priority:
        try:
            priority = IssuePriority(args.priority.lower())
        except ValueError:
            print(f"Warning: Invalid priority '{args.priority}'. Using MEDIUM instead.")
    
    # Parse labels
    labels = []
    if args.labels:
        labels = [label.strip() for label in args.labels.split(",")]
    
    # Create the issue
    author = get_current_user()
    issue = Issue.create(
        project_id=project_id,
        title=title,
        description=description,
        author=author,
        priority=priority,
        labels=labels,
    )
    
    # Save the issue
    default_storage.save_issue(issue)
    
    print(f"Issue submitted successfully with ID: {issue.id}")
    print(format_issue(issue, detailed=True))
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    """List issues."""
    project_id = args.project or get_current_project_id()
    if not project_id:
        print("Error: Could not determine project ID. Please specify with --project.")
        return 1
    
    # Get issues for the project
    issues = default_storage.get_issues(project_id)
    
    # Filter by status if specified
    if args.status:
        try:
            status = IssueStatus(args.status.lower())
            issues = [i for i in issues if i.status == status]
        except ValueError:
            print(f"Warning: Invalid status '{args.status}'. Showing all issues.")
    
    # Filter by priority if specified
    if args.priority:
        try:
            priority = IssuePriority(args.priority.lower())
            issues = [i for i in issues if i.priority == priority]
        except ValueError:
            print(f"Warning: Invalid priority '{args.priority}'. Showing all issues.")
    
    # Filter by label if specified
    if args.label:
        issues = [i for i in issues if args.label in i.labels]
    
    # Sort issues
    if args.sort == "priority":
        # Sort by priority (highest first)
        priority_order = {
            IssuePriority.CRITICAL: 0,
            IssuePriority.HIGH: 1,
            IssuePriority.MEDIUM: 2,
            IssuePriority.LOW: 3,
        }
        issues.sort(key=lambda i: priority_order.get(i.priority, 4))
    elif args.sort == "created":
        # Sort by creation date (newest first)
        issues.sort(key=lambda i: i.created_at, reverse=True)
    elif args.sort == "updated":
        # Sort by update date (newest first), with None values last
        issues.sort(key=lambda i: (i.updated_at is None, i.updated_at or datetime.datetime.min), reverse=True)
    
    # Display issues
    if not issues:
        print(f"No issues found for project '{project_id}'.")
        return 0
    
    print(f"Issues for project '{project_id}':")
    for i, issue in enumerate(issues, 1):
        print(f"\n{i}. {format_issue(issue, detailed=args.detailed)}")
    
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    """Show details of a specific issue."""
    project_id = args.project or get_current_project_id()
    if not project_id:
        print("Error: Could not determine project ID. Please specify with --project.")
        return 1
    
    issue_id = args.issue_id
    if not issue_id:
        print("Error: Issue ID is required.")
        return 1
    
    # Get the issue
    issue = default_storage.get_issue(project_id, issue_id)
    if not issue:
        print(f"Error: Issue '{issue_id}' not found in project '{project_id}'.")
        return 1
    
    # Display the issue
    print(format_issue(issue, detailed=True))
    return 0


def cmd_comment(args: argparse.Namespace) -> int:
    """Add a comment to an issue."""
    project_id = args.project or get_current_project_id()
    if not project_id:
        print("Error: Could not determine project ID. Please specify with --project.")
        return 1
    
    issue_id = args.issue_id
    if not issue_id:
        print("Error: Issue ID is required.")
        return 1
    
    # Get the issue
    issue = default_storage.get_issue(project_id, issue_id)
    if not issue:
        print(f"Error: Issue '{issue_id}' not found in project '{project_id}'.")
        return 1
    
    # Get comment content
    content = args.content
    if not content:
        # If no content is provided, prompt for it
        print("Please enter your comment (press Ctrl+D or Ctrl+Z on a new line to finish):")
        content_lines = []
        try:
            while True:
                line = input()
                content_lines.append(line)
        except EOFError:
            content = "\n".join(content_lines)
    
    # Add the comment
    author = get_current_user()
    issue.add_comment(author, content)
    
    # Save the issue
    default_storage.save_issue(issue)
    
    print(f"Comment added to issue {issue_id}.")
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    """Update an issue."""
    project_id = args.project or get_current_project_id()
    if not project_id:
        print("Error: Could not determine project ID. Please specify with --project.")
        return 1
    
    issue_id = args.issue_id
    if not issue_id:
        print("Error: Issue ID is required.")
        return 1
    
    # Get the issue
    issue = default_storage.get_issue(project_id, issue_id)
    if not issue:
        print(f"Error: Issue '{issue_id}' not found in project '{project_id}'.")
        return 1
    
    # Update status if specified
    if args.status:
        try:
            status = IssueStatus(args.status.lower())
            issue.update_status(status)
            print(f"Status updated to {status.value}.")
        except ValueError:
            print(f"Warning: Invalid status '{args.status}'. Status not updated.")
    
    # Update priority if specified
    if args.priority:
        try:
            priority = IssuePriority(args.priority.lower())
            issue.update_priority(priority)
            print(f"Priority updated to {priority.value}.")
        except ValueError:
            print(f"Warning: Invalid priority '{args.priority}'. Priority not updated.")
    
    # Update assignee if specified
    if args.assignee:
        issue.assign(args.assignee)
        print(f"Assignee updated to {args.assignee}.")
    
    # Add label if specified
    if args.add_label:
        issue.add_label(args.add_label)
        print(f"Label '{args.add_label}' added.")
    
    # Save the issue
    default_storage.save_issue(issue)
    
    print(f"Issue {issue_id} updated successfully.")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="Agentic Issues - Issue tracking for Agentic projects")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Submit command
    submit_parser = subparsers.add_parser("submit", help="Submit a new issue")
    submit_parser.add_argument("--project", help="Project ID (defaults to current directory)")
    submit_parser.add_argument("--title", help="Issue title")
    submit_parser.add_argument("--description", help="Issue description")
    submit_parser.add_argument("--priority", help="Issue priority (low, medium, high, critical)")
    submit_parser.add_argument("--labels", help="Comma-separated list of labels")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List issues")
    list_parser.add_argument("--project", help="Project ID (defaults to current directory)")
    list_parser.add_argument("--status", help="Filter by status (open, in_progress, resolved, closed)")
    list_parser.add_argument("--priority", help="Filter by priority (low, medium, high, critical)")
    list_parser.add_argument("--label", help="Filter by label")
    list_parser.add_argument("--sort", choices=["priority", "created", "updated"], default="priority",
                            help="Sort order (default: priority)")
    list_parser.add_argument("--detailed", action="store_true", help="Show detailed information")
    
    # Show command
    show_parser = subparsers.add_parser("show", help="Show issue details")
    show_parser.add_argument("issue_id", help="Issue ID")
    show_parser.add_argument("--project", help="Project ID (defaults to current directory)")
    
    # Comment command
    comment_parser = subparsers.add_parser("comment", help="Add a comment to an issue")
    comment_parser.add_argument("issue_id", help="Issue ID")
    comment_parser.add_argument("--project", help="Project ID (defaults to current directory)")
    comment_parser.add_argument("--content", help="Comment content")
    
    # Update command
    update_parser = subparsers.add_parser("update", help="Update an issue")
    update_parser.add_argument("issue_id", help="Issue ID")
    update_parser.add_argument("--project", help="Project ID (defaults to current directory)")
    update_parser.add_argument("--status", help="New status (open, in_progress, resolved, closed)")
    update_parser.add_argument("--priority", help="New priority (low, medium, high, critical)")
    update_parser.add_argument("--assignee", help="Assign to user")
    update_parser.add_argument("--add-label", help="Add a label")
    
    args = parser.parse_args(argv)
    
    if args.command == "submit":
        return cmd_submit(args)
    elif args.command == "list":
        return cmd_list(args)
    elif args.command == "show":
        return cmd_show(args)
    elif args.command == "comment":
        return cmd_comment(args)
    elif args.command == "update":
        return cmd_update(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())

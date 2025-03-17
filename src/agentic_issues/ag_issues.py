#!/usr/bin/env python3
"""
Entry point for the `ag issue` command.

This script is installed as a command in the Agentic framework to handle
the `ag issue` subcommand.
"""

import sys
import os
import argparse
import datetime
from pathlib import Path

from .storage import default_storage
from .models import Issue, IssueStatus, IssuePriority

def get_project_id(args):
    """Get the project ID from the arguments or the current directory."""
    if args.project:
        return args.project
    
    # Default to the current directory name
    return Path.cwd().name

def format_issue_list(issues, detailed=False):
    """Format a list of issues for display."""
    if not issues:
        return "No issues found."
    
    result = []
    for issue in issues:
        if detailed:
            result.append(f"ID: {issue.id}")
            result.append(f"Title: {issue.title}")
            result.append(f"Status: {issue.status.value}")
            result.append(f"Priority: {issue.priority.value}")
            result.append(f"Created: {issue.created_at.strftime('%Y-%m-%d %H:%M')}")
            if issue.updated_at:
                result.append(f"Updated: {issue.updated_at.strftime('%Y-%m-%d %H:%M')}")
            else:
                result.append("Updated: Not updated yet")
            if issue.assignee:
                result.append(f"Assignee: {issue.assignee}")
            if issue.labels:
                result.append(f"Labels: {', '.join(issue.labels)}")
            result.append("")
        else:
            priority_marker = {
                IssuePriority.LOW: "⚪",
                IssuePriority.MEDIUM: "🔵",
                IssuePriority.HIGH: "🔶",
                IssuePriority.CRITICAL: "🔴"
            }.get(issue.priority, "⚪")
            
            status_marker = {
                IssueStatus.OPEN: "🆕",
                IssueStatus.IN_PROGRESS: "🔄",
                IssueStatus.RESOLVED: "✅",
                IssueStatus.CLOSED: "❌"
            }.get(issue.status, "🆕")
            
            result.append(f"{priority_marker} {status_marker} {issue.id}: {issue.title}")
    
    return "\n".join(result)

def format_issue_detail(issue):
    """Format a single issue for detailed display."""
    result = [
        f"ID: {issue.id}",
        f"Title: {issue.title}",
        f"Status: {issue.status.value}",
        f"Priority: {issue.priority.value}",
        f"Created: {issue.created_at.strftime('%Y-%m-%d %H:%M')}"
    ]
    
    if issue.updated_at:
        result.append(f"Updated: {issue.updated_at.strftime('%Y-%m-%d %H:%M')}")
    else:
        result.append("Updated: Not updated yet")
    
    if issue.assignee:
        result.append(f"Assignee: {issue.assignee}")
    
    if issue.labels:
        result.append(f"Labels: {', '.join(issue.labels)}")
    
    result.append("")
    result.append("Description:")
    result.append(issue.description)
    
    if issue.comments:
        result.append("")
        result.append("Comments:")
        for comment in issue.comments:
            result.append(f"--- {comment.created_at.strftime('%Y-%m-%d %H:%M')} by {comment.author} ---")
            result.append(comment.content)
            result.append("")
    
    return "\n".join(result)

def issue_command(args=None):
    """
    Handle the `ag issue` command.
    
    This function is called by the Agentic framework's `ag` script when
    the user runs `ag issue`.
    
    Args:
        args: Command-line arguments passed to the `ag issue` command.
    
    Returns:
        int: Exit code.
    """
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
    
    parsed_args = parser.parse_args(args)
    
    if parsed_args.command is None:
        parser.print_help()
        return 1
    
    # Handle the list command
    if parsed_args.command == "list":
        project_id = get_project_id(parsed_args)
        issues = default_storage.get_issues(project_id)
        
        # Apply filters
        if parsed_args.status:
            try:
                status = IssueStatus(parsed_args.status)
                issues = [i for i in issues if i.status == status]
            except ValueError:
                print(f"Invalid status: {parsed_args.status}")
                return 1
        
        if parsed_args.priority:
            try:
                priority = IssuePriority(parsed_args.priority)
                issues = [i for i in issues if i.priority == priority]
            except ValueError:
                print(f"Invalid priority: {parsed_args.priority}")
                return 1
        
        if parsed_args.label:
            issues = [i for i in issues if parsed_args.label in (i.labels or [])]
        
        # Sort issues
        if parsed_args.sort == "priority":
            # Sort by priority (critical -> high -> medium -> low)
            issues.sort(key=lambda i: i.priority.value, reverse=True)
        elif parsed_args.sort == "created":
            issues.sort(key=lambda i: i.created_at, reverse=True)
        elif parsed_args.sort == "updated":
            issues.sort(key=lambda i: i.updated_at, reverse=True)
        
        print(format_issue_list(issues, parsed_args.detailed))
        return 0
    
    # Handle the show command
    elif parsed_args.command == "show":
        project_id = get_project_id(parsed_args)
        issue = default_storage.get_issue(project_id, parsed_args.issue_id)
        
        if issue:
            print(format_issue_detail(issue))
            return 0
        else:
            print(f"Issue {parsed_args.issue_id} not found in project {project_id}")
            return 1
    
    # Handle the submit command
    elif parsed_args.command == "submit":
        project_id = get_project_id(parsed_args)
        
        if not parsed_args.title:
            print("Error: Title is required")
            return 1
        
        description = parsed_args.description or "No description provided"
        
        # Parse priority
        try:
            priority = IssuePriority.MEDIUM  # Default priority
            if parsed_args.priority:
                priority = IssuePriority(parsed_args.priority)
        except ValueError:
            print(f"Invalid priority: {parsed_args.priority}")
            print(f"Valid priorities are: {', '.join(p.value for p in IssuePriority)}")
            return 1
        
        # Parse labels
        labels = []
        if parsed_args.labels:
            labels = [label.strip() for label in parsed_args.labels.split(",") if label.strip()]
        
        # Create the issue
        issue = Issue.create(
            project_id=project_id,
            title=parsed_args.title,
            description=description,
            author=os.environ.get("USER", "unknown"),
            priority=priority,
            labels=labels
        )
        
        # Save the issue
        default_storage.save_issue(issue)
        
        print(f"Issue created with ID: {issue.id}")
        return 0
    
    # Handle the update command
    elif parsed_args.command == "update":
        project_id = get_project_id(parsed_args)
        issue = default_storage.get_issue(project_id, parsed_args.issue_id)
        
        if not issue:
            print(f"Issue {parsed_args.issue_id} not found in project {project_id}")
            return 1
        
        # Update status if specified
        if parsed_args.status:
            try:
                status = IssueStatus(parsed_args.status)
                issue.update_status(status)
                print(f"Status updated to {status.value}")
            except ValueError:
                print(f"Invalid status: {parsed_args.status}")
                print(f"Valid statuses are: {', '.join(s.value for s in IssueStatus)}")
                return 1
        
        # Update priority if specified
        if parsed_args.priority:
            try:
                priority = IssuePriority(parsed_args.priority)
                issue.update_priority(priority)
                print(f"Priority updated to {priority.value}")
            except ValueError:
                print(f"Invalid priority: {parsed_args.priority}")
                print(f"Valid priorities are: {', '.join(p.value for p in IssuePriority)}")
                return 1
        
        # Update assignee if specified
        if parsed_args.assignee:
            issue.assign(parsed_args.assignee)
            print(f"Assignee updated to {parsed_args.assignee}")
        
        # Add label if specified
        if parsed_args.add_label:
            issue.add_label(parsed_args.add_label)
            print(f"Label '{parsed_args.add_label}' added")
        
        # Save the updated issue
        default_storage.save_issue(issue)
        
        print(f"Issue {parsed_args.issue_id} updated successfully")
        return 0
    
    # Handle the comment command
    elif parsed_args.command == "comment":
        project_id = get_project_id(parsed_args)
        issue = default_storage.get_issue(project_id, parsed_args.issue_id)
        
        if not issue:
            print(f"Issue {parsed_args.issue_id} not found in project {project_id}")
            return 1
        
        if not parsed_args.content:
            print("Error: Comment content is required")
            return 1
        
        # Add the comment to the issue
        author = os.environ.get("USER", "unknown")
        comment = issue.add_comment(author, parsed_args.content)
        
        # Save the updated issue
        default_storage.save_issue(issue)
        
        print(f"Comment added to issue {parsed_args.issue_id}")
        return 0
    
    # For other commands, show a placeholder message
    print(f"Agentic Issues - {parsed_args.command.capitalize()} command")
    print("This functionality is not yet fully implemented.")
    print(f"Arguments: {parsed_args}")
    
    return 0


if __name__ == "__main__":
    # When run directly, pass all command-line arguments to the issue_command function
    exit_code = issue_command(sys.argv[1:])
    sys.exit(exit_code)

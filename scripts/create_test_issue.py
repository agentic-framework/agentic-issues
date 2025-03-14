#!/usr/bin/env python3
"""
Create a test issue to verify that the Agentic Issues system works correctly.

This script creates a test issue in the specified project.
"""

import os
import sys
import argparse
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from agentic_issues.models import Issue, IssuePriority
    from agentic_issues.storage import default_storage
except ImportError:
    print("Error: Could not import the agentic_issues package.")
    print("Please make sure the package is installed by running:")
    print("  cd ~/Agentic/projects/agentic-issues")
    print("  source .venv/bin/activate")
    print("  uv pip install -e .")
    sys.exit(1)

def main():
    """Create a test issue."""
    parser = argparse.ArgumentParser(description="Create a test issue")
    parser.add_argument("--project", default="test-project",
                        help="Project ID (default: test-project)")
    parser.add_argument("--title", default="Test Issue",
                        help="Issue title (default: Test Issue)")
    parser.add_argument("--description", default="This is a test issue created by the create_test_issue.py script.",
                        help="Issue description")
    parser.add_argument("--priority", default="medium",
                        choices=["low", "medium", "high", "critical"],
                        help="Issue priority (default: medium)")
    parser.add_argument("--author", default=os.environ.get("USER", "test-user"),
                        help="Issue author (default: current user)")
    args = parser.parse_args()
    
    # Parse priority
    priority_map = {
        "low": IssuePriority.LOW,
        "medium": IssuePriority.MEDIUM,
        "high": IssuePriority.HIGH,
        "critical": IssuePriority.CRITICAL,
    }
    priority = priority_map.get(args.priority, IssuePriority.MEDIUM)
    
    # Create the issue
    issue = Issue.create(
        project_id=args.project,
        title=args.title,
        description=args.description,
        author=args.author,
        priority=priority,
        labels=["test"],
    )
    
    # Save the issue
    default_storage.save_issue(issue)
    
    print(f"Created test issue with ID: {issue.id}")
    print(f"Project: {args.project}")
    print(f"Title: {args.title}")
    print(f"Priority: {args.priority}")
    print(f"Author: {args.author}")
    print(f"Labels: test")
    print(f"\nYou can view this issue by running:")
    print(f"  ag issues show {issue.id} --project {args.project}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

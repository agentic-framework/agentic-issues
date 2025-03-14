"""
Storage module for the Agentic Issues system.

This module handles persisting issues to disk and loading them back.
"""

import dataclasses
import datetime
import json
import os
import pathlib
from typing import Dict, List, Optional, Union

from .models import Issue, IssueComment, IssuePriority, IssueStatus


class EnhancedJSONEncoder(json.JSONEncoder):
    """JSON encoder that can handle dataclasses, enums, and datetime objects."""

    def default(self, o):
        if dataclasses.is_dataclass(o) and not isinstance(o, type):
            return dataclasses.asdict(o)
        if isinstance(o, (IssueStatus, IssuePriority)):
            return o.value
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        return super().default(o)


def _decode_issue(issue_dict: Dict) -> Issue:
    """Decode an issue from a dictionary."""
    # Convert string status and priority to enum values
    issue_dict["status"] = IssueStatus(issue_dict["status"])
    issue_dict["priority"] = IssuePriority(issue_dict["priority"])

    # Convert string timestamps to datetime objects
    if issue_dict["created_at"]:
        issue_dict["created_at"] = datetime.datetime.fromisoformat(issue_dict["created_at"])
    if issue_dict["updated_at"]:
        issue_dict["updated_at"] = datetime.datetime.fromisoformat(issue_dict["updated_at"])

    # Convert comment dictionaries to IssueComment objects
    comments = []
    for comment_dict in issue_dict.get("comments", []):
        if comment_dict["created_at"]:
            comment_dict["created_at"] = datetime.datetime.fromisoformat(comment_dict["created_at"])
        if comment_dict.get("updated_at"):
            comment_dict["updated_at"] = datetime.datetime.fromisoformat(comment_dict["updated_at"])
        comments.append(IssueComment(**comment_dict))
    issue_dict["comments"] = comments

    return Issue(**issue_dict)


class IssueStorage:
    """Storage for issues."""

    def __init__(self, base_dir: Union[str, pathlib.Path]):
        """Initialize the storage with a base directory."""
        self.base_dir = pathlib.Path(base_dir)
        self.issues_dir = self.base_dir / "issues"
        self.issues_dir.mkdir(parents=True, exist_ok=True)

    def _get_project_file(self, project_id: str) -> pathlib.Path:
        """Get the path to the file for a project's issues."""
        return self.issues_dir / f"{project_id}.json"

    def save_issue(self, issue: Issue) -> None:
        """Save an issue to storage."""
        project_file = self._get_project_file(issue.project_id)
        
        # Load existing issues for the project
        issues = self.get_issues(issue.project_id)
        
        # Update or add the issue
        issue_index = next((i for i, x in enumerate(issues) if x.id == issue.id), None)
        if issue_index is not None:
            issues[issue_index] = issue
        else:
            issues.append(issue)
        
        # Save all issues back to the file
        with open(project_file, "w") as f:
            json.dump([dataclasses.asdict(i) for i in issues], f, cls=EnhancedJSONEncoder, indent=2)

    def get_issues(self, project_id: str) -> List[Issue]:
        """Get all issues for a project."""
        project_file = self._get_project_file(project_id)
        if not project_file.exists():
            return []
        
        with open(project_file, "r") as f:
            try:
                issues_data = json.load(f)
                return [_decode_issue(issue_dict) for issue_dict in issues_data]
            except json.JSONDecodeError:
                # If the file is empty or invalid, return an empty list
                return []

    def get_issue(self, project_id: str, issue_id: str) -> Optional[Issue]:
        """Get a specific issue by ID."""
        issues = self.get_issues(project_id)
        return next((i for i in issues if i.id == issue_id), None)

    def delete_issue(self, project_id: str, issue_id: str) -> bool:
        """Delete an issue by ID."""
        issues = self.get_issues(project_id)
        initial_count = len(issues)
        issues = [i for i in issues if i.id != issue_id]
        
        if len(issues) == initial_count:
            # No issue was removed
            return False
        
        project_file = self._get_project_file(project_id)
        with open(project_file, "w") as f:
            json.dump([dataclasses.asdict(i) for i in issues], f, cls=EnhancedJSONEncoder, indent=2)
        
        return True

    def get_all_project_ids(self) -> List[str]:
        """Get all project IDs that have issues."""
        project_files = list(self.issues_dir.glob("*.json"))
        return [p.stem for p in project_files]


# Create a default storage instance
default_storage = IssueStorage(os.path.expanduser("~/Agentic/shared/agentic-issues"))

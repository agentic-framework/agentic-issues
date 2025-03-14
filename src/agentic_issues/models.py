"""
Data models for the Agentic Issues system.
"""

import dataclasses
import datetime
import enum
import uuid
from typing import List, Optional


class IssueStatus(enum.Enum):
    """Status of an issue."""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class IssuePriority(enum.Enum):
    """Priority of an issue."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclasses.dataclass
class IssueComment:
    """A comment on an issue."""
    id: str
    issue_id: str
    author: str
    content: str
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime] = None


@dataclasses.dataclass
class Issue:
    """An issue in the Agentic Issues system."""
    id: str
    project_id: str
    title: str
    description: str
    status: IssueStatus
    priority: IssuePriority
    author: str
    assignee: Optional[str] = None
    created_at: datetime.datetime = dataclasses.field(default_factory=datetime.datetime.now)
    updated_at: Optional[datetime.datetime] = None
    comments: List[IssueComment] = dataclasses.field(default_factory=list)
    labels: List[str] = dataclasses.field(default_factory=list)

    @classmethod
    def create(cls, project_id: str, title: str, description: str, author: str,
               priority: IssuePriority = IssuePriority.MEDIUM,
               labels: Optional[List[str]] = None) -> "Issue":
        """Create a new issue."""
        return cls(
            id=str(uuid.uuid4()),
            project_id=project_id,
            title=title,
            description=description,
            status=IssueStatus.OPEN,
            priority=priority,
            author=author,
            labels=labels or [],
        )

    def add_comment(self, author: str, content: str) -> IssueComment:
        """Add a comment to the issue."""
        comment = IssueComment(
            id=str(uuid.uuid4()),
            issue_id=self.id,
            author=author,
            content=content,
            created_at=datetime.datetime.now(),
        )
        self.comments.append(comment)
        self.updated_at = datetime.datetime.now()
        return comment

    def update_status(self, status: IssueStatus) -> None:
        """Update the status of the issue."""
        self.status = status
        self.updated_at = datetime.datetime.now()

    def update_priority(self, priority: IssuePriority) -> None:
        """Update the priority of the issue."""
        self.priority = priority
        self.updated_at = datetime.datetime.now()

    def assign(self, assignee: str) -> None:
        """Assign the issue to a user."""
        self.assignee = assignee
        self.updated_at = datetime.datetime.now()

    def add_label(self, label: str) -> None:
        """Add a label to the issue."""
        if label not in self.labels:
            self.labels.append(label)
            self.updated_at = datetime.datetime.now()

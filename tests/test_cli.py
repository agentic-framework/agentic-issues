"""
Tests for the CLI module.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agentic_issues.cli import main, cmd_submit, cmd_list, cmd_show, cmd_comment, cmd_update
from agentic_issues.models import Issue, IssueStatus, IssuePriority


class TestCLI(unittest.TestCase):
    """Tests for the CLI module."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for testing
        self.test_dir = Path(__file__).parent / "test_data"
        self.test_dir.mkdir(exist_ok=True)
        
        # Set up environment variables for testing
        self.old_home = os.environ.get("HOME")
        os.environ["HOME"] = str(self.test_dir)
        
        # Create a mock storage
        self.mock_storage = MagicMock()
        self.mock_storage.get_issues.return_value = []
        
        # Create a mock issue
        self.mock_issue = MagicMock(spec=Issue)
        self.mock_issue.id = "test-id"
        self.mock_issue.title = "Test Issue"
        self.mock_issue.description = "Test Description"
        self.mock_issue.status = IssueStatus.OPEN
        self.mock_issue.priority = IssuePriority.MEDIUM
        self.mock_issue.author = "test-user"
        self.mock_issue.assignee = None
        self.mock_issue.created_at = None
        self.mock_issue.updated_at = None
        self.mock_issue.comments = []
        self.mock_issue.labels = []
        
        # Set up patches
        self.patches = [
            patch("agentic_issues.cli.default_storage", self.mock_storage),
            patch("agentic_issues.cli.get_current_project_id", return_value="test-project"),
            patch("agentic_issues.cli.get_current_user", return_value="test-user"),
            patch("agentic_issues.cli.Issue.create", return_value=self.mock_issue),
        ]
        
        # Start patches
        for p in self.patches:
            p.start()
    
    def tearDown(self):
        """Tear down test fixtures."""
        # Stop patches
        for p in self.patches:
            p.stop()
        
        # Restore environment variables
        if self.old_home:
            os.environ["HOME"] = self.old_home
        else:
            del os.environ["HOME"]
        
        # Clean up test directory
        for file in self.test_dir.glob("*"):
            if file.is_file():
                file.unlink()
        
        if self.test_dir.exists():
            self.test_dir.rmdir()
    
    def test_main_no_command(self):
        """Test main function with no command."""
        with patch("sys.argv", ["ag-issues"]):
            result = main()
        self.assertEqual(result, 1)
    
    def test_cmd_submit(self):
        """Test submit command."""
        args = MagicMock()
        args.project = "test-project"
        args.title = "Test Issue"
        args.description = "Test Description"
        args.priority = "medium"
        args.labels = "bug,ui"
        
        result = cmd_submit(args)
        
        self.assertEqual(result, 0)
        self.mock_storage.save_issue.assert_called_once_with(self.mock_issue)
    
    def test_cmd_list(self):
        """Test list command."""
        args = MagicMock()
        args.project = "test-project"
        args.status = None
        args.priority = None
        args.label = None
        args.sort = "priority"
        args.detailed = False
        
        self.mock_storage.get_issues.return_value = [self.mock_issue]
        
        result = cmd_list(args)
        
        self.assertEqual(result, 0)
        self.mock_storage.get_issues.assert_called_once_with("test-project")
    
    def test_cmd_show(self):
        """Test show command."""
        args = MagicMock()
        args.project = "test-project"
        args.issue_id = "test-id"
        
        self.mock_storage.get_issue.return_value = self.mock_issue
        
        result = cmd_show(args)
        
        self.assertEqual(result, 0)
        self.mock_storage.get_issue.assert_called_once_with("test-project", "test-id")
    
    def test_cmd_comment(self):
        """Test comment command."""
        args = MagicMock()
        args.project = "test-project"
        args.issue_id = "test-id"
        args.content = "Test Comment"
        
        self.mock_storage.get_issue.return_value = self.mock_issue
        
        result = cmd_comment(args)
        
        self.assertEqual(result, 0)
        self.mock_storage.get_issue.assert_called_once_with("test-project", "test-id")
        self.mock_storage.save_issue.assert_called_once_with(self.mock_issue)
        self.mock_issue.add_comment.assert_called_once_with("test-user", "Test Comment")
    
    def test_cmd_update(self):
        """Test update command."""
        args = MagicMock()
        args.project = "test-project"
        args.issue_id = "test-id"
        args.status = "in_progress"
        args.priority = None
        args.assignee = None
        args.add_label = None
        
        self.mock_storage.get_issue.return_value = self.mock_issue
        
        result = cmd_update(args)
        
        self.assertEqual(result, 0)
        self.mock_storage.get_issue.assert_called_once_with("test-project", "test-id")
        self.mock_storage.save_issue.assert_called_once_with(self.mock_issue)
        self.mock_issue.update_status.assert_called_once()


if __name__ == "__main__":
    unittest.main()

from setuptools import setup, find_packages

setup(
    name="agentic-issues",
    version="0.1.0",
    description="Issue tracking plugin for the Agentic framework",
    author="Agentic Team",
    author_email="example@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    entry_points={
        "agentic.commands": [
            "issues=agentic_issues.ag_issues:issues_command"
        ],
        "console_scripts": [
            "ag-issues=agentic_issues.ag_issues:issues_command"
        ]
    }
)

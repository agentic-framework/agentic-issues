#!/usr/bin/env python3
"""
Installation script for the Agentic Issues system.

This script installs the Agentic Issues system into the Agentic framework,
allowing the `ag issue` command to be used from anywhere.
"""

import os
import sys
import shutil
import argparse
import subprocess
from pathlib import Path

def main():
    """Install the Agentic Issues system into the Agentic framework."""
    parser = argparse.ArgumentParser(description="Install the Agentic Issues system")
    parser.add_argument("--agentic-dir", default=os.path.expanduser("~/Agentic"),
                        help="Path to the Agentic directory")
    args = parser.parse_args()
    
    # Get the path to the Agentic framework
    agentic_dir = Path(args.agentic_dir)
    agentic_scripts_dir = agentic_dir / "agentic" / "scripts"
    
    # Check if the Agentic framework exists
    if not agentic_dir.exists():
        print(f"Error: Agentic directory not found at {agentic_dir}")
        return 1
    
    if not agentic_scripts_dir.exists():
        print(f"Error: Agentic scripts directory not found at {agentic_scripts_dir}")
        return 1
    
    # Get the path to this project
    project_dir = Path(__file__).parent.parent
    
    # Install the package in development mode
    print(f"Installing the Agentic Issues package...")
    try:
        # Try using uv first
        uv_result = subprocess.run(["uv", "pip", "install", "-e", str(project_dir)],
                                  check=False, capture_output=True)
        
        if uv_result.returncode == 0:
            print("Package installed successfully using uv")
        else:
            # Fall back to pip if uv fails
            pip_result = subprocess.run([sys.executable, "-m", "pip", "install", "-e", str(project_dir)],
                                      check=True, capture_output=True)
            print("Package installed successfully using pip")
    except subprocess.CalledProcessError as e:
        print(f"Error installing package: {e.stderr.decode() if hasattr(e.stderr, 'decode') else e.stderr}")
        return 1
    except FileNotFoundError:
        print("Error: Neither uv nor pip is available. Please install one of them.")
        return 1
    
    # Create the issue_command.py script in the Agentic scripts directory
    issue_command_path = agentic_scripts_dir / "issue_command.py"
    
    print(f"Creating issue_command.py script at {issue_command_path}...")
    
    with open(issue_command_path, "w") as f:
        f.write("""#!/usr/bin/env python3
\"\"\"
Issue command for the Agentic framework.

This script provides the `ag issue` command for the Agentic framework.
\"\"\"

import sys
import importlib.util
import subprocess

def issue_command(args):
    \"\"\"
    Handle the `ag issue` command.
    
    Args:
        args: Command-line arguments passed to the `ag issue` command.
    
    Returns:
        int: Exit code.
    \"\"\"
    try:
        # Try to import the agentic_issues package
        import agentic_issues.ag_issues
        return agentic_issues.ag_issues.issue_command(args)
    except ImportError:
        # If the package is not installed, suggest installing it
        print("Error: The Agentic Issues package is not installed.")
        print("Please install it by running:")
        print("  cd ~/Agentic/projects/agentic-issues")
        print("  source .venv/bin/activate")
        print("  uv pip install -e .")
        return 1

if __name__ == "__main__":
    sys.exit(issue_command(sys.argv[1:]))
""")
    
    # Make the script executable
    os.chmod(issue_command_path, 0o755)
    
    # Update the ag script to include the issue command
    ag_script_path = agentic_dir / "agentic" / "ag"
    
    if not ag_script_path.exists():
        print(f"Warning: ag script not found at {ag_script_path}")
        print("You will need to manually update the ag script to include the issue command")
    else:
        print(f"Checking if the issue command is already in the ag script...")
        
        # Read the ag script
        with open(ag_script_path, "r") as f:
            ag_script = f.read()
        
        # Check if the issue command is already in the script
        if '"issue"' in ag_script and "issue_command" in ag_script:
            print("The issue command is already in the ag script")
        else:
            print("Adding the issue command to the ag script...")
            
            # Create a backup of the ag script
            backup_path = ag_script_path.with_suffix(".bak")
            shutil.copy2(ag_script_path, backup_path)
            print(f"Created backup of ag script at {backup_path}")
            
            # Find the COMMAND_STRUCTURE dictionary in the ag script
            command_structure_start = ag_script.find("COMMAND_STRUCTURE = {")
            if command_structure_start == -1:
                print("Error: Could not find COMMAND_STRUCTURE in the ag script")
                return 1
            
            # Find the end of the COMMAND_STRUCTURE dictionary
            command_structure_end = ag_script.find("}", command_structure_start)
            if command_structure_end == -1:
                print("Error: Could not find the end of COMMAND_STRUCTURE in the ag script")
                return 1
            
            # Insert the issue command into the COMMAND_STRUCTURE dictionary
            issue_command_def = """    "issue": {
        "description": "Issue tracking commands",
        "subcommands": {
            "submit": {
                "description": "Submit a new issue",
                "module": "issue_command",
                "function": "issue_command"
            },
            "list": {
                "description": "List issues",
                "module": "issue_command",
                "function": "issue_command"
            },
            "show": {
                "description": "Show issue details",
                "module": "issue_command",
                "function": "issue_command"
            },
            "comment": {
                "description": "Add a comment to an issue",
                "module": "issue_command",
                "function": "issue_command"
            },
            "update": {
                "description": "Update an issue",
                "module": "issue_command",
                "function": "issue_command"
            }
        }
    },"""
            
            # Insert the issue command definition before the end of the COMMAND_STRUCTURE dictionary
            new_ag_script = (
                ag_script[:command_structure_end] +
                issue_command_def +
                ag_script[command_structure_end:]
            )
            
            # Write the updated ag script
            with open(ag_script_path, "w") as f:
                f.write(new_ag_script)
            
            print("Updated the ag script to include the issue command")
    
    print("\nInstallation complete!")
    print("You can now use the `ag issue` command from anywhere.")
    print("For example, try running:")
    print("  ag issue list")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

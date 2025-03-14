#!/usr/bin/env python3
"""
Installation script for the Agentic Issues system.

This script installs the Agentic Issues system into the Agentic framework,
allowing the `ag issues` command to be used from anywhere.
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
    
    # Create the issues_command.py script in the Agentic scripts directory
    issues_command_path = agentic_scripts_dir / "issues_command.py"
    
    print(f"Creating issues_command.py script at {issues_command_path}...")
    
    with open(issues_command_path, "w") as f:
        f.write("""#!/usr/bin/env python3
\"\"\"
Issues command for the Agentic framework.

This script provides the `ag issues` command for the Agentic framework.
\"\"\"

import sys
import importlib.util
import subprocess

def issues_command(args):
    \"\"\"
    Handle the `ag issues` command.
    
    Args:
        args: Command-line arguments passed to the `ag issues` command.
    
    Returns:
        int: Exit code.
    \"\"\"
    try:
        # Try to import the agentic_issues package
        import agentic_issues.ag_issues
        return agentic_issues.ag_issues.issues_command(args)
    except ImportError:
        # If the package is not installed, suggest installing it
        print("Error: The Agentic Issues package is not installed.")
        print("Please install it by running:")
        print("  cd ~/Agentic/projects/agentic-issues")
        print("  source .venv/bin/activate")
        print("  uv pip install -e .")
        return 1

if __name__ == "__main__":
    sys.exit(issues_command(sys.argv[1:]))
""")
    
    # Make the script executable
    os.chmod(issues_command_path, 0o755)
    
    # Update the ag script to include the issues command
    ag_script_path = agentic_dir / "agentic" / "ag"
    
    if not ag_script_path.exists():
        print(f"Warning: ag script not found at {ag_script_path}")
        print("You will need to manually update the ag script to include the issues command")
    else:
        print(f"Checking if the issues command is already in the ag script...")
        
        # Read the ag script
        with open(ag_script_path, "r") as f:
            ag_script = f.read()
        
        # Check if the issues command is already in the script
        if '"issues"' in ag_script and "issues_command" in ag_script:
            print("The issues command is already in the ag script")
        else:
            print("Adding the issues command to the ag script...")
            
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
            
            # Insert the issues command into the COMMAND_STRUCTURE dictionary
            issues_command_def = """    "issues": {
        "description": "Issue tracking commands",
        "subcommands": {
            "submit": {
                "description": "Submit a new issue",
                "module": "issues_command",
                "function": "issues_command"
            },
            "list": {
                "description": "List issues",
                "module": "issues_command",
                "function": "issues_command"
            },
            "show": {
                "description": "Show issue details",
                "module": "issues_command",
                "function": "issues_command"
            },
            "comment": {
                "description": "Add a comment to an issue",
                "module": "issues_command",
                "function": "issues_command"
            },
            "update": {
                "description": "Update an issue",
                "module": "issues_command",
                "function": "issues_command"
            }
        }
    },"""
            
            # Insert the issues command definition before the end of the COMMAND_STRUCTURE dictionary
            new_ag_script = (
                ag_script[:command_structure_end] +
                issues_command_def +
                ag_script[command_structure_end:]
            )
            
            # Write the updated ag script
            with open(ag_script_path, "w") as f:
                f.write(new_ag_script)
            
            print("Updated the ag script to include the issues command")
    
    print("\nInstallation complete!")
    print("You can now use the `ag issues` command from anywhere.")
    print("For example, try running:")
    print("  ag issues list")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

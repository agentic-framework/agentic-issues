#!/usr/bin/env python3
"""
Entry point for the `ag issues` command.

This script is installed as a command in the Agentic framework to handle
the `ag issues` subcommand.
"""

import sys
import os
import importlib.util

def issues_command(args=None):
    """
    Handle the `ag issues` command.
    
    This function is called by the Agentic framework's `ag` script when
    the user runs `ag issues`.
    
    Args:
        args: Command-line arguments passed to the `ag issues` command.
    
    Returns:
        int: Exit code.
    """
    # Get the path to the CLI module
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cli_path = os.path.join(script_dir, "cli.py")
    
    # Import the CLI module dynamically
    spec = importlib.util.spec_from_file_location("cli", cli_path)
    if spec is None or spec.loader is None:
        print(f"Error: Could not load CLI module from {cli_path}")
        return 1
        
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)
    
    # Call the main function
    return cli.main(args)


if __name__ == "__main__":
    # When run directly, pass all command-line arguments to the issues_command function
    exit_code = issues_command(sys.argv[1:])
    sys.exit(exit_code)

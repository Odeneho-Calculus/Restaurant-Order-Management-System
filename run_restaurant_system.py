#!/usr/bin/env python3
"""
Quick launcher script for Restaurant Order Management System.

This script provides an easy way to start the restaurant management
application with proper error handling and system checks.
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version meets requirements."""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required.")
        print(f"Current version: Python {sys.version}")
        print("\nPlease upgrade Python and try again.")
        return False
    return True

def check_tkinter():
    """Check if tkinter is available."""
    try:
        import tkinter as tk
        # Test tkinter by creating a hidden window
        root = tk.Tk()
        root.withdraw()
        root.destroy()
        return True
    except ImportError:
        print("Error: tkinter is not available.")
        print("Please install tkinter package for your Python distribution.")
        return False
    except Exception as e:
        print(f"Error: tkinter test failed: {e}")
        return False

def main():
    """Main launcher function."""
    print("=" * 60)
    print("Restaurant Order Management System")
    print("Version 1.0.0")
    print("=" * 60)

    # Check system requirements
    print("Checking system requirements...")

    if not check_python_version():
        return 1

    if not check_tkinter():
        return 1

    print("✓ Python version check passed")
    print("✓ GUI framework (tkinter) available")

    # Add project root to path
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))

    try:
        print("Starting application...")
        print("-" * 60)

        # Import and run the application
        from restaurant_system.main import main as app_main
        return app_main()

    except ImportError as e:
        print(f"Error: Failed to import application modules: {e}")
        print("\nPlease ensure all files are present and try again.")
        return 1

    except KeyboardInterrupt:
        print("\nApplication interrupted by user.")
        return 0

    except Exception as e:
        print(f"Error: Unexpected error occurred: {e}")
        print("\nPlease check the log files for more details.")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"Fatal error in launcher: {e}")
        sys.exit(1)
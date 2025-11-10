"""
Quick launcher script for the GUI application
"""

import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from plagiarism_checker_gui import main
    main()
except ImportError as e:
    print(f"Error: Missing dependencies - {e}")
    print("\nPlease install required packages:")
    print("  pip install -r requirements.txt")
    input("\nPress Enter to exit...")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    input("\nPress Enter to exit...")

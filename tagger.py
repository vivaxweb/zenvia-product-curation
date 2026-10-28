"""
Entry point shortcut: invokes scripts/run_tagger.py with provided arguments.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scripts.run_tagger import main

if __name__ == "__main__":
    main()

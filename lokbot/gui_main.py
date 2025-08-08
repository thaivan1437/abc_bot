#!/usr/bin/env python3
"""
Entry point cho GUI version của LokBot
"""

import sys
from pathlib import Path

# Thêm thư mục gốc vào Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lokbot.gui import main

if __name__ == "__main__":
    main()
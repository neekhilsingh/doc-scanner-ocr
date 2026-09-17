#!/usr/bin/env python3
# entry point - actual logic lives in scanner/
#
# Author: Neekhil Kumar Singh
# Registration No.: 24BAI10907
#
# usage:
#   python main.py --input path/to/photo.jpg --output scanned.jpg

import sys

from scanner.cli import main

if __name__ == "__main__":
    sys.exit(main())

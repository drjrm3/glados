#!/usr/bin/env python3
"""
Main entry point for glados.

Copyright © 2023 J. Robert Michael, PhD. All rights reserved.
"""

import sys

from .utils import getArgs
from .core import turretServer

#-------------------------------------------------------------------------------
def main():
    """Main routine."""
    action = sys.argv[1]
    args = getArgs()

    if action == "turret":
        turretServer(args.port, args.config)

#-------------------------------------------------------------------------------
main()

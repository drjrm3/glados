#!/usr/bin/env python3
"""
Initialization for glados.

Copyright © 2023, J. Robert Michael, PhD. All rights reserved.
"""
import os
from subprocess import run, PIPE

#-------------------------------------------------------------------------------
def updateVersion():
    """ Return the version of this repository based on the git tag. """

    versionFile = os.path.join(os.path.dirname(__file__), "version.py")

    # Try to update the version file based on the git commit if possible.
    cmd = ["git", "describe", "--tags"]
    proc = run(cmd, stdout=PIPE, stderr=PIPE, check=False)
    if proc.returncode == 0:
        gitVersion = proc.stdout.decode("utf-8").rstrip().split("-")
        _version = gitVersion[0].lstrip('v')
        if len(gitVersion) > 1:
            _version += f"+{gitVersion[1]}"
        if len(gitVersion) > 2:
            _version += f".{gitVersion[2]}"
        with open(versionFile, "w", encoding="UTF-8") as fout:
            print('""" Version. """', file=fout)
            print(f"__version__ = '{_version}'", file=fout)

updateVersion()

# pylint: disable=wrong-import-position
from .version import __version__
# pylint: enable=wrong-import-position

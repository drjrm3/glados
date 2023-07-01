#!/usr/bin/env python3
""" Basic utilities for glados. """

import argparse
import io
import subprocess
import sys

from typing import Tuple

from glados import __version__

#-------------------------------------------------------------------------------
def getArgs(argv=None):
    """ Get arguments. """
    if not argv:
        argv = sys.argv

    parser = argparse.ArgumentParser(prog="aidedpy")
    parser.add_argument("-v", "--version", action='version',
                        version=__version__)

    args = parser.parse_args(argv)

    return args

#-------------------------------------------------------------------------------
def runCommand(cmdStr: str, shell=False, stdout=None, stderr=None) -> Tuple[str, str, int]:
    """ Run a shell command from Python.

    Args:
        cmdStr: Command to run.
        shell: Whether or not to run with shell as True or False.
        stdout: How to direct stdout (None -> subprocess.PIPE).
        stderr: How to direct stderr (None -> subprocess.PIPE).

    Returns:
        outStr: Results of stdout.
        errStr: Results of stderr.
        returnCode: Return code of the command.
    """

    assert isinstance(cmdStr, str)

    for stdeo in [stdout, stderr]:
        if not isinstance(stdeo, io.TextIOWrapper):
            stdeo = subprocess.PIPE

    cmd = cmdStr if shell else shlex.split(cmdStr)

    try:
        proc = subprocess.run(cmd, stdout=stdout, stderr=stderr,
                              shell=shell, check=False)
    except FileNotFoundError:
        stdout = ""
        stderr = f"Command {cmd[0]} not found"
        returnCode = 127
        return stdout, stderr, returnCode

    outStr = proc.stdout.decode("utf-8") if proc.stdout else ""
    errStr = proc.stderr.decode("utf-8") if proc.stderr else ""
    returnCode = proc.returncode

    return outStr, errStr, returnCode

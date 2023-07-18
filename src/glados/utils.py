#!/usr/bin/env python3
"""
Basic utilities for glados.

Copyright © 2023, J. Robert Michael, PhD. All rights reserved.
"""

import argparse
import shlex
import subprocess
import sys

from typing import Tuple

from . import __version__

#-------------------------------------------------------------------------------
def getArgs(argv=None):
    """Get arguments."""
    if not argv:
        argv = sys.argv

    parser = argparse.ArgumentParser(prog="glados")
    parser.add_argument("-v", "--version", action='version',
                        version=f"glados {__version__}")
    subparser = parser.add_subparsers(help="Actions.")

    # 'turret'
    # - Run the turret client to feed data to glados.
    turretP = subparser.add_parser("turret", help="Run the turret client.")
    #turretP.add_argument("-c", "--config", type=str,
    #                     help="Configuration file to use.")
    turretP.add_argument("-p", "--port", type=int, required=True,
                         help="Port to run on.")
    turretP.add_argument("-v", "--version", action='version',
                         version=f"turret {__version__}")

    # 'serve'
    # - Serve the glados website.
    #serveP = subparser.add_parser("serve", help="Serve glados site.")
    #serveP.add_argument("-i", --inputDataDir", type=str, required=True,
    #                    help="Input directory with .rrd files for data.")
    #serveP.add_argument("-p", --port", type=int, default=8081,
    #                    help="Port to serve on.")

    # 'rust'
    # - Check on the status a turret / server / input file.
    #rustP = subparser.add_parser("rust", help="R U Still There?")
    #rustP = rustP.add_argument("-t", "--timeOut", type=int,
    #                           help="Heartbeat threshold.")

    args = parser.parse_args(argv[1:])

    return args

#-------------------------------------------------------------------------------
def runCommand(cmdStr: str, shell=False, stdout=None, stderr=None) -> Tuple[str, str, int]:
    """Run a shell command from Python.

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

    if not stdout:
        stdout = subprocess.PIPE
    if not stderr:
        stderr = subprocess.PIPE

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

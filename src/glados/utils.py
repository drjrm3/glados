#!/usr/bin/env python3
"""
Basic utilities for glados.

Copyright © 2023, J. Robert Michael, PhD. All rights reserved.
"""

import argparse
import json
from os.path import exists as ope
import shlex
import subprocess
import sys

from typing import Tuple, Dict

from . import __version__

#-------------------------------------------------------------------------------
def getParamsFromConfig(configFile: str = "") -> Dict:
    """Get config variables from config file

    Args:
        configFile: Path to input config file in Json format.

    Returns:
        configs: Dictionary of config options.
    """

    params = {
        "sleepTime": 5,
        "FileTurrets": [],
        "JsonTurrets": [],
    }

    if isinstance(configFile, str) and ope(configFile):
        with open(configFile, "r", encoding="UTF-8") as finp:
            _params = json.loads(finp.read())
            for _key in _params:
                if _key in params:
                    params[_key] = _params[_key]

    return params

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
    turretP.add_argument("-c", "--config", type=str,
                         help="Configuration file to use.")
    turretP.add_argument("-p", "--port", type=int, required=True,
                         help="Port to run on.")
    turretP.add_argument("-v", "--version", action='version',
                         version=f"turret {__version__}")

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

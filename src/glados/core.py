#!/usr/bin/env python3
"""
Serves Turrets.

Copyright © 2023, J. Robert Michael, PhD. All rights reserved.
"""

import time
import pkgutil
from importlib import import_module
from typing import List

import os.path as op

from prometheus_client import make_wsgi_app, start_wsgi_server
from prometheus_client.core import REGISTRY

from .utils import runCommand, getParamsFromConfig
from .turrets.JsonTurret import JsonTurret

#-------------------------------------------------------------------------------
def isSpecializedTurret(turretStr: str) -> bool:
    """Whether or not a turret is specialized and not just "Turret"."""
    return turretStr.endswith("Turret") and turretStr != "Turret"

#-------------------------------------------------------------------------------
def getTurretExcludeList() -> List[str]:
    """Get the default Turret exclude list for the turretServer.

    Args: None.

    Returns:
        turretExcludeList: List of module names which should not be called by
            default with not extra arguments.
    """

    # JsonTurret and CsvTurret are specialized and require input files.
    turretExcludeList = ["JsonTurret", "CsvTurret"]
    # NvidiaGpuTurret uses "nvidia-smi" and should not run if returnCode != 0.
    if runCommand("nvidia-smi")[-1] != 0:
        turretExcludeList.append("NvidiaGpuTurret")

    return turretExcludeList

#-------------------------------------------------------------------------------
def getDefaultTurrets(turretsModulePath: str, excludeList: list) -> List:
    """Find all "local" turrets in glados which should run by default input with
    no extra file based input. Any turrets which should *not* be run should have
    previously been added to the exclude list.

    Args:
        turretsModulePath: Path to module (directory) containing turret modules.
        excludeList: List of strings to skip identifying specialized turrets.

    Returns:
        defaultTurrets: List of all turret classes detected in turret modules.
    """

    defaultTurrets = []
    for _, turretModule, _ in pkgutil.iter_modules([turretsModulePath]):
        if isSpecializedTurret(turretModule):
            turretClass = import_module(f"glados.turrets.{turretModule}")
            for turretStr in dir(turretClass):
                # Skip over any abstract / excluded turrets like "JsonTurret".
                if any(b in turretStr for b in excludeList):
                    continue
                # Skip over anything in turretClass that is not "*Turret".
                if isSpecializedTurret(turretStr):
                    turret = getattr(turretClass, turretStr)
                    defaultTurrets.append(turret())

    return defaultTurrets

#-------------------------------------------------------------------------------
def getFileTurrets(turretFiles: List) -> List:
    """Override a specialized turret with a file.

    Args:
        turretFiles: Turret files to use for overriding turret.

    Returns:
        turrets: Tuple of (server, Turret)
    """

    turrets = []
    for turretFile in turretFiles:
        turretModule = op.basename(turretFile).replace(".turret", "")
        try:
            turretClass = import_module(f"glados.turrets.{turretModule}Turret")
        except ModuleNotFoundError:
            print(f"[W] Unable to find module for {turretFile}.")
            continue
        turretStrs = [t for t in dir(turretClass) if isSpecializedTurret(t)]
        if len(turretStrs) == 1:
            hostname = op.basename(op.dirname(turretFile))
            turret = getattr(turretClass, turretStrs[0])
            turrets.append(turret(turretFile, hostname))

    return turrets

#-------------------------------------------------------------------------------
def getJsonTurrets(jsonFiles: List) -> List:
    """Deploys a turret from a JSON file.

    Args:
        jsonFiles: Json files to use for turrets.

    Returns:
        jsonTurrets: List of JsonTurrets to call.
    """

    jsonTurrets = []
    for jsonFile in jsonFiles:
        jsonTurrets.append(JsonTurret(jsonFile))

    return jsonTurrets

#-------------------------------------------------------------------------------
def turretServer(port: int, configFile=""):
    """Serve all turrets found.

    Args:
        port: Port on which to serve.
        params: Config file to use.
    """
    assert isinstance(port, int), "!isinstance(port, int)"

    def turretStr(tur):
        return str(tur).rsplit(".", maxsplit=1)[-1].split(" ")[0]

    params = getParamsFromConfig(configFile)

    # Make and start the app.
    print(f"[*] Serving turrets on port '{port}'")
    make_wsgi_app(disable_compression=True)
    start_wsgi_server(port)

    turretsModulePath = op.join(op.dirname(__file__), "turrets")
    turretExcludeList = getTurretExcludeList()
    for turret in getDefaultTurrets(turretsModulePath, turretExcludeList):
        print(f"[I] Found turret {turretStr(turret)}.")
        REGISTRY.register(turret)

    for turret in getJsonTurrets(params["JsonTurrets"]):
        print(f"[I] Found turret {turretStr(turret)}:\n    {turret.fileName}")
        REGISTRY.register(turret)

    for turret in getFileTurrets(params["FileTurrets"]):
        print(f"[I] Found turret {turretStr(turret)}:\n    {turret.fileName}")
        REGISTRY.register(turret)

    # Sleep between each collection.
    while True:
        time.sleep(params["sleepTime"])

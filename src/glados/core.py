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

# TODO: Implement logger.

#-------------------------------------------------------------------------------
def getLocalTurrets(turretsModulePath: str, blacklist: list) -> List:
    """Find all turrets in glados.

    Args:
        turretsModulePath: Path to module (directory) containing turret modules.
        blacklist: Tuple of strings to skip identifying specialized turrets.

    Returns:
        allTurrets: List of all turret classes detected in turret modules.
    """

    def isSpecializedTurret(turretStr: str) -> bool:
        """Whether or not a turret is specialized and not just "Turret"."""
        return turretStr.endswith("Turret") and turretStr != "Turret"

    allTurrets = []
    for _, turretModule, _ in pkgutil.iter_modules([turretsModulePath]):
        if isSpecializedTurret(turretModule):
            turretClass = import_module(f"glados.turrets.{turretModule}")
            for turret in dir(turretClass):
                # Skip over any abstract / blacklist turrets like "JsonTurret".
                if any(b in turret for b in blacklist):
                    continue
                if isSpecializedTurret(turret):
                    turret = getattr(turretClass, turret)
                    allTurrets.append(turret)

    return allTurrets

#-------------------------------------------------------------------------------
def turretServer(port: int):
    """Serve all turrets found.

    Args:
        port: Port on which to serve.
    """
    assert isinstance(port, int), "!isinstance(port, int)"

    # Make and start the app.
    print(f"[*] Serving turrets on port '{port}'")
    make_wsgi_app(disable_compression=True)
    start_wsgi_server(port)

    turretsModulePath = op.join(op.dirname(__file__), "turrets")
    turretBlackList = ["JsonTurret"]
    for collector in getLocalTurrets(turretsModulePath, turretBlackList):
        collectorStr = str(collector).rsplit(".", maxsplit=1)[-1].split("'")[0]
        print(f"[I] Found turret {collectorStr}")

        REGISTRY.register(collector())

    # Sleep between each collection.
    while True:
        time.sleep(1)

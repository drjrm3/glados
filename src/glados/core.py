#!/usr/bin/env python3
"""
Serves Turrets.

Copyright © 2023, J. Robert Michael, PhD. All rights reserved.
"""

import time

from prometheus_client import make_wsgi_app, start_wsgi_server
from prometheus_client.core import REGISTRY

from .turrets.CpuStatsTurret import CpuStatsTurret
from .turrets.StorageTurret import StorageUsageTurret

#-------------------------------------------------------------------------------
def turretServer(port: int):
    """ Serve all turrets found.

    Args:
        port: Port on which to serve.
    """
    assert isinstance(port, int), "!isinstance(port, int)"

    # Make and start the app.
    print(f"[*] Serving turrets on port '{port}'")
    make_wsgi_app(disable_compression=True)
    start_wsgi_server(port)

    # TODO: Auto-detect all Turrets and register them here.
    for collectorStr in ["CpuStatsTurret", "StorageUsageTurret"]:
        collector = globals()[collectorStr]()
        REGISTRY.register(collector)

    # Sleep between each collection.
    while True:
        time.sleep(1)

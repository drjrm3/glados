#!/usr/bin/env python3
"""
CPU Stats collector.
Example of not using 'acquire' and doing everything through 'collect' natively.

Copyright © 2023, J. Robert Michael, PhD. All rights reserved.
"""

from prometheus_client.core import GaugeMetricFamily as GMF

from .Turret import Turret

#-------------------------------------------------------------------------------
class CpuStatsTurret(Turret):
    """Collect CPU statistics."""
    #---------------------------------------------------------------------------
    def __init__(self):
        """Initialization."""
        super().__init__()
        self._fileName = "/proc/cpuinfo"

    #---------------------------------------------------------------------------
    def collect(self):
        """Run the collector."""
        self._readFileInfo()
        vCoreSpeeds = GMF(
            "vcore_speeds",
            f"Gauge of current vCPU speeds for {self.hostname}",
            labels=["host", "vcore"],
        )
        vCore = -1
        vCoreGHz = 0.0
        for line in self._turretFileInfo.splitlines():
            words = line.split(":")
            key = words[0].strip()
            value = words[-1].strip()
            if key == "processor":
                vCore = int(value)
            elif key == "cpu MHz":
                vCoreGHz = float(value) / 1000.0
            if ":" not in line:
                vCoreSpeeds.add_metric([self.hostname, f"{vCore}"], vCoreGHz)

        yield vCoreSpeeds

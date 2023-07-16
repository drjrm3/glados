#!/usr/bin/env python3
"""
CPU Stats collector.

Copyright © 2023, J. Robert Michael, PhD. All rights reserved.
"""

from prometheus_client.core import GaugeMetricFamily as GMF

from .Turret import Turret

#-------------------------------------------------------------------------------
class CpuStatsTurret(Turret):
    """ Collect CPU statistics. """
    #---------------------------------------------------------------------------
    def __init__(self):
        """ Initialization. """
        super().__init__()
        self.__procCpuInfo = ""
        self._readProcCpuInfo()

    #---------------------------------------------------------------------------
    def _readProcCpuInfo(self):
        """ Read /proc/cpuinfo. """
        with open("/proc/cpuinfo", "r", encoding="UTF-8") as finp:
            self.__procCpuInfo = finp.read()

    #---------------------------------------------------------------------------
    def collect(self):
        """ Run the collector. """
        self._readProcCpuInfo()
        vCoreSpeeds = GMF("vcore_speeds", "Gauge of current vCPU speeds.",
                          labels=["vcore"])
        vCore = -1
        vCoreGHz = 0.0
        for line in self.__procCpuInfo.splitlines():
            words = line.split(':')
            key = words[0].strip()
            value = words[-1].strip()
            if key == "processor":
                vCore = int(value)
            elif key == "cpu MHz":
                vCoreGHz = float(value)/1000.
            if ":" not in line:
                vCoreSpeeds.add_metric([f"{vCore}"], vCoreGHz)

        yield vCoreSpeeds

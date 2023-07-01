#!/usr/bin/env python3
"""
Storage Stats Turret.

Copyright © 2023, J. Robert Michael, PhD. All rights reserved.
"""

from prometheus_client.core import GaugeMetricFamily as GMF

from ..utils import runCommand
from .Turret import Turret

#-------------------------------------------------------------------------------
class StorageUsageTurret(Turret):
    """ Storage Usage statistics. """
    #---------------------------------------------------------------------------
    def __init__(self):
        """ Initialization. """
        super().__init__()
        self.__dfInfo = ""
        self.__excludeList = ["tmpfs"]
        self._readDfInfo()

    #---------------------------------------------------------------------------
    def _readDfInfo(self):
        """ Read df. """
        outStr, _errStr, returnCode = runCommand("df")
        assert returnCode == 0
        self.__dfInfo = outStr

    #---------------------------------------------------------------------------
    def collect(self):
        """ Run the collector. """
        self._readDfInfo()
        mntUsePct = GMF("mnt_used_pct", "Mount usage pct.", labels=["mnt"])
        mntAvailGB = GMF("mnt_avail", "Mount available in GB.", labels=["mnt"])
        mnt = ""
        usePct = 0.0
        for line in self.__dfInfo.splitlines()[1:]:
            if any(e in line for e in self.__excludeList):
                continue
            words = line.split()

            _fs, _sizeStr, _useStr, availStr, usePctStr, mnt = words
            usePct = float(usePctStr.replace("%", ""))
            mntUsePct.add_metric([f"{mnt}"], usePct)
            availGB = float(availStr) / (1024. * 1024.)
            mntAvailGB.add_metric([f"{mnt}"], availGB)

        yield mntUsePct
        yield mntAvailGB

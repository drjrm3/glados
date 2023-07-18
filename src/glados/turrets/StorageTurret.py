#!/usr/bin/env python3
"""
Storage Stats Turret.
Example of using 'acquire' and allowing Turret to invoke 'collect'.

Copyright © 2023, J. Robert Michael, PhD. All rights reserved.
"""

from ..utils import runCommand
from .Turret import Turret
from .Turret import TurretGauge

#-------------------------------------------------------------------------------
class StorageUsageTurret(Turret):
    """Storage Usage statistics."""
    #---------------------------------------------------------------------------
    def __init__(self):
        """Initialization."""
        super().__init__()
        self.__dfInfo = ""
        self.__excludeList = ["/tmpfs", "/snap"]
        self._readDfInfo()

    #---------------------------------------------------------------------------
    def _readDfInfo(self):
        """Read df."""
        outStr, _errStr, returnCode = runCommand("df")
        assert returnCode == 0
        self.__dfInfo = outStr

    #---------------------------------------------------------------------------
    def acquire(self):
        """Acquire storage stats and call collector."""
        self._readDfInfo()

        self.gauges = {
            "mnt_used_pct": TurretGauge("mnt_used_pct", "Mount usage pct.", "mnt"),
            "mnt_avail": TurretGauge("mnt_avail", "Mount available in GB.", "mnt")
        }
        for name in self.gauges:
            self.metrics[name] = []

        mnt = ""
        usePct = 0.0
        for line in self.__dfInfo.splitlines()[1:]:
            if any(e in line for e in self.__excludeList):
                continue
            words = line.split()

            _fs, _sizeStr, _useStr, availStr, usePctStr, mnt = words
            usePct = float(usePctStr.replace("%", ""))
            self.metrics["mnt_used_pct"].append((mnt, usePct))

            availGB = float(availStr) / (1024.0 * 1024.0)
            self.metrics["mnt_avail"].append((mnt, availGB))

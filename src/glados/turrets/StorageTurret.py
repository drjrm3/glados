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
    def __init__(self, file="", hostname=""):
        """Initialization."""
        super().__init__(file, hostname)
        self._turretFileInfo = ""
        self._readDfInfo()

    #---------------------------------------------------------------------------
    def _readDfInfo(self) -> None:
        """Read df."""
        if self._fileName:
            self._readFileInfo()
        else:
            outStr, _errStr, returnCode = runCommand("df")
            assert returnCode == 0
            self._turretFileInfo = outStr

    #---------------------------------------------------------------------------
    def acquire(self):
        """Acquire storage stats and call collector."""
        self._readDfInfo()

        self.gauge = TurretGauge("storage_usage", "Mount usage pct.",
                                 ["host", "mnt", "metric"])

        mnt = ""
        usePct = 0.0
        for line in self._turretFileInfo.splitlines()[1:]:
            words = line.split()

            _fs, _sizeStr, _useStr, availStr, usePctStr, mnt = words
            usePct = float(usePctStr.replace("%", ""))
            self.gauge.add_metric([self.hostname, mnt, "usePct"], usePct)

            availGB = float(availStr) / (1024.0 * 1024.0)
            self.gauge.add_metric([self.hostname, mnt, "availGB"], availGB)

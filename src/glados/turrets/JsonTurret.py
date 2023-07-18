#!/usr/bin/env python3
"""
Basic JsonTurret.

Copyright © 2023, J. Robert Michael, PhD. All rights reserved.
"""

import json

from .Turret import Turret, TurretGauge

#-------------------------------------------------------------------------------
class JsonTurret(Turret):
    """Collect CPU statistics."""
    #---------------------------------------------------------------------------
    def __init__(self, jsonFile: str):
        """Initialization.

        Args:
            jsonFile: Path to a json file to read for information.
        """
        super().__init__()
        self._fileName = jsonFile
        self._parseJson()

    #---------------------------------------------------------------------------
    def _parseJson(self):
        """Parse the JSON file."""
        self._readFileInfo()
        self.data = json.loads(self._turretFileInfo)
        # TODO: Add timestamp once TurretGauge supports it.
        self.gauge = TurretGauge(self.data["name"], self.data["description"],
                                 self.data["labels"])

    #---------------------------------------------------------------------------
    def acquire(self) -> None:
        """Acquire the data. File format / naming convention here.
        """
        self._parseJson()

        for labels, value in self.data["metrics"]:
            self.addMetric(labels, value)

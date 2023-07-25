#!/usr/bin/env python3
"""
CPU Stats Turret.

Copyright © 2023, J. Robert Michael, PhD. All rights reserved.
"""

import os.path as op
from typing import Dict, Optional, List, Tuple

from prometheus_client.registry import Collector
from prometheus_client.core import GaugeMetricFamily

from . import hostname as hostnameActual

#-------------------------------------------------------------------------------
class TurretGauge(GaugeMetricFamily):
    """Basic Gauge."""
    #---------------------------------------------------------------------------
    # TODO: Add timestamp.
    def __init__(
        self, name="", documentation="", labels: Optional[List] = None
    ):
        """Initialization."""
        if not isinstance(labels, List):
            labels = [""]
        super().__init__(name, documentation, labels=labels)

#-------------------------------------------------------------------------------
class Turret(Collector):
    """Basic turret."""
    #---------------------------------------------------------------------------
    def __init__(self, file: str = "", hostname: str = ""):
        """Initialization."""
        self.gauge: GaugeMetricFamily
        self.metrics: Dict[str, List[Tuple[List[str], float]]] = {}
        self.hostname = hostname if hostname else hostnameActual

        self.fileName = file
        self.turretFileInfo = ""

    #---------------------------------------------------------------------------
    def _readFileInfo(self):
        """If the Turret was given a file to read then process the file."""
        with open(self.fileName, "r", encoding="UTF-8") as finp:
            self.turretFileInfo = finp.read()

    #---------------------------------------------------------------------------
    def addMetric(self, labels: List[str], value: float) -> None:
        """Add a metric to the gauge

        Args:
            labels: A list of label values.
            value: The float value to add.
        """
        self.gauge.add_metric(labels, value)

    #---------------------------------------------------------------------------
    def acquire(self):
        """Overridable function which creates self.gauges and self.metrics."""

        raise NotImplementedError

    #---------------------------------------------------------------------------
    def collect(self):
        """Basic Collector.collect method. Calls acquire to get gauges and
        metrics, then creates and yields each gauge.
        """
        if self.fileName:
            self._readFileInfo()

        self.acquire()

        yield self.gauge

    #---------------------------------------------------------------------------
    @property
    def fileName(self) -> str:
        """Return the underlying filename assigned."""
        return self._fileName

    @fileName.setter
    def fileName(self, file: str) -> None:
        """Set the underlying filename."""
        self._fileName = op.realpath(file) if op.exists(file) else file
        if self._fileName and not op.exists(self._fileName):
            raise FileNotFoundError(self._fileName)

    #---------------------------------------------------------------------------
    @property
    def turretFileInfo(self) -> str:
        """Return the underlying file information."""
        return self._turretFileInfo

    @turretFileInfo.setter
    def turretFileInfo(self, turretFileInfo: str) -> None:
        """Set the underlying file information."""
        self._turretFileInfo = turretFileInfo

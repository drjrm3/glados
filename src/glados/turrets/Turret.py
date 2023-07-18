#!/usr/bin/env python3
"""
CPU Stats Turret.

Copyright © 2023, J. Robert Michael, PhD. All rights reserved.
"""

from typing import List, Tuple

from prometheus_client.registry import Collector
from prometheus_client.core import GaugeMetricFamily

#-------------------------------------------------------------------------------
class TurretGauge(GaugeMetricFamily):
    """Basic Gauge."""
    #---------------------------------------------------------------------------
    def __init__(self, name="", documentation="", label=""):
        """Initialization."""
        super().__init__(name, documentation, labels=[label])

    #---------------------------------------------------------------------------
    def createCollector(self, gaugeMetrics: List[Tuple[str, float]]):
        """Create a collector from the acquire step."""
        for key, value in gaugeMetrics:
            self.add_metric([key], value)

#-------------------------------------------------------------------------------
class Turret(Collector):
    """Basic turret."""
    #---------------------------------------------------------------------------
    def __init__(self):
        """Initialization."""
        self.gauges = {}  # str -> TurretGauge
        self.metrics = {} # str -> List[Tuple[str, float]]

    #---------------------------------------------------------------------------
    def acquire(self):
        """Overridable function which creates self.gauges and self.metrics."""

        raise NotImplementedError

    #---------------------------------------------------------------------------
    def collect(self):
        """Basic Collector.collect method. Calls acquire to get gauges and
        metrics, then creates and yields each gauge.
        """
        self.acquire()

        for name, gauge in self.gauges.items():
            gaugeMetrics = self.metrics[name]
            gauge.createCollector(gaugeMetrics)

        for name, gauge in self.gauges.items():
            yield gauge

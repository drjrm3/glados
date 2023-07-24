#!/usr/bin/env python3
""" Test basic utilities for glados. """

import unittest as ut
from glados import turrets

from prometheus_client.metrics_core import GaugeMetricFamily

import numpy as np

#-------------------------------------------------------------------------------
def sampleDebugger(sample):
    """ Print out all attributes of a sample for debugging. """
    print("*** SAMPLE ***")
    for k in [d for d in sample.__dir__() if not d.startswith("_")]:
        v = getattr(sample, k)
        print(f"{k}: '{v}' ({type(k)}: {type(v)}))")

#-------------------------------------------------------------------------------
def metricDebugger(metric):
    """ Print out all attributes of a metric for debugging. """
    print("*** METRIC ***")
    for k, v in metric.__dict__.items():
        print(f"{k}: '{v}' ({type(k)}: {type(v)}))")

#-------------------------------------------------------------------------------
class TestCpuStatsTurret(ut.TestCase):
    #---------------------------------------------------------------------------
    def setUp(self):
        self.turretFactory = turrets.CpuStatsTurret.CpuStatsTurret

    #---------------------------------------------------------------------------
    # TODO: Move this into a more modular Turret tester to avoid reuse.
    def testCreation(self):
        """ Create the basic Turret class for now. """
        self.turretFactory()

    #---------------------------------------------------------------------------
    # TODO: Move this into a more modular Turret tester to avoid reuse.
    def testCollectionGenerics(self):
        """ Generic turret tests. """
        turret = self.turretFactory()
        metric = next(turret.collect())
        metricDebugger(metric)
        self.assertEqual(metric.type, "gauge")
        self.assertIsInstance(metric, GaugeMetricFamily)

    #---------------------------------------------------------------------------
    def testCollectionSpecifics(self):
        """ Test collection of the turret. """
        turret = self.turretFactory()

        numCores = 0
        speeds = []
        vcores = []
        for sample in next(turret.collect()).samples:
            sampleDebugger(sample)
            numCores += 1
            self.assertEqual(sorted(sample.labels.keys()), ["host", "vcore"])
            speeds.append(float(sample.value))
            vcores.append(int(sample.labels['vcore']))
        print(speeds)
        print(min(speeds), np.mean(speeds), max(speeds))
        self.assertEqual(vcores, list(range(numCores)))
        self.assertLess(0.0, min(speeds))
        self.assertGreater(10.0, max(speeds))

#-------------------------------------------------------------------------------
class TestStorageUsageTurret(ut.TestCase):
    #---------------------------------------------------------------------------
    def setUp(self):
        self.turretFactory = turrets.StorageTurret.StorageUsageTurret

    #---------------------------------------------------------------------------
    # TODO: Move this into a more modular Turret tester to avoid reuse.
    def testCreation(self):
        """ Create the basic Turret class for now. """
        self.turretFactory()

    #---------------------------------------------------------------------------
    # TODO: Move this into a more modular Turret tester to avoid reuse.
    def testCollectionGenerics(self):
        """ Generic turret tests. """
        turret = self.turretFactory()
        metric = next(turret.collect())
        self.assertEqual(metric.type, "gauge")
        self.assertIsInstance(metric, GaugeMetricFamily)
        #for k, v in metric.__dict__.items():
        #    print(f"{k}: '{v}' ({type(k)}: {type(v)}))")

    #---------------------------------------------------------------------------
    def testCollectionSpecifics(self):
        """ Test collection of the turret. """
        turret = self.turretFactory()

        g = turret.collect()
        allMetrics = next(g)

        mnts = [] # Mounts.
        pcts = [] # Percentage disk utilization.
        avails = [] # GB availability.

        for sample in allMetrics.samples:
            mnts.append(sample.labels["mnt"])
            metric = sample.labels["metric"]
            if metric == "usePct":
                pcts.append(sample.value)
            elif metric == "availGB":
                avails.append(sample.value)

        mnts = list(set(mnts))

        self.assertTrue(all("/" in mnt for mnt in mnts))
        self.assertTrue(all(float(pct) < 100. for pct in pcts))
        self.assertTrue(all(float(avail) > 0. for avail in avails))

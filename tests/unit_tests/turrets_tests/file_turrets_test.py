#!/usr/bin/env python3
""" Test file based turrets for glados. """

import unittest as ut
import os.path as op
from os.path import exists as ope, dirname as opd, join as opj
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
class TestGoveeTurret(ut.TestCase):
    #---------------------------------------------------------------------------
    def setUp(self):
        self.turretFactory = turrets.JsonTurret.JsonTurret
        testDataDir = opj(opd(opd(op.realpath(__file__))), "data")
        self.testFileName = opj(testDataDir, "goveeSensor.json")

    #---------------------------------------------------------------------------
    # TODO: Move this into a more modular Turret tester to avoid reuse.
    def testCreation(self):
        """ Create the basic Turret class for now. """
        self.turretFactory(self.testFileName)

    #---------------------------------------------------------------------------
    # TODO: Move this into a more modular Turret tester to avoid reuse.
    def testCollectionGenerics(self):
        """ Generic turret tests. """
        turret = self.turretFactory(self.testFileName)
        metric = next(turret.collect())
        metricDebugger(metric)
        self.assertEqual(metric.type, "gauge")
        self.assertIsInstance(metric, GaugeMetricFamily)

    #---------------------------------------------------------------------------
    def testCollectionSpecifics(self):
        """ Test collection of the turret. """
        turret = self.turretFactory(self.testFileName)

        g = turret.collect()
        allMetrics = next(g)
        print(allMetrics)
        for sample in allMetrics.samples:
            print(sample)

        locations = []    # Rooms being measured.
        humidities = []   # Humidities.
        temperatures = [] # Temperatures.

        for sample in allMetrics.samples:
            locations.append(sample.labels["location"])
            metric = sample.labels["metric"]
            if metric == "humidity":
                humidities.append(sample.value)
            elif metric == "temp":
                temperatures.append(sample.value)

        self.assertTrue(all("room" in loc for loc in locations))
        self.assertEqual(humidities, [44.2, 45.3, 47.0])
        self.assertEqual(temperatures, [24.0, 25.9, 31.6])

#-------------------------------------------------------------------------------
class TestNvidiaFileTurret(ut.TestCase):
    #---------------------------------------------------------------------------
    def setUp(self):
        self.hostname = "randomServer"
        self.turretFactory = turrets.NvidiaGpuTurret.NvidiaGpuTurret
        testDataDir = opj(opd(opd(op.realpath(__file__))), "data")
        self.testFileName = opj(testDataDir, self.hostname, "NvidiaGpu.turret")
        self.gsDict = {
            ('randomServer', 'device_0', 'usage_pct'): 0,
            ('randomServer', 'device_0', 'temperature'): 38,
            ('randomServer', 'device_0', 'power'): 18,
            ('randomServer', 'device_0', 'mem_use_mb'): 30,
            ('randomServer', 'device_0', 'mem_max_mb'): 8193,
            ('randomServer', 'device_1', 'usage_pct'): 5,
            ('randomServer', 'device_1', 'temperature'): 35,
            ('randomServer', 'device_1', 'power'): 20,
            ('randomServer', 'device_1', 'mem_use_mb'): 32,
            ('randomServer', 'device_1', 'mem_max_mb'): 8194
        }

    #---------------------------------------------------------------------------
    # TODO: Move this into a more modular Turret tester to avoid reuse.
    def testCreation(self):
        """ Create the basic Turret class for now. """
        self.turretFactory(self.testFileName, self.hostname)

    #---------------------------------------------------------------------------
    # TODO: Move this into a more modular Turret tester to avoid reuse.
    def testCollectionGenerics(self):
        """ Generic turret tests. """
        turret = self.turretFactory(self.testFileName, self.hostname)
        metric = next(turret.collect())
        metricDebugger(metric)
        self.assertEqual(metric.type, "gauge")
        self.assertIsInstance(metric, GaugeMetricFamily)

    #---------------------------------------------------------------------------
    def testCollectionSpecifics(self):
        """ Test collection of the turret. """
        turret = self.turretFactory(self.testFileName, self.hostname)

        g = turret.collect()
        allMetrics = next(g)
        atDict = {}
        for sample in allMetrics.samples:
            key = tuple(v for _, v in sample.labels.items())
            atDict[key] = sample.value

        self.assertDictEqual(self.gsDict, atDict)

#-------------------------------------------------------------------------------
class TestNegativesFileTurret(ut.TestCase):
    #---------------------------------------------------------------------------
    def setUp(self):
        self.hostname = "randomServer"
        self.turretFactory = turrets.NvidiaGpuTurret.NvidiaGpuTurret
        testDataDir = opj(opd(opd(op.realpath(__file__))), "data",)
        self.testFileName = opj(testDataDir, "Dumb.turret")

    #---------------------------------------------------------------------------
    def testFileNotFoundError(self):
        """Test that NvidiaSmiTurret raises file not found error."""
        with self.assertRaises(FileNotFoundError):
            self.turretFactory("foo")

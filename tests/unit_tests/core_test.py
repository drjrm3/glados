#!/usr/bin/env python3
""" Test basic utilities for glados. """

import glob
import os.path as op
import socket
import unittest as ut
import timeout_decorator
from timeout_decorator.timeout_decorator import TimeoutError

from glados.core import turretServer, getFileTurrets, getJsonTurrets

#-------------------------------------------------------------------------------
def getOpenPort() -> int:
    """ Get an open port.
    Taken from https://stackoverflow.com/questions/1365265
                      /on-localhost-how-do-i-pick-a-free-port-number
    """
    sock = socket.socket()
    sock.bind(('', 0))
    return sock.getsockname()[1]

#-------------------------------------------------------------------------------
class TestGetFileTurrets(ut.TestCase):
    """Test invocation of getFileTurrets function."""
    #---------------------------------------------------------------------------
    def setUp(self):
        self.testDataDir = op.join(op.dirname(op.realpath(__file__)), "data")

    #---------------------------------------------------------------------------
    def testGetFileTurrets(self):
        """Test finding correct file turrets."""
        turretFiles = glob.glob(self.testDataDir + "/randomServer/*")
        turrets = getFileTurrets(turretFiles)
        fxns = ["acquire", "addMetric", "_readFileInfo", "collect"]
        for turret in turrets:
            dirTurret = dir(turret)
            self.assertTrue(all([f in dirTurret for f in fxns]))

#-------------------------------------------------------------------------------
class TestGetJsonTurrets(ut.TestCase):
    """Test invocation of getJsonTurrets function."""
    #---------------------------------------------------------------------------
    def setUp(self):
        self.testDataDir = op.join(op.dirname(op.realpath(__file__)), "data")
        self.testFile = op.join(self.testDataDir, "goveeSensor.json")

    #---------------------------------------------------------------------------
    def testGetJsonTurret(self):
        """Test finding correct file turrets."""
        turretJsons = [self.testFile]
        turrets = getJsonTurrets(turretJsons)
        fxns = ["acquire", "addMetric", "_readFileInfo", "collect"]
        for turret in turrets:
            dirTurret = dir(turret)
            self.assertTrue(all([f in dirTurret for f in fxns]))

#-------------------------------------------------------------------------------
class TestTurretServer(ut.TestCase):
    """ Test invocations of turretServer. """
    #---------------------------------------------------------------------------
    def setUp(self):
        self.testDataDir = op.join(op.dirname(op.realpath(__file__)), "data")

    #---------------------------------------------------------------------------
    def testWrongPortType(self):
        """ Assert that the call fails without an integer (port) input. """
        with self.assertRaises(AssertionError):
            turretServer("foo")

    #---------------------------------------------------------------------------
    @timeout_decorator.timeout(0.25)
    def testHangingSuccessNoConfigs(self):
        """ Assert turretServer works by asserting a timeout error. """
        with self.assertRaises(TimeoutError):
            configFile = op.join(self.testDataDir, "config3.json")
            turretServer(2024, configFile=configFile)

    #---------------------------------------------------------------------------
    @timeout_decorator.timeout(1)
    def testPermissionDeniedError(self):
        """ Assert that we cannot run on a denied port. """
        with self.assertRaises(PermissionError):
            turretServer(22)

    #---------------------------------------------------------------------------
    @timeout_decorator.timeout(1)
    def testDuplicatePortError(self):
        """ Assert that we cannot run on a port already in use. """
        sock = socket.socket()
        sock.bind(('', 0))
        portNum = sock.getsockname()[1]
        with self.assertRaises(OSError):
            turretServer(portNum)

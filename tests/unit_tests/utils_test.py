#!/usr/bin/env python3
"""Test basic utilities for glados."""

import math
import os.path as op
import unittest as ut

from glados import utils

#-------------------------------------------------------------------------------
class TestStrToFloat(ut.TestCase):
    """Test invocations of strToFloat."""
    #---------------------------------------------------------------------------
    def testGoodStrs(self):
        """Test good examples of conversion."""
        kvs = {"1.5": 1.5, "1": 1.0, "five": math.nan}

        for gsKey, gsValue in kvs.items():
            atValue = utils.strToFloat(gsKey)
            if math.isnan(gsValue):
                self.assertTrue(math.isnan(atValue))
            else:
                self.assertEqual(gsValue, atValue)

#-------------------------------------------------------------------------------
class TestGetParamsFromConfig(ut.TestCase):
    """Test invocations of TestGetParamsFromConfig function."""
    #---------------------------------------------------------------------------
    def setUp(self):
        self.testDataDir = op.join(op.dirname(op.realpath(__file__)), "data")

    #---------------------------------------------------------------------------
    def testNoConfig(self):
        """Test default options from no file input."""
        gsParams = { "sleepTime": 5, "FileTurrets": [], "JsonTurrets": [] }
        params = utils.getParamsFromConfig()
        self.assertDictEqual(params, gsParams)

    #---------------------------------------------------------------------------
    def testConfig1(self):
        """Test that config1.json matches up."""
        gsParams = {"sleepTime": 5, "FileTurrets": [],
                    "JsonTurrets": ["./unit_tests/data/goveeSensor.json"]}
        config = op.join(self.testDataDir, "config1.json")
        print(type(config), config)
        params = utils.getParamsFromConfig(config)
        self.assertDictEqual(params, gsParams)

#-------------------------------------------------------------------------------
class TestRunCommand(ut.TestCase):
    """Test invocations of runCommand function."""
    #---------------------------------------------------------------------------
    def testCommandNotFound(self):
        """Assert that runCommand fails on command not found."""
        outStr, errStr, rCode = utils.runCommand("foo")
        self.assertEqual(outStr, "")
        self.assertEqual(errStr, "Command foo not found")
        self.assertEqual(rCode, 127)

    #---------------------------------------------------------------------------
    @ut.expectedFailure
    def testCommandNotStr(self):
        """Assert failure on calling runCommand with integer."""
        utils.runCommand(1)

    #---------------------------------------------------------------------------
    def testGoodCommand(self):
        """Test a good call to runCommand."""
        outStr, errStr, rCode = utils.runCommand("echo hello world")
        self.assertEqual(outStr, "hello world\n")
        self.assertEqual(errStr, "")
        self.assertEqual(rCode, 0)

    #---------------------------------------------------------------------------
    def testShellInjection(self):
        """Ensure runCommmand is RCE proof."""
        outStr, errStr, rCode = utils.runCommand("echo foo; touch RCEfailure")
        self.assertEqual(outStr, "foo; touch RCEfailure\n")
        self.assertEqual(errStr, "")
        self.assertEqual(rCode, 0)

#!/usr/bin/env python3
""" Test basic utilities for glados. """

import unittest as ut

from glados import utils

#-------------------------------------------------------------------------------
class TestRunCommand(ut.TestCase):
    """ Test invocations of runCommand function. """
    #---------------------------------------------------------------------------
    def testCommandNotFound(self):
        """ Assert that runCommand fails on command not found. """
        outStr, errStr, rCode = utils.runCommand("foo")
        self.assertEqual(outStr, "")
        self.assertEqual(errStr, "Command foo not found")
        self.assertEqual(rCode, 127)

    #---------------------------------------------------------------------------
    @ut.expectedFailure
    def testCommandNotStr(self):
        """ Assert failure on calling runCommand with integer. """
        utils.runCommand(1)

    #---------------------------------------------------------------------------
    def testGoodCommand(self):
        """ Test a good call to runCommand. """
        outStr, errStr, rCode = utils.runCommand("echo hello world")
        self.assertEqual(outStr, "hello world\n")
        self.assertEqual(errStr, "")
        self.assertEqual(rCode, 0)

    #---------------------------------------------------------------------------
    def testShellInjection(self):
        """ Ensure runCommmand is RCE proof. """
        outStr, errStr, rCode = utils.runCommand("echo foo; touch RCEfailure")
        self.assertEqual(outStr, "foo; touch RCEfailure\n")
        self.assertEqual(errStr, "")
        self.assertEqual(rCode, 0)

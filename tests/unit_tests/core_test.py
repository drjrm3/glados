#!/usr/bin/env python3
""" Test basic utilities for glados. """

import socket
import unittest as ut
import timeout_decorator
from timeout_decorator.timeout_decorator import TimeoutError

from glados.core import turretServer

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
class TestTurretServer(ut.TestCase):
    """ Test invocations of turretServer. """
    #---------------------------------------------------------------------------
    def testWrongPortType(self):
        """ Assert that the call fails without an integer (port) input. """
        with self.assertRaises(AssertionError):
            turretServer("foo")

    #---------------------------------------------------------------------------
    @timeout_decorator.timeout(0.25)
    def testHangingSuccess(self):
        """ Assert turretServer works by asserting a timeout error. """
        with self.assertRaises(TimeoutError):
            turretServer(2024)

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

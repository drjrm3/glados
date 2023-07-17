#!/usr/bin/env python3
""" Test basic utilities for glados. """

import unittest as ut
from collections.abc import Generator

from glados.turrets.Turret import Turret

#-------------------------------------------------------------------------------
class TestTurret(ut.TestCase):
    """ Test Basic Turret class functionality. """
    #---------------------------------------------------------------------------
    def testCreation(self):
        """ Create the basic Turret class for now. """
        _ = Turret

    #---------------------------------------------------------------------------
    def testAcquireNotImplementedError(self):
        """ Test NotImplementedError in acquire(). """

        with self.assertRaises(NotImplementedError):
            Turret().acquire()

    #---------------------------------------------------------------------------
    def testCollectNotImplementedError(self):
        """ Test NotImplementedError upon caling next() on collect() """
        # Generator. No raising of NotImplementedError until called.
        collector = Turret().collect()
        self.assertIsInstance(collector, Generator)
        with self.assertRaises(NotImplementedError):
            yield collector

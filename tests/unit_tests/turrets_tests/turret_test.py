#!/usr/bin/env python3
""" Test basic utilities for glados. """

import unittest as ut

from glados.turrets.Turret import Turret

#-------------------------------------------------------------------------------
class TestTurret(ut.TestCase):
    """ Test Basic Turret class functionality. """
    #---------------------------------------------------------------------------
    def testCreation(self):
        """ Create the basic Turret class for now. """
        turret = Turret

    #---------------------------------------------------------------------------
    def testAcquireHmmm(self):
        """
        One of 'acquire' or 'collect' must raise NotImplementedError which is to
        be used by the inheriting Turret to create metrics.
        The other should be doing the actual collection here.
        Not sure which one should be which yet.
        """
        with self.assertRaises(NotImplementedError):
            Turret().acquire()

    #---------------------------------------------------------------------------
    def testCollectHmmm(self):
        """
        One of 'acquire' or 'collect' must raise NotImplementedError which is to
        be used by the inheriting Turret to create metrics.
        The other should be doing the actual collection here.
        Not sure which one should be which yet.
        """
        with self.assertRaises(NotImplementedError):
            Turret().collect()

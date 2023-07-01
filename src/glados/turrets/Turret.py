#!/usr/bin/env python3
"""
CPU Stats Turret.

Copyright © 2023, J. Robert Michael, PhD. All rights reserved.
"""

from prometheus_client.registry import Collector

#-------------------------------------------------------------------------------
class Turret(Collector):
    """ Basic turret. """
    #---------------------------------------------------------------------------
    def __init__(self):
        """ Initialization. """

    #---------------------------------------------------------------------------
    def collect(self):
        """
        Basic Collector.collect method.

        In the future this should act as the specific collector method and
        being able to create a collector from json files.
        """
        self.acquire()

    def acquire(self):
        """
        More generalized Collector.collect method. In the future this will have
        the ability to read from json file, read output from looping script,
        possibly other implementations to aid in ease of use.

        For now this relies on the 'acquire' method being equal to 'collect'.
        """
        raise NotImplementedError

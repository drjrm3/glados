#!/usr/bin/env python3
"""
Initializaton for turrets module.

Copyright © 2023, J. Robert Michael, PhD. All rights reserved.
"""

import glob
from os.path import dirname as opd, basename as opb

turrets = []
for __tFile in [opb(f) for f in glob.glob(f"{opd(__file__)}/*Turret.py")]:
    #if pyFile.endswith("Turret.py") and not pyFile.starts:
    if __tFile != "Turret.py":
        __turret = __tFile.split(".")[0]
        turrets.append(__turret)

#!/usr/bin/env python3
"""
Nvidia GPU Stats Turret.
Monitor statistics from GPU using simple 'nvidia-smi'.

Copyright © 2023, J. Robert Michael, PhD. All rights reserved.
"""

from dataclasses import dataclass
from typing import List

from ..utils import runCommand
from .Turret import Turret
from .Turret import TurretGauge

#-------------------------------------------------------------------------------
@dataclass
class Device():
    """Data class for keeping Nvidia device information."""
    # TODO: Keep track of processes on this device.

    #---------------------------------------------------------------------------
    def __init__(self, nvSmiChunk: List[str]):
        """Define all data based on nvidia-smi device chunk. Expected format:
        |   0  NVIDIA GeForce ...  On   | 00000000:2A:00.0 Off |                  N/A |
        |  0%   38C    P8    18W / 220W |     30MiB /  8192MiB |      0%      Default |
        |                               |                      |                  N/A |
        """
        self.__sections = [""]
        keys = ["id", "fanSpeed", "temp", "pwr", "pwrMax", "memUse", "memMax",
                "usage"]
        for key in keys:
            setattr(self, key, -1)
        for key in ["perf", "busId"]:
            setattr(self, key, "")

        if not len(nvSmiChunk) == 4:
            print("[W] Passing on following NvSmiChunk:\n")
            for _line in nvSmiChunk:
                print(_line)
        else:
            self._processLine1(nvSmiChunk[1])
            self._processLine2(nvSmiChunk[2])
            # Don't do anything with line 3.

    #---------------------------------------------------------------------------
    def __str__(self) -> str:
        """String repr."""
        outStr = "\n"
        for key in ["id", "fanSpeed", "temp", "pwr", "pwrMax", "memUse",
                    "memMax", "usage"]:
            outStr += f"{key} = {getattr(self, key)}\n"
        return outStr

    #---------------------------------------------------------------------------
    def _getValue(self, section: int, word: int, remove="") -> str:
        """Get a value from a line in nvidia-smi.

        Args:
            section: The section of a nvidia-smi line gated by '|'.
            word: The token in that section.
            rep: What (if anything) to remove in that word.

        Returns: The value as a string.
        """

        return self.__sections[section].split()[word].replace(remove, "")

    #---------------------------------------------------------------------------
    def _processLine1(self, line: str):
        """Process the 1st line of an nvidia-smi device chunk. Expected format:
        |   0  NVIDIA GeForce ...  On   | 00000000:2A:00.0 Off |                  N/A |
        """
        self.__sections = line.split("|")
        self.id = int(self._getValue(1, 0))
        self.busId = self._getValue(2, 0)

    #---------------------------------------------------------------------------
    def _processLine2(self, line: str):
        """Process the 2nd line of an nvidia-smi device chunk. Expected format:
        |  0%   38C    P8    18W / 220W |     30MiB /  8192MiB |      0%      Default |
        """
        self.__sections = line.split("|")

        # First section.
        self.fanSpeed = int(self._getValue(1, 0, "%"))
        self.temp = int(self._getValue(1, 1, "C"))
        self.perf = self._getValue(1, 2)
        self.pwr = int(self._getValue(1, 3, "W"))
        self.pwrMax = int(self._getValue(1, 5, "W"))

        # Second section.
        self.memUse = int(self._getValue(2, 0, "MiB"))
        self.memMax = int(self._getValue(2, 2, "MiB"))
        self.usage = int(self._getValue(3, 0, "%"))

#-------------------------------------------------------------------------------
class NvInfo():
    """Nvidia Information class based on 'nvidia-smi' output. """
    #---------------------------------------------------------------------------
    def __init__(self, nvSmiOut: str):
        """Initialize NvInfo data from nvidia-smi output.

        Args:
            nvSmiOut: Output of running `nvidia-smi`.
        """
        self.date = ""
        self.driverVersion = ""
        self.cudaVersion = ""
        self.nGpus = -1
        self.devs = {}

        nvSmiLines = nvSmiOut.split("\n   ")[0].splitlines()

        self.date = nvSmiLines.pop(0).strip()
        self._handleHeader(nvSmiLines.pop(1))
        nvSmiLines.pop(-1)

        idx = min(i for i, _line in enumerate(nvSmiLines) if "|===" in _line)
        nvSmiLines = nvSmiLines[idx:]
        for i in range(0, len(nvSmiLines), 4):
            chunk = nvSmiLines[i: i + 4]
            dev = Device(chunk)
            self.devs[dev.id] = dev

    #---------------------------------------------------------------------------
    def _handleHeader(self, hLine: str):
        """ Process the header line. """
        self.driverVerion = hLine.split("Driver Version:")[0].split()[0].strip()
        self.cudaVerion = hLine.split("CUDA Version:")[0].split()[0].strip()

#-------------------------------------------------------------------------------
class NvidiaGpuTurret(Turret):
    """NvidiaGpu Usage statistics."""
    #---------------------------------------------------------------------------
    def __init__(self, file="", hostname=""):
        """Initialization."""
        super().__init__(file, hostname)
        self._turretFileInfo = ""
        self.nvInfo = self._readNvInfo()

    #---------------------------------------------------------------------------
    def _readNvInfo(self) -> NvInfo:
        """Read nvidia-smi."""
        if self._fileName:
            self._readFileInfo()
        else:
            outStr, _errStr, returnCode = runCommand("nvidia-smi")
            assert returnCode == 0
            self._turretFileInfo = outStr

        return NvInfo(self._turretFileInfo)

    #---------------------------------------------------------------------------
    def acquire(self):
        """Acquire storage stats and call collector."""
        nvInfo = self._readNvInfo()

        self.gauge = TurretGauge(
                f"gpu_metrics_{self.hostname}", "Multiple GPU metrics",
                ["host", "device", "metric"]
            )

        for devId, device in nvInfo.devs.items():
            devName = f"device_{devId}"
            self.addMetric([self.hostname, devName, "usage_pct"], device.usage)
            self.addMetric([self.hostname, devName, "temperature"], device.temp)
            self.addMetric([self.hostname, devName, "power"], device.pwr)
            self.addMetric([self.hostname, devName, "mem_use_mb"], device.memUse)
            self.addMetric([self.hostname, devName, "mem_max_mb"], device.memMax)

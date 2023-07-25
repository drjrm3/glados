#!/usr/bin/env python3
"""
Nvidia GPU Stats Turret.
Monitor statistics from GPU using simple 'nvidia-smi'.

Copyright © 2023, J. Robert Michael, PhD. All rights reserved.
"""

from dataclasses import dataclass
import math
from typing import Dict, List

from ..utils import runCommand, strToFloat
from .Turret import Turret
from .Turret import TurretGauge

#-------------------------------------------------------------------------------
def rmStrDups(line: str) -> str:
    """Remove contiguous duplicates in a string.

    Args:
        line: Any string input.

    Returns:
        outStr: line with contiguous duplicates removed.
    """

    outStr = ""
    for char in line:
        if outStr and char == outStr[-1]:
            continue
        outStr = outStr + char

    return outStr

#-------------------------------------------------------------------------------
@dataclass
class Device:
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
        keys = [
            "id",
            "fanSpeed",
            "temp",
            "pwr",
            "pwrMax",
            "memUse",
            "memMax",
            "usage",
        ]
        for key in keys:
            setattr(self, key, math.nan)
        for key in ["perf", "busId"]:
            setattr(self, key, "")

        assert len(nvSmiChunk) == 4, "[E] len(nvSmiChunk) != 4"
        self._processLine1(nvSmiChunk[1])
        self._processLine2(nvSmiChunk[2])
        # Don't do anything with line 3.

    #---------------------------------------------------------------------------
    def __str__(self) -> str:
        """String repr."""
        outStr = "\n"
        for key in [
            "id",
            "fanSpeed",
            "temp",
            "pwr",
            "pwrMax",
            "memUse",
            "memMax",
            "usage",
        ]:
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
        self.fanSpeed = strToFloat(self._getValue(1, 0, "%"))
        self.temp = strToFloat(self._getValue(1, 1, "C"))
        self.perf = self._getValue(1, 2)
        self.pwr = strToFloat(self._getValue(1, 3, "W"))
        self.pwrMax = strToFloat(self._getValue(1, 5, "W"))

        # Second section.
        self.memUse = strToFloat(self._getValue(2, 0, "MiB"))
        self.memMax = strToFloat(self._getValue(2, 2, "MiB"))
        self.usage = strToFloat(self._getValue(3, 0, "%"))

#-------------------------------------------------------------------------------
def getNvChunks(nvSmiLines: List[str]) -> List[List[str]]:
    """Get chunks of nvidia-smi output for each device.

    Args:
        nvSmiLines: Output of nvidia-smi.

    Returns:
        chunks: chunks of 4 line lists, each defining a 'device' in nvidia-smi.
    """
    # Trim off everything before "|===" where each device information starts.
    startPos = min(i for i, _line in enumerate(nvSmiLines) if "|===" in _line)
    nvSmiLines = nvSmiLines[startPos:]

    # Get the indices of all cutoff points between devices.
    idxs = []
    for idx, line in enumerate(nvSmiLines):
        if rmStrDups(line) in ["+-+-+-+", "|=+=+=|"]:
            idxs.append(idx)
    idxs.append(len(nvSmiLines))

    # Loop through indices and get device chunks.
    chunks = []
    for i in range(len(idxs) - 1):
        idx1 = idxs[i]
        idx2 = idxs[i + 1]
        if idx2 - idx1 != 4:
            continue
        chunk = []
        for line in nvSmiLines[idx1:idx2]:
            chunk.append(line)
        chunks.append(chunk)

    return chunks

#-------------------------------------------------------------------------------
class NvInfo:
    """Nvidia Information class based on 'nvidia-smi' output."""
    #---------------------------------------------------------------------------
    def __init__(self, nvSmiOut: str):
        """Initialize NvInfo data from nvidia-smi output.

        Args:
            nvSmiOut: Output of running `nvidia-smi`.
        """
        self.date = ""
        self.driverVersion = ""
        self.cudaVersion = ""
        self.nGpus = math.nan
        self.devs: Dict[int, Device] = {}

        nvSmiLines = nvSmiOut.splitlines()
        chunks = getNvChunks(nvSmiLines)
        for chunk in chunks:
            dev = Device(chunk)
            self.devs[dev.id] = dev

        self.date = nvSmiLines.pop(0).strip()
        self._handleHeader(nvSmiLines.pop(1))

    #---------------------------------------------------------------------------
    def _handleHeader(self, hLine: str):
        """Process the header line."""
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

    #---------------------------------------------------------------------------
    def _readNvInfo(self) -> NvInfo:
        """Read nvidia-smi."""
        if self._fileName:
            self._readFileInfo()
        else:
            outStr, _, returnCode = runCommand("nvidia-smi")
            assert returnCode == 0
            self._turretFileInfo = outStr

        return NvInfo(self._turretFileInfo)

    #---------------------------------------------------------------------------
    def acquire(self):
        """Acquire storage stats and call collector."""
        nvInfo = self._readNvInfo()

        self.gauge = TurretGauge(
            f"gpu_metrics_{self.hostname}",
            "Multiple GPU metrics",
            ["host", "device", "metric"]
        )

        for devId, device in nvInfo.devs.items():
            devName = f"device_{devId}"
            self.addMetric([self.hostname, devName, "usage_pct"], device.usage)
            self.addMetric([self.hostname, devName, "temperature"], device.temp)
            self.addMetric([self.hostname, devName, "power"], device.pwr)
            self.addMetric([self.hostname, devName, "mem_use_mb"], device.memUse)
            self.addMetric([self.hostname, devName, "mem_max_mb"], device.memMax)

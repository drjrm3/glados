#!/usr/bin/env python3
"""
Get diff score upon running black.

Copyright © 2023 J. Robert Michael, PhD. All rights reserved.
"""

import subprocess
from subprocess import PIPE
import shlex
from typing import Dict, List, Tuple

#-------------------------------------------------------------------------------
def runBlack() -> Tuple[str, str, int]:
    """Run black on hardocded dirrectory '../src/black' and get the diff."""

    cmd = shlex.split("black -l 80 --diff ../src/glados")

    proc = subprocess.run(cmd, stdout=PIPE, stderr=PIPE, shell=False, check=True)

    outStr = proc.stdout.decode("utf-8") if proc.stdout else ""
    errStr = proc.stderr.decode("utf-8") if proc.stderr else ""
    returnCode = proc.returncode

    return outStr, errStr, returnCode

#-------------------------------------------------------------------------------
def getDiffChunks(diffOut: str) -> Dict[Tuple[str, str], List[str]]:
    """Read a .diff file and return a list of diff chunks.

    Args:
        diffFile: Contents of diffFile.

    Returns:
        diffChunks: Dictionary of diff chunks.
            key: (fileName, position)
            val: List of strings in diff chunk.
    """

    diffChunks = {}
    fileName = ""
    key = ("", "")
    chunkLines = []

    for line in diffOut.splitlines():
        # Get the file for this chunk.
        if line.startswith("---"):
            fileName = line.split()[1]
            continue
        if line.startswith("+++"):
            assert line.split()[1] == fileName
            continue

        # Get the diff section for this chunk.
        if line.startswith("@@"):
            # Save old chunkLines
            if any([l.startswith("+") for l in chunkLines]):
                diffChunks[key] = chunkLines
            chunkLines = []

            # Create new key.
            pos = line.strip()
            key = (fileName, pos)
            diffChunks[key] = []
            continue

        # Put all of found ilnes in this diffChunk.
        chunkLines.append(line)

    return diffChunks

#-------------------------------------------------------------------------------
def runSedBlack() -> Tuple[str, str, int]:
    """Run the sedBlack.sh script.
    TODO: Replace this with pure python!
    """

    cmd = shlex.split("./sedBlack.sh")

    proc = subprocess.run(cmd, stdout=PIPE, stderr=PIPE, shell=False, check=True)

    outStr = proc.stdout.decode("utf-8") if proc.stdout else ""
    errStr = proc.stderr.decode("utf-8") if proc.stderr else ""
    returnCode = proc.returncode

    return outStr, errStr, returnCode

#-------------------------------------------------------------------------------
def main():
    """Main routine."""
    blkDiffOut0, _blkDiffErr0, blkDiffRc0 = runBlack()
    assert blkDiffRc0 == 0, f"ERROR: black RC = {blkDiffRc0}"
    with open("black.diff0", "w") as fout:
        print(blkDiffOut0, file=fout)

    blkDiffOut1, _blkDiffErr1, blkDiffRc1 = runSedBlack()
    assert blkDiffRc1 == 0, f"ERROR: black RC = {blkDiffRc1}"
    
    chunks = getDiffChunks(blkDiffOut1)
    # POC to ensure this works as intended.
    for key, val in chunks.items():
        if len(val) > 3:
            print(f"--- {key[0]}")
            print(f"+++ {key[0]}")
            print(f"{key[1]}")
            for line in val:
                print(line)

#-------------------------------------------------------------------------------
if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import os
from setuptools import setup, find_packages
from src.glados.__init__ import __version__

with open("requirements.txt", "r", encoding="UTF-8") as finp:
    required = finp.read().splitlines()

setup(name="glados",
      version=__version__,
      description="Generic Load AuDiting Of Servers.",
      author="J. Robert Michael, PhD",
      author_email="j.robert.michael@gmail.com",
      install_requires=required,
      scripts=[f"bin/{f}" for f in os.listdir("bin")],
      package_dir={"": "src"},
      packages=find_packages("src"),
      zip_safe=False)

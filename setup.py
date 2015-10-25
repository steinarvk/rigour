#!/usr/bin/env python

from distutils.core import setup

setup(name="rigour",
      version="1.0",
      description="JSON validation and decoding library",
      author="Steinar V. Kaldager",
      author_email="steinarvk@google.com",
      url="https://github.com/steinarvk/rigour",
      packages=["rigour"],
      requires=["dateutil"],
)

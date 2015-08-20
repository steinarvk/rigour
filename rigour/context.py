from __future__ import absolute_import

from rigour.errors import ValidationFailed

import contextlib

@contextlib.contextmanager
def contained_as(suffix):
  try:
    yield
  except ValidationFailed as e:
    e.context.insert(0, suffix)
    raise

@contextlib.contextmanager
def member(name):
  with contained_as("." + name):
    yield

@contextlib.contextmanager
def index(key):
  with contained_as("[" + str(key) + "]"):
    yield


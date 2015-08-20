from __future__ import absolute_import

from rigour.errors import (ValidationFailed, ProgrammingError)
from rigour.util import run_check

def from_json(t, value):
  try:
    rv = t.from_json(value)
  except ValueError as e:
    raise ValidationFailed(e.message)
  run_check(t.check, rv)
  return rv

def to_json(t, value):
  run_check(t.check, value)
  return t.to_json(value)

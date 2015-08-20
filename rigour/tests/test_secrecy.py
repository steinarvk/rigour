from __future__ import absolute_import

from rigour.errors import ValidationFailed
from rigour.types import *
from rigour.constraints import length_between
import rigour

import pytest

def test_secrecy_declared_before():
  t = String().secret().constrain(length_between(4,6))
  with pytest.raises(ValidationFailed) as excinfo:
    t.check("xxx")
  message = str(excinfo)
  assert "xxx" not in message

def test_secrecy_declared_after():
  t = String().constrain(length_between(4,6)).secret()
  with pytest.raises(ValidationFailed) as excinfo:
    t.check("xxx")
  message = str(excinfo)
  assert "xxx" not in message

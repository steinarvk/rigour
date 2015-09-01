# Copyright 2015 Google Inc.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#      http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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

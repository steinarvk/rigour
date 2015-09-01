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

from rigour.errors import ProgrammingError, ValidationFailed

def run_check(f, value):
  """Runs a check on a value.

  This function is used to guard against the easily made mistake of
  providing a constraint that signals an error by returning a value,
  instead of raising an exception if the check fails.

  This error would otherwise cause an invalid value to be erroneously
  passed through as valid.
  """
  try:
    rv = f(value)
  except ValidationFailed as e:
    if e.value is None:
      e.value = value
    raise
  if rv is not None:
    message = "checker {} should not be returning a value, but returned {}"
    raise ProgrammingError(message.format(f, rv))

def assert_type(t):
  """Verifies that a variable is a JsonType.

  This guards against the potential confusion between a JsonType and
  a callable that will _produce_ a JsonType.
  """
  if not isinstance(t, JsonType):
    raise ProgrammingError("expected {} to be a JsonType")

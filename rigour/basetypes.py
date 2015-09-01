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

from rigour.util import run_check
from rigour.errors import ValidationFailed

class JsonType(object):
  def _name(self, depth):
    return "<anonymous type>"

  def _check(self, value):
    pass

  def constrain(self, *checkers):
    return Constrained(self, *checkers)

  def is_secret(self):
    return False

  def is_required(self):
    return True

  def optional(self):
    return Optional(self)

  def secret(self):
    return Secret(self)

  def name(self, depth):
    return self._name(depth)

  def to_json(self, value):
    if not self.is_required() and value is None:
      return None
    return self._to_json(value)

  def from_json(self, value):
    if not self.is_required() and value is None:
      return None
    return self._from_json(value)

  def check(self, value):
    if value is None:
      if not self.is_required():
        return
      raise ValidationFailed("missing")
    try:
      self._check(value)
    except ValidationFailed as e:
      if self.is_secret():
        e.secret = True
      raise

class _ModifierType(JsonType):
  def __init__(self, t):
    self._t = t

  def _name(self, depth):
    return self._t.name(depth)

  def _to_json(self, value):
    return self._t.to_json(value)

  def _from_json(self, json_value):
    return self._t.from_json(json_value)

  def is_required(self):
    return self._t.is_required()

  def is_secret(self):
    return self._t.is_secret()

  def _check(self, value):
    return run_check(self._t.check, value)

class Optional(_ModifierType):
  def __init__(self, t):
    _ModifierType.__init__(self, t)

  def is_required(self):
    return False

class Secret(_ModifierType):
  def __init__(self, t):
    _ModifierType.__init__(self, t)

  def is_secret(self):
    return True

class Constrained(_ModifierType):
  def __init__(self, t, *checkers):
    _ModifierType.__init__(self, t)
    self._checkers = checkers

  def _check(self, value):
    for checker in self._checkers:
      try:
        run_check(checker, value)
      except ValidationFailed as e:
        if e.value is None:
          e.value = value
        raise
    _ModifierType._check(self, value)

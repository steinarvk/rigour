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
from rigour.basetypes import JsonType

import dateutil.parser
import datetime
import re
import sys

class _SimpleType(JsonType):
  def __init__(self, python_type, type_name=None):
    self._python_type = python_type
    self._type_name = type_name or python_type.__name__

  def _name(self, depth):
    return self._type_name

  def _check(self, value):
    if not isinstance(value, self._python_type):
      raise ValidationFailed("expected " + self._type_name, value=value)

  def _to_json(self, value):
    return value

  def _from_json(self, value):
    return value

class String(_SimpleType):
  def __init__(self):
    if sys.version_info.major == 2:
      types = (unicode, str)
    else:
      types = (str,)
    _SimpleType.__init__(self, types, "string")

class Integer(_SimpleType):
  def __init__(self):
    if sys.version_info.major == 2:
      types = (int, long)
    else:
      types = (int,)
    _SimpleType.__init__(self, types, "integer")

class Float(_SimpleType):
  def __init__(self):
    if sys.version_info.major == 2:
      types = (float, int, long)
    else:
      types = (float, int)
    _SimpleType.__init__(self, types, "floating-point")

class StringEnum(JsonType):
  def __init__(self, *choices):
    self._choices = choices

  def _name(self, depth):
    return "{" + " | ".join(self._choices) + "}"

  def _check(self, value):
    if value not in self._choices:
      raise ValidationFailed("expected one of: {}".format(self._choices))

  def _from_json(self, value):
    return value

  def _to_json(self, value):
    return value

class Datetime(JsonType):
  def _name(self, depth):
    return "datetime"

  def _check(self, value):
    if not isinstance(value, datetime.datetime):
      raise ValidationFailed("expected datetime", value=value)
    if not value.tzinfo:
      raise ValidationFailed("expected datetime with time-zone", value=value)

  def _to_json(self, value):
    return value.isoformat()

  def _from_json(self, json_string):
    try:
      return dateutil.parser.parse(json_string)
    except ValueError as e:
      message = "failed to parse datetime: {}".format(e.message)
      raise ValidationFailed(message, value=json_string)

class Date(JsonType):
  _date_pattern = re.compile(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})")

  def _name(self, depth):
    return "date"

  def _check(self, value):
    if not isinstance(value, datetime.date):
      raise ValidationFailed("expected date", value=value)

  def _to_json(self, value):
    return value.isoformat()

  def _from_json(self, json_string):
    m = Date._date_pattern.match(json_string)
    if not m:
      raise ValidationFailed("expected date of format YYYY-MM-DD")
    year = int(m.group("year"))
    month = int(m.group("month"))
    day = int(m.group("day"))
    try:
      return datetime.date(year, month, day)
    except ValueError as e:
      raise ValidationError(e.message)

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
from __future__ import print_function

from rigour.errors import ValidationFailed
from rigour.tests.schema import Request
import rigour

import pytest

def test_basic_valid():
  req = {
    "username": "svk",
    "password": "hunter2",
  }
  val = rigour.from_json(Request, req)
  assert val.username == "svk"
  assert val.password == "hunter2"

def test_basic_invalid():
  req = {
    "username": "x",
    "password": "hunter2",
  }
  with pytest.raises(ValidationFailed) as excinfo:
    rigour.from_json(Request, req)
  message = str(excinfo)
  print(message)
  assert "username:" in message
  assert "too short" in message
  assert "value was: 'x'" in message

def test_secret_invalid():
  req = {
    "username": "svk",
    "password": "hunt",
  }
  with pytest.raises(ValidationFailed) as excinfo:
    rigour.from_json(Request, req)
  message = str(excinfo)
  print(message)
  assert "password:" in message
  assert "too short" in message
  assert "hunt" not in message
  assert "value was: <elided>" in message

def test_nested_fields():
  req = {
    "username": "buffy",
    "password": "slayer",
    "name": {
      "given_name": "Buffy",
      "middle_name": "Anne",
      "family_name": "Summers",
    },
  }
  val = rigour.from_json(Request, req)
  assert val.name.given_name == "Buffy"
  assert val.name.middle_name == "Anne"
  assert val.name.family_name == "Summers"

def test_required_nested_field():
  req = {
    "username": "harald",
    "password": "Rex999",
    "name": {
      "given_name": "Harald",
    },
  }
  with pytest.raises(ValidationFailed) as excinfo:
    rigour.from_json(Request, req)
  message = str(excinfo)
  print(message)
  assert "name: missing field 'family_name'" in message

def test_string_enum_valid():
  req = {
    "username": "sonja",
    "password": "123456",
    "gender": "female",
  }
  val = rigour.from_json(Request, req)
  assert val.gender == "female"

def test_string_enum_invalid():
  req = {
    "username": "sonja",
    "password": "123456",
    "gender": "femal3",
  }
  with pytest.raises(ValidationFailed) as excinfo:
    rigour.from_json(Request, req)
  message = str(excinfo)
  print(message)
  assert "gender:" in message
  assert "femal3" in message
  assert "female" in message

def test_luhn_validation():
  req = {
    "username": "sonja",
    "password": "123456",
    "payment_info": {
      "card_number": "1234-5678-9012-3456",
    }
  }
  with pytest.raises(ValidationFailed) as excinfo:
    rigour.from_json(Request, req)
  message = str(excinfo)
  print(message)
  assert "invalid check digit" in message

def test_array():
  req = {
    "username": "svk",
    "password": "hunter2",
    "titles": ["Programmer"],
  }
  val = rigour.from_json(Request, req)
  assert val.titles == ["Programmer"]

def test_array_with_wrong_type():
  req = {
    "username": "svk",
    "password": "hunter2",
    "titles": ["Programmer", 42],
  }
  with pytest.raises(ValidationFailed) as excinfo:
    rigour.from_json(Request, req)
  message = str(excinfo)
  print(message)
  assert "expected string" in message

def test_fixed_array_valid():
  req = {
    "username": "svk",
    "password": "hunter2",
    "position": [123, 456],
  }
  val = rigour.from_json(Request, req)
  assert val.position[0] == 123
  assert val.position[1] == 456

def test_fixed_array_wrong_length():
  req = {
    "username": "svk",
    "password": "hunter2",
    "position": [123, 456, 789],
  }
  with pytest.raises(ValidationFailed) as excinfo:
    rigour.from_json(Request, req)
  message = str(excinfo)
  print(message)
  assert "expected 2 elements, got 3" in message

def test_full_type_name():
  name = Request.name(float("inf"))
  assert "position" in name
  assert "given_name" in name
  assert "card_number" in name
  assert "female" in name

def test_birthdate():
  req = {
    "username": "harald",
    "password": "Rex999",
    "birthdate": "1937-02-21",
  }
  val = rigour.from_json(Request, req)
  assert val.birthdate.year == 1937
  assert val.birthdate.month == 2
  assert val.birthdate.day == 21

def test_timestamp():
  req = {
    "username": "harald",
    "password": "Rex999",
    "timestamp": "2015-08-20T01:58:42.205677 UTC"
  }
  val = rigour.from_json(Request, req)
  assert val.timestamp.year == 2015
  assert val.timestamp.second == 42
  assert val.timestamp.tzinfo
  
def test_basic_roundtrip():
  req = {
    "username": "harald",
    "password": "hunter2",
    "birthdate": "1937-02-21",
    "timestamp": "2015-08-20T01:58:42.205677+00:00",
    "titles": ["Programmer"],
    "payment_info": {
      "card_number": "4111-1111-1111-1111",
    },
    "name": {
      "given_name": "Harald",
      "family_name": "Rex",
    },
    "position": [123, 456],
    "gender": "male",
  }
  val = rigour.from_json(Request, req)
  js = rigour.to_json(Request, val)
  assert req == js

def test_nonexistent():
  req = {
    "username": "svk",
    "password": "hunter2",
    "this_field_does_not_exist": 42,
  }
  with pytest.raises(ValidationFailed) as excinfo:
    rigour.from_json(Request, req)
  message = str(excinfo)
  print(message)
  assert "'this_field_does_not_exist'" in message

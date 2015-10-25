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

from rigour.types import *
from rigour.constraints import (length_between, matches_regex)

class CardNumber(JsonType):
  _regex_pattern = re.compile(r"\d{4}-\d{4}-\d{4}-\d{4}")

  def from_json(self, value):
    if not CardNumber._regex_pattern.match(value):
      raise ValidationFailed("badly formatted card number")
    return "".join(value.split("-"))

  def to_json(self, s):
    return "{}-{}-{}-{}".format(s[:4], s[4:8], s[8:12], s[12:])

  def check(self, s):
    if not isinstance(s, str):
      raise ValidationFailed("expected string")
    if not s.isdigit() or len(s) != 16:
      raise ValidationFailed("invalid card number")

def luhn_algorithm(number):
  """An example domain-specific checker, the Luhn check digit algorithm."""
  if not number.isdigit():
    raise ValidationFailed("expected a purely numeric string")
  digits = list(map(int, number))
  v = sum(digits[-1::-2]) + sum(sum(map(int,str(2*x))) for x in digits[-2::-2])
  if v % 10:
    raise ValidationFailed("invalid check digit")

Request = Object(
  username = String().constrain(length_between(2,32)),
  password = String().secret().constrain(length_between(6,256)),
  name = Object(
    given_name = String().constrain(
      length_between(1,64), matches_regex(r"^[A-Z][a-z]*"),
    ),
    family_name = String().constrain(length_between(1,64)),
    middle_name = String().optional().constrain(length_between(1,64)),
  ).optional(),
  titles = Array(String()).optional(),
  position = FixArray(Float(), Float()).optional(),
  birthdate = Date().optional(),
  gender = StringEnum("male", "female", "other").optional(),
  timestamp = Datetime().optional(),
  payment_info = Object(
    card_number = CardNumber().constrain(luhn_algorithm),
  ).secret().optional(),
  extra = Any().optional(),
)

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

import re

def length_between(min_, max_):
  def f(xs):
    l = len(xs)
    if l < min_:
      message = "too short ({} is below threshold {})".format(l, min_)
      raise ValidationFailed(message)
    if l > max_:
      message = "too long ({} exceeds limit of {})".format(l, max_)
      raise ValidationFailed(message)
  return f

def matches_regex(regex, description=None):
  requirement = description or "string matching '{}'".format(regex)
  regex = re.compile("^" + regex + "$")
  def f(s):
    if not regex.match(s):
      raise ValidationFailed("expected {}".format(requirement))
  return f

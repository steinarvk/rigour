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

class ProgrammingError(Exception):
  pass

class ValidationFailed(Exception):
  def __init__(self, message, value=None, context=(), secret=False):
    self.message = message
    self.value = value
    self.context = list(context)
    self.secret = secret

  def show_value(self, show_secrets):
    if self.secret and not show_secrets:
      return "<elided>"
    elif self.value:
      return repr(self.value)

  def show_context(self):
    if self.context:
      rv = "".join(map(str, self.context))
      if rv.startswith("."):
        rv = rv[1:]
      return rv

  def format(self, show_secrets=False):
    ctx = self.show_context() or ""
    val = self.show_value(show_secrets) or ""
    rv = []
    if ctx:
      rv.append("{}: ".format(ctx))
    rv.append(self.message)
    if val:
      rv.append(", value was: {}".format(val))
    return "".join(rv)
  
  def __str__(self):
    return self.format()

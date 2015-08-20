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

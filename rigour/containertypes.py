from __future__ import absolute_import

from rigour.basetypes import JsonType
from rigour.errors import ValidationFailed
from rigour.util import run_check

from rigour import context

class FixArray(JsonType):
  def __init__(self, *fields):
    self._fields = fields

  def _name(self, depth):
    return "[" + ", ".join(field.name(depth) for field in self._fields) + "]"

  def _check(self, value):
    if len(value) != len(self._fields):
      msg = "expected {} elements, got {}".format(len(self._fields), len(value))
      raise ValidationFailed(msg, value=value)
    for i, (t, el) in enumerate(zip(self._fields, value)):
      with context.index(i):
        run_check(t.check, el)

  def _to_json(self, value):
    return [t.to_json(el) for (t, el) in zip(self._fields, value)]

  def _from_json(self, json_value):
    if len(json_value) != len(self._fields):
      message = "expected {} elements, got {}".format(
        len(self._fields), len(json_value))
      raise ValidationFailed(message)
    rv = []
    for i, (t, el) in enumerate(zip(self._fields, json_value)):
      with context.index(i):
        rv.append(t.from_json(el))
    return rv

class Array(JsonType):
  def __init__(self, t):
    self._t = t

  def _name(self, depth):
    return "[" + self._t.name(depth) + "..]"

  def _check(self, value):
    for i, el in enumerate(value):
      with context.index(i):
        run_check(self._t.check, el)

  def _to_json(self, value):
    return [self._t.to_json(x) for x in value]

  def _from_json(self, value):
    rv = []
    for i, x in enumerate(value):
      with context.index(i):
        rv.append(self._t.from_json(x))
    return rv

class Object(JsonType):
  def __init__(self, **fields):
    self._fields = fields
  
  def _name(self, depth):
    if depth <= 0:
      return "Object"
    return "{" + ", ".join("{}: {}".format(n, t.name(depth-1)) for (n,t) in self._fields.items()) + "}"

  def _from_json(outer_self, value):
    class ObjectAccessor(dict):
      def __getattr__(self, name):
        if name in outer_self._fields:
          return self.get(name)
        else:
          raise AttributeError("no such attribute: " + name)
      
      def __setattr__(self, name, value):
        if name in outer_self._fields:
          self[name] = value
        else:
          raise AttributeError("no such attribute: " + name)

      def __delattr__(self, name):
        if name in outer_self._fields:
          if name in self:
            del self[name]
        else:
          raise AttributeError("no such attribute: " + name)

      def __repr__(self):
        return "[Object: {}]".format(outer_self.name(1))
    for name in value:
      if name not in outer_self._fields:
        raise ValidationFailed("unexpected field '{}'".format(name))
    d = {}
    for name, t in outer_self._fields.items():
      with context.member(name):
        d[name] = t.from_json(value.get(name))
    return ObjectAccessor(**d)

  def _to_json(self, value):
    return {k: self._fields[k].to_json(v)
            for k, v in value.items()
            if v is not None}

  def _check(self, value):
    if value is None:
      raise ValidationFailed("expected Object")
    reasons = []
    for name, t in self._fields.items():
      subvalue = value.get(name)
      try:
        with context.member(name):
          run_check(t.check, subvalue)
      except ValidationFailed as e:
        if subvalue is None:
          reasons.append(ValidationFailed("missing field '{}'".format(name)))
        else:
          reasons.append(e)
    for name in value.__dict__:
      if name not in self._fields:
        reasons.append(ValidationFailed("unexpected field '{}'".format(name)))
    if reasons:
      if len(reasons) == 1:
        raise reasons[0]
      raise ValidationFailed(", ".join(r.format() for r in reasons))

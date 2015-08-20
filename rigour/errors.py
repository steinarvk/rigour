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

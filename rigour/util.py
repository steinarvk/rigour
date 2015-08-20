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

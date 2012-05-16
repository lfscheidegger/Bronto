"""
expect

Contains the expect() function, with similar functionality to
jasmine's
"""

class InverseChecker:
  """
  InverseChecker raises assertion errors when its expectations pass
  """
  def __init__(self, value, original):
    """
    __init__(value: Object, original: Checker) -> None
    """
    self.value = value
    self.not_ = original

  def toBe(self, value):
    """
    toBe(value: Object) -> None

    raises AssertionError if value and self.value match
    """
    if self.value == value:
      msg = "expected " + self.value + " not to be " + value
      raise AssertionError(msg)

  def toEqual(self, value):
    """
    toEqual(value: Object) -> None
    
    alias to toBe.
    """
    self.toBe(value)

class Checker:
  """
  Checker raises assertion errors when its expectations fail
  """
  def __init__(self, value):
    """
    __init__(value: Object) -> None
    """
    self.value = value
    self.not_ = InverseChecker(value, self)

  def toBe(self, value):
    """
    toBe(value: Object) -> None

    raises AssertionError if value and self.value don't match
    """
    if self.value != value:
      msg = "expected " + self.value + " to be " + value
      raise AssertionError(msg)

  def toEqual(self, value):
    """
    toEqual(value: Object) -> None

    alias to toBe.
    """
    self.toBe(value)

def expect(value):
  """
  expect(value: Object) -> Checker
  
  returns a Checker object that will receive the second Object in this
  assertion, e.g.  expect(1).toBe(2)
  """
  return Checker(value)

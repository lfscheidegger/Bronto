# Bronto - tests for Python that look like Jasmine
# Copyright (C) 2012 Luiz Scheidegger

"""
Matcher.py

Contains the Matcher class, with methods similar to jasmine's
matchers.
"""

class InverseMatcher:
  """
  InverseMatcher raises assertion errors when its expectations pass
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
      msg = "expected " + str(self.value) + " not to be " + str(value)
      raise AssertionError(msg)

  def toEqual(self, value):
    """
    toEqual(value: Object) -> None
    
    alias to toBe.
    """
    self.toBe(value)

class Matcher:
  """
  Matcher raises assertion errors when its expectations fail
  """
  def __init__(self, value):
    """
    __init__(value: Object) -> None
    """
    self.value = value
    self.not_ = InverseMatcher(value, self)

  def toBe(self, value):
    """
    toBe(value: Object) -> None

    raises AssertionError if value and self.value don't match
    """
    if self.value != value:
      msg = "expected " + str(self.value) + " to be " + str(value)
      raise AssertionError(msg)

  def toEqual(self, value):
    """
    toEqual(value: Object) -> None

    alias to toBe.
    """
    self.toBe(value)

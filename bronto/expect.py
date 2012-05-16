# Bronto - tests for Python that look like Jasmine
# Copyright (C) 2012 Luiz Scheidegger

"""
expect

Contains the expect() function, with similar functionality to
jasmine's
"""

from bronto.Matcher import Matcher

def expect(value):
  """
  expect(value: Object) -> Checker
  
  returns a Checker object that will receive the second Object in this
  assertion, e.g.  expect(1).toBe(2)
  """
  return Matcher(value)

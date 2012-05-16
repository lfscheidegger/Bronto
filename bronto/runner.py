# Bronto - tests for Python that look like Jasmine
# Copyright (C) 2012 Luiz Scheidegger

"""
runner.py

Main Bronto runner
"""

import bronto.Suite
from bronto.bash_support import print_colored, put_colored
import pkgutil
import inspect
import os
import time

def reservedMethods():
  """
  reservedMethods() -> []

  returns a const list of specially-named methods that aren't supposed
  to be run by the test runner.
  """
  return ['beforeEach', 'afterEach']

def emptyFunction(self):
  """
  emptyFunction() -> None
  """

def registerClass(klass):
  """
  registerClass(klass: Class) 
    -> [{ contextStack: [Class], testMethod: Method }]
  
  Given a Suite subclass, fetches all valid test methods
  and returns them in a list
  """

  contextStack = []
  result = []

  def registerClassRec(klass):
    """
    registerClassRec(klass: Class) -> None
    
    recursively traverse the internal Suite subclasses
    of the base Suite subclass being analyzed.
    """
    contextStack.append(klass)

    # append test cases in current context
    testCases = inspect.getmembers(klass, inspect.ismethod)  
    for testCaseName, testCaseObj in testCases:
      if testCaseName in reservedMethods():
        continue

      result.append({
        'contextStack': list(contextStack),
        'testMethod': testCaseObj
      })

    classes = inspect.getmembers(klass, inspect.isclass)
    for _, classObj in classes:
      if issubclass(classObj, bronto.Suite):
        registerClassRec(classObj)

    # pop contexts back from the stack
    contextStack.pop()

  registerClassRec(klass)

  return result

def getTestCases(testSource):
  """
  getTestCases(testSource: str) -> []

  given the path of a python package containing Bronto tests,
  find all the tests and return them in a list
  """
  baseName = os.path.split(os.path.dirname(testSource))[-1]  

  testCases = []
  for _, modname, _ in pkgutil.walk_packages(
    path=testSource, onerror=lambda x: None):
    if not modname.startswith(baseName):
      # we only care about things in the base name folder
      continue

    module = pkgutil.get_loader(modname).load_module(modname)
    classes = inspect.getmembers(module, inspect.isclass)
    
    for _, classObj in classes:
      if not issubclass(classObj, bronto.Suite):        
        continue
      
      testCases += registerClass(classObj)

  return testCases

def run(testSource):
  """
  run(testSource: str) -> None

  given the path of a python package containing Bronto tests,
  run all those tests and print output to the console.
  """

  testCases = getTestCases(testSource)

  print 'Bronto running', len(testCases), 'tests:'
  print '=' * 80
  
  before = time.clock()
  successes = 0
  failures = []

  idx = 0
  for idx in range(len(testCases)):
    testCase = testCases[idx]
    try:
      runTestCase(testCase)
      put_colored('+ ', color='green')
      successes += 1

    except Exception, err:
      put_colored('* ', color='red')
      failures.append(err)

    if idx % 40 == 39:
      put_colored('\n')

  put_colored('\n')

  timeDelta = time.clock() - before

  print successes, 'tests passed and', len(failures),\
      'failed (in', timeDelta, 'seconds)'
  print '=' * 80

  for fail in failures:
    printError(fail)

def printError(err):
  """
  printError(err: Exception) -> None

  prints an exception in red
  """
  print_colored(err, color='red')

def runTestCase(testCase):
  """
  runTestCase(testCase)

  runs an individual test case, going through the full
  beforeEach/afterEach setup/teardown process
  """
  class EmptyObject:
    """
    EmptyObject is just a placeholder for attributes that will be set
    by calls to beforeEach()
    """
    pass

  def copyProperties(src, dst):
    """
    copyProperties(src: Object, dst: Object) -> None

    Copies attr properties from Object src to Object dst.
    """
    for prop in src.__dict__:
      setattr(dst, prop, src.__dict__[prop])

  contextStack = testCase['contextStack']
  testMethod = testCase['testMethod']

  objectStack = []
  previous = EmptyObject()

  for klass in contextStack:
    obj = klass()
    copyProperties(previous, obj)
    
    if hasattr(obj, 'beforeEach'):
      obj.beforeEach()

    objectStack.append(obj)
    previous = obj

  testMethod(objectStack[-1])

  for obj in reversed(objectStack):
    if hasattr(obj, 'afterEach'):
      obj.afterEach()

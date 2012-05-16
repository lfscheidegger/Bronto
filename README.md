Bronto
======

Jasmine-like tests in Python

# Jasmine tests #

As it happens, [Jasmine](https://github.com/pivotal/jasmine) is a
Javascript library that offers BDD support for web applications. But
more importantly, it has a very elegant, attractive syntax to define
test cases and suites. Bronto, on the other hand, is a Python library
that provides (in as much as possible) a test runner for Pyhton code
with similar syntax.

# Getting Started #

The best way to introduce Bronto is to show some examples. First,
we'll go through a very simple test specification in Javascript, using
Jasmine. We'll then show how this test can be written in Python, using
Bronto.

## Basic Jasmine Test ##

Suppose we have the following test suite in Jasmine:

```javascript
describe('[unit] A Selectable button', function() {
  var button;

  beforeEach(function() {
    button = new SelectableButton();
    button.setLabel('Click me!');
  });

  it('button should have a label', function() {
    expect(button.getLabel()).toBe('Click me!');
  });

  it('button should not be selected by default', function() {
    expect(button.getSelected()).not_.toBe(true);
  });

  describe('clicking', function() {
    it('clicking on a button should select it', function() {
      button.click();
      expect(button.getSelected()).toBe(true);
    });

    it('clicking on a button twice should deselect it', function() {
      button.click();
      button.click();
      expect(button.getSelected()).toBe(false);
    });
  });
});
```

This test suite can be translated almost line-by-line to a Bronto test
suite:

```python
from bronto.expect import expect
from bronto.Suite import Suite

class SelectableButtonSpec(Suite):
  """[unit] A Selectable button"""
  
  def beforeEach(self):
    self.button = SelectableButton()
    self.button.setLabel('Click me!')

  def testFeature1(self):
    """button should have a label"""
    expect(self.button.getLabel()).toBe('Click me!')

  def testFeature2(self):
    """button should not be selected by default"""
    expect(button.getSelected()).not_.toBe(true)

  class SelectableButtonClickingSpec(Suite):
    """clicking"""
    def testFeature3(self):
      """clicking on a button should select it"""
      button.click()
      expect(button.getSelected()).toBe(true)

    def testFeature4(self):
      """clicking on a button twice should deselect it"""
      button.click()
      button.click()
      expect(button.getSelected()).toBe(false)
```

This example is rich enough to demonstrate various aspects of Bronto:

* Calls to `describe` get replaced by class definitions. The name of
  these classes is completely irrelevant. As long as they subclass
  `bronto.Suite`, they will be picked up by Bronto's test
  runner. We recommend, however, that you name these classes using
  UpperCamelCase, and end their names with `Spec`.

* Calls to `it` become methods in `bronto.Suite` subclasses. The names
  of these methods do not matter - they all get picked up by
  Bronto's runner (except reserved methods, such as `beforeEach` and
  `afterEach`, which get treated differently). However, we recommend
  naming them using camelCase, and starting their names with
  `test`.

* The strings passed as first arguments to `describe` and `it` calls are
  replaced by docstrings in Bronto's methods and classes

* Nested calls to `describe` become nested `bronto.Suite` class
  definitions

Users that are familiar with Jasmine should be able to follow these
simple rules to write Python tests with Jasmine's syntax. Below, we go
into more detail about some of the caveats and inner workings of
Bronto:

# Importing tests #

You will notice in the example above that the code defining
`SelectableButtonSpec` does nothing, besides defining the class. In
order to actually run the tests that are defined, we need a _test
runner_. Bronto ships with a simple test runner that executes the
tests and prints a simple summary to stdout. In order to use this
runner, your test code must follow some simple structural
conventions. All Bronto test suites must be defined in Python modules
(usually `.py` files), and these files must be imported in a common
`.py` file. Assuming our example above is defined in a file called
`tests/unit/button_spec.py`, the common file (let's call it
`__init__.py`, in a folder called `__tests__`) could look something
like this:

```python
import tests.unit.button_spec
import tests.unit.checkbox_spec
```

(We're also assuming you have another Bronto test suite under
`tests/unit/checkbox_spec.py`). Under this configuration, you should
only need to run `bronto __tests__/__init__.py` and it should be able
to do the rest, printing the test run's summary to stdout. Contrast
this with a very similar convention in Javascript, using CommonJS:

```javascript
require('tests/unit/button_spec');
require('tests/unit/checkbox_spec');
```

# Class Scope #

You will notice from our previous example that, while in Javascript
the `button` variable was declared in the scope of the outermost
`describe` block, in Bronto it was declared in the outermost
`beforeEach` function. This is a consequence of differences between
the way Python and Javascript deal with methods/functions. In Bronto
(just as in Jasmine), all nested beforeEach methods are called, in order, before
each test method. Additionally, everything assigned to `self`,
on any level, is available to the test method:

```python
class OuterSpec(bronto.Suite):
  def beforeEach(self):
    self.foo = "foo"

  def test0(self):
    expect(self.foo).toEqual("foo")

  class InnerSpec(bronto.Suite):
    def beforeEach(self):
      self.bar = "bar"

    def test0(self):
      expect(self.foo).toEqual("foo") # this will pass!
      expect(self.bar).toEqual("bar") # this will pass too!

  def test1(self):
    expect(self.bar).toEqual("bar") # this, however, will fail
```

This allows common initialization code to be factored into outer calls
to `beforeEach`, just as they would in Jasmine.

# A note about not #

Jasmine matchers have an attribute, `.not`, which contains another
matcher that returns the inverse of its owner. This is very convenient
for writing expectations like this:

```javascript
expect(1).not.toBe(2)
```

Unfortunately, `not` is a reserved keyword in Python. Bronto remedies
this by introducing a `not_` property:

```python
expect(1).not_.toBe(2)
```

# Running tests without the test runner #

Although we recommend using Bronto's test runner for Bronto tests, it
is possible to write simple one-time tests without it. Any Python file
can import `bronto.expect`, and write expectations. `expect` is simply
a global-level function that returns a checker for the value
provided. The checkers raise `AssertionError` exceptions if their
corresponding tests fail.

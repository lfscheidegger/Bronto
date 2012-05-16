"""
main.py

Bronto entry point. Pass it a python file containing imports with all
the test cases
"""

import bronto.runner
import bronto.TestGroup
import os
import sys

def main():
  """
  main() -> None

  bronto script entry point.
  """
  if len(sys.argv) < 2:
    print "Usage:", sys.argv[0], "<python file importing the tests>"
    sys.exit(1)

  testSource = sys.argv[1]
  testSource = os.path.abspath(testSource)

  bronto.runner.run(testSource)

if __name__ == '__main__':
  main()

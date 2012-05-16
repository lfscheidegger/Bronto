# Bronto - tests for Python that look like Jasmine
# Copyright (C) 2012 Luiz Scheidegger
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

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

# Raptor - smart hooks for git
# Copyright (C) 2012 Luiz Scheidegger

"""
bash_support.py
miscellaneous functions to interact with a bash shell.
"""

import subprocess
import sys

color_code_map = {
    'none': '\033[0m',
    'black':  '\033[030m',
    'red':    '\033[31m',
    'green':  '\033[32m',
    'brown':  '\033[033m',
    'blue':   '\033[034m',
    'purple': '\033[35m',
    'cyan':   '\033[36m',
    'gray':   '\033[037m',
    'yellow': '\033[1;33m'
}

def print_colored(*args, **kwargs):
    """
    print_colore(args: [str,], kwargs: { color: str }) -> None

    Similar to native print, but prints a colored message.
    """
    color = color_code_map['none']
    try:
        color = color_code_map[kwargs['color']]
    except KeyError:
        pass

    print color + ' '.join(args) + color_code_map['none']

def put_colored(*args, **kwargs):
  """
  put_colored(args: [str, ], kwargs: { color: str }) -> None
  
  Puts colored character without the newline that usually
  follows a print.
  """
  color = color_code_map['none']
  try:
    color = color_code_map[kwargs['color']]
  except KeyError:
    pass  

  sys.stdout.write(color + ' '.join(args) + color_code_map['none'])

def run_command(cmd, **kwargs):
    """
    run_command(cmd: string, kwargs: { ignore_output: boolean }) -> { stdout: str, stderr: str }

    Runs the command under 'cmd' and returns a dictionary with stdout
    and stderr.
    """
    if kwargs.has_key('ignore_output'):
        subprocess.call(cmd.split())
    else:
        [stdout, stderr] = subprocess.Popen(
            cmd.split(),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

        return {
            'stdout': str(stdout),
            'stderr': str(stderr)
            }

def call_command(cmd):
    """
    call_command(cmd: str) -> int
    
    Calls the command cmd and returns its exit code.
    """
    return subprocess.call(cmd.split())

def prompt(message, default):
    """
    prompt(message: str, default: bool) -> bool

    Prompts user with a yes/no message and default choice
    """
    message += (' [Y/n]: ' if default else ' [y/N]: ')
    result = raw_input(message)
    while True:
        if result == "":
            return default

        result = result.upper()
        if result == 'Y':
            return True
        elif result == 'N':
            return False
        else:
            result = raw_input("Please answer 'y' or 'n': ")
            if result == "": 
                result = 'x'

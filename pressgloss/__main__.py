# -*- coding: utf-8 -*-
""" pressgloss module

Run --help for more specific instructions

Version:
--------
- pressgloss v0.0.1
"""

# Standard library imports
import logging
import argparse
import sys

# pressgloss imports
import pressgloss.core as PRESSGLOSS
import pressgloss.helpers as helpers
import pressgloss.daideapp as DAIDEAPP
from . import create_app

# python -m pressgloss --operation translate --daide "FRM (ENG) (FRA ITA) (PRP (PCE (FRA ITA)))" --tones "Haughty,Urgent"
# python -m pressgloss --operation translate --daide "FRM (ENG) (FRA ITA) (PRP (PCE (FRA ITA)))" --tones "Objective"
# python -m pressgloss --operation test --daide "FRM ( ENG) (FRA  ITA) (PRP (PCE (FRA ITA) ))"
def main(): # type: () -> None
  logging.basicConfig(format='%(asctime)-15s %(message)s', level=logging.DEBUG)
  leParser = argparse.ArgumentParser()
  leParser.add_argument('--operation', help='What do you want to do? (translate)')
  leParser.add_argument('--daide', help='The DAIDE format press to use')
  leParser.add_argument('--tones', help='The tones to use')
  lesArgs = leParser.parse_args()
  if not hasattr(lesArgs, 'operation') or lesArgs.operation is None:
    logging.error('pressgloss needs to know what to do - maybe translate?')
    leParser.print_help()
    sys.exit(2)
  if lesArgs.operation == 'translate':
    tones = []
    if hasattr(lesArgs, 'tones'):
      tones = [curtone for curtone in lesArgs.tones.split(',')]
    english = PRESSGLOSS.daide2gloss(lesArgs.daide, tones)
    print(english)
  elif lesArgs.operation == 'app':
    app = create_app()
    app.run(debug=True)
  elif lesArgs.operation == 'test':
    exprlist = helpers.daide2lists(lesArgs.daide)
    print(str(len(exprlist)))

if __name__ == '__main__':
  main()

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
import random

# pressgloss imports
import pressgloss.core as PRESSGLOSS
import pressgloss.helpers as helpers
import pressgloss.daideapp as DAIDEAPP
from . import create_app

# python -m pressgloss --operation translate --daide "FRM (ENG) (FRA ITA) (PRP (PCE (FRA ITA)))" --tones "Haughty,Urgent"
# python -m pressgloss --operation translate --daide "FRM (ENG) (FRA ITA) (PRP (PCE (FRA ITA)))" --tones "Objective"
# python -m pressgloss --operation translate --daide "FRM (ENG) (FRA ITA) (PRP (AND (PCE (FRA ITA)) (XDO ((ENG AMY LVP) RTO YOR))))" --tones "Objective"
# python -m pressgloss --operation test --daide "FRM ( ENG) (FRA  ITA) (PRP (PCE (FRA ITA) ))"
def main(): # type: () -> None
  logging.basicConfig(format='%(asctime)-15s %(message)s', level=logging.DEBUG)
  leParser = argparse.ArgumentParser()
  leParser.add_argument('--operation', help='What do you want to do? (translate|random|app|test)')
  leParser.add_argument('--number', help='How many expressions to create.')
  leParser.add_argument('--daide', help='The DAIDE format press to use.')
  leParser.add_argument('--tones', help='The tones to use.')
  lesArgs = leParser.parse_args()
  if not hasattr(lesArgs, 'operation') or lesArgs.operation is None:
    logging.error('pressgloss needs to know what to do - maybe translate?')
    leParser.print_help()
    sys.exit(2)

  iterations = 1
  if hasattr(lesArgs, 'number') and lesArgs.number is not None:
    iterations = int(lesArgs.number)
  if lesArgs.operation == 'translate':
    tones = []
    if hasattr(lesArgs, 'tones') and lesArgs.tones is not None:
      tones = [curtone for curtone in lesArgs.tones.split(',')]
    for citer in range(0, iterations):
      english = PRESSGLOSS.daide2gloss(lesArgs.daide, tones)
      print(english)
  if lesArgs.operation == 'random':
    for citer in range(0, iterations):
      tones = random.sample(helpers.tonelist, random.randint(1, 3))
      utterance = PRESSGLOSS.PressUtterance(None, tones)
      print(utterance.daide + ' --> ' + utterance.english)
  elif lesArgs.operation == 'app':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')
  elif lesArgs.operation == 'test':
    exprlist = helpers.daide2lists(lesArgs.daide)
    print(str(len(exprlist)))

if __name__ == '__main__':
  main()

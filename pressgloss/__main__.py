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
import os

# pressgloss imports
import pressgloss.core as PRESSGLOSS
import pressgloss.helpers as helpers
import pressgloss.gamelog as GAMELOG
import pressgloss.daideapp as DAIDEAPP
import pressgloss.daide_translate as DAIDE
from . import create_app

# python -m pressgloss --operation translate --daide "FRM (ENG) (FRA ITA) (PRP (PCE (FRA ITA)))" --tones "Haughty,Urgent"
# python -m pressgloss --operation translate --daide "FRM (ENG) (FRA ITA) (PRP (PCE (FRA ITA)))" --tones "Objective"
# python -m pressgloss --operation translate --daide "FRM (FRA) (ENG) (PRP (XDO ((ENG AMY LVP) MTO (SPA NCS))))" --tones "Objective"
# python -m pressgloss --operation translate --daide "FRM (ENG) (FRA ITA) (PRP (AND (PCE (FRA ITA)) (XDO ((ENG AMY LVP) RTO YOR))))" --tones "Objective"
# python -m pressgloss --operation translate --daide "FRM (FRA) (ENG) (PRP (XDO ((ENG AMY LVP) MTO YOR)))" --tones "Objective,Expert"
# python -m pressgloss --operation test --daide "FRM ( ENG) (FRA  ITA) (PRP (PCE (FRA ITA) ))"
# python -m pressgloss --operation expound --number 100 --daide "FRM (ENG) (FRA) (PRP (PCE (FRA ENG)))"
# python -m pressgloss --operation random --number 10
# python -m pressgloss --operation prettifygamefile --input c:\data\shade\data\games\OliveJunglefowlRosalyn25_1651251697467.json --output c:\data\shade\data\games\OliveJunglefowlRosalyn25_1651251697467.html
# python -m pressgloss --operation analyzelogs --input c:\data\shade\data_20220526\games
# python -m pressgloss --operation analyzegym --input c:\data\shade\botgamelogs > c:\data\shade\botgamelogs\analysis.txt

# aws s3 --profile=shade ls s3://jataware-diplomacy/
# aws s3 --profile=shade cp s3://jataware-diplomacy/data-2022-05-21T16:00:01.zip c:\data\shade\data_2.zip

def main(): # type: () -> None
  logging.basicConfig(format='%(asctime)-15s %(message)s', level=logging.DEBUG)
  leParser = argparse.ArgumentParser()
  leParser.add_argument('--operation', help='What do you want to do? (translate|random|app|test|analyzelogs|analyzegym|encode|finetune)')
  leParser.add_argument('--number', help='How many expressions to create.')
  leParser.add_argument('--daide', help='The DAIDE format press to use.')
  leParser.add_argument('--english', help='The English message to translate.')
  leParser.add_argument('--model', help='The model to use.')
  leParser.add_argument('--tones', help='The tones to use.')
  leParser.add_argument('--gameid', help='The ID of a game to analyze.')
  leParser.add_argument('--input', help='An input file or folder.')
  leParser.add_argument('--output', help='An output file or folder.')
  leParser.add_argument('--config', help='A configuration file with various settings.')

  lesArgs = leParser.parse_args()
  if not hasattr(lesArgs, 'operation') or lesArgs.operation is None:
    logging.error('pressgloss needs to know what to do - maybe translate?')
    leParser.print_help()
    sys.exit(2)
  if hasattr(lesArgs, 'config') and lesArgs.config is not None:
    helpers.loadconfig(lesArgs.config)

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
  elif lesArgs.operation == 'random':
    legaltones = [tone for tone in helpers.tonelist if tone not in ['Urgent', 'Expert', 'Obsequious', 'Haughty', 'PigLatin']]
    print('DAIDE,Tones,Gloss')
    for citer in range(0, iterations):
      curtones = [random.choice(legaltones)]
      if random.choice([True, False]):
        curtones.append('Urgent')
      if random.choice([True, False]):
        curtones.append('Expert')
      utterance = PRESSGLOSS.PressUtterance(None, curtones)
      print('"' + utterance.daide + '","' + ';'.join(curtones) + '","' + utterance.english + '"')
  elif lesArgs.operation == 'expound':
    print('DAIDE,Tones,Gloss')
    legaltones = [tone for tone in helpers.tonelist if tone not in ['Urgent', 'Expert', 'Obsequious', 'Haughty', 'PigLatin']]
    for citer in range(0, iterations):
      tones = [random.choice(legaltones)]
      if random.choice([True, False]):
        tones.append('Urgent')
      if random.choice([True, False]):
        tones.append('Expert')
      english = PRESSGLOSS.daide2gloss(lesArgs.daide, tones)
      print('"' + lesArgs.daide + '","' + str(tones) + '","' + english + '"')
  elif lesArgs.operation == 'app':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')
  elif lesArgs.operation == 'prettifygamefile':
    GAMELOG.prettifygamefile(lesArgs.input, lesArgs.output)
  elif lesArgs.operation == 'analyzelogs':
    interestinggames = GAMELOG.analyzebackup(lesArgs.input)
    for curgame in interestinggames:
      GAMELOG.prettifygamefile(curgame, curgame)
  elif lesArgs.operation == 'analyzegym':
    interestinggames = GAMELOG.analyzegym(lesArgs.input)
    print('There were ' + str(len(interestinggames)) + ' game files found.')
  elif lesArgs.operation == 'test':
    print('testing')
  elif lesArgs.operation == 'encode':
    tones = []
    if hasattr(lesArgs, 'tones') and lesArgs.tones is not None:
      tones = [curtone for curtone in lesArgs.tones.split(',')]
    encoding = DAIDE.gloss2daide(lesArgs.english, tones, lesArgs.model)
    print(encoding)
  elif lesArgs.operation == 'finetune':
    model = DAIDE.fine_tuned_model.finetune()
    print(f'{model} fine tuned, use -- model to use') 

if __name__ == '__main__':
  main()

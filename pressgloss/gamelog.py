# Standard imports
import json
import os
from collections import Counter

# pressgloss imports
import pressgloss.core as PRESSGLOSS

def prettifygamefile(inpath, outpath): # type: (str, str) -> None
  """
  Reads a JSON game log file and writes it prettily to another file

  :param inpath: the location on disk of the JSON game log
  :type inpath: str
  :param outpath: the location on disk to write the pretty JSON game log
  :type outpath: str

  """

  with open(inpath, 'r', encoding='UTF-8') as jf:
    curgame = json.load(jf)

  with open(outpath, 'w', encoding='UTF-8') as of:
    json.dump(curgame, of, indent=2)

def analyzebackup(inpath): # type: (str) -> []
  """
  Searches through a folder for game logs and returns a list of paths to those which might be interesting for analysis.

  :param inpath: the folder that the logs are in
  :type inpath: str

  """

  retset = set()
  tonesused = Counter()
  daideoperators = Counter()
  messages = 0
  daideerrors = 0

  for root, dirs, files in os.walk(os.path.abspath(inpath)):
    for file in files:
      curfullpath = os.path.join(root, file)
      if file.endswith('.json'):
        with open(curfullpath, 'r', encoding='UTF-8') as jf:
          curgame = json.load(jf)
        if 'message_history' in curgame:
          for curkey, messagelist in curgame['message_history'].items():
            for curmessage in messagelist:
              curtonesstr = curmessage['tones']
              if curtonesstr == '':
                curtonesstr = 'Objective'
              curtones = curtonesstr.split(',')
              for curtone in curtones:
                tonesused[curtone] += 1
              print('Trying to process: ' + curmessage['daide'] + ': ' + str(curtones))
              curdaide = PRESSGLOSS.PressUtterance(curmessage['daide'], curtones)
              messages += 1
              if 'Ahem' in curdaide.english:
                daideerrors += 1
              if curdaide.content is not None:
                daideoperators[curdaide.content.operator] += 1
                if curdaide.content.details is not None:
                  daideoperators[curdaide.content.details.operator] += 1
            if len(messagelist) > 0 and curfullpath not in retset:
              print('Found messages in ' + curfullpath)
              retset.add(curfullpath)

  print('Press found in ' + str(len(retset)) + ' games.')
  print('  ' + str(messages) + ' messages found.')
  print('  ' + str(daideerrors) + ' DAIDE errors found.')
  print(str(tonesused.most_common()))
  print(str(daideoperators.most_common()))

  return list(retset)

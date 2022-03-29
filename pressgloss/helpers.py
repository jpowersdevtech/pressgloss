# -*- coding: utf-8 -*-

# Standard library imports
import os
import csv
import json
import re
import random

# pressgloss imports
import pressgloss.core

refData = []

# Initialization loads reference data from resources CSV.
this_dir, this_filename = os.path.split(__file__)
refPath = os.path.join(this_dir, 'resources', 'reference.csv')
if (os.path.isfile(refPath)):
  with open(refPath) as refFile:
    refData = [{colName: str(cellValue) for colName, cellValue in row.items()}
               for row in csv.DictReader(refFile, skipinitialspace=True)]

powerdict = {curdata['trigram']: curdata for curdata in refData if curdata['type'] == 'Power'}
powerlist = list(powerdict.keys())
provincedict = {curdata['trigram']: curdata for curdata in refData if curdata['type'] == 'Province'}
provincelist = list(provincedict.keys())
unitdict = {curdata['trigram']: curdata for curdata in refData if curdata['type'] == 'Unit'}
unitlist = list(unitdict.keys())
sealist = [curdata['trigram'] for curdata in refData if curdata['Sea'] == '1' or curdata['Coast'] == '1']
supplylist = [curdata['trigram'] for curdata in refData if curdata['Supply'] == '1']
tonelist = ['Haughty', 'Objective', 'Urgent', 'Obsequious', 'PigLatin']

def initcap(instr): # type: (str) -> str
  """
  Creates a sentence case string

  :param instr: the input string
  :type instr: str

  :return: sentence capitalized version of the input
  :rtype: str

  """

  if instr is None or len(instr) == 1:
    return ''

  return instr[0].upper() + instr[1:]

def daidecontains(daidelist, match): # type: ([], str) -> bool
  """
  Determines whether a given string appears anywhere in the nested list representation
  of the DAIDE expression.  Works because of DAIDE's no-repeats trigram vocabulary.

  :param daidelist: the DAIDE content in list form
  :type daidelist: []
  :param match: the string to look for
  :type match: str

  :return: if the match is present in the DAIDE expression
  :rtype: bool
  """

  daidestr = json.dumps(daidelist)
  return match.lower() in daidestr.lower()

def listOfProvinces(provincelist): # type: ([]) -> str
  """
  Creates a list of names of provinces

  :param provincelist: the Provinces trigram list
  :type provincelist: []

  :return: an English list of provinces
  :rtype: str
  """

  retstr = ''
  if len(provincelist) == 0:
    return 'Ahem.'

  spellings = [provincedict[curprov]['Objective'] for curprov in provincelist]

  retstr = ', '.join(spellings)
  if ', ' in retstr:
    lastcomma = retstr.rfind(', ')
    retstr = retstr[:lastcomma] + ' and' + retstr[lastcomma + 1:]

  return retstr

def listOfPowers(powerlist, frompower, topowers, case='Objective'): # type: ([], str, [], str) -> str
  """
  Creates a list of names of Powers relative to a sender and recipient and with case if needed

  :param powerlist: the Powers trigram list
  :type powerlist: []
  :param frompower: the Power that sent the message with the list
  :type frompower: str
  :param topowers: the Powers that received the message with the list
  :type topowers: []
  :param case: the case for a pronoun if needed (Objective|Subjective)
  :type case: str

  :return: an English list of powers
  :rtype: str
  """

  if case == 'Possessive':
    if frompower in powerlist:
      if len(powerlist) == 1:
        return 'my'
      else:
        return 'our'
    else:
      listedto = [curpower for curpower in topowers if curpower in powerlist]
      if len(listedto) > 0:
        return 'your'
      else:
        return 'their'

  whoami = 'me'
  if case == 'Subjective':
    whoami = 'I'

  if len(powerlist) == 0:
    return 'Ahem.'

  allinclusive = False
  if topowers is not None:
    listedto = [curpower for curpower in topowers if curpower in powerlist]
    allinclusive = len(listedto) == len(topowers)

  orderedlist = []
  if allinclusive:
    if len(topowers) == 1:
      orderedlist.append('you')
    else:
      orderedlist.append('you ' + str(size2numstr(topowers)))

  for curpower in powerlist:
    if curpower != frompower and curpower not in topowers:
      orderedlist.append(powerdict[curpower]['Objective'])

  if frompower in powerlist:
    orderedlist.append(whoami)

  retstr = ', '.join(orderedlist)
  if len(orderedlist) > 1:
    retpref = retstr[:retstr.rfind(', ')]
    retsuff = retstr[retstr.rfind(', ') + 2:]
    retstr = retpref + ' and ' + retsuff

  if retstr == 'you and me':
    if random.choice([True, False]):
      retstr = 'us'

  if retstr == 'you and I':
    if random.choice([True, False]):
      retstr = 'we'

  return retstr

def size2numstr(inlist): # type: ([]) -> str
  """
  Creates an English word representation of the size of a list

  :param inlist: the list
  :type inlist: []

  :return: a textual representation of the size of the list
  :rtype: str
  """

  if inlist is None:
    return 'zero'

  thelen = len(inlist)
  if thelen == 0:
    return 'zero'
  elif thelen == 1:
    return 'one'
  elif thelen == 2:
    return 'two'
  elif thelen == 3:
    return 'three'
  elif thelen == 4:
    return 'four'
  elif thelen == 5:
    return 'five'
  elif thelen == 6:
    return 'six'
  elif thelen == 7:
    return 'seven'
  else:
    return 'all'

def daide2lists(daide): # type: (str) -> []
  """
  Convert DAIDE formatted syntax to JSON-like nested lists

  :param daide: a press utterance in DAIDE syntax (with From and To info)
  :type daide: str
  """

  retlist = []

  # standardizing
  metamorphosis = daide.strip().upper() # FRM ( ENG) (FRA ITA) (PRP (ALY (ENG  FRA ITA)VSS(RUS TUR) ))
  metamorphosis = '(' + metamorphosis + ')' # (FRM ( ENG) (FRA ITA) (PRP (ALY (ENG  FRA ITA)VSS(RUS TUR) )))

  # corrections for whitespace
  metamorphosis = re.sub(r'\( +', r'(', metamorphosis) # (FRM (ENG) (FRA ITA) (PRP (ALY (ENG  FRA ITA)VSS(RUS TUR) )))
  metamorphosis = re.sub(r' +\)', r')', metamorphosis) # (FRM (ENG) (FRA ITA) (PRP (ALY (ENG  FRA ITA)VSS(RUS TUR))))
  metamorphosis = re.sub(r'\)([A-Z])', r') \1', metamorphosis) # FRM (ENG) (FRA ITA) (PRP (ALY (ENG  FRA ITA) VSS(RUS TUR)))
  metamorphosis = re.sub(r'([A-Z])\(', r'\1 (', metamorphosis) # FRM (ENG) (FRA ITA) (PRP (ALY (ENG  FRA ITA) VSS (RUS TUR)))
  metamorphosis = re.sub(r' +', r' ', metamorphosis) # (FRM (ENG) (FRA ITA) (PRP (ALY (ENG FRA ITA) VSS (RUS TUR))))

  # transformations to JSON
  metamorphosis = re.sub(r'([A-Z]{3})', r'"\1"', metamorphosis) # ("FRM" ("ENG") ("FRA" "ITA") ("PRP" ("ALY" ("ENG" "FRA" "ITA") "VSS" ("RUS" "TUR"))))
  metamorphosis = re.sub(r' ', r', ', metamorphosis) # ("FRM", ("ENG"), ("FRA", "ITA"), ("PRP", ("ALY", ("ENG", "FRA", "ITA"), "VSS", ("RUS", "TUR"))))
  metamorphosis = re.sub(r'\(', r'[', metamorphosis) # ["FRM", ["ENG"), ["FRA", "ITA"), ["PRP", ["ALY", ["ENG", "FRA", "ITA"), "VSS", ["RUS", "TUR"))))
  metamorphosis = re.sub(r'\)', r']', metamorphosis) # ["FRM", ["ENG"], ["FRA", "ITA"], ["PRP", ["ALY", ["ENG", "FRA", "ITA"], "VSS", ["RUS", "TUR"]]]]

  try:
    retlist = json.loads(metamorphosis)
  except ValueError:
    retlist = []

  return retlist

def piglatinword(inword): # type: (str) -> str
  """
  Converts a word to Pig Latin

  :param inword: the original word, assumed to be just a word, no punctuation or other horsing around
  :type inword: str

  :return: the word in Pig Latin
  :rtype: str

  """

#  print('Started with ' + inword)

  if len(inword) == 1:
    return inword + 'way'

  initcap = inword[0:1].isupper()
  initvowel = inword[0:1].lower() in ['a', 'e', 'i', 'o', 'u']
  secondcons = inword[1:2].lower() not in ['a', 'e', 'i', 'o', 'u', 'y']
  thirdcons = len(inword) >= 3 and secondcons and inword[2:3].lower() not in ['a', 'e', 'i', 'o', 'u', 'y']

  retword = ''
  if initvowel:
#    print('  Initial vowel')
    retword = inword + 'way'
  else:
    swappos = 1
#    print('  Swapping at position ' + str(swappos))
    if thirdcons:
      swappos = 3
    elif secondcons:
      swappos = 2
    moving = inword[0:swappos].lower()
    staying = inword[swappos:]
    retword = staying + moving + 'ay'
#    print('  Swapped: ' + retword)
    if initcap:
#      print('  Re-capitalizing')
      retword = retword[0:1].upper() + retword[1:]

#  print('  Final word: ' + retword)
  return retword

def piglatinize(instr): # type: (str) -> str
  """
  Converts a text to Pig Latin

  :param instr: the original text, assumed to be sentence-like English
  :type instr: str

  :return: the text in Pig Latin
  :rtype: str

  """

  words = instr.split()
  newwords = []
  for curword in words:
    newword = curword.strip()
    prelisted = False
    postlisted = False
    punctuation = None
    if newword.startswith('<li>'):
      prelisted = True
      newword = newword[4:]
    if newword.endswith('</li>'):
      postlisted = True
      newword = newword[:-5]
    if newword[-1] in [',', '.', '?', '!', ':']:
      punctuation = newword[-1]
      newword = newword[:-1]
    newword = piglatinword(newword)
    if prelisted:
      newword = '<li>' + newword
    if punctuation is not None:
      newword = newword + punctuation
    if postlisted:
      newword = newword + '</li>'
    newwords.append(newword)

  return ' '.join(newwords)

def tonetize(utterance, glosssofar): # type: (pressgloss.core.PressUtterance, str) -> str
  """
  Take a basic expression and apply tones to it if possible.

  :param utterance: the original DAIDE utterance
  :type utterance: pressgloss.core.PressUtterance
  :param glosssofar: the English gloss that has been produced so far.
  :type glosssofar: str

  """

  if glosssofar == '' or glosssofar == 'Ahem.':
    return glosssofar

  retstr = glosssofar
  if 'HUH' in utterance.daide or 'BWX' in utterance.daide:
    return retstr
  if 'Haughty' in utterance.tones:
    if 'CCL' in utterance.daide:
      retstr = retstr + ' Pray we do not alter the deal further.'
    elif 'YES' in utterance.daide or 'REJ' in utterance.daide:
      retstr = powerdict[utterance.frompower]['Haughty'] + ' has deigned to respond to your missive: ' + retstr
      if 'Urgent' in utterance.tones:
        if 'REJ' in utterance.daide:
          retstr = retstr + ' Now leave me alone for a while, many things are afoot.'
        else:
          retstr = retstr + ' I expect to see action on this matter from you soon.'
    else:
      retstr = powerdict[utterance.frompower]['Haughty'] + ' demands your attention in this matter. ' + retstr + ' What say you to that?'
      if 'PRP' in utterance.daide and 'Urgent' in utterance.tones:
        retstr = retstr + ' You don\'t have much time to waste in considering your response.'
  elif 'Obsequious' in utterance.tones:
    if 'CCL' in utterance.daide:
      retstr = retstr + ' Sorry for bothering you.'
    elif 'YES' in utterance.daide or 'REJ' in utterance.daide:
      retstr = powerdict[utterance.frompower]['Familiar'] + ' is happy to provide a response: ' + retstr
      if 'Urgent' in utterance.tones:
        if 'REJ' in utterance.daide:
          retstr = retstr + ' Not much time to chat, but all the best for your game.'
        else:
          retstr = retstr + ' I really need a response if you could be so kind.'
    else:
      if len(utterance.topowers) == 1:
        retstr = 'Oh great leader of ' + powerdict[utterance.topowers[0]]['Haughty'] + ', please hear me out. ' + retstr + '. Respectfully, the nation of ' + powerdict[utterance.frompower]['Objective'] + '.'
      else:
        retstr + 'Oh great Powers of Europe, please hear me out. ' + retstr + '. Respectfully, the nation of ' + powerdict[utterance.frompower]['Objective'] + '.'
      if 'PRP' in utterance.daide and 'Urgent' in utterance.tones:
        retstr = retstr + ' I really need a response if you could be so kind.'
  elif 'Urgent' in utterance.tones:
    if 'PRP' in utterance.daide:
      if 'CCL' in utterance.daide or 'REJ' in utterance.daide:
        retstr = retstr + ' No time to consider that for now.'
      elif 'YES' in utterance.daide:
        retstr = retstr + " Let's get going on this now that it's agreed."
      else:
        retstr = retstr + ' We need to move fast on this.'

  if 'PigLatin' in utterance.tones:
    retstr = piglatinize(retstr)

  return retstr

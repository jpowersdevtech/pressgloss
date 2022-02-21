# -*- coding: utf-8 -*-

# Standard library imports
import os
import csv
import json
import re

refData = []

# Initialization loads reference data from resources CSV.
this_dir, this_filename = os.path.split(__file__)
refPath = os.path.join(this_dir, 'resources', 'reference.csv')
if (os.path.isfile(refPath)):
  with open(refPath) as refFile:
    refData = [{colName: str(cellValue) for colName, cellValue in row.items()}
               for row in csv.DictReader(refFile, skipinitialspace=True)]

powerdict = {curdata['trigram']: curdata for curdata in refData if curdata['type'] == 'Power'}
provincedict = {curdata['trigram']: curdata for curdata in refData if curdata['type'] == 'Province'}
unitdict = {curdata['trigram']: curdata for curdata in refData if curdata['type'] == 'Unit'}

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
  Creates a list of names of Powers relative to a sender and recipient and with tone

  :param powerlist: the Powers trigram list
  :type powerlist: []
  :param frompower: the Power that sent the message with the list
  :type frompower: str
  :param topowers: the Powers that received the message with the list
  :type topowers: []
  :param case: the case for a pronoun if needed
  :type case: str

  :return: an English list of powers
  :rtype: str
  """

  retstr = ''

  whoami = 'me'
  if case == 'Subjective':
    whoami = 'I'

  if len(powerlist) == 0:
    return 'Ahem.'

  everyoneelse = powerlist
  if topowers is not None and frompower is not None:
    everyoneelse = [curpower for curpower in powerlist if curpower not in topowers and curpower != frompower]
  elif frompower is not None:
    everyoneelse = [curpower for curpower in powerlist if curpower != frompower]
  elif topowers is not None:
    everyoneelse = [curpower for curpower in powerlist if curpower not in topowers]

  allinclusive = False
  if topowers is not None:
    listedto = [curpower for curpower in topowers if curpower in powerlist]
    allinclusive = len(listedto) == len(topowers)

  fromincluded = False
  if frompower is not None:
    fromincluded = frompower in powerlist

  if len(powerlist) == 1:
    if fromincluded:
      retstr = whoami
    elif allinclusive:
      retstr = 'you'
    else:
      retstr = powerdict[powerlist[0]]['Objective']
  else:
    numused = 0
    if allinclusive:
      retstr = 'you'
      numused += len(topowers)
      if numused == len(powerlist) - 1:
        retstr += ' and '
      elif numused < len(powerlist):
        retstr += ', '
    if fromincluded:
      retstr += whoami
      numused += 1
      if numused == len(powerlist) - 1:
        retstr += ' and '
      elif numused < len(powerlist):
        retstr += ', '
    for curpower in everyoneelse:
      retstr += powerdict[curpower]['Objective']
      numused += 1
      if numused == len(powerlist) - 1:
        retstr += ' and '
      elif numused < len(powerlist):
        retstr += ', '

  return retstr.strip()

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

def tonetize(daide, glosssofar, frompower, topowers, tones): # type: (str, str, str, [], []) -> str
  """
  Take a basic expression and apply tones to it if possible.

  :param daide: the original DAIDE syntax expression
  :type daide: str
  :param glosssofar: the English gloss that has been produced so far.
  :type glosssofar: str
  :param frompower: the Power that is sending the message
  :type frompower: str
  :param topowers: the Powers who will receive the message
  :type topowers: []
  :param tones: the tones to use
  :type tones: []

  """

  retstr = glosssofar
  if 'HUH' in daide or 'BWX' in daide:
    return retstr
  if 'Haughty' in tones:
    if 'CCL' in daide:
      retstr = retstr + ' Pray we do not alter the deal further.'
    elif 'YES' in daide or 'REJ' in daide:
      retstr = powerdict[frompower]['Haughty'] + ' has deigned to respond to your missive: ' + retstr
      if 'Urgent' in tones:
        if 'REJ' in daide:
          retstr = retstr + ' Now leave me alone for a while, many things are afoot.'
        else:
          retstr = retstr + ' I expect to see action on this matter from you soon.'
    else:
      retstr = powerdict[frompower]['Haughty'] + ' demands your attention in this matter. ' + retstr + ' What say you to that?'
      if 'PRP' in daide and 'Urgent' in tones:
        retstr = retstr + ' You don\'t have much time to waste in considering your response.'
  elif 'Obsequious' in tones:
    if 'CCL' in daide:
      retstr = retstr + ' Sorry for bothering you.'
    elif 'YES' in daide or 'REJ' in daide:
      retstr = powerdict[frompower]['Familiar'] + ' is happy to provide a response: ' + retstr
      if 'Urgent' in tones:
        if 'REJ' in daide:
          retstr = retstr + ' Not much time to chat, but all the best for your game.'
        else:
          retstr = retstr + ' I really need a response if you could be so kind.'
    else:
      if len(topowers) == 1:
        retstr = 'Oh great leader of ' + powerdict[topowers[0]]['Haughty'] + ', please hear me out. ' + retstr + '. Respectfully, the nation of ' + powerdict[frompower]['Objective'] + '.'
      else:
        retstr + 'Oh great Powers of Europe, please hear me out. ' + retstr + '. Respectfully, the nation of ' + powerdict[frompower]['Objective'] + '.'
      if 'PRP' in daide and 'Urgent' in tones:
        retstr = retstr + ' I really need a response if you could be so kind.'

  return retstr

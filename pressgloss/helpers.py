# -*- coding: utf-8 -*-

# Standard library imports
import os
import csv
import json
import re
import random
import configparser

import subprocess

# 3rd-party imports
from bs4 import BeautifulSoup

# pressgloss imports
import pressgloss.core

#grammarimport: 
from daidepp.grammar.grammar_utils import create_daide_grammar

refData = []

#save list of dicts to 

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
tonelist = ['Haughty', 'Objective', 'Urgent', 'Obsequious', 'PigLatin', 'Hostile', 'Friendly', 'Fearful', 'Confident', 'Empathetic', 'Upset', 'Expert']
powername2sym = {
                 'FRANCE': 'FRA',
                 'AUSTRIA': 'AUS',
                 'GERMANY': 'GER',
                 'TURKEY': 'TUR',
                 'ENGLAND': 'ENG',
                 'RUSSIA': 'RUS',
                 'ITALY': 'ITA',
                 'GLOBAL': 'ITA FRA GER AUS TUR RUS ENG'
                }
eventcols = ['gameID', 'turn', 'eventtype', 'conversation', 'countryID',
             'toCountryID', 'timeSent', 'message', 'intentDeceive', 'suspectedIncomingDeception',
             'type', 'unitType', 'terrID', 'fromTerrID', 'toTerrID', 'viaConvoy', 'success']
configs = None

def loadconfig(inpath): # type: (str) -> None
  """
  Loads config information from a file, makes available through
  a global helpers variable

  :param inpath: the path to the config file (probably .ini)
  :type inpath: str

  """

  global configs

  configs = configparser.ConfigParser()
  configs.read(inpath)

def html2text(inhtml): # type: (str) -> str
  """
  Strips HTML coding and replaces, if possible, with UTF-8 characters.
  Removes newlines.

  :param inhtml: text that might include HTML tags
  :type inhtml: str

  :return: UTF-8 text with no HTML or newlines
  :rtype: str

  """

  parsed = BeautifulSoup(inhtml, features='html.parser')
  rettext = parsed.get_text()
  rettext = rettext.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')

  return rettext

def writeCSV(outpath, data, headers=None): # type: (str, [], []) -> None
  """
  Writes a list of dictionaries to a CSV file.  Each dictionary
  must have exactly the headers as keys.

  :param outpath: the location on disk to write the file
  :type outpath: str
  :param data: the list of dictionaries that will become rows
  :type data: []
  :param headers: the list of column headers.  If none is provided, use the list of keys from the first dictionary in data.
  :type headers: []
  """

  useheaders = headers
  if headers is None or len(headers) == 0:
    useheaders = list(data[0].keys())

  with open(outpath, 'w', encoding='utf-8', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=useheaders)
    writer.writeheader()
    writer.writerows(data)

def getresourcefolder(): # type: () -> str
  """
  Returns the path of the folder that module resources
  are stored in.
  """

  this_dir, this_filename = os.path.split(__file__)
  resourcePath = os.path.join(this_dir, 'resources')

  return resourcePath

def coastalize(instr): # type: (str) -> str
  """
  Replaces the internal 6-character representation of coasts with DAIDE
  parentheticals.

  :param instr: a DAIDE expression that might have 6-character coast representations
  :type instr: str

  :return: a DAIDE expression with coasts as parentheticals
  :rtype: str

  """

  retstr = instr
  retstr = re.sub(r'([A-Z]{3})([ENS]C)S', r'(\1 \2S)', retstr)
  return retstr

def datccoastalize(instr): # type: (str) -> str
  """
  Replaces the internal 6-character representation of coasts with DATC
  notation.

  :param instr: a DAIDE expression that might have 6-character coast representations
  :type instr: str

  :return: a DATC expression with coasts in shorthand
  :rtype: str

  """

  retstr = instr
  retstr = re.sub(r'([A-Z]{3})([ENS])CS', r'\1/\2C', retstr)

  return retstr

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

  orderedlist = []
  if (frompower is None or frompower == '') and (topowers is None or len(topowers) == 0):
    orderedlist = [powerdict[curpower]['Objective'] for curpower in powerlist]
  else:
    allinclusive = False
    if topowers is not None:
      listedto = [curpower for curpower in topowers if curpower in powerlist]
      allinclusive = len(listedto) == len(topowers)

    if allinclusive:
      if len(topowers) < 2:
        orderedlist.append('you')
      else:
        orderedlist.append('you ' + str(size2numstr(topowers)))
    elif frompower not in powerlist:
      orderedlist = [powerdict[curpower]['Objective'] for curpower in powerlist]

    for curpower in powerlist:
      if curpower != frompower and curpower not in topowers and powerdict[curpower]['Objective'] not in orderedlist:
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

  Example: FRM ( ENG) (FRA ITA) (PRP (ALY (ENG  FRA ITA)VSS(RUS TUR) ))
  yields ["FRM", ["ENG"], ["FRA", "ITA"], ["PRP", ["ALY", ["ENG", "FRA", "ITA"], "VSS", ["RUS", "TUR"]]]]

  :param daide: a press utterance in DAIDE syntax (with From and To info)
  :type daide: str

  :return: a nested list representation resulting from replacing DAIDE parentheses with JSON brackets
  :rtype: []

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

  # handle the coasts - unsure if DAIDE really specifies it this way, but was observed in the wild
  metamorphosis = re.sub(r'\(([A-Z]+) ([ENS])CS\)', r'\1\2CS', metamorphosis) # (FRM (FRA) (ENG) (PRP (XDO ((ENG AMY LVP) MTO (SPA NCS))))) to (FRM (FRA) (ENG) (PRP (XDO ((ENG AMY LVP) MTO SPANCS))))
  metamorphosis = re.sub(r'([A-Z]+)/([ENS])CS?', r'\1\2CS', metamorphosis) # (FRM (FRA) (ENG) (PRP (XDO ((ENG AMY LVP) MTO SPA/NC)))) to (FRM (FRA) (ENG) (PRP (XDO ((ENG AMY LVP) MTO SPANCS))))

  # transformations to JSON
  metamorphosis = re.sub(r'([A-Z]+)', r'"\1"', metamorphosis) # ("FRM" ("ENG") ("FRA" "ITA") ("PRP" ("ALY" ("ENG" "FRA" "ITA") "VSS" ("RUS" "TUR"))))
  metamorphosis = re.sub(r' ', r', ', metamorphosis) # ("FRM", ("ENG"), ("FRA", "ITA"), ("PRP", ("ALY", ("ENG", "FRA", "ITA"), "VSS", ("RUS", "TUR"))))
  metamorphosis = re.sub(r'\(', r'[', metamorphosis) # ["FRM", ["ENG"), ["FRA", "ITA"), ["PRP", ["ALY", ["ENG", "FRA", "ITA"), "VSS", ["RUS", "TUR"))))
  metamorphosis = re.sub(r'\)', r']', metamorphosis) # ["FRM", ["ENG"], ["FRA", "ITA"], ["PRP", ["ALY", ["ENG", "FRA", "ITA"], "VSS", ["RUS", "TUR"]]]]

  try:
    retlist = json.loads(metamorphosis)
  except ValueError:
    retlist = []

  return retlist

def datc2lists(owner, shorthand, thirdparty=''): # type: (str, str, str) -> []
  """
  Translates a DATC move shorthand to a nested list representation compatible
  with those parsed by the DAIDE expression parsers

  :param owner: the trigram of the owner of the units mentioned in the shorthand
  :type owner: str
  :param shorthand: a space-delimited move shorthand such as F NWG C A NWY - EDI or A IRO R MAO
  :type shorthand: str
  :param thirdparty: trigram of the owner of a supported or convoyed unit if the supported unit is of a different power than the owner
  :type thirdparty: str

  :return: a list form of a DAIDE XDO expression representing the move such as
           ['XDO', [['ENG', 'FLT', 'NWG'], 'CVY', ['FRA', 'AMY', 'NWY'], 'CTO', 'EDI']

  """

  cleansh = shorthand.strip().upper()
  cleansh = re.sub(r'([A-Z]+)/([ENS])CS', r'\1\2CS', cleansh)
  cleansh = re.sub(r'([A-Z]+)/([ENS])C', r'\1\2CS', cleansh)
  cleansh = re.sub(r'([A-Z]+)/([ENS])', r'\1\2CS', cleansh)
  shwords = cleansh.strip().split()

  retlist = ["XDO", []]

  # F NWG C A NWY - EDI => XDO ((ENG FLT NWG) CVY (FRA AMY NWY) CTO EDI)
  if ' C ' in cleansh:
    target = owner
    if thirdparty != '':
      target = thirdparty
    retlist[1].append([owner, 'FLT', shwords[1]])
    retlist[1].append('CVY')
    retlist[1].append([target, 'AMY', shwords[4]])
    retlist[1].append('CTO')
    retlist[1].append(shwords[6])
  # A IRO R MAO => XDO ((ENG AMY IRO) RTO MAO)
  elif ' R ' in cleansh:
    unittype = 'AMY'
    if cleansh.startswith('F '):
      unittype = 'FLT'
    retlist[1].append([owner, unittype, shwords[1]])
    retlist[1].append('RTO')
    retlist[1].append(shwords[3])
  # A IRO D => XDO ((ENG AMY IRO) DSB)
  elif cleansh.endswith(' D'):
    unittype = 'AMY'
    if cleansh.startswith('F '):
      unittype = 'FLT'
    retlist[1].append([owner, unittype, shwords[1]])
    retlist[1].append('DSB')
  # A LON B => XDO ((ENG AMY LON) BLD)
  elif cleansh.endswith(' B'):
    unittype = 'AMY'
    if cleansh.startswith('F '):
      unittype = 'FLT'
    retlist[1].append([owner, unittype, shwords[1]])
    retlist[1].append('BLD')
  # A LON H => XDO ((ENG AMY LON) HLD)
  elif cleansh.endswith(' H'):
    unittype = 'AMY'
    if cleansh.startswith('F '):
      unittype = 'FLT'
    retlist[1].append([owner, unittype, shwords[1]])
    retlist[1].append('HLD')
  # A IRI - MAO VIA => XDO ((ENG AMY IRI) CTO MAO VIA (UNK))
  elif cleansh.endswith(' VIA'):
    retlist[1].append([owner, 'AMY', shwords[1]])
    retlist[1].append('CTO')
    retlist[1].append(shwords[3])
    retlist[1].append('VIA')
    retlist[1].append(['UNK'])
  # A WAL S F MAO - IRI => XDO ((ENG AMY WAL) SUP (FRA FLT MAO) MTO IRI)
  elif ' S ' in cleansh and ' - ' in cleansh:
    target = owner
    if thirdparty != '':
      target = thirdparty
    unittype = 'AMY'
    if cleansh.startswith('F '):
      unittype = 'FLT'
    tarunittype = 'AMY'
    if shwords[3] == 'F':
      tarunittype = 'FLT'
    retlist[1].append([owner, unittype, shwords[1]])
    retlist[1].append('SUP')
    retlist[1].append([target, tarunittype, shwords[4]])
    retlist[1].append('MTO')
    retlist[1].append(shwords[6])
  # A WAL S F LON => XDO ((ENG AMY WAL) SUP (FRA FLT LON))
  elif ' S ' in cleansh:
    target = owner
    if thirdparty != '':
      target = thirdparty
    unittype = 'AMY'
    if cleansh.startswith('F '):
      unittype = 'FLT'
    tarunittype = 'AMY'
    if shwords[3] == 'F':
      tarunittype = 'FLT'
    retlist[1].append([owner, unittype, shwords[1]])
    retlist[1].append('SUP')
    retlist[1].append([target, tarunittype, shwords[4]])
  # F IRI - MAO => XDO ((ENG FLT IRI) MTO MAO)
  elif ' - ' in cleansh:
    unittype = 'AMY'
    if cleansh.startswith('F '):
      unittype = 'FLT'
    retlist[1].append([owner, unittype, shwords[1]])
    retlist[1].append('MTO')
    retlist[1].append(shwords[3])

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
  elif 'Hostile' in utterance.tones:
    if 'CCL' in utterance.daide:
      retstr = retstr + ' This agreement, and your participation, aren\'t worth my time.'
    elif 'REJ' in utterance.daide:
      retstr = powerdict[utterance.frompower]['Objective'] + ' cannot waste time on ' + random.choice(['this foolishness', 'you', listOfPowers(utterance.topowers, '', [])]) + ': ' + retstr
      if 'Urgent' in utterance.tones:
        retstr = retstr + ' Now leave me alone for a while, many things are afoot.'
    elif 'YES' in utterance.daide:
      retstr = 'This had better work, or ' + random.choice(['you', listOfPowers(utterance.topowers, '', [])]) + ' will soon be seeing my armies rolling into your provinces: ' + retstr
      if 'Urgent' in utterance.tones:
        retstr = retstr + ' I expect to see action on this matter from you soon.'
    elif 'PRP' in utterance.daide:
      if len(utterance.topowers) == 1:
        retstr = 'This might be your last chance. ' + retstr + ' ' + random.choice(['I await', powerdict[utterance.frompower]['Haughty'] + ' awaits']) + ' your response.'
      else:
        retstr + 'You ' + size2numstr(utterance.topowers) + ' think you\'ve got it all figured out. No matter - I have the following to propose: ' + retstr + ' ' + random.choice(['I await', powerdict[utterance.frompower]['Haughty'] + ' awaits']) + ' your response.'
    elif 'FCT' in utterance.daide:
      retstr = 'You are getting in my way - this should make you worried: ' + retstr
  elif 'Friendly' in utterance.tones:
    if 'CCL' in utterance.daide:
      retstr = retstr + ' Apologies - had to change course, but hope to work with you on other initiatives.'
    elif 'REJ' in utterance.daide:
      retstr = powerdict[utterance.frompower]['Objective'] + ' cannot make this commitment right now, but I want to find another way to work together: ' + retstr
      if 'Urgent' in utterance.tones:
        retstr = retstr + ' Let\'s talk over another possibility in the next couple turns.'
    elif 'YES' in utterance.daide:
      retstr = 'Yes, this will be a helpful move for both you and me.  ' + retstr + random.choice([' Pleasure doing business with you!', ' Best of luck with your plans!'])
    elif 'PRP' in utterance.daide:
      if len(utterance.topowers) == 1:
        retstr = 'I think this proposal will help us both out. ' + retstr + ' ' + random.choice(['You seem to be a reasonable sort.', 'I think our interests are aligned for the time being.'])
      else:
        retstr = 'Let\'s collaborate together in this phase of the game.' + retstr + ' We have more to gain from working together than going on our own.'
    elif 'FCT' in utterance.daide:
      retstr = 'Here\'s something I have learned recently.  Hope it helps with your game: ' + retstr
  elif 'Fearful' in utterance.tones:
    if 'CCL' in utterance.daide:
      retstr = retstr + ' I\'m having second thoughts about this situation.  I am nervous about your position.'
    elif 'REJ' in utterance.daide:
      retstr = powerdict[utterance.frompower]['Objective'] + ' cannot see how this benefits me, and I worry about your growing strength: ' + retstr
      if 'Urgent' in utterance.tones:
        retstr = retstr + ' Convince me you are not a significant threat to me, or I may seek alliances elsewhere.'
    elif 'YES' in utterance.daide:
      retstr = 'I agree, and hope this appeases you for the time being.  ' + retstr + random.choice([' Peaceful journey!', ' Best of luck with your plans!'])
    elif 'PRP' in utterance.daide:
      if len(utterance.topowers) == 1:
        retstr = 'Would this offer do anything to keep your armies off my territory? ' + retstr + ' ' + random.choice(['You seem to be a reasonable sort.', 'I appeal to your better nature.'])
      else:
        retstr = 'I address you as one who needs your help - things are not going well for me.' + retstr + ' We have more to gain from working together than going on our own.'
    elif 'FCT' in utterance.tones:
      retstr = 'Here\'s something I have learned recently.  It makes me nervous: ' + retstr
  elif 'Confident' in utterance.tones:
    if 'CCL' in utterance.daide:
      retstr = retstr + ' That\'s not actually the best choice I have right now - I\'m going to look for other options.'
    elif 'REJ' in utterance.daide:
      retstr = powerdict[utterance.frompower]['Objective'] + ' can do better right now, given my position in the game. ' + retstr
      if 'Urgent' in utterance.tones:
        retstr = retstr + ' I\'m close to reaching my goals - come up with a better proposal soon if you want to do something.'
    elif 'YES' in utterance.daide:
      retstr = 'This is a good proposal for me.  ' + powerdict[utterance.frompower]['Objective'] + '\'s position will be strengthened.  ' + retstr + random.choice([' Look out for ' + powerdict[utterance.frompower]['Haughty'] + '!', ' Best of luck with your plans!'])
    elif 'PRP' in utterance.daide:
      retstr = 'I can see that you might need my help.  What do you say to this? ' + retstr
    elif 'FCT' in utterance.daide:
      retstr = 'Here\'s something I have learned recently.  In my position, I can afford to share some intel: ' + retstr
  elif 'Empathetic' in utterance.tones:
    if 'CCL' in utterance.daide:
      retstr = retstr + ' I do sympathize with your position, but I must retract this.'
    elif 'REJ' in utterance.daide:
      retstr = powerdict[utterance.frompower]['Objective'] + ' sees that this would be of benefit to you, but I need more from the deal: ' + retstr
      if 'Urgent' in utterance.tones:
        retstr = retstr + ' Given how the game is going for you, come back to me soon with something better.'
    elif 'YES' in utterance.daide:
      retstr = 'I agree, and hope this helps you out for the time being.  ' + retstr + random.choice([' Peaceful journey!', ' Best of luck with your plans!'])
    elif 'PRP' in utterance.daide:
      if len(utterance.topowers) == 1:
        retstr = 'I can see that the game is not going so well for you.  Would you like some help: ' + retstr + ' ' + random.choice(['You should be able to get back on track soon.', 'I can see a couple ways out of trouble for you.'])
      else:
        retstr = 'We\'re all in the same boat.  What about a plan to move forward:' + retstr + ' We have more to gain from working together than going on our own.'
    elif 'FCT' in utterance.daide:
      retstr = 'Here\'s something I have learned recently.  Hope it helps you out: ' + retstr
  elif 'Upset' in utterance.tones:
    if 'CCL' in utterance.daide:
      retstr = retstr + ' You\'re getting on my nerves - I won\'t be willing to help you out in future.'
    elif 'REJ' in utterance.daide:
      retstr = 'This is a ridiculous offer - what makes you think I would be interested? ' + retstr
      if 'Urgent' in utterance.tones:
        retstr = retstr + ' Start paying attention or get ready to see my armies marching into your provinces.'
    elif 'YES' in utterance.daide:
      retstr = 'For now, I agree, but you need to start showing better faith: ' + retstr
      if 'Urgent' in utterance.tones:
        retstr = retstr + ' I want to see you take action on this soon, or I will lose interest in cooperating.'
    elif 'PRP' in utterance.daide:
      if len(utterance.topowers) == 1:
        retstr = 'Your recent moves are not appropriate for a peaceful relationship.  This is my last offer: ' + retstr + ' ' + random.choice(['You need to reconsider your approach.', 'I can see a difficult future for you.'])
      else:
        retstr = 'You ' + size2numstr(utterance.topowers) + ' are getting on my nerves.  This is my last offer:' + retstr + ' We should work together, but you are making that impossible.'
    elif 'FCT' in utterance.daide:
      retstr = 'Here\'s something I have learned recently.  You had better take notice: ' + retstr
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

simple_system = '''You are an assistant for the board game diplomacy that helps players convert between DAIDE and English messages. 
        The format of the inputs will be
```
FRM (RECIPIENT) (SENDER): (English message)

```
        The format of the outputs will be
```
FRM (RECIPIENT) (SENDER) (DAIDE Code)
```
A movement order is in the form of
Order Format 	
Hold: (unit) HLD 	
Move: (unit) MTO province
Support to hold: (unit) SUP (unit) 	
Support to move: (unit) SUP (unit) MTO prov_no_coast
Convoy: (unit) CVY (unit) CTO province 
Move by convoy: (unit) CTO province VIA (sea_province sea_province ...)

Press can come in the form of 
Proposal: PRP ((Press message) (Press message) (Press message)...)
Orders to do next phase: XDO ((Order) (Order) (Order)...)
Alliance of powers against another: ALY (power power...) VSS (power power...)
Peace between powers: PCE (power power...)
Demilitarized zone: DMZ (power power...) (province province...)
Query: QRY (Press message or order)
ORR: (ORR (Press message) (Press message))
AND: (AND (Press message) (Press message))
```
'''

arrangement_list = ['DMZ', 'ALY', 'PCE', 'AND', 'ORR', 'XDO']

grammar = create_daide_grammar(level=130)


def add_paranthesis(substring, string):
    match=re.findall(substring, string)
    for i in match:
        string = string.replace(i, '('+i+')')
    return string
    
#A function to remove extra characters between ALY and VSS
def aly_fix(string):
    match=re.search('(?<=ALY\(.*?\))(.*?)(?=VSS)', string)
    if match:
        start, end = match.span()
        string = string[:start] + string[end:]
        return string
    else:
        return string


def error_fetch(string):
    try:
        grammar.parse(string)
        error = 'No Error'
        return error, None
    except Exception as e:
        error = str(e)
        error_type = re.findall(r"\s'(.*?)'\s", error)[0]
        return error, error_type

def grammar_cleaner(daide_attempt:str)->str:
    i = 0

    #We need to remove some alterations that happen to the string due to preprocessing of prompts
    #Remove extra spaces
    string = re.sub(r'\s', '', daide_attempt)
    # uppercasing the string in case the training algorithm removed its uppercase. 

    string = string.upper()
    error, error_type = error_fetch(string)
    # We need to add this string in case the training prep script removed it as header. 
    

    #Check if daide_attempt starts with 'FRM ('
    if not string.startswith('FRM ('):
        string = 'FRM (' + string
    while error != 'No Error' and i < 10:
        #Get rid of incorrect server-client commands
        string = re.sub(r'\sBNC\([A-Z]*\)', '', string)
        #Replace incorrectly labeled units
        string = re.sub(r'\sA\s', ' AMY ', string)
        string = re.sub(r'\sF\s', ' FLT ', string)
        string = re.sub(r'\sFLE\s', ' FLT ', string)
        if string.count('(') > string.count(')'):
            string = string + ')'
        elif string.count('(') < string.count(')'):
            #Remove the last parenthesis
            string = string[:-1]
        
        error, error_type = error_fetch(string)
        tokens = re.findall(r'[\s\(\)]*([A-Z]{3})[\s\(\)]*', string)
        powers = []
        arrangements = []
        error_bits = re.findall(r"\s'(.*?)'[\s]*", error)
        if len(error_bits) > 1:
            message_mismatch = re.findall(r"\s'(.*?)'[\s]*", error)[1]
            message_mismatch = re.sub(r'\(', r'\(', message_mismatch)
            message_mismatch = re.sub(r'\)', r'\)', message_mismatch)
        else:
            message_mismatch = None
        for token in tokens:
            if token in powerlist:
                powers.append(token)
            if token in arrangement_list:
                arrangements.append(token)
        print(tokens)
        if 'AND' and 'PRP' in tokens:
            string = re.sub('(?<=PRP\()(.*?)(?=AND)', '', string)
        if error_type == 'message':
            print('dealing with message error')

            
            if string[:3] in arrangement_list:
                string = 'PRP(' + string + ')'

            if error[:38] == "Rule 'message' matched in its entirety": 

                string = re.sub('\s' + message_mismatch, '', string)    

            # #Remove substrings in the form of with BNC(*)
            # string = re.sub(r'\sBNC\([A-Z]*\)', '', string)
            # print(string)
            #Try to parse the string again
            print('parsing again')
            original_error = error
            error, error_type = error_fetch(string)
        elif error_type == 'rpar' or error_type == 'lpar':
            print('dealing with parenthesis error')

            print(error)
            #Count number of tokens that are in arrangement_list
            # if len(powers)>1:
            #     string = re.sub(r'\sDMZ', ' DMZ' + '(' + powers[0] + ' ' + powers[1] + ')', string)
            #     print(string)
            if len(arrangements) > 1 and 'AND' not in tokens: 
                string = re.sub(r'PRP\(', 'PRP(AND ', string)
            if 'AND' in tokens:
                #Add parenthesis to around PCE(...)
                string = add_paranthesis(r'PCE\(.*?\)(?=\s)', string)

                #Add parenthesis to around DMZ(...)
                string = add_paranthesis(r'(?<=\s)DMZ[\s]*\(.*?\)[\s]*\(.*?\)', string)
                string = add_paranthesis(r'ALY\(.*?\)[\s]*VSS[\s]*\(.*?\)(?=\s)', string)
                string = add_paranthesis(r'XDO\(.*?\).*?\)(?<=\s)', string)
            #Count paranthesis and balance them across the string 
            print('parsing again')
            original_error = error
            error, error_type = error_fetch(string)
        elif error_type == 'arrangement': 
            print('dealing with arrangement error')
            if message_mismatch == None: 
                return string
            message_mismatch = message_mismatch[:3]
            if 'VSS' in tokens:
                #Replace mismatch string with ALY
                string = re.sub(message_mismatch, 'ALY', string)
                #remove characters between ALY(.*?) and VSS 
                string = re.sub('(?<=ALY\(.{7}?\))(.*?)(?=VSS)', '', string)
            else:
                print(message_mismatch)
                string = re.sub(message_mismatch, 'PCE', string)
            print('parsing again')
            error, error_type = error_fetch(string)
        elif error_type == 'press_message':

            if string[:3] == 'YES' and 'PRP' not in tokens:
                string = string[:3] + '(PRP' + string[3:] + ')'


            print('parsing again')
            error, error_type = error_fetch(string)

        print(string)

        i += 1
    i += 1

    if error != 'No Error':
        return(daide_attempt)
    else:
        return string

def jsonl_loader(json_file_pointer: str)->list: 
  with open(json_file_pointer, 'r') as json_file:
    return list(json_file)
  

def dicts_to_jsonl(data_list: list, filename: str) -> None:
    """
    Method saves list of dicts into jsonl file.
    :param data: (list) list of dicts to be stored,
    :param filename: (str) path to the output file. If suffix .jsonl is not given then methods appends
        .jsonl suffix into the file.
    """
    sjsonl = '.jsonl'
    # Check filename
    if not filename.endswith(sjsonl):
        filename = filename + sjsonl
    # Save data
    with open(filename, 'w') as out:
        for ddict in data_list:
            jout = json.dumps(ddict) + '\n'
            out.write(jout)

def run_cmd(cmd):
    result = subprocess.run([
      '/bin/bash',
      '-c',
      cmd
    ], stdout=subprocess.PIPE)
    returncode = result.returncode
    stdout = result.stdout
    return { 'returncode' : returncode, 'stdout': stdout}
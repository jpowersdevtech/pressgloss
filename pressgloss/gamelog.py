# Standard imports
import json
import os
from collections import Counter
import copy

# pressgloss imports
import pressgloss.core as PRESSGLOSS
from . import helpers

def analyzedblog(ingameid, eventspath, summarypath): # type: (int, str, str) -> None
  """
  Analyze game logs from a database source (initialized by helper and
  a command-line config argument).

  :param ingameid: the ID of the game to analyze
  :type ingameid: int
  :param eventspath: a file location to write event results
  :type eventspath: str
  :param summarypath: a file location to write summary results
  :type summarypath: str

  """

  conn = helpers.getSQLConnection()
  # Show tables
  # alltblcur = conn.cursor(prepared=True)
  # alltblcur.execute('show tables;')
  # results = alltblcur.fetchall()
  # alltblcur.close()
  # for curresult in results:
  #   curtablename = str(curresult[0])
  #   tblcur = conn.cursor(prepared=True)
  #   tblcur.execute('describe ' + curtablename)
  #   tblresults = tblcur.fetchall()
  #   tblcur.close()
  #   print('Table name: ' + curtablename)
  #   for curcol in tblresults:
  #     print('  ' + str(curcol))
  #   print('')

  # get game info from wd_games
  gamecur = conn.cursor(prepared=True)
  gamecur.execute('select * from wd_games where id=?', (ingameid,))
  gamedata = helpers.cursor2dicts(gamecur)
  gamecur.close()
  if len(gamedata) != 1:
    print('Strange results for game ' + str(ingameid))
    return
  variantid = gamedata[0]['variantID']

  # get variant info from wd_variantinfo
  variantcur = conn.cursor(prepared=True)
  variantcur.execute('select * from wd_variantinfo where variantID=?', (variantid,))
  variantdata = helpers.cursor2dicts(variantcur)
  variantcur.close()
  if len(variantdata) != 1:
    print('String results for variant ' + str(variantid))
    return
  countrylabels = variantdata[0]['countriesList'].split(',')
  mapid = variantdata[0]['mapID']
  # get country mappings
  index2countryname = {cCountry + 1: curLabel for cCountry, curLabel in enumerate(countrylabels)}

  # get territory data
  terrcur = conn.cursor(prepared=True)
  terrcur.execute('select * from wd_territories where mapID=?', (mapid,))
  terrdata = helpers.cursor2dicts(terrcur)
  terrcur.close()
  # get territory mappings
  id2territory = {currow['id']: currow['name'] for currow in terrdata}

  # get turndate data for inspection
  # turncur = conn.cursor(prepared=True)
  # turncur.execute('select * from wd_turndate where gameID=?', (ingameid,))
  # turndata = helpers.cursor2dicts(turncur)
  # turncur.close()
  # print(str(turndata))

  # get move data
  movecur = conn.cursor(prepared=True)
  movecur.execute('select * from wd_movesarchive where gameID=?', (ingameid,))
  movedata = helpers.cursor2dicts(movecur)
  movecur.close()

  # apply country and territory labels to relevant columns
  for curmove in movedata:
    curmove['terrID'] = id2territory[curmove['terrID']]
    curmove['countryID'] = index2countryname[curmove['countryID']]
    if curmove['toTerrID'] is not None and curmove['toTerrID'] in id2territory:
      curmove['toTerrID'] = id2territory[curmove['toTerrID']]
    else:
      curmove['toTerrID'] = ''
    if curmove['fromTerrID'] is not None and curmove['fromTerrID'] in id2territory:
      curmove['fromTerrID'] = id2territory[curmove['fromTerrID']]
    else:
      curmove['fromTerrID'] = ''

  # get messages
  messagecur = conn.cursor(prepared=True)
  messagecur.execute('select * from wD_GameMessages where gameID=? order by id', (ingameid,))
  messagedata = helpers.cursor2dicts(messagecur)
  messagecur.close()
  conn.close()

  summaries = {}
  # apply country labels to to and from columns, roll up behavior
  for curmessage in messagedata:
    curmessage['fromCountryID'] = index2countryname[curmessage['fromCountryID']]
    curmessage['toCountryID'] = index2countryname[curmessage['toCountryID']]
    if curmessage['fromCountryID'] + '-' + curmessage['toCountryID'] not in summaries:
      summaries[curmessage['fromCountryID'] + '-' + curmessage['toCountryID']] = Counter()
    if curmessage['fromCountryID'] + '_as_sender' not in summaries:
      summaries[curmessage['fromCountryID'] + '_as_sender'] = Counter()
    if curmessage['toCountryID'] + '_as_recipient' not in summaries:
      summaries[curmessage['toCountryID'] + '_as_recipient'] = Counter()
    summaries[curmessage['fromCountryID'] + '-' + curmessage['toCountryID']]['messages'] += 1
    summaries[curmessage['fromCountryID'] + '_as_sender']['messages'] += 1
    summaries[curmessage['toCountryID'] + '_as_recipient']['messages'] += 1
    if curmessage['intentDeceive'] is None or curmessage['intentDeceive'] == 'no':
      summaries[curmessage['fromCountryID'] + '-' + curmessage['toCountryID']]['sent_honestly'] += 1
      summaries[curmessage['fromCountryID'] + '_as_sender']['was_honest'] += 1
      summaries[curmessage['toCountryID'] + '_as_recipient']['got_honest_messages'] += 1
    elif curmessage['intentDeceive'] == 'unsure':
      summaries[curmessage['fromCountryID'] + '-' + curmessage['toCountryID']]['sent_uncertainly'] += 1
      summaries[curmessage['fromCountryID'] + '_as_sender']['was_uncertain'] += 1
      summaries[curmessage['toCountryID'] + '_as_recipient']['got_uncertain_messages'] += 1
    else:
      summaries[curmessage['fromCountryID'] + '-' + curmessage['toCountryID']]['sent_deceptively'] += 1
      summaries[curmessage['fromCountryID'] + '_as_sender']['was_deceptive'] += 1
      summaries[curmessage['toCountryID'] + '_as_recipient']['got_deceptive_messages'] += 1
    if curmessage['suspectedIncomingDeception'] is None or curmessage['suspectedIncomingDeception'] == '':
      summaries[curmessage['fromCountryID'] + '-' + curmessage['toCountryID']]['not_judged_by_recipient'] += 1
      summaries[curmessage['fromCountryID'] + '_as_sender']['messages_not_judged'] += 1
      summaries[curmessage['toCountryID'] + '_as_recipient']['did_not_judge_messages'] += 1
    elif curmessage['intentDeceive'] == 'no':
      summaries[curmessage['fromCountryID'] + '-' + curmessage['toCountryID']]['judged_as_honest'] += 1
      summaries[curmessage['fromCountryID'] + '_as_sender']['messages_judged_as_honest'] += 1
      summaries[curmessage['toCountryID'] + '_as_recipient']['judged_messages_as_honest'] += 1
    else:
      summaries[curmessage['fromCountryID'] + '-' + curmessage['toCountryID']]['judged_as_deceptive'] += 1
      summaries[curmessage['fromCountryID'] + '_as_sender']['messages_judged_as_deceptive'] += 1
      summaries[curmessage['toCountryID'] + '_as_recipient']['judged_messages_as_deceptive'] += 1

  movecolset = set(list(movedata[0].keys()))
  movecolset.remove('dislodged')
  messagecolset = set(list(messagedata[0].keys()))
  messagecolset.remove('id')
  messagecolset.remove('phaseMarker')
  messagecolset.remove('fromCountryID')
  moveonly = movecolset.difference(messagecolset)
  messageonly = messagecolset.difference(movecolset)

  # create unified event list
  events = []
  for curmessage in messagedata:
    for curcol in moveonly:
      curmessage[curcol] = ''
    del curmessage['id']
    del curmessage['phaseMarker']
    curmessage['eventtype'] = 'Message'
    curmessage['countryID'] = curmessage.pop('fromCountryID')
    curmessage['conversation'] = '-'.join(sorted([curmessage['countryID'], curmessage['toCountryID']]))
    curmessage['message'] = helpers.html2text(curmessage['message'])
    events.append(curmessage)
  for curmove in movedata:
    for curcol in messageonly:
      curmove[curcol] = ''
    del curmove['dislodged']
    curmove['eventtype'] = 'Move'
    curmove['conversation'] = ''
    events.append(curmove)

  print('Got ' + str(len(events)) + ' events')
  helpers.writeCSV(eventspath, events, helpers.eventcols)

  summarydata = []
  for curkey, curval in summaries.items():
    for curlabel, curstat in curval.items():
      curdict = {}
      curdict['Conversation'] = curkey
      curdict['Annotation'] = curlabel
      curdict['Count'] = curstat
      summarydata.append(curdict)
  helpers.writeCSV(summarypath, summarydata, ['Conversation', 'Annotation', 'Count'])

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

def extractdatc(incontent): # type: (PRESSGLOSS.PressMessage) -> []
  """
  Returns a list of DATC shorthands for any XDOs contained within the message.  Does not understand negation at this time.

  :param incontent: the DAIDE message
  :type incontent PRESSGLOSS.PressMessage

  :return: a list of DATC shorthands
  :rtype: []

  """

  if incontent.operator == 'XDO':
    return [incontent.formDATC()[1]]
  elif incontent.operator in ['PRP', 'YES']:
    return extractdatc(incontent.details)
  elif incontent.operator == 'AND':
    retlist = []
    for curconj in incontent.conjuncts:
      retlist.extend(extractdatc(curconj))
    return retlist
  elif incontent.operator == 'ORR':
    retlist = []
    for curdisj in incontent.disjuncts:
      retlist.extend(extractdatc(curdisj))
    return retlist

  return []

def operatorcounts(incontent): # type: (PRESSGLOSS.PressMessage) -> Counter
  """
  Counts the uses of each DAIDE operator in the message.

  :param incontent: the DAIDE message
  :type incontent PRESSGLOSS.PressMessage

  :return: how many times each DAIDE operator was used in the message
  :rtype: Counter

  """

  retct = Counter()
  if incontent is None or incontent.operator is None:
    if incontent is not None and incontent.details is not None:
      retct += operatorcounts(incontent.details)
    return retct

  retct[incontent.operator] += 1
  if incontent.details is not None:
    retct += operatorcounts(incontent.details)
  if incontent.operator == 'AND':
    for curconj in incontent.conjuncts:
      retct += operatorcounts(curconj)
  elif incontent.operator == 'ORR':
    for curdisj in incontent.disjuncts:
      retct += operatorcounts(curdisj)
  elif incontent.operator == 'IFF':
    retct += operatorcounts(incontent.antecedent)
    retct += operatorcounts(incontent.consequent)
    if incontent.alternative is not None:
      retct += operatorcounts(incontent.alternative)

  return retct

def annotatelog(inlog): # type: ({}) -> {}
  """
  Annotate a Diplomacy game log with glosses for each message containing only DAIDE

  :param inlog: the parsed-from-JSON representation of a Diplomacy game log
  :type inlog: {}

  :return: the same game log with press which was DAIDE annotated with English glosses.
  :rtype: {}

  """

  retdict = copy.deepcopy(inlog)

  if 'phases' in retdict:
    retdict['id'] += '_gloss'
    for curphase in retdict['phases']:
      if 'messages' in curphase:
        for curmessage in curphase['messages']:
          cursender = curmessage['sender']
          cursendersym = helpers.powername2sym[cursender]
          currecipient = curmessage['recipient']
          currecsym = helpers.powername2sym[currecipient]
          if currecipient != 'GLOBAL':
            curcontent = curmessage['message']
            curdaide = 'FRM (' + cursendersym + ') (' + currecsym + ') (' + curcontent + ')'
            curutterance = PRESSGLOSS.PressUtterance(curdaide, ['Objective', 'Expert'])
            curutterance.formenglish()
            curpress = curutterance.english
            if 'Ahem' in curpress:
              curmessage['message'] = curcontent + ':\nNot glossable DAIDE.'
            else:
              curpress = curpress.replace('<ul>', '\n')
              curpress = curpress.replace('</ul>', '')
              curpress = curpress.replace('<li>', '* ')
              curpress = curpress.replace('</li>', '\n')
              curpress = curpress.replace('<br>', '\n')
              curpress = curpress.replace('<br/>', '\n')
              curmessage['message'] = curcontent + ':\n' + curpress
          else:
            curmessage['message'] += ':\nGlobal messages not glossed.'

  return retdict

def findPromises(ingame): # type: ({}) -> []
  """
  Analyzes moves and DAIDE press to find instances of cooperation on XDO proposals and/or acceptances.

  :param ingame: a parsed JSON game log
  :type ingame: {}

  :return: a list of descriptions of moves and actors, and if they had been previously proposed and/or accepted.
  :rtype: []

  """

  retlist = []

  if 'phases' in ingame:
    datc2proposals = {}
    datc2accepts = {}
    for curphase in ingame['phases']:
      if 'messages' in curphase:
        for curmessage in curphase['messages']:
          cursender = curmessage['sender']
          cursendersym = helpers.powername2sym[cursender]
          currecipient = curmessage['recipient']
          currecsym = helpers.powername2sym[currecipient]
          if currecipient != 'GLOBAL':
            curcontent = curmessage['message']
            curdaide = 'FRM (' + cursendersym + ') (' + currecsym + ') (' + curcontent + ')'
            curutterance = PRESSGLOSS.PressUtterance(curdaide, ['Objective', 'Expert'])
            curutterance.formenglish()
            curpress = curutterance.english
            if 'Ahem' not in curpress:
              if curutterance.content.operator == 'PRP':
                datcs = extractdatc(curutterance.content)
                for curdatc in datcs:
                  moverkey = currecsym + '::' + curdatc
                  requesterdict = {'Mover Power': currecsym,
                                   'Move': curdatc,
                                   'Requester Power': cursendersym,
                                   'Request Phase': curphase['name']}
                  if moverkey not in datc2proposals:
                    datc2proposals[moverkey] = []
                  datc2proposals[moverkey].append(requesterdict)
              elif curutterance.content.operator == 'YES':
                datcs = extractdatc(curutterance.content)
                for curdatc in datcs:
                  moverkey = cursendersym + '::' + curdatc
                  accepterdict = {'Accepter Power': cursendersym,
                                  'Accept Phase': curphase['name']}
                  if moverkey not in datc2accepts:
                    datc2accepts[moverkey] = []
                  datc2accepts[moverkey].append(accepterdict)
      if 'orders' in curphase:
        for powername, curorders in curphase['orders'].items():
          if curorders is not None:
            powersym = helpers.powername2sym[powername]
            for curorder in curorders:
              cleanorder = curorder.replace('ENG', 'ECH')
              basemovedict = {'Game': ingame['id'],
                              'Mover Power': powersym,
                              'Move': cleanorder,
                              'Move Phase': curphase['name']}
              if powersym + '::' + cleanorder in datc2proposals:
                for curpropsal in datc2proposals[powersym + '::' + cleanorder]:
                  curmovedict = {key: val for key, val in basemovedict.items()}
                  curmovedict.update(curpropsal)
                  if powersym + '::' + cleanorder in datc2accepts:
                    for curaccept in datc2accepts[powersym + '::' + cleanorder]:
                      curaccdict = {key: val for key, val in curmovedict.items()}
                      curaccdict.update(curaccept)
                      retlist.append(curaccdict)
                  else:
                    curmovedict['Accepter Power'] = ''
                    curmovedict['Accept Phase'] = ''
                    retlist.append(curmovedict)
              else:
                basemovedict['Requester Power'] = ''
                basemovedict['Request Phase'] = ''
                basemovedict['Accepter Power'] = ''
                basemovedict['Accept Phase'] = ''
                retlist.append(basemovedict)

  return retlist

def analyzegym(inpath): # type: (str) -> []
  """
  Searches through a folder for game logs and returns a list of paths to those which might be interesting for analysis.
  Also creates prettyfied JSON logs and game transcripts with press gloss

  :param inpath: the folder that the logs are in
  :type inpath: str

  :return: a list of paths to game log files used in the analysis
  :rtype: []

  """

  retset = set()

  promises = []
  for root, dirs, files in os.walk(os.path.abspath(inpath)):
    for file in files:
      curfullpath = os.path.join(root, file)
      if file.endswith('.json') and '_pretty.json' not in file and '_gloss.json' not in file:
        print('Processing ' + file)
        with open(curfullpath, 'r', encoding='UTF-8') as jf:
          curgame = json.load(jf)
        promises.extend(findPromises(curgame))
        if 'phases' in curgame:
          daideoperators = Counter()
          powerdaideuse = {'FRANCE': Counter(),
                           'ENGLAND': Counter(),
                           'AUSTRIA': Counter(),
                           'GERMANY': Counter(),
                           'ITALY': Counter(),
                           'RUSSIA': Counter(),
                           'TURKEY': Counter()}
          messagesenders = Counter()
          messagerecipients = Counter()
          messageexchanges = Counter()
          messages = 0
          daideerrors = 0
          retset.add(curfullpath)
          prtyfile = file.replace('.json', '_pretty.json')
          fullprettypath = os.path.join(root, prtyfile)
          prettifygamefile(curfullpath, fullprettypath)
          for curphase in curgame['phases']:
            if 'messages' in curphase:
              for curmessage in curphase['messages']:
                messages += 1
                cursender = curmessage['sender']
                messagesenders[cursender] += 1
                cursendersym = helpers.powername2sym[cursender]
                currecipient = curmessage['recipient']
                messagerecipients[currecipient] += 1
                currecsym = helpers.powername2sym[currecipient]
                messageexchanges[cursender + '->' + currecipient] += 1
                if currecipient != 'GLOBAL':
                  curcontent = curmessage['message']
                  curdaide = 'FRM (' + cursendersym + ') (' + currecsym + ') (' + curcontent + ')'
                  curutterance = PRESSGLOSS.PressUtterance(curdaide, ['Objective', 'Expert'])
                  daideoperators += operatorcounts(curutterance.content)
                  powerdaideuse[cursender] += operatorcounts(curutterance.content)
                  curutterance.formenglish()
                  curpress = curutterance.english
                  if 'Ahem' in curpress:
                    daideerrors += 1
                    powerdaideuse[cursender]['Error'] += 1
          curglossgame = annotatelog(curgame)
          glossfile = file.replace('.json', '_gloss.json')
          fullglosspath = os.path.join(root, glossfile)
          with open(fullglosspath, 'w', encoding='UTF-8') as of:
            json.dump(curglossgame, of, indent=2)
          print(curfullpath)
          print('  ' + str(messages) + ' messages sent')
          print('  ' + str(daideerrors) + ' DAIDE errors')
          print('  Messages sent by ' + str(messagesenders.most_common()))
          print('  Messages sent to ' + str(messagerecipients.most_common()))
          print('  Message pairs ' +  str(messageexchanges.most_common()))
          print('  DAIDE usage ' +  str(daideoperators.most_common()))
          for curpower, curdaideuse in powerdaideuse.items():
            print('  ' + curpower + ' DAIDE usage ' + str(curdaideuse.most_common()))

  helpers.writeCSV(os.path.join(inpath, 'moves.csv'), promises)

  return list(retset)

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
              curdaide = PRESSGLOSS.PressUtterance(curmessage['daide'], curtones)
              messages += 1
              if 'Ahem' in curdaide.english:
                daideerrors += 1
              if curdaide.content is not None:
                daideoperators[curdaide.content.operator] += 1
                if curdaide.content.details is not None:
                  daideoperators[curdaide.content.details.operator] += 1
            if len(messagelist) > 0 and curfullpath not in retset:
              retset.add(curfullpath)
        if 'status' in curgame and curgame['status'] == 'completed':
          print(curfullpath + ' completed')
          print('  won by ' + str(curgame['victory']))
          print('  outcome: ' + str(curgame['outcome']))
        else:
          print(curfullpath + ' in progress')
        ctrl2powers = {}
        for curpower, powerinfo in curgame['powers'].items():
          print(curpower + ':')
          dummyct = 0
          for ctrlid, ctrlname in powerinfo['controller'].items():
            cleanname = ctrlname.strip().lower()
            if cleanname == 'dummy':
              dummyct += 1
            if cleanname not in ctrl2powers:
              ctrl2powers[cleanname] = set()
            ctrl2powers[cleanname].add(curpower)
          if len(powerinfo['controller']) == dummyct and dummyct > 0:
            print('  Dummy')
          elif dummyct > 0:
            print('  Hybrid')
          elif dummyct == 0:
            print('  All Human')
          else:
            print('  Odd controller data')
        print(str(ctrl2powers))
        print('  ' + str(len(curgame['order_history'])) + ' seasons played')

  print('Press found in ' + str(len(retset)) + ' games.')
  print('  ' + str(messages) + ' messages found.')
  print('  ' + str(daideerrors) + ' DAIDE errors found.')
  print(str(tonesused.most_common()))
  print(str(daideoperators.most_common()))

  return list(retset)

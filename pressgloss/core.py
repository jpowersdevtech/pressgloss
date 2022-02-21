# -*- coding: utf-8 -*-
"""%pressgloss% library"""

# Standard library imports
import logging

# pressgloss imports
from . import helpers

class PressUtterance:
  """ A statement by a Diplomacy Power addressed to other Powers and regarding some in-game topic """

  def __init__(self, daide='', tones=None): # type: (str, []) -> None
    """
    Initialize the utterance with a DAIDE expression

    :param daide: the press utterance in DAIDE syntax
    :type daide: str
    :param tones: the tones to use when forming English
    :type tones: []
    """

    if tones is None:
      self.tones = []
    else:
      self.tones = tones
    self.daide = daide
    thelists = helpers.daide2lists(daide)
    if len(thelists) == 4 and thelists[0] == 'FRM':
      self.frompower = thelists[1][0]
      self.topowers = thelists[2]
      self.content = PressMessage(thelists[3])
      self.content.daide = daide
    else:
      self.frompower = ''
      self.topowers = []
      self.content = None
    self.english = 'Ahem.'

  def __eq__(self, other): # type: (PressUtterance) -> bool
    """
    Override default equality with a comparison of DAIDE expressions

    :param other: the other utterance to compare
    :type other: PressUtterance
    :return: if these utterances are equal
    :rtype: bool
    """

    return self.daide.lower() == other.daide.lower()

  def __ne__(self, other): # type: (PressUtterance) -> bool
    """
    Override default inequality with reference to equality

    :param other: the other utterance to compare
    :type other: PressUtterance
    :return: if these utterances are not equal
    :rtype: bool
    """

    return not self.__eq__(other)

  def formenglish(self, tones=None): # type ([]) -> None
    """
    Creates an English expression either using the initial tones or a given new set.
    Stores the English in the object as the 'english' attribute.

    :param tones: the tones to use when forming English
    :type tones: []
    """

    if tones is not None and len(tones) > 0:
      self.tones = tones

    if self.content is None or len(self.content.details) == 0:
      self.english = 'Ahem.'
    else:
      self.english = self.content.formenglish(self.frompower, self.topowers, self.tones)

class PressMessage:
  """ The game-related content of an utterance. """

  def __init__(self, details=None): # type: ([], []) -> None
    """
    Initialize the message with a DAIDE expression

    :param details: the press message in JSON list form
    :type details: []
    """

    self.daide = ''
    if details is None:
      self.details = []
    else:
      self.details = details

  def __eq__(self, other): # type: (PressMessage) -> bool
    """
    Override default equality with a comparison of DAIDE expressions

    :param other: the other message to compare
    :type other: PressMessage
    :return: if these messages are equal
    :rtype: bool
    """

    return self.details == other.details

  def __ne__(self, other): # type: (PressMessage) -> bool
    """
    Override default inequality with reference to equality

    :param other: the other message to compare
    :type other: PressMessage
    :return: if these messages are not equal
    :rtype: bool
    """

    return not self.__eq__(other)

  def longTerm(self, arrangement, frompower, topowers): # type ([], str, []) -> str
    """
    Creates an English description of a long-term arrangement.

    :param arrangement: the nested list form of the DAIDE arrangement
    :type arrangement: []
    :param frompower: the trigram of the sending power
    :type frompower: str
    :param topowers: the trigrams of the receiving powers
    :type topowers: []

    :return: the English arrangement gloss
    :rtype: str
    """

    retstr = 'Ahem.'

    if arrangement[0] == 'PCE':
      outoftheloop = [curpower for curpower in arrangement[1] if curpower != frompower and curpower not in topowers]
      if len(outoftheloop) == 0:
        if frompower in arrangement[1]:
          retstr = 'a peace treaty between us'
        else:
          retstr = 'a peace treaty between you'
      else:
        retstr = 'a peace treaty between ' + helpers.listOfPowers(arrangement[1], frompower, topowers)
    elif arrangement[0] == 'ALY':
      maskedallies = [curpower for curpower in arrangement[1] if curpower != frompower and curpower not in topowers]
      if len(maskedallies) > 0:
        if frompower in arrangement[1]:
          retstr = 'an alliance against ' + helpers.listOfPowers(arrangement[3], frompower, topowers) + ' involving ' + helpers.listOfPowers(maskedallies, None, None)
        else:
          retstr = 'an alliance against ' + helpers.listOfPowers(arrangement[3], frompower, topowers) + ' involving ' + helpers.listOfPowers(maskedallies, None, None)
      elif frompower in arrangement[1]:
        retstr = 'an alliance against ' + helpers.listOfPowers(arrangement[3], frompower, topowers)
      else:
        retstr = 'an alliance against ' + helpers.listOfPowers(arrangement[3], frompower, topowers) + ' involving ' + helpers.listOfPowers(arrangement[1], frompower, topowers)
    elif arrangement[0] == 'DMZ':
      retstr = 'a Demilitarized Zone in ' + helpers.listOfProvinces(arrangement[2]) + ' for ' + helpers.listOfPowers(arrangement[1], frompower, topowers)

    return retstr

  def endGame(self, endgoal, frompower, topowers):
    """
    Creates an English description of an end goal.

    :param endgoal: the nested list form of the DAIDE endgoal
    :type endgoal: []
    :param frompower: the trigram of the sending power
    :type frompower: str
    :param topowers: the trigrams of the receiving powers
    :type topowers: []

    :return: the English endgoal gloss
    :rtype: str
    """

    retstr = ''

    if endgoal[0] == 'DRW':
      if len(endgoal) == 1:
        retstr = 'a draw between you and me'
      else:
        retstr = 'a draw between ' + helpers.listOfPowers(endgoal[1], frompower, topowers)
    elif endgoal[0] == 'SLO':
      if frompower in endgoal[1]:
        retstr = 'a solo win by me'
      elif len(topowers) == 1 and topowers[0] in endgoal[1]:
        retstr = 'a solo win by you'
      else:
        retstr = 'a solo win by ' + helpers.listOfPowers(endgoal[1], frompower, topowers)

    return retstr

  def bustAMove(self, movedetails, frompower, topowers): # type ([], str, []) -> str
    """
    Creates an English description of a Diplomacy move.

    :param movedetails: the nested list form of the DAIDE move
    :type movedetails: []
    :param frompower: the trigram of the sending power
    :type frompower: str
    :param topowers: the trigrams of the receiving powers
    :type topowers: []

    :return: the English move gloss
    :rtype: str
    """

    retstr = ''

    if len(movedetails) < 2:
      return retstr

    if movedetails[1] == 'HLD' and len(movedetails[0]) > 2:
      retstr = helpers.powerdict[movedetails[0][0]]['Objective'] + \
               ' holds their ' + \
               helpers.unitdict[movedetails[0][1]]['Objective'] + \
               ' in ' + \
               helpers.provincedict[movedetails[0][2]]['Objective'] + '.'
    elif movedetails[1] == 'MTO' and len(movedetails) > 2 and len(movedetails[0]) > 2:
      retstr = helpers.powerdict[movedetails[0][0]]['Objective'] + \
               ' moves their ' + \
               helpers.unitdict[movedetails[0][1]]['Objective'] + \
               ' from ' + \
               helpers.provincedict[movedetails[0][2]]['Objective'] + \
               ' to ' + \
               helpers.provincedict[movedetails[2]]['Objective'] + '.'
    elif len(movedetails) == 5 and movedetails[1] == 'SUP' and movedetails[3] == 'MTO' and len(movedetails[0]) > 2 and len(movedetails[2]) > 2:
      retstr = helpers.powerdict[movedetails[0][0]]['Objective'] + \
               ' provides support with their ' + \
               helpers.unitdict[movedetails[0][1]]['Objective'] + \
               ' in ' + \
               helpers.provincedict[movedetails[0][2]]['Objective'] + \
               ' so ' + \
               helpers.powerdict[movedetails[2][0]]['Objective'] + \
               ' can move their ' + \
               helpers.unitdict[movedetails[2][1]]['Objective'] + \
               ' from ' + \
               helpers.provincedict[movedetails[2][2]]['Objective'] + \
               ' into ' + \
               helpers.provincedict[movedetails[4]]['Objective'] + '.'
    elif movedetails[1] == 'SUP' and len(movedetails) > 2 and len(movedetails[2]) > 2 and len(movedetails[0]) > 2:
      retstr = helpers.powerdict[movedetails[0][0]]['Objective'] + \
               ' provides support with their ' + \
               helpers.unitdict[movedetails[0][1]]['Objective'] + \
               ' in ' + \
               helpers.provincedict[movedetails[0][2]]['Objective'] + \
               ' for ' + \
               helpers.powerdict[movedetails[2][0]]['Objective'] + \
               ' to hold their ' + \
               helpers.unitdict[movedetails[2][1]]['Objective'] + \
               ' in ' + \
               helpers.provincedict[movedetails[2][2]]['Objective'] + '.'
    elif movedetails[1] == 'CVY' and len(movedetails) > 4 and len(movedetails[2]) > 2 and len(movedetails[0]) > 2:
      retstr = helpers.powerdict[movedetails[0][0]]['Objective'] + \
               '\'s ' + \
               helpers.unitdict[movedetails[0][1]]['Objective'] + \
               ' in ' + \
               helpers.provincedict[movedetails[0][2]]['Objective'] + \
               ' convoys ' + \
               helpers.powerdict[movedetails[2][0]]['Objective'] + \
               '\'s ' + \
               helpers.unitdict[movedetails[2][1]]['Objective'] + \
               ' from ' + \
               helpers.provincedict[movedetails[2][2]]['Objective'] + \
               ' into ' + \
               helpers.provincedict[movedetails[4]]['Objective'] + '.'
    elif len(movedetails) == 5 and movedetails[1] == 'CTO' and movedetails[3] == 'VIA' and len(movedetails[0]) > 2:
      retstr = helpers.powerdict[movedetails[0][0]]['Objective'] + \
               '\'s ' + \
               helpers.unitdict[movedetails[0][1]]['Objective'] + \
               ' in ' + \
               helpers.provincedict[movedetails[0][2]]['Objective'] + \
               ' moves by convoy to ' + \
               helpers.provincedict[movedetails[2]]['Objective'] + \
               ' following this path: ' + \
               helpers.listOfProvinces(movedetails[4]) + '.'
    elif movedetails[1] == 'RTO' and len(movedetails) > 2 and len(movedetails[0]) > 2:
      retstr = helpers.powerdict[movedetails[0][0]]['Objective'] + \
               '\'s ' + \
               helpers.unitdict[movedetails[0][1]]['Objective'] + \
               ' retreats from ' + \
               helpers.provincedict[movedetails[0][2]]['Objective'] + \
               ' to ' + \
               helpers.provincedict[movedetails[2]]['Objective'] + '.'
    elif movedetails[1] == 'DSB' and len(movedetails[0]) > 2:
      retstr = helpers.powerdict[movedetails[0][0]]['Objective'] + \
               '\'s ' + \
               helpers.unitdict[movedetails[0][1]]['Objective'] + \
               ' in ' + \
               helpers.provincedict[movedetails[0][2]]['Objective'] + \
               ' retreats from the board.'
    elif movedetails[1] == 'BLD' and len(movedetails[0]) > 1:
      retstr = helpers.powerdict[movedetails[0][0]]['Objective'] + \
               ' builds a new ' + \
               helpers.unitdict[movedetails[0][1]]['Objective'] + \
               ' in ' + \
               helpers.provincedict[movedetails[0][2]]['Objective'] + \
               '.'
    elif movedetails[1] == 'REM' and len(movedetails[0]) > 2:
      retstr = helpers.powerdict[movedetails[0][0]]['Objective'] + \
               ' removes their ' + \
               helpers.unitdict[movedetails[0][1]]['Objective'] + \
               ' in ' + \
               helpers.provincedict[movedetails[0][2]]['Objective'] + \
               '.'
    elif movedetails[1] == 'WVE':
      retstr = helpers.powerdict[movedetails[0]]['Objective'] + \
               ' waives their next build phase.'

    return retstr

  def negate(self, negation, frompower, topowers): # type ([], str, []) -> str
    """
    Creates an English negation of an arrangement or move

    :param negation: the nested list form of the DAIDE negation
    :type negation: str
    :param frompower: the trigram of the sending power
    :type frompower: str
    :param topowers: the trigrams of the receiving powers
    :type topowers: []

    :return: the English negation
    :rtype: str
    """

    retstr = 'Ahem.'

    arrangement = negation[1]
    if arrangement[0] in ['PCE', 'ALY', 'DMZ']:
      retstr = 'It is not the case that there is ' + self.longTerm(arrangement, frompower, topowers) + '.'
    elif arrangement[0] in ['SLO', 'DRW']:
      retstr = 'It is not the case that there is ' + self.endGame(arrangement, frompower, topowers) + '.'
    elif arrangement[0] == 'XDO':
      retstr = 'The following move will not happen: ' + self.bustAMove(arrangement, frompower, topowers) + '.'

    return retstr

  def noidea(self, unknown, frompower, topowers): # type ([], str, []) -> str
    """
    Creates an English absence of evidence of an arrangement or move

    :param negation: the nested list form of the DAIDE unknown
    :type negation: str
    :param frompower: the trigram of the sending power
    :type frompower: str
    :param topowers: the trigrams of the receiving powers
    :type topowers: []

    :return: the English unknown
    :rtype: str
    """

    retstr = 'Ahem.'

    arrangement = unknown[1]
    if arrangement[0] in ['PCE', 'ALY', 'DMZ']:
      retstr = 'I do not know if there is ' + self.longTerm(arrangement, frompower, topowers) + '.'
    elif arrangement[0] in ['SLO', 'DRW']:
      retstr = 'I do not know that there is ' + self.endGame(arrangement, frompower, topowers) + '.'
    elif arrangement[0] == 'XDO':
      retstr = 'I don\'t know if this move will happen: ' + self.bustAMove(arrangement, frompower, topowers) + '.'

    return retstr

  def englishConfuseProposal(self, frompower, topowers): # type (str, []) -> str
    """
    Creates an English confusion about a proposal in the context of a sender, recipients and desired tone.

    :param frompower: the trigram of the sending power
    :type frompower: str
    :param topowers: the trigrams of the receiving powers
    :type topowers: []

    :return: the English confusion about the proposal
    :rtype: str
    """

    retstr = 'I don\'t understand your proposal.'

    arrangement = self.details[1][1]
    if helpers.daidecontains(arrangement, 'AND'):
      retstr = 'I don\'t understand your set of proposals.'
    elif helpers.daidecontains(arrangement, 'ORR'):
      retstr = 'I don\'t understand your set of proposals.'
    elif helpers.daidecontains(arrangement, 'PCE'):
      retstr = 'I don\'t understand your peace proposal.'
    elif helpers.daidecontains(arrangement, 'ALY'):
      retstr = 'I don\'t understand your alliance proposal.'
    elif helpers.daidecontains(arrangement, 'DRW'):
      retstr = 'I don\'t understand your draw proposal.'
    elif helpers.daidecontains(arrangement, 'SLO'):
      retstr = 'I don\'t understand your solo proposal.'
    elif helpers.daidecontains(arrangement, 'XDO'):
      retstr = 'I don\'t understand your move proposal.'
    elif helpers.daidecontains(arrangement, 'DMZ'):
      retstr = 'I don\'t understand your Demilitarized Zone proposal.'

    return retstr

  def englishConfuse(self, frompower, topowers): # type (str, []) -> str
    """
    Creates an English confusion response in the context of a sender, recipients and desired tone.

    :param frompower: the trigram of the sending power
    :type frompower: str
    :param topowers: the trigrams of the receiving powers
    :type topowers: []

    :return: the English confusion
    :rtype: str
    """

    retstr = 'Ahem.'
    arrangement = self.details[1]
    if arrangement[0] == 'PRP':
      retstr = self.englishConfuseProposal(frompower, topowers)
    return retstr

  def englishCancelAgreement(self, frompower, topowers): # type (str, []) -> str
    """
    Creates an English cancellation of an agreeement in the context of a sender, recipients and desired tone.

    :param frompower: the trigram of the sending power
    :type frompower: str
    :param topowers: the trigrams of the receiving powers
    :type topowers: []

    :return: the English cancellation of the agreement
    :rtype: str
    """

    retstr = 'I wish to cancel my agreement to your latest proposal.'

    arrangement = self.details[1][1] # (PRP (PCE or (PRP (NOT (PCE
    if helpers.daidecontains(arrangement, 'AND'):
      retstr = 'I wish to cancel my agreement to your set of proposals.'
    elif helpers.daidecontains(arrangement, 'ORR'):
      retstr = 'I wish to cancel my agreement to your set of proposals.'
    elif helpers.daidecontains(arrangement, 'PCE'):
      retstr = 'I wish to cancel my agreement to your peace proposal.'
    elif helpers.daidecontains(arrangement, 'ALY'):
      retstr = 'I wish to cancel my agreement to your alliance proposal.'
    elif helpers.daidecontains(arrangement, 'DRW'):
      retstr = 'I wish to cancel my agreement to your draw proposal.'
    elif helpers.daidecontains(arrangement, 'SLO'):
      retstr = 'I wish to cancel my agreement to your solo proposal.'
    elif helpers.daidecontains(arrangement, 'XDO'):
      retstr = 'I wish to cancel my agreement to your proposal about the move: '
      if arrangement[1][0] == 'XDO':
        subarrangement = arrangement[1][1]
        retstr += self.bustAMove(subarrangement, frompower, topowers)
      elif arrangement[1][0] in ['NOT', 'NAR']:
        subarrangement = arrangement[1][1][1]
        retstr += self.bustAMove(subarrangement, frompower, topowers)
    elif helpers.daidecontains(arrangement, 'DMZ'):
      retstr = 'I wish to cancel my agreement to your proposal regarding the Demilitarized Zone in '
      if arrangement[1][0] == 'DMZ':
        subarrangement = arrangement[1]
        retstr += helpers.listOfProvinces(subarrangement[2]) + '.'
      elif arrangement[1][0] in ['NOT', 'NAR']:
        subarrangement = arrangement[1][1]
        retstr += helpers.listOfProvinces(subarrangement[2]) + '.'

    return retstr

  def englishCancelProposal(self, frompower, topowers): # type (str, []) -> str
    """
    Creates an English cancellation of a proposal in the context of a sender, recipients and desired tone.

    :param frompower: the trigram of the sending power
    :type frompower: str
    :param topowers: the trigrams of the receiving powers
    :type topowers: []

    :return: the English cancellation of the proposal
    :rtype: str
    """

    retstr = 'Ahem.'

    arrangement = self.details[1][1]
    if arrangement[0] in ['PCE', 'ALY', 'DMZ']:
      retstr = 'I wish to cancel my proposal regarding ' + self.longTerm(arrangement, frompower, topowers) + '.'
    elif arrangement[0] in ['DRW', 'SLO']:
      retstr = 'I wish to cancel my proposal regarding ' + self.endGame(arrangement, frompower, topowers) + '.'
    elif arrangement[0] == 'XDO':
      retstr = 'I wish to cancel my proposed move: ' + self.bustAMove(arrangement[1], frompower, topowers)
    elif arrangement[0] == 'NOT':
      subarrangement = arrangement[1]
      if subarrangement[0] in ['PCE', 'ALY', 'DMZ']:
        retstr = 'I wish to cancel my proposal against ' + self.longTerm(subarrangement, frompower, topowers) + '.'
      elif subarrangement[0] in ['DRW', 'SLO']:
        retstr = 'I wish to cancel my proposal against ' + self.endGame(subarrangement, frompower, topowers) + '.'
      elif subarrangement[0] == 'XDO':
        retstr = 'I wish to cancel my opposition to the move: ' + self.bustAMove(subarrangement[1], frompower, topowers)
    elif arrangement[0] == 'NAR':
      subarrangement = arrangement[1]
      if subarrangement[0] in ['PCE', 'ALY', 'DMZ']:
        retstr = 'I wish to cancel my proposal regarding ' + self.longTerm(subarrangement, frompower, topowers) + '.'
      elif subarrangement[0] in ['DRW', 'SLO']:
        retstr = 'I wish to cancel my proposal regarding ' + self.endGame(subarrangement, frompower, topowers) + '.'
      elif subarrangement[0] == 'XDO':
        retstr = 'I wish to cancel my ambivalence about the move: ' + self.bustAMove(subarrangement[1], frompower, topowers)
    elif arrangement[0] == 'ORR':
      retstr = 'I wish to cancel my proposal of ' + str(len(arrangement) - 1) + ' choices.'
    elif arrangement[0] == 'AND':
      retstr = 'I wish to cancel my proposal of ' + str(len(arrangement) - 1) + ' propositions.'

    return retstr

  def englishCancel(self, frompower, topowers): # type (str, []) -> str
    """
    Creates an English cancellation in the context of a sender, recipients and desired tone.

    :param frompower: the trigram of the sending power
    :type frompower: str
    :param topowers: the trigrams of the receiving powers
    :type topowers: []

    :return: the English cancellation
    :rtype: str
    """

    retstr = 'Ahem.'
    arrangement = self.details[1]
    if arrangement[0] == 'PRP':
      retstr = self.englishCancelProposal(frompower, topowers)
    elif arrangement[0] == 'YES':
      retstr = self.englishCancelAgreement(frompower, topowers)
    return retstr

  def englishRejectProposal(self, inarr, frompower, topowers): # type ([], str, []) -> str
    """
    Creates an English rejection to a proposal in the context of a sender, recipients and desired tone.

    :param inarr: the proposed arrangement in nest list DAIDE form
    :type inarr: []
    :param frompower: the trigram of the sending power
    :type frompower: str
    :param topowers: the trigrams of the receiving powers
    :type topowers: []

    :return: the English rejection of the proposal
    :rtype: str
    """

    retstr = 'Ahem.'

    arrangement = self.details[1][1]
    if arrangement[0] in ['PCE', 'ALY', 'DMZ']:
      retstr = 'I will not accept ' + self.longTerm(arrangement, frompower, topowers) + '.'
    elif arrangement[0] in ['DRW', 'SLO']:
      retstr = 'I will not accept ' + self.endGame(arrangement, frompower, topowers) + '.'
    elif arrangement[0] == 'XDO':
      retstr = 'I will not execute the move: ' + self.bustAMove(arrangement[1], frompower, topowers)
    elif arrangement[0] == 'NOT':
      subarrangement = arrangement[1]
      if subarrangement[0] in ['PCE', 'ALY', 'DMZ']:
        retstr = 'Despite your request, I will support ' + self.longTerm(subarrangement, frompower, topowers) + '.'
      elif subarrangement[0] in ['DRW', 'SLO']:
        retstr = 'Despite your request, I will support ' + self.endGame(subarrangement, frompower, topowers) + '.'
      elif subarrangement[0] == 'XDO':
        retstr = 'I will go ahead and execute the move regardless: ' + self.bustAMove(subarrangement[1], frompower, topowers)
    elif arrangement[0] == 'NAR':
      subarrangement = arrangement[1]
      if subarrangement[0] in ['PCE', 'ALY', 'DMZ']:
        retstr = 'Despite your request, I might support ' + self.longTerm(subarrangement, frompower, topowers) + '.'
      elif subarrangement[0] in ['DRW', 'SLO']:
        retstr = 'Despite your request, I might support ' + self.endGame(subarrangement, frompower, topowers) + '.'
      elif subarrangement[0] == 'XDO':
        retstr = 'I might go ahead and execute the move regardless: ' + self.bustAMove(subarrangement[1], frompower, topowers)
    elif arrangement[0] == 'ORR':
      retstr = 'I decline to pick any of these proposals: <br><ul>'
      for cSub in range(1, len(arrangement)):
        retstr += '<li>' + self.englishProposal(arrangement[cSub], frompower, topowers) + '</li>'
      retstr += '</ul>'
    elif arrangement[0] == 'AND':
      retstr = 'I reject these proposals: <br><ul>'
      for cSub in range(1, len(arrangement)):
        retstr += '<li>' + self.englishProposal(arrangement[cSub], frompower, topowers) + '</li>'
      retstr += '</ul>'

    return retstr

  def englishReject(self, frompower, topowers): # type (str, []) -> str
    """
    Creates an English rejection response in the context of a sender, recipients and desired tone.

    :param frompower: the trigram of the sending power
    :type frompower: str
    :param topowers: the trigrams of the receiving powers
    :type topowers: []

    :return: the English rejection
    :rtype: str
    """

    retstr = 'Ahem.'
    arrangement = self.details[1]
    if arrangement[0] == 'PRP':
      retstr = self.englishRejectProposal(arrangement, frompower, topowers)
    return retstr

  def englishYesProposal(self, inarr, frompower, topowers): # type ([], str, []) -> str
    """
    Creates an English agreement to a proposal in the context of a sender, recipients and desired tone.

    :param inarr: the proposed arrangement in nest list DAIDE form
    :type inarr: []
    :param frompower: the trigram of the sending power
    :type frompower: str
    :param topowers: the trigrams of the receiving powers
    :type topowers: []

    :return: the English agreement to the proposal
    :rtype: str
    """

    retstr = 'Ahem.'

    arrangement = inarr[1]
    if arrangement[0] in ['PCE', 'ALY', 'DMZ']:
      retstr = 'Yes, I will agree to ' + self.longTerm(arrangement, frompower, topowers) + '.'
    elif arrangement[0] in ['DRW', 'SLO']:
      retstr = 'Yes, I will agree to ' + self.endGame(arrangement, frompower, topowers) + '.'
    elif arrangement[0] == 'XDO':
      retstr = 'I agree to do my part in executing the move: ' + self.bustAMove(arrangement[1], frompower, topowers)
    elif arrangement[0] == 'NOT':
      subarrangement = arrangement[1]
      if subarrangement[0] in ['PCE', 'ALY', 'DMZ']:
        retstr = 'I agree to oppose ' + self.longTerm(subarrangement, frompower, topowers) + '.'
      elif subarrangement[0] in ['DRW', 'SLO']:
        retstr = 'I agree to oppose ' + self.endGame(subarrangement, frompower, topowers) + '.'
      elif subarrangement[0] == 'XDO':
        retstr = 'I agree to do my part in not executing the move: ' + self.bustAMove(subarrangement[1], frompower, topowers)
    elif arrangement[0] == 'NAR':
      subarrangement = arrangement[1]
      if subarrangement[0] in ['PCE', 'ALY', 'DMZ']:
        retstr = 'I agree to be mysterious about ' + self.longTerm(subarrangement, frompower, topowers) + '.'
      elif subarrangement[0] in ['DRW', 'SLO']:
        retstr = 'I agree to be mysterious about ' + self.endGame(subarrangement, frompower, topowers) + '.'
      elif subarrangement[0] == 'XDO':
        retstr = 'I agree to be ambivalent about the move: ' + self.bustAMove(subarrangement[1], frompower, topowers)
    elif arrangement[0] == 'AND':
      retstr = 'I agree to all these proposals: <br><ul>'
      for cSub in range(1, len(arrangement)):
        retstr += '<li>' + self.englishProposal(arrangement[cSub], frompower, topowers) + '</li>'
      retstr += '</ul>'

    return retstr

  def englishYes(self, frompower, topowers): # type (str, []) -> str
    """
    Creates an English agreement response in the context of a sender, recipients and desired tone.

    :param frompower: the trigram of the sending power
    :type frompower: str
    :param topowers: the trigrams of the receiving powers
    :type topowers: []

    :return: the English agreement
    :rtype: str
    """

    retstr = 'Ahem.'
    arrangement = self.details[1]
    if arrangement[0] == 'PRP':
      retstr = self.englishYesProposal(arrangement, frompower, topowers)
    return retstr

  def englishArrangement(self, inarr, frompower, topowers): # type ([], str, []) -> str
    """
    Creates an atomic English arrangement in the context of a sender and recipients.

    :param inarr: the proposed arrangement in nest list DAIDE form
    :type inarr: []
    :param frompower: the trigram of the sending power
    :type frompower: str
    :param topowers: the trigrams of the receiving powers
    :type topowers: []

    :return: the English arrangement
    :rtype: str
    """

    retstr = 'Ahem.'

    arrangement = inarr
    if arrangement[0] in ['PCE', 'ALY', 'DMZ']:
      retstr = self.longTerm(arrangement, frompower, topowers) + '.'
    elif arrangement[0] in ['SLO', 'DRW']:
      retstr = self.endGame(arrangement, frompower, topowers) + '.'
    elif arrangement[0] == 'XDO':
      retstr = self.bustAMove(arrangement[1], frompower, topowers)
    elif arrangement[0] == 'NOT' and len(arrangement) > 1:
      subarrangement = arrangement[1]
      if subarrangement[0] in ['PCE', 'ALY', 'DMZ']:
        retstr = 'That there not be ' + self.longTerm(subarrangement, frompower, topowers) + '.'
      elif subarrangement[0] in ['SLO', 'DRW']:
        retstr = 'I do not want ' + self.endGame(subarrangement, frompower, topowers) + '.'
      elif subarrangement[0] == 'XDO':
        retstr = 'I do not support the following move: ' + self.bustAMove(subarrangement[1], frompower, topowers)
    elif arrangement[0] == 'NAR' and len(arrangement) > 1:
      subarrangement = arrangement[1]
      if subarrangement[0] in ['PCE', 'ALY', 'DMZ']:
        retstr = 'I am not ready for ' + self.longTerm(subarrangement, frompower, topowers) + '.'
      elif subarrangement[0] in ['SLO', 'DRW']:
        retstr = 'I am not ready for ' + self.endGame(subarrangement, frompower, topowers) + '.'
      elif subarrangement[0] == 'XDO':
        retstr = 'I am ambivalent about the following move: ' + self.bustAMove(subarrangement[1], frompower, topowers)

    return retstr

  def englishProposal(self, inarr, frompower, topowers): # type ([], str, []) -> str
    """
    Creates an English proposal in the context of a sender, recipients and desired tone.

    :param inarr: the proposed arrangement in nest list DAIDE form
    :type inarr: []
    :param frompower: the trigram of the sending power
    :type frompower: str
    :param topowers: the trigrams of the receiving powers
    :type topowers: []

    :return: the English proposal
    :rtype: str
    """

    retstr = 'Ahem.'

    arrangement = inarr[1]
    if arrangement[0] in ['PCE', 'ALY', 'DMZ']:
      retstr = 'I propose ' + self.longTerm(arrangement, frompower, topowers) + '.'
    elif arrangement[0] in ['SLO', 'DRW']:
      retstr = 'I propose ' + self.endGame(arrangement, frompower, topowers) + '.'
    elif arrangement[0] == 'XDO':
      retstr = 'I propose the following move: ' + self.bustAMove(arrangement[1], frompower, topowers)
    elif arrangement[0] == 'NOT' and len(arrangement) > 1:
      subarrangement = arrangement[1]
      if subarrangement[0] in ['PCE', 'ALY', 'DMZ']:
        retstr = 'I propose that there not be ' + self.longTerm(subarrangement, frompower, topowers) + '.'
      elif subarrangement[0] in ['SLO', 'DRW']:
        retstr = 'I do not want ' + self.endGame(subarrangement, frompower, topowers) + '.'
      elif subarrangement[0] == 'XDO':
        retstr = 'I do not support the following move: ' + self.bustAMove(subarrangement[1], frompower, topowers)
    elif arrangement[0] == 'NAR' and len(arrangement) > 1:
      subarrangement = arrangement[1]
      if subarrangement[0] in ['PCE', 'ALY', 'DMZ']:
        retstr = 'I am not ready for ' + self.longTerm(subarrangement, frompower, topowers) + '.'
      elif subarrangement[0] in ['SLO', 'DRW']:
        retstr = 'I am not ready for ' + self.endGame(subarrangement, frompower, topowers) + '.'
      elif subarrangement[0] == 'XDO':
        retstr = 'I am ambivalent about the following move: ' + self.bustAMove(subarrangement[1], frompower, topowers)
    elif arrangement[0] == 'ORR':
      retstr = 'I propose you choose one of the following options: <br><ul>'
      for cSub in range(1, len(arrangement)):
        retstr += '<li>' + self.englishArrangement(arrangement[cSub], frompower, topowers) + '</li>'
      retstr += '</ul>'
    elif arrangement[0] == 'AND':
      retstr = 'I propose the following set of actions: <br><ul>'
      for cSub in range(1, len(arrangement)):
        retstr += '<li>' + self.englishArrangement(arrangement[cSub], frompower, topowers) + '</li>'
      retstr += '</ul>'
    elif arrangement[0] == 'IFF' and len(arrangement) == 3:
      retstr = 'I propose the following quid pro quo: If ' + self.englishArrangement(arrangement[1], frompower, topowers) + ', then ' + self.englishArrangement(arrangement[2], frompower, topowers)
      retstr = retstr.replace('.,', ',')

    return retstr

  def englishFact(self, situation, frompower, topowers): # type ([], str, []) -> str
    """
    Creates an English fact in the context of a sender, recipients and desired tone.

    :param situation: the fact in nest list DAIDE form
    :type situation: []
    :param frompower: the trigram of the sending power
    :type frompower: str
    :param topowers: the trigrams of the receiving powers
    :type topowers: []

    :return: the English fact
    :rtype: str
    """

    retstr = 'Ahem.'

    arrangement = situation[1]
    if arrangement[0] in ['PCE', 'ALY', 'DMZ']:
      retstr = 'It is a fact that there is a ' + self.longTerm(arrangement, frompower, topowers) + '.'
    elif arrangement[0] in ['SLO', 'DRW']:
      retstr = 'It is likely that there is ' + self.endGame(arrangement, frompower, topowers) + '.'
    elif arrangement[0] == 'XDO':
      retstr = 'The following move will happen: ' + self.bustAMove(arrangement, frompower, topowers) + '.'
    elif arrangement[0] == 'NOT':
      retstr = self.negate(arrangement, frompower, topowers)
    elif arrangement[0] == 'NAR':
      retstr = self.noidea(arrangement, frompower, topowers)
    elif arrangement[0] == 'ORR':
      retstr = 'One of the following is a fact: <br><ul>'
      for cSub in range(1, len(arrangement)):
        retstr += '<li>' + self.englishArrangement(arrangement[cSub], frompower, topowers) + '</li>'
      retstr += '</ul>'
    elif arrangement[0] == 'AND':
      retstr = 'The following are facts: <br><ul>'
      for cSub in range(1, len(arrangement)):
        retstr += '<li>' + self.englishArrangement(arrangement[cSub], frompower, topowers) + '</li>'
      retstr += '</ul>'

    return retstr

  def formenglish(self, frompower, topowers, tones): # type (str, [], []) -> str
    """
    Creates an English expression in the context of a sender, recipients and desired tone.

    :param frompower: the trigram of the sending power
    :type frompower: str
    :param topowers: the trigrams of the receiving powers
    :type topowers: []
    :param tones: the tones to use when forming English
    :type tones: []

    :return: the English expression
    :rtype: str
    """

    retstr = 'Ahem.'
    if self.details[0] == 'PRP':
      retstr = self.englishProposal(self.details, frompower, topowers)
    elif self.details[0] == 'FCT':
      retstr = self.englishFact(self.details, frompower, topowers)
    elif self.details[0] == 'YES':
      retstr = self.englishYes(frompower, topowers)
    elif self.details[0] == 'REJ':
      retstr = self.englishReject(frompower, topowers)
    elif self.details[0] == 'BWX':
      retstr = ''
    elif self.details[0] == 'HUH':
      retstr = self.englishConfuse(frompower, topowers)
    elif self.details[0] == 'CCL':
      retstr = self.englishCancel(frompower, topowers)
    if retstr != 'Ahem.' and retstr != '':
      retstr = helpers.tonetize(self.daide, retstr, frompower, topowers, tones)
      
    return retstr

def daide2gloss(daide, tones=None): # type: (str, []) -> str
  """
  Create a new utterance from DAIDE, return an English gloss

  :param daide: the press utterance in DAIDE syntax
  :type daide: str
  :param tones: the tones to use when forming English
  :type tones: []
  """

  if daide is None or len(daide.strip()) < 3:
    return 'Ahem.'
  utterance = PressUtterance(daide, tones)
  utterance.formenglish()
  return utterance.english

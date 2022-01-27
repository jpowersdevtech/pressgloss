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
    if helpers.daidecontains(arrangement, 'PCE'):
      retstr = 'I don\'t understand your peace proposal.'
    if helpers.daidecontains(arrangement, 'ALY'):
      retstr = 'I don\'t understand your alliance proposal.'
    if helpers.daidecontains(arrangement, 'DRW'):
      retstr = 'I don\'t understand your draw proposal.'
    if helpers.daidecontains(arrangement, 'SLO'):
      retstr = 'I don\'t understand your solo proposal.'
    if helpers.daidecontains(arrangement, 'XDO'):
      retstr = 'I don\'t understand your move proposal.'
    if helpers.daidecontains(arrangement, 'DMZ'):
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
    if helpers.daidecontains(arrangement, 'PCE'):
      retstr = 'I wish to cancel my agreement to your peace proposal.'
    if helpers.daidecontains(arrangement, 'ALY'):
      retstr = 'I wish to cancel my agreement to your alliance proposal.'
    if helpers.daidecontains(arrangement, 'DRW'):
      retstr = 'I wish to cancel my agreement to your draw proposal.'
    if helpers.daidecontains(arrangement, 'SLO'):
      retstr = 'I wish to cancel my agreement to your solo proposal.'
    if helpers.daidecontains(arrangement, 'XDO'):
      retstr = 'I wish to cancel my agreement to your proposal about the move: '
      if arrangement[1][0] == 'XDO':
        subarrangement = arrangement[1][1]
        retstr += self.bustAMove(subarrangement, frompower, topowers)
      elif arrangement[1][0] in ['NOT', 'NAR']:
        subarrangement = arrangement[1][1][1]
        retstr += self.bustAMove(subarrangement, frompower, topowers)
    if helpers.daidecontains(arrangement, 'DMZ'):
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
    if arrangement[0] == 'PCE':
      if frompower in arrangement[1]:
        retstr = 'I wish to cancel the request that we sign a peace deal.'
      else:
        retstr = 'I wish to cancel the request that you sign a peace deal.'
    elif arrangement[0] == 'ALY':
      retstr = 'I wish to cancel the proposed alliance against ' + helpers.listOfPowers(arrangement[3], frompower, topowers) + '.'
    elif arrangement[0] == 'DRW':
      retstr = 'I wish to cancel the proposed draw.'
    elif arrangement[0] == 'SLO':
      retstr = 'I wish to cancel my support for your solo win.'
    elif arrangement[0] == 'XDO':
      retstr = 'I wish to cancel my proposed move: ' + self.bustAMove(arrangement[1], frompower, topowers)
    elif arrangement[0] == 'DMZ':
      retstr = 'I wish to cancel my proposed Demilitarized Zone in ' + helpers.listOfProvinces(arrangement[2]) + '.'
    elif arrangement[0] == 'NOT':
      subarrangement = arrangement[1]
      if subarrangement[0] == 'PCE':
        if frompower in subarrangement[1]:
          retstr = 'I wish to cancel my opposition to our peace deal.'
        else:
          retstr = 'I wish to cancel my opposition to your peace deal.'
      elif subarrangement[0] == 'ALY':
        retstr = 'I wish to cancel my opposition to the proposed alliance against ' + helpers.listOfPowers(subarrangement[3], frompower, topowers) + '.'
      elif subarrangement[0] == 'DRW':
        retstr = 'I wish to cancel my opposition to a draw.'
      elif subarrangement[0] == 'SLO':
        retstr = 'I wish to cancel my opposition to your solo win.'
      elif subarrangement[0] == 'XDO':
        retstr = 'I wish to cancel my opposition to the move: ' + self.bustAMove(subarrangement[1], frompower, topowers)
      elif subarrangement[0] == 'DMZ':
        retstr = 'I wish to cancel my opposition to the Demilitarized Zone in ' + helpers.listOfProvinces(subarrangement[2]) + '.'
    elif arrangement[0] == 'NAR':
      subarrangement = arrangement[1]
      if subarrangement[0] == 'PCE':
        if frompower in subarrangement[1]:
          retstr = 'I wish to cancel my opposition to our peace deal.'
        else:
          retstr = 'I wish to cancel my opposition to your peace deal.'
      elif subarrangement[0] == 'ALY':
        retstr = 'I wish to cancel my opposition to the proposed alliance against ' + helpers.listOfPowers(subarrangement[3], frompower, topowers) + '.'
      elif subarrangement[0] == 'DRW':
        retstr = 'I wish to cancel my opposition to a draw.'
      elif subarrangement[0] == 'SLO':
        retstr = 'I wish to cancel my opposition to your solo win.'
      elif subarrangement[0] == 'XDO':
        retstr = 'I wish to cancel my ambivalence about the move: ' + self.bustAMove(subarrangement[1], frompower, topowers)
      elif subarrangement[0] == 'DMZ':
        retstr = 'I wish to cancel my ambivalence about the Demilitarized Zone in ' + helpers.listOfProvinces(subarrangement[2]) + '.'

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

  def englishRejectProposal(self, frompower, topowers): # type (str, []) -> str
    """
    Creates an English rejection to a proposal in the context of a sender, recipients and desired tone.

    :param frompower: the trigram of the sending power
    :type frompower: str
    :param topowers: the trigrams of the receiving powers
    :type topowers: []

    :return: the English rejection of the proposal
    :rtype: str
    """

    retstr = 'Ahem.'

    arrangement = self.details[1][1]
    if arrangement[0] == 'PCE':
      possiblepartners = [curpower for curpower in arrangement[1] if curpower != frompower]
      retstr = 'I will not sign a peace deal with ' + helpers.listOfPowers(possiblepartners, None, None) + '.'
    elif arrangement[0] == 'ALY':
      possibleallies = [curpower for curpower in arrangement[1] if curpower != frompower]
      retstr = 'I will not ally with ' + helpers.listOfPowers(possibleallies, frompower, None) + ' against ' + helpers.listOfPowers(arrangement[3], frompower, topowers) + '.'
    elif arrangement[0] == 'DRW':
      if len(arrangement) == 1:
        retstr = 'I reject a draw.'
      else:
        retstr = 'I reject a draw between us.'
    elif arrangement[0] == 'SLO':
      if frompower in arrangement[1]:
        retstr = 'I am not pursuing a solo win at this time.'
      elif len(topowers) == 1 and topowers[0] in arrangement[1]:
        retstr = 'I will block your attempt at a solo win.'
      else:
        retstr = 'I will block ' + helpers.listOfPowers(arrangement[1], frompower, None) + '\'s solo win bid.'
    elif arrangement[0] == 'XDO':
      retstr = 'I will not execute the move: ' + self.bustAMove(arrangement[1], frompower, topowers)
    elif arrangement[0] == 'DMZ':
      retstr = 'I will not respect the Demilitarized Zone in ' + helpers.listOfProvinces(arrangement[2]) + '.'
    elif arrangement[0] == 'NOT':
      subarrangement = arrangement[1]
      if subarrangement[0] == 'PCE':
        possiblepartners = [curpower for curpower in subarrangement[1] if curpower != frompower]
        if len(possiblepartners) < len(topowers):
          retstr = 'I won\'t promise not to make peace with ' + helpers.listOfPowers(possiblepartners, None, None) + '.'
        else:
          retstr = 'I think a peace treaty would be a good idea between the ' + helpers.size2numstr(subarrangement[1]) + ' of us.'
      elif subarrangement[0] == 'ALY':
        retstr = 'I think an alliance against ' + helpers.listOfPowers(subarrangement[3], frompower, topowers) + ' is a good idea.'
      elif subarrangement[0] == 'DRW':
        retstr = 'I will still be seeking a draw condition.'
      elif subarrangement[0] == 'SLO':
        if frompower in subarrangement[1]:
          retstr = 'I will pursue a solo win if I want to.'
        elif len(topowers) == 1 and topowers[0] in subarrangement[1]:
          retstr = 'I think you are going for a solo win despite what you say.'
        else:
          retstr = 'I think ' + helpers.listOfPowers(subarrangement[1], frompower, None) + ' is going for a solo win despite what you say.'
      elif subarrangement[0] == 'XDO':
        retstr = 'I will go ahead and execute the move regardless: ' + self.bustAMove(subarrangement[1], frompower, topowers)
      elif subarrangement[0] == 'DMZ':
        retstr = 'Regardless, I will still respect the Demilitarized Zone in ' + helpers.listOfProvinces(subarrangement[2]) + '.'
    elif arrangement[0] == 'NAR':
      subarrangement = arrangement[1]
      if subarrangement[0] == 'PCE':
        possiblepartners = [curpower for curpower in subarrangement[1] if curpower != frompower]
        retstr = 'I can\'t promise I won\'t pursue peace between me and ' + helpers.listOfPowers(possiblepartners, None, None) + '.'
      elif subarrangement[0] == 'ALY':
        retstr = 'I can\'t promise not to ally against ' + helpers.listOfPowers(subarrangement[3], frompower, topowers) + '.'
      elif subarrangement[0] == 'DRW':
        retstr = 'I think a draw is very possible now.'
      elif subarrangement[0] == 'SLO':
        if frompower in subarrangement[1]:
          retstr = 'A solo win is still on the table if I want to.'
        elif len(topowers) == 1 and topowers[0] in subarrangement[1]:
          retstr = 'I don\'t know what your intentions for a solo win are.'
        else:
          retstr = 'I don\'t know what ' + helpers.listOfPowers(subarrangement[1], frompower, None) + '\'s intentions for a solo win are.'
      elif subarrangement[0] == 'XDO':
        retstr = 'I am not ambiguous about the move: ' + self.bustAMove(subarrangement[1], frompower, topowers)
      elif subarrangement[0] == 'DMZ':
        retstr = 'I am not ambiguous about the Demilitarized Zone in ' + helpers.listOfProvinces(subarrangement[2]) + '.'

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
      retstr = self.englishRejectProposal(frompower, topowers)
    return retstr

  def englishYesProposal(self, frompower, topowers): # type (str, []) -> str
    """
    Creates an English agreement to a proposal in the context of a sender, recipients and desired tone.

    :param frompower: the trigram of the sending power
    :type frompower: str
    :param topowers: the trigrams of the receiving powers
    :type topowers: []

    :return: the English agreement to the proposal
    :rtype: str
    """

    retstr = 'Ahem.'

    arrangement = self.details[1][1]
    if arrangement[0] == 'PCE':
      retstr = 'Yes, I will sign a peace treaty between ' + helpers.listOfPowers(arrangement[1], frompower, None) + '.'
    elif arrangement[0] == 'ALY':
      retstr = 'Yes, I will sign an alliance between ' + helpers.listOfPowers(arrangement[1], frompower, None) + ' against ' + helpers.listOfPowers(arrangement[3], frompower, topowers) + '.'
    elif arrangement[0] == 'DRW':
      if len(arrangement) == 1:
        retstr = 'Yes, I agree to a draw.'
      else:
        retstr = 'Yes, I agree to a draw between our ' + helpers.size2numstr(arrangement[1]) + ' countries.'
    elif arrangement[0] == 'SLO':
      if frompower in arrangement[1]:
        retstr = 'I will use your support to pursue a solo win.'
      elif len(topowers) == 1 and topowers[0] in arrangement[1]:
        retstr = 'I will support your solo win bid.'
      else:
        retstr = 'I will support ' + helpers.listOfPowers(arrangement[1], frompower, None) + '\'s solo win bid.'
    elif arrangement[0] == 'XDO':
      retstr = 'I agree to do my part in executing the move: ' + self.bustAMove(arrangement[1], frompower, topowers)
    elif arrangement[0] == 'DMZ':
      retstr = 'I agree to do my part in respecting the Demilitarized Zone in ' + helpers.listOfProvinces(arrangement[2]) + '.'
    elif arrangement[0] == 'NOT':
      subarrangement = arrangement[1]
      if subarrangement[0] == 'PCE':
        possiblepartners = [curpower for curpower in subarrangement[1] if curpower != frompower]
        retstr = 'I will end any peace treaties between me and ' + helpers.listOfPowers(possiblepartners, None, None) + '.'
      elif subarrangement[0] == 'ALY':
        possibleallies = [curpower for curpower in subarrangement[1] if curpower != frompower]
        retstr = 'I will not ally with ' + helpers.listOfPowers(possibleallies, None, None) + ' against ' + helpers.listOfPowers(subarrangement[3], frompower, topowers) + '.'
      elif subarrangement[0] == 'DRW':
        retstr = 'You\'re right, it\'s not the time for a draw.'
      elif subarrangement[0] == 'SLO':
        if frompower in subarrangement[1]:
          retstr = 'I will not pursue a solo win.'
        elif len(topowers) == 1 and topowers[0] in subarrangement[1]:
          retstr = 'I agree you shouldn\'t pursue a solo win bid.'
        else:
          retstr = 'I agree that ' + helpers.listOfPowers(subarrangement[1], frompower, None) + ' should not pursue a solo win.'
      elif subarrangement[0] == 'XDO':
        retstr = 'I agree to do my part in not executing the move: ' + self.bustAMove(subarrangement[1], frompower, topowers)
      elif subarrangement[0] == 'DMZ':
        retstr = 'I agree to do my part in ignoring the Demilitarized Zone in ' + helpers.listOfProvinces(subarrangement[2]) + '.'
    elif arrangement[0] == 'NAR':
      subarrangement = arrangement[1]
      if subarrangement[0] == 'PCE':
        possiblepartners = [curpower for curpower in subarrangement[1] if curpower != frompower]
        retstr = 'I agree, no peace with ' + helpers.listOfPowers(possiblepartners, None, None) + '.'
      elif subarrangement[0] == 'ALY':
        retstr = 'I agree, no alliance against ' + helpers.listOfPowers(subarrangement[3], frompower, topowers) + '.'
      elif subarrangement[0] == 'DRW':
        retstr = 'I agree, a draw is not right at this time.'
      elif subarrangement[0] == 'SLO':
        if frompower in subarrangement[1]:
          retstr = 'If I will pursue a solo win, I won\'t rely on your support.'
        elif len(topowers) == 1 and topowers[0] in subarrangement[1]:
          retstr = 'I agree that you can\'t rely on me to support your solo win bid.'
        else:
          retstr = 'I agree that ' + helpers.listOfPowers(subarrangement[1], frompower, None) + ' should not rely on me to support a solo win.'
      elif subarrangement[0] == 'XDO':
        retstr = 'I agree that I may or may not participate in the move: ' + self.bustAMove(subarrangement[1], frompower, topowers)
      elif subarrangement[0] == 'DMZ':
        retstr = 'I agree that I may or may not respect the Demilitarized Zone in ' + helpers.listOfProvinces(subarrangement[2]) + '.'

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
      retstr = self.englishYesProposal(frompower, topowers)
    return retstr

  def englishProposal(self, frompower, topowers): # type (str, []) -> str
    """
    Creates an English proposal in the context of a sender, recipients and desired tone.

    :param frompower: the trigram of the sending power
    :type frompower: str
    :param topowers: the trigrams of the receiving powers
    :type topowers: []

    :return: the English proposal
    :rtype: str
    """

    retstr = 'Ahem.'

    if len(self.details) < 2:
      return retstr

    arrangement = self.details[1]
    if arrangement[0] == 'PCE':
      maskedparticipants = [curpower for curpower in arrangement[1] if curpower != frompower and curpower not in topowers]
      if frompower in arrangement[1]:
        retstr = 'Let us sign a peace treaty together.'
      elif len(maskedparticipants) > 0:
        retstr = 'Would ' + helpers.listOfPowers(arrangement[1], frompower, topowers) + ' agree to end any conflict between you and sign a peace treaty?'
      else:
        retstr = 'Would you ' + helpers.size2numstr(arrangement[1]) + ' agree to end any conflict between you and sign a peace treaty?'
    elif arrangement[0] == 'ALY':
      maskedallies = [curpower for curpower in arrangement[1] if curpower != frompower and curpower not in topowers]
      if len(maskedallies) > 0:
        if frompower in arrangement[1]:
          retstr = 'Let us declare an alliance against ' + helpers.listOfPowers(arrangement[3], frompower, topowers) + ' with ' + helpers.listOfPowers(maskedallies, None, None) + '.'
        elif len(topowers) == 1:
          retstr = 'Would you declare an alliance against ' + helpers.listOfPowers(arrangement[3], frompower, topowers) + ' with ' + helpers.listOfPowers(maskedallies, None, None) + '?'
        else:
          retstr = 'Would you ' + helpers.size2numstr(topowers) + ' declare an alliance against ' + helpers.listOfPowers(arrangement[3], frompower, topowers) + ' with ' + helpers.listOfPowers(maskedallies, None, None) + '?'
      elif frompower in arrangement[1]:
        retstr = 'Let us declare an alliance against ' + helpers.listOfPowers(arrangement[3], frompower, topowers) + '.'
      else:
        retstr = 'Would you ' + helpers.size2numstr(arrangement[1]) + ' ally against ' + helpers.listOfPowers(arrangement[3], frompower, topowers) + '?'
    elif arrangement[0] == 'DRW':
      if len(arrangement) == 1:
        retstr = 'Are you amenable to a draw?'
      else:
        retstr = 'Are you amenable to a draw between ' + helpers.listOfPowers(arrangement[1], None, None) + '?'
    elif arrangement[0] == 'SLO':
      if frompower in arrangement[1]:
        retstr = 'You should let me go for a solo win.'
      elif len(topowers) == 1 and topowers[0] in arrangement[1]:
        retstr = 'You should go for a solo win, I won\'t get in your way.'
      else:
        retstr = 'We should let ' + helpers.listOfPowers(arrangement[1], frompower, topowers) + ' go for a solo victory.'
    elif arrangement[0] == 'XDO':
      retstr = 'I propose the following move: ' + self.bustAMove(arrangement[1], frompower, topowers)
    elif arrangement[0] == 'DMZ':
      retstr = 'I propose that ' + helpers.listOfPowers(arrangement[1], frompower, topowers) + ' agree to create a Demilitarized Zone in ' + helpers.listOfProvinces(arrangement[2]) + '.'
      retstr = retstr.replace(' me ', ' I ')
    elif arrangement[0] == 'NOT' and len(arrangement) > 1:
      subarrangement = arrangement[1]
      if subarrangement[0] == 'PCE':
        if frompower in subarrangement[1]:
          retstr = 'I propose that we end any promises of peace between us.'
        else:
          retstr = 'I propose that you end your treaty together.'
      elif subarrangement[0] == 'ALY':
        if frompower in subarrangement[1]:
          retstr = 'We should not ally against ' + helpers.listOfPowers(subarrangement[3], frompower, topowers) + '.'
        elif frompower in subarrangement[3]:
          retstr = 'Please do not form an alliance against ' + helpers.listOfPowers(subarrangement[3], frompower, topowers) + '.'
        else:
          retstr = 'Don\'t ally together against ' + helpers.listOfPowers(subarrangement[3], frompower, topowers) + '.'
      elif subarrangement[0] == 'DRW':
        if len(subarrangement) == 1:
          if len(topowers) == 1:
            retstr = 'I wouldn\'t agree to a draw with ' + helpers.listOfPowers(subarrangement[1], None, topowers) + '.'
          else:
            retstr = 'I wouldn\'t agree to a draw with you ' + helpers.size2numstr(topowers) + '.'
        else:
          retstr = 'I wouldn\'t agree to a draw between ' + helpers.listOfPowers(subarrangement[1], None, None) + '.'
      elif subarrangement[0] == 'SLO':
        if frompower in subarrangement[1]:
          retstr = 'You should not let me go for a solo win.'
        elif len(topowers) == 1 and topowers[0] in subarrangement[1]:
          retstr = 'I wouldn\'t try for a solo win if I were you.'
        else:
          retstr = 'We should not let ' + helpers.listOfPowers(subarrangement[1], frompower, topowers) + ' go for a solo victory.'
      elif subarrangement[0] == 'XDO':
        retstr = 'I do not support the following move: ' + self.bustAMove(subarrangement[1], frompower, topowers)
      elif subarrangement[0] == 'DMZ':
        retstr = 'I propose that ' + helpers.listOfPowers(subarrangement[1], frompower, topowers) + ' do not create a Demilitarized Zone in ' + helpers.listOfProvinces(subarrangement[2]) + '.'
        retstr = retstr.replace(' me ', ' I ')
    elif arrangement[0] == 'NAR' and len(arrangement) > 1:
      subarrangement = arrangement[1]
      if subarrangement[0] == 'PCE':
        if frompower in subarrangement[1]:
          retstr = 'I propose we don\'t make peace at this time.'
        else:
          retstr = 'You shouldn\'t sign a peace agreement together.'
      elif subarrangement[0] == 'ALY':
        if frompower in subarrangement[1]:
          retstr = 'I propose we make no alliance against ' + helpers.listOfPowers(subarrangement[3], frompower, topowers) + '.'
        elif frompower in subarrangement[3]:
          retstr = 'Please do not form an alliance against ' + helpers.listOfPowers(subarrangement[3], frompower, topowers) + '.'
        else:
          retstr = 'I propose you don\'t ally together against ' + helpers.listOfPowers(subarrangement[3], frompower, topowers) + '.'
      elif subarrangement[0] == 'DRW':
        retstr = 'There is no draw condition between us.'
      elif subarrangement[0] == 'SLO':
        if frompower in subarrangement[1]:
          retstr = 'You should not support my solo win attempt.'
        elif len(topowers) == 1 and topowers[0] in subarrangement[1]:
          retstr = 'I won\'t pledge support of your solo win.'
        else:
          retstr = 'We should not support ' + helpers.listOfPowers(subarrangement[1], frompower, topowers) + '\'s solo victory.'
      elif subarrangement[0] == 'XDO':
        retstr = 'I am ambivalent about the following move: ' + self.bustAMove(subarrangement[1], frompower, topowers)
      elif subarrangement[0] == 'DMZ':
        retstr = 'I am ambivalent about ' + helpers.listOfPowers(subarrangement[1], frompower, topowers) + ' creating a Demilitarized Zone in ' + helpers.listOfProvinces(subarrangement[2]) + '.'
        retstr = retstr.replace(' me ', ' I ')

    return retstr

  def englishFact(self, frompower, topowers): # type (str, []) -> str
    """
    Creates an English fact in the context of a sender, recipients and desired tone.

    :param frompower: the trigram of the sending power
    :type frompower: str
    :param topowers: the trigrams of the receiving powers
    :type topowers: []

    :return: the English fact
    :rtype: str
    """

    retstr = 'Ahem.'

    if len(self.details) < 2:
      return retstr

    arrangement = self.details[1]
    if arrangement[0] == 'PCE':
      possibleparticipants = [curpower for curpower in arrangement[1] if curpower != frompower]
      if frompower in arrangement[1]:
        retstr = 'I have a peace deal with ' + helpers.listOfPowers(possibleparticipants, frompower, topowers) + '.'
      else:
        retstr = 'There is a peace deal between ' + helpers.listOfPowers(possibleparticipants, frompower, topowers) + '.'
    elif arrangement[0] == 'ALY':
      possibleallies = [curpower for curpower in arrangement[1] if curpower != frompower]
      if frompower in arrangement[1]:
        retstr = 'I have an alliance with ' + helpers.listOfPowers(possibleallies, frompower, topowers) + ' against ' + helpers.listOfPowers(arrangement[3], frompower, topowers) + '.'
      else:
        retstr = 'There is an alliance between ' + helpers.listOfPowers(possibleallies, frompower, topowers) + ' against ' + helpers.listOfPowers(arrangement[3], frompower, topowers) + '.'
    elif arrangement[0] == 'DRW':
      if len(arrangement) == 1:
        retstr = 'I am in a draw condition.'
      elif frompower in arrangement[1]:
        possibleparticipants = [curpower for curpower in arrangement[1] if curpower != frompower]
        retstr = 'I am in a draw condition with ' + helpers.listOfPowers(possibleparticipants, frompower, topowers) + '.'
      else:
        retstr = 'There is a draw condition between ' + helpers.listOfPowers(arrangement[1], None, None) + '.'
    elif arrangement[0] == 'SLO':
      if frompower in arrangement[1]:
        retstr = 'I am going for a solo win.'
      else:
        retstr = helpers.listOfPowers(arrangement[1], frompower, topowers) + ' is going for a solo win.'
    elif arrangement[0] == 'NOT':
      subarrangement = arrangement[1]
      if subarrangement[0] == 'PCE':
        possibleparticipants = [curpower for curpower in subarrangement[1] if curpower != frompower]
        if frompower in subarrangement[1]:
          retstr = 'I broke my peace deal with ' + helpers.listOfPowers(possibleparticipants, frompower, None) + '.'
        else:
          retstr = 'There is no longer a peace deal between ' + helpers.listOfPowers(possibleparticipants, frompower, topowers) + '.'
      elif subarrangement[0] == 'ALY':
        possibleallies = [curpower for curpower in subarrangement[1] if curpower != frompower]
        if frompower in subarrangement[1]:
          retstr = 'I do not have an alliance with ' + helpers.listOfPowers(possibleallies, frompower, topowers) + ' against ' + helpers.listOfPowers(subarrangement[3], frompower, topowers) + '.'
        else:
          retstr = 'There is no alliance between ' + helpers.listOfPowers(possibleallies, frompower, topowers) + ' against ' + helpers.listOfPowers(subarrangement[3], frompower, topowers) + '.'
      elif subarrangement[0] == 'DRW':
        if len(subarrangement) == 1:
          retstr = 'I am not in a draw condition.'
        else:
          possibleparticipants = [curpower for curpower in subarrangement[1] if curpower != frompower]
          retstr = 'I am not in a draw condition with ' + helpers.listOfPowers(possibleparticipants, frompower, topowers) + '.'
      elif subarrangement[0] == 'SLO':
        if frompower in subarrangement[1]:
          retstr = 'I am not going for a solo win.'
        else:
          retstr = helpers.listOfPowers(subarrangement[1], frompower, topowers) + ' is not going for a solo win.'
    elif arrangement[0] == 'NAR':
      subarrangement = arrangement[1]
      if subarrangement[0] == 'PCE':
        possibleparticipants = [curpower for curpower in subarrangement[1] if curpower != frompower]
        if frompower in subarrangement[1]:
          retstr = 'I have no peace deal with ' + helpers.listOfPowers(possibleparticipants, frompower, None) + '.'
        else:
          retstr = 'There is no peace deal between ' + helpers.listOfPowers(possibleparticipants, frompower, topowers) + '.'
      elif subarrangement[0] == 'ALY':
        possibleallies = [curpower for curpower in subarrangement[1] if curpower != frompower]
        if frompower in subarrangement[1]:
          retstr = 'I do not have an alliance with ' + helpers.listOfPowers(possibleallies, frompower, topowers) + ' against ' + helpers.listOfPowers(subarrangement[3], frompower, topowers) + '.'
        else:
          retstr = 'There is no alliance between ' + helpers.listOfPowers(possibleallies, frompower, topowers) + ' against ' + helpers.listOfPowers(subarrangement[3], frompower, topowers) + '.'
      elif subarrangement[0] == 'DRW':
        if len(subarrangement) == 1:
          retstr = 'A draw is not something I\'ve considered.'
        else:
          possibleparticipants = [curpower for curpower in subarrangement[1] if curpower != frompower]
          retstr = 'I haven\'t considered a draw with ' + helpers.listOfPowers(possibleparticipants, frompower, topowers) + '.'
      elif subarrangement[0] == 'SLO':
        if frompower in subarrangement[1]:
          retstr = 'A solo win is not something I\'ve considered.'
        else:
          retstr = 'I haven\'t considered a solo win by ' + helpers.listOfPowers(subarrangement[1], frompower, topowers) + '.'

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
      retstr = self.englishProposal(frompower, topowers)
    elif self.details[0] == 'FCT':
      retstr = self.englishFact(frompower, topowers)
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

# -*- coding: utf-8 -*-
"""%pressgloss% library"""

# Standard library imports
import logging
import random
import json

# pressgloss imports
from . import helpers

class PressUtterance:
  """ A statement by a Diplomacy Power addressed to other Powers and regarding some in-game topic with a tone """

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

    if daide is None or daide == '':
      self.frompower = random.choice(helpers.powerlist)
      self.topowers = []
      tolist = [curpower for curpower in helpers.powerlist if curpower != self.frompower]
      self.topowers = random.sample(tolist, random.randint(1, 4))
      contentword = random.choice(['PRP', 'FCT', 'YES', 'REJ', 'HUH', 'BWX', 'CCL'])
      self.content = randomFactory(self, None, contentword)
      self.daide = self.formDAIDE()
    else:
      self.daide = daide
      thelists = helpers.daide2lists(daide)
      if len(thelists) == 4 and thelists[0] == 'FRM':
        self.frompower = thelists[1][0]
        self.topowers = thelists[2]
        self.content = messageFactory(self, None, thelists[3])
      else:
        self.frompower = ''
        self.topowers = []
        self.content = None

    self.formenglish()

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

    if self.content is None:
      self.english = 'Ahem.'
    else:
      self.english = self.content.formenglish()

  def formDAIDE(self): # type () -> str
    """
    Create a DAIDE representation of this Utterance

    :return: the DAIDE message
    :rtype: str
    """

    return 'FRM (' + self.frompower + ') (' + ' '.join(self.topowers) + ') (' + self.content.formDAIDE() + ')'

class PressMessage:
  """ The game-related content of an utterance. Top-level DAIDE class that should never be used directly. """

  def __init__(self, utterance, container): # type: (PressUtterance, PressMessage) -> None
    """
    Initialize the message with an utterance

    :param utterance: the press utterance that this message is within the content for
    :type utterance: PressUtterance
    :param container: the press message that contains this one
    :type container: PressMessage
    """

    self.utterance = utterance
    self.container = container
    self.operator = ''
    self.details = None
    self.english = 'Ahem.'

  def __eq__(self, other): # type: (PressMessage) -> bool
    """
    Override default equality with a comparison of DAIDE expressions

    :param other: the other message to compare
    :type other: PressMessage
    :return: if these messages are equal
    :rtype: bool
    """

    return self.utterance.daide.lower() == other.utterance.daide.lower()

  def __ne__(self, other): # type: (PressMessage) -> bool
    """
    Override default inequality with reference to equality

    :param other: the other message to compare
    :type other: PressMessage
    :return: if these messages are not equal
    :rtype: bool
    """

    return not self.__eq__(other)

  def formenglish(self): # type () -> str
    """
    Creates an English expression in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    self.english = helpers.tonetize(self.utterance, self.english)

    return self.english

  def formlistenglish(self): # type: () -> str
    """
    Creates a simple English statement, without any context like proposals, negations, etc.
    Useful for lists of conjunctions or other contexts in which simplicity is valued over flavor.

    :return: the simple English statement
    :rtype: str

    """

    self.simpleenglish = 'A DAIDE expression.'

    return self.simpleenglish

  def formclauseenglish(self): # type: () -> str
    """
    Creates a simple English clause, without any context like proposals, negations, etc.
    Useful for conditional statements or other contexts in which simplicity is valued over flavor.

    :return: the simple English clause
    :rtype: str

    """

    self.simpleenglish = 'A DAIDE clause.'

    return self.simpleenglish

  def formDAIDE(self): # type () -> str
    """
    Create a DAIDE representation of this Message

    :return: the DAIDE message
    :rtype: str
    """

    return self.operator

class PressFact(PressMessage):
  """ The game-related content of a fact. """

  def __init__(self, utterance, container, thelists): # type: (PressUtterance, PressMessage, []) -> None
    """
    Initialize the message with an utterance

    :param utterance: the press utterance that this message is within the content for
    :type utterance: PressUtterance
    :param container: the press message that contains this one
    :type container: PressMessage
    :param thelists: the parsed, nested DAIDE statement
    :type thelists: []
    """

    super().__init__(utterance, container)
    if thelists is None or len(thelists) == 0:
      self.operator = 'FCT'
      contentword = random.choice(['PCE', 'ALY', 'DMZ', 'SLO', 'DRW', 'XDO', 'NOT', 'NAR', 'AND', 'ORR', 'IFF'])
      self.details = randomFactory(utterance, self, contentword)
    elif len(thelists) == 2:
      self.operator = thelists[0]
      self.details = messageFactory(utterance, self, thelists[1])

  def formenglish(self): # type () -> str
    """
    Creates an English expression about the fact in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    if self.details is None:
      return super().formenglish()

    self.english = self.details.formenglish()
    if self.container is None:
      self.english = helpers.tonetize(self.utterance, self.english)

    return self.english

  def formlistenglish(self): # type: () -> str
    """
    Creates a simple English statement, without any context like proposals, negations, etc.
    Useful for lists of conjunctions or other contexts in which simplicity is valued over flavor.

    :return: the simple English statement
    :rtype: str

    """

    self.simpleenglish = self.details.formlistenglish()

    return self.simpleenglish

  def formclauseenglish(self): # type: () -> str
    """
    Creates a simple English clause, without any context like proposals, negations, etc.
    Useful for conditional statements or other contexts in which simplicity is valued over flavor.

    :return: the simple English clause
    :rtype: str

    """

    self.simpleenglish = self.formlistenglish()

    return self.simpleenglish

  def formDAIDE(self): # type () -> str
    """
    Create a DAIDE representation of this Message

    :return: the DAIDE message
    :rtype: str
    """

    return 'FCT (' + self.details.formDAIDE() + ')'

class PressProposal(PressMessage):
  """ The game-related content of a proposal. """

  def __init__(self, utterance, container, thelists): # type: (PressUtterance, PressMessage, []) -> None
    """
    Initialize the message with an utterance

    :param utterance: the press utterance that this message is within the content for
    :type utterance: PressUtterance
    :param container: the press message that contains this one
    :type container: PressMessage
    :param thelists: the parsed, nested DAIDE statement
    :type thelists: []
    """

    super().__init__(utterance, container)
    if thelists is None or len(thelists) == 0:
      self.operator = 'PRP'
      contentword = random.choice(['PCE', 'ALY', 'DMZ', 'SLO', 'DRW', 'XDO', 'NOT', 'NAR', 'AND', 'ORR', 'IFF'])
      self.details = randomFactory(utterance, self, contentword)
    elif len(thelists) == 2:
      self.operator = thelists[0]
      self.details = messageFactory(utterance, self, thelists[1])

  def formenglish(self): # type () -> str
    """
    Creates an English expression about the proposal in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    if self.details is None:
      return super().formenglish()

    self.english = self.details.formenglish()
    if self.container is None:
      self.english = helpers.tonetize(self.utterance, self.english)

    return self.english

  def formlistenglish(self): # type: () -> str
    """
    Creates a simple English statement, without any context like proposals, negations, etc.
    Useful for lists of conjunctions or other contexts in which simplicity is valued over flavor.

    :return: the simple English statement
    :rtype: str

    """

    self.simpleenglish = self.details.formlistenglish()

    return self.simpleenglish

  def formclauseenglish(self): # type: () -> str
    """
    Creates a simple English clause, without any context like proposals, negations, etc.
    Useful for conditional statements or other contexts in which simplicity is valued over flavor.

    :return: the simple English clause
    :rtype: str

    """

    self.simpleenglish = self.formlistenglish()

    return self.simpleenglish

  def formDAIDE(self): # type () -> str
    """
    Create a DAIDE representation of this Message

    :return: the DAIDE message
    :rtype: str
    """

    return 'PRP (' + self.details.formDAIDE() + ')'

class PressAccept(PressMessage):
  """ The game-related content of an acceptance. """

  def __init__(self, utterance, container, thelists): # type: (PressUtterance, PressMessage, []) -> None
    """
    Initialize the message with an utterance

    :param utterance: the press utterance that this message is within the content for
    :type utterance: PressUtterance
    :param container: the press message that contains this one
    :type container: PressMessage
    :param thelists: the parsed, nested DAIDE statement
    :type thelists: []
    """

    super().__init__(utterance, container)
    if thelists is None or len(thelists) == 0:
      self.operator = 'YES'
      self.details = randomFactory(utterance, self, 'PRP')
    elif len(thelists) == 2:
      self.operator = thelists[0]
      self.details = messageFactory(utterance, self, thelists[1])

  def formenglish(self): # type () -> str
    """
    Creates an English expression about the acceptance in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    if self.details is None:
      return super().formenglish()

    self.english = self.details.formenglish()
    if self.container is None:
      self.english = helpers.tonetize(self.utterance, self.english)

    return self.english

  def formlistenglish(self): # type: () -> str
    """
    Creates a simple English statement, without any context like proposals, negations, etc.
    Useful for lists of conjunctions or other contexts in which simplicity is valued over flavor.

    :return: the simple English statement
    :rtype: str

    """

    self.simpleenglish = 'I accept your proposal.'

    return self.simpleenglish

  def formclauseenglish(self): # type: () -> str
    """
    Creates a simple English clause, without any context like proposals, negations, etc.
    Useful for conditional statements or other contexts in which simplicity is valued over flavor.

    :return: the simple English clause
    :rtype: str

    """

    self.simpleenglish = self.formlistenglish()

    return self.simpleenglish

  def formDAIDE(self): # type () -> str
    """
    Create a DAIDE representation of this Message

    :return: the DAIDE message
    :rtype: str
    """

    return 'YES (' + self.details.formDAIDE() + ')'

class PressReject(PressMessage):
  """ The game-related content of a rejection. """

  def __init__(self, utterance, container, thelists): # type: (PressUtterance, PressMessage, []) -> None
    """
    Initialize the message with an utterance

    :param utterance: the press utterance that this message is within the content for
    :type utterance: PressUtterance
    :param container: the press message that contains this one
    :type container: PressMessage
    :param thelists: the parsed, nested DAIDE statement
    :type thelists: []
    """

    super().__init__(utterance, container)
    if thelists is None or len(thelists) == 0:
      self.operator = 'REJ'
      self.details = randomFactory(utterance, self, 'PRP')
    elif len(thelists) == 2:
      self.operator = thelists[0]
      self.details = messageFactory(utterance, self, thelists[1])

  def formenglish(self): # type () -> str
    """
    Creates an English expression about the rejection in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    if self.details is None:
      return super().formenglish()

    self.english = self.details.formenglish()
    if self.container is None:
      self.english = helpers.tonetize(self.utterance, self.english)

    return self.english

  def formlistenglish(self): # type: () -> str
    """
    Creates a simple English statement, without any context like proposals, negations, etc.
    Useful for lists of conjunctions or other contexts in which simplicity is valued over flavor.

    :return: the simple English statement
    :rtype: str

    """

    self.simpleenglish = 'I reject your proposal.'

    return self.simpleenglish

  def formclauseenglish(self): # type: () -> str
    """
    Creates a simple English clause, without any context like proposals, negations, etc.
    Useful for conditional statements or other contexts in which simplicity is valued over flavor.

    :return: the simple English clause
    :rtype: str

    """

    self.simpleenglish = self.formlistenglish()

    return self.simpleenglish

  def formDAIDE(self): # type () -> str
    """
    Create a DAIDE representation of this Message

    :return: the DAIDE message
    :rtype: str
    """

    return 'REJ (' + self.details.formDAIDE() + ')'

class PressCancel(PressMessage):
  """ The game-related content of a cancellation. """

  def __init__(self, utterance, container, thelists): # type: (PressUtterance, PressMessage, []) -> None
    """
    Initialize the message with an utterance

    :param utterance: the press utterance that this message is within the content for
    :type utterance: PressUtterance
    :param container: the press message that contains this one
    :type container: PressMessage
    :param thelists: the parsed, nested DAIDE statement
    :type thelists: []
    """

    super().__init__(utterance, container)
    if thelists is None or len(thelists) == 0:
      self.operator = 'CCL'
      self.details = randomFactory(utterance, self, 'PRP')
    elif len(thelists) == 2:
      self.operator = thelists[0]
      self.details = messageFactory(utterance, self, thelists[1])

  def formenglish(self): # type () -> str
    """
    Creates an English expression about the rejection in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    if self.details is None:
      return super().formenglish()

    self.english = self.details.formenglish()
    if self.container is None:
      self.english = helpers.tonetize(self.utterance, self.english)

    return self.english

  def formlistenglish(self): # type: () -> str
    """
    Creates a simple English statement, without any context like proposals, negations, etc.
    Useful for lists of conjunctions or other contexts in which simplicity is valued over flavor.

    :return: the simple English statement
    :rtype: str

    """

    self.simpleenglish = 'I wish to cancel my last message.'

    return self.simpleenglish

  def formclauseenglish(self): # type: () -> str
    """
    Creates a simple English clause, without any context like proposals, negations, etc.
    Useful for conditional statements or other contexts in which simplicity is valued over flavor.

    :return: the simple English clause
    :rtype: str

    """

    self.simpleenglish = self.formlistenglish()

    return self.simpleenglish

  def formDAIDE(self): # type () -> str
    """
    Create a DAIDE representation of this Message

    :return: the DAIDE message
    :rtype: str
    """

    return 'CCL (' + self.details.formDAIDE() + ')'

class PressHuh(PressMessage):
  """ The game-related content of a confusion. """

  def __init__(self, utterance, container, thelists): # type: (PressUtterance, PressMessage, []) -> None
    """
    Initialize the message with an utterance

    :param utterance: the press utterance that this message is within the content for
    :type utterance: PressUtterance
    :param container: the press message that contains this one
    :type container: PressMessage
    :param thelists: the parsed, nested DAIDE statement
    :type thelists: []
    """

    super().__init__(utterance, container)
    if thelists is None or len(thelists) == 0:
      self.operator = 'HUH'
      self.details = randomFactory(utterance, self, random.choice(['PRP', 'FCT']))
    elif len(thelists) == 2:
      self.operator = thelists[0]
      self.details = messageFactory(utterance, self, thelists[1])

  def formenglish(self): # type () -> str
    """
    Creates an English expression about the confusion in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    if self.details is None:
      return super().formenglish()

    self.english = self.details.formenglish()

    return self.english

  def formlistenglish(self): # type: () -> str
    """
    Creates a simple English statement, without any context like proposals, negations, etc.
    Useful for lists of conjunctions or other contexts in which simplicity is valued over flavor.

    :return: the simple English statement
    :rtype: str

    """

    self.simpleenglish = 'I did not understand your message.'

    return self.simpleenglish

  def formclauseenglish(self): # type: () -> str
    """
    Creates a simple English clause, without any context like proposals, negations, etc.
    Useful for conditional statements or other contexts in which simplicity is valued over flavor.

    :return: the simple English clause
    :rtype: str

    """

    self.simpleenglish = self.formlistenglish()

    return self.simpleenglish

  def formDAIDE(self): # type () -> str
    """
    Create a DAIDE representation of this Message

    :return: the DAIDE message
    :rtype: str
    """

    return 'HUH (' + self.details.formDAIDE() + ')'

class PressIgnore(PressMessage):
  """ The game-related content of an ignoring. """

  def __init__(self, utterance, container, thelists): # type: (PressUtterance, PressMessage, []) -> None
    """
    Initialize the message with an utterance

    :param utterance: the press utterance that this message is within the content for
    :type utterance: PressUtterance
    :param container: the press message that contains this one
    :type container: PressMessage
    :param thelists: the parsed, nested DAIDE statement
    :type thelists: []
    """

    super().__init__(utterance, container)
    if thelists is None or len(thelists) == 0:
      self.operator = 'BWX'
      self.details = randomFactory(utterance, self, 'PRP')
    elif len(thelists) == 2:
      self.operator = thelists[0]
      self.details = messageFactory(utterance, self, thelists[1])

  def formenglish(self): # type () -> str
    """
    Creates an English expression about the ignoring in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    if random.choice([True,False]):
      self.english = ''
    else:
      self.english = helpers.powerdict[self.utterance.frompower]['Objective'] + ' ignores you.'

    return self.english

  def formlistenglish(self): # type: () -> str
    """
    Creates a simple English statement, without any context like proposals, negations, etc.
    Useful for lists of conjunctions or other contexts in which simplicity is valued over flavor.

    :return: the simple English statement
    :rtype: str

    """

    self.simpleenglish = self.formenglish()

    return self.simpleenglish

  def formclauseenglish(self): # type: () -> str
    """
    Creates a simple English clause, without any context like proposals, negations, etc.
    Useful for conditional statements or other contexts in which simplicity is valued over flavor.

    :return: the simple English clause
    :rtype: str

    """

    self.simpleenglish = self.formlistenglish()

    return self.simpleenglish

  def formDAIDE(self): # type () -> str
    """
    Create a DAIDE representation of this Message

    :return: the DAIDE message
    :rtype: str
    """

    return 'BWX (' + self.details.formDAIDE() + ')'

class PressPeace(PressMessage):
  """ The game-related content of a peace treaty. """

  def __init__(self, utterance, container, thelists): # type: (PressUtterance, PressMessage, []) -> None
    """
    Initialize the message with an utterance

    :param utterance: the press utterance that this message is within the content for
    :type utterance: PressUtterance
    :param container: the press message that contains this one
    :type container: PressMessage
    :param thelists: the parsed, nested DAIDE statement
    :type thelists: []
    """

    super().__init__(utterance, container)
    if thelists is None or len(thelists) == 0:
      self.operator = 'PCE'
      if random.choice([True, True, False]):
        self.allies = [curpower for curpower in helpers.powerlist if curpower in utterance.topowers or curpower == utterance.frompower]
      else:
        self.allies = random.sample(helpers.powerlist, random.randint(2, 4))
    elif len(thelists) == 2:
      self.operator = thelists[0]
      self.allies = thelists[1]

  def formenglish(self): # type () -> str
    """
    Creates an English expression about the ignoring in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    if self.container.operator == 'PRP':
      # (PRP (PCE
      if self.container.container is None:
        if random.choice([True, False]):
          self.english = 'I ' + random.choice(['propose', 'request', 'offer']) + \
                         ' a ' + random.choice(['peace treaty', 'peace deal', 'non-agression pact', 'cease-fire']) + \
                         ' between ' + helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers) + '.'
        else:
          self.english = 'I ' + random.choice(['propose', 'request']) + ' that ' + \
                         helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers, case='Subjective') + ' ' + \
                         random.choice(['form', 'sign', 'agree to', 'establish']) + ' a ' + \
                         random.choice(['peace treaty', 'peace deal', 'non-agression pact', 'cease-fire']) + '.'
      # (YES (PRP (PCE
      elif self.container.container.operator == 'YES':
        self.english = 'I ' + random.choice(['agree to', 'concur with', 'would appreciate']) + ' a ' + \
                       random.choice(['peace treaty', 'peace deal', 'non-agression pact', 'cease-fire']) + \
                       ' between ' + helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers) + '.'
      # (REJ (PRP (PCE
      elif self.container.container.operator == 'REJ':
        self.english = 'I ' + random.choice(['reject', 'do not concur with', 'do not approve of']) + ' a ' + \
                       random.choice(['peace treaty', 'peace deal', 'non-agression pact', 'cease-fire']) + \
                       ' between ' + helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers) + '.'
      # (CCL (PRP (PCE
      elif self.container.container.operator == 'CCL':
        self.english = 'I wish to ' + random.choice(['cancel', 'retract', 'take back']) + ' my proposal of a ' + \
                       random.choice(['peace treaty', 'peace deal', 'non-agression pact', 'cease-fire']) + \
                       ' between ' + helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers) + '.'
      # (HUH (PRP (PCE
      elif self.container.container.operator == 'HUH':
        self.english = 'I do not understand your peace proposal.'
    elif self.container.operator == 'NOT':
      if self.container.container.operator == 'PRP':
        # (PRP (NOT (PCE
        if self.container.container.container is None:
          self.english = 'I ' + random.choice(['propose', 'request']) + ' that ' + \
                         helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers, case='Subjective') + ' ' + \
                         random.choice(['break', 'cancel', 'annul']) + ' ' + \
                         helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers, case='Possessive') + ' ' + \
                         random.choice(['peace treaty', 'peace deal', 'non-agression pact', 'cease-fire']) + '.'
        # (YES (PRP (NOT (PCE
        elif self.container.container.container.operator == 'YES':
          self.english = 'I ' + random.choice(['agree', 'concur']) + ' that ' + \
                         helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers, case='Subjective') + ' ' + \
                         random.choice(['break', 'cancel', 'annul']) + ' ' + \
                         helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers, case='Possessive') + ' ' + \
                         random.choice(['peace treaty', 'peace deal', 'non-agression pact', 'cease-fire']) + '.'
        # (REJ (PRP (NOT (PCE
        elif self.container.container.container.operator == 'REJ':
          if random.choice([True, False]):
            self.english = 'I ' + random.choice(['disagree', 'reject']) + ' that ' + \
                           helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers, case='Subjective') + \
                           ' should ' + random.choice(['break', 'cancel', 'annul']) + ' ' + \
                           helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers, case='Possessive') + ' ' + \
                           random.choice(['peace treaty', 'peace deal', 'non-agression pact', 'cease-fire']) + '.'
          else:
            self.english = 'No, ' + helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers, case='Subjective') + ' ' + \
                           random.choice(['should not', 'cannot', 'ought not']) + ' ' + random.choice(['break', 'cancel', 'annul']) + ' ' + \
                           helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers, case='Possessive') + ' ' + \
                           random.choice(['peace treaty', 'peace deal', 'non-agression pact', 'cease-fire']) + '.'
        # (CCL (PRP (NOT (PCE
        elif self.container.container.container.operator == 'CCL':
          self.english = 'I wish to ' + random.choice(['cancel', 'retract', 'take back']) + ' my proposal that ' + \
                         helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers, case='Subjective') + ' ' + \
                         random.choice(['break', 'cancel', 'annul']) + ' ' + \
                         helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers, case='Possessive') + ' ' + \
                         random.choice(['peace treaty', 'peace deal', 'non-agression pact', 'cease-fire']) + '.'
        # (HUH (PRP (NOT (PCE
        elif self.container.container.container.operator == 'HUH':
          self.english = 'I do not understand your proposal about a peace treaty.'
      elif self.container.container.operator == 'FCT':
        # (FCT (NOT (PCE
        if self.container.container.container is None:
          self.english = helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers, case='Subjective') + ' ' + \
                         random.choice(['are not in a current', 'do not have a current', 'are not in an active', 'do not have an active', 'are not in a', 'do not have a']) + ' ' + \
                         random.choice(['peace treaty', 'peace deal', 'non-agression pact', 'cease-fire']) + '.'
        # (HUH (FCT (NOT (PCE
        elif self.container.container.container.operator == 'HUH':
          self.english = 'I do not understand your statement about a peace treaty.'
    elif self.container.operator == 'NAR':
      if self.container.container.operator == 'PRP':
        # (PRP (NAR (PCE
        if self.container.container.container is None:
          self.english = 'I ' + random.choice(['propose', 'request']) + ' that ' + \
                         helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers, case='Subjective') + ' not ' + \
                         random.choice(['form', 'sign', 'agree to', 'establish']) + ' a ' + \
                         random.choice(['peace treaty', 'peace deal', 'non-agression pact', 'cease-fire']) + '.'
        # (YES (PRP (NAR (PCE
        elif self.container.container.container.operator == 'YES':
          self.english = 'I ' + random.choice(['agree', 'concur']) + ' that ' + \
                         helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers, case='Subjective') + ' not ' + \
                         random.choice(['form', 'sign', 'agree to', 'establish']) + ' a ' + \
                         random.choice(['peace treaty', 'peace deal', 'non-agression pact', 'cease-fire']) + '.'
        # (REJ (PRP (NAR (PCE
        elif self.container.container.container.operator == 'REJ':
          self.english = 'No, I ' + random.choice(['think', 'believe']) + ' that ' + \
                         helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers, case='Subjective') + \
                         ' should in fact ' + random.choice(['form', 'sign', 'agree to', 'establish']) + ' a ' + \
                         random.choice(['peace treaty', 'peace deal', 'non-agression pact', 'cease-fire']) + '.'
        # (CCL (PRP (NAR (PCE
        elif self.container.container.container.operator == 'CCL':
          self.english = 'I wish to ' + random.choice(['cancel', 'retract', 'take back']) + ' my proposal that ' + \
                         helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers, case='Subjective') + \
                         ' avoid ' + random.choice(['forming', 'signing', 'agreeing to', 'establishing']) + ' a ' + \
                         random.choice(['peace treaty', 'peace deal', 'non-agression pact', 'cease-fire']) + '.'
        # (HUH (PRP (NAR (PCE
        elif self.container.container.container.operator == 'HUH':
          self.english = 'I do not understand your proposal about a peace treaty.'
      elif self.container.container.operator == 'FCT':
        # (FCT (NAR (PCE
        if self.container.container.container is None:
          self.english = 'It is unclear if ' + helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers, case='Subjective') + ' ' + \
                         random.choice(['are in a', 'have a']) + ' ' + \
                         random.choice(['peace treaty', 'peace deal', 'non-agression pact', 'cease-fire']) + '.'
        # (HUH (FCT (NAR (PCE
        elif self.container.container.container.operator == 'HUH':
          self.english = 'I do not understand your statement about a peace treaty.'
    elif self.container.operator == 'FCT':
      # (FCT (PCE
      if self.container.container is None:
        self.english = helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers, case='Subjective') + ' ' + \
                       random.choice(['are in a', 'have a']) + ' ' + \
                       random.choice(['peace treaty', 'peace deal', 'non-agression pact', 'cease-fire']) + '.'
      # (HUH (FCT (PCE
      elif self.container.container.operator == 'HUH':
        self.english = 'I do not understand your statement about a peace treaty.'
    else:
      self.english = self.formlistenglish()

    return self.english

  def formlistenglish(self): # type: () -> str
    """
    Creates a simple English statement about this peace deal, without any context like proposals, negations, etc.
    Useful for lists of conjunctions or other contexts in which simplicity is valued over flavor.

    :return: the simple English statement
    :rtype: str

    """

    self.simpleenglish = helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers, case='Subjective') + ' ' + \
                         random.choice(['form', 'sign', 'agree to', 'establish']) + ' a ' + \
                         random.choice(['peace treaty', 'peace deal', 'non-agression pact', 'cease-fire']) + '.'

    return self.simpleenglish

  def formclauseenglish(self): # type: () -> str
    """
    Creates a simple English statement about this peace deal, without any context like proposals, negations, etc.
    Useful for lists of conjunctions or other contexts in which simplicity is valued over flavor.

    :return: the simple English statement
    :rtype: str

    """
    if self.container.operator == "NOT":
      self.simpleenglish = helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers,
                                                case='Subjective') + ' ' + \
                           random.choice(['will not form', 'refuses', 'disagree to', 'will not establish']) + ' a ' + \
                           random.choice(['peace treaty', 'peace deal', 'non-agression pact', 'cease-fire'])
    else:
      self.simpleenglish = helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers, case='Subjective') + ' ' + \
                         random.choice(['form', 'sign', 'agree to', 'establish']) + ' a ' + \
                         random.choice(['peace treaty', 'peace deal', 'non-agression pact', 'cease-fire'])

    return self.simpleenglish

  def formDAIDE(self): # type () -> str
    """
    Create a DAIDE representation of this Message

    :return: the DAIDE message
    :rtype: str
    """

    return 'PCE (' + ' '.join(self.allies) + ')'

class PressAlliance(PressMessage):
  """ The game-related content of an alliance. """

  def __init__(self, utterance, container, thelists): # type: (PressUtterance, PressMessage, []) -> None
    """
    Initialize the message with an utterance

    :param utterance: the press utterance that this message is within the content for
    :type utterance: PressUtterance
    :param container: the press message that contains this one
    :type container: PressMessage
    :param thelists: the parsed, nested DAIDE statement
    :type thelists: []
    """

    super().__init__(utterance, container)
    if thelists is None or len(thelists) == 0:
      self.operator = 'ALY'
      if random.choice([True, True, False]):
        self.allies = [curpower for curpower in helpers.powerlist if curpower in utterance.topowers or curpower == utterance.frompower]
        opplist = [curpower for curpower in helpers.powerlist if curpower not in self.allies]
        self.opponents = random.sample(opplist, random.randint(1, min(3, len(opplist))))
      else:
        self.allies = random.sample(helpers.powerlist, random.randint(2, 3))
        opplist = [curpower for curpower in helpers.powerlist if curpower not in self.allies and curpower != utterance.frompower]
        self.opponents = random.sample(opplist, random.randint(1, min(3, len(opplist))))
    elif len(thelists) == 4:
      self.operator = thelists[0]
      self.allies = thelists[1]
      self.opponents = thelists[3]

  def formenglish(self): # type () -> str
    """
    Creates an English expression about the alliance in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    if self.container.operator == 'PRP':
      # (PRP (ALY
      if self.container.container is None:
        if random.choice([True, False]):
          self.english = 'I ' + random.choice(['propose', 'request', 'offer']) + \
                         ' ' + random.choice(['an alliance', 'a joint military operation', 'military cooperation', 'a military coalition']) + \
                         ' between ' + helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers) + \
                         ' against ' + helpers.listOfPowers(self.opponents, self.utterance.frompower, self.utterance.topowers) + '.'
        else:
          self.english = 'I ' + random.choice(['propose', 'request']) + ' that ' + \
                         helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers, case='Subjective') + ' ' + \
                         random.choice(['form', 'sign', 'agree to', 'establish']) + ' ' + \
                         random.choice(['an alliance', 'a joint military operation', 'military cooperation', 'a military coalition']) + \
                         ' against ' + helpers.listOfPowers(self.opponents, self.utterance.frompower, self.utterance.topowers) + '.'
      # (YES (PRP (ALY
      elif self.container.container.operator == 'YES':
        self.english = 'I ' + random.choice(['agree to', 'concur with', 'would appreciate']) + ' ' + \
                       random.choice(['an alliance', 'a joint military operation', 'military cooperation', 'a military coalition']) + \
                       ' between ' + helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers) + \
                       ' against ' + helpers.listOfPowers(self.opponents, self.utterance.frompower, self.utterance.topowers) + '.'
      # (REJ (PRP (ALY
      elif self.container.container.operator == 'REJ':
        self.english = 'I ' + random.choice(['reject', 'do not concur with', 'do not approve of']) + ' ' + \
                       random.choice(['an alliance', 'a joint military operation', 'military cooperation', 'a military coalition']) + \
                       ' between ' + helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers) + \
                       ' against ' + helpers.listOfPowers(self.opponents, self.utterance.frompower, self.utterance.topowers) + '.'
      # (CCL (PRP (ALY
      elif self.container.container.operator == 'CCL':
        self.english = 'I wish to ' + random.choice(['cancel', 'retract', 'take back']) + ' my proposal of ' + \
                       random.choice(['an alliance', 'a joint military operation', 'military cooperation', 'a military coalition']) + \
                       ' between ' + helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers) + \
                       ' against ' + helpers.listOfPowers(self.opponents, self.utterance.frompower, self.utterance.topowers) + '.'
      # (HUH (PRP (ALY
      elif self.container.container.operator == 'HUH':
        self.english = 'I do not understand your alliance proposal.'
    elif self.container.operator == 'NOT':
      if self.container.container.operator == 'PRP':
        # (PRP (NOT (ALY
        if self.container.container.container is None:
          self.english = 'I ' + random.choice(['propose', 'request', 'demand']) + ' that ' + \
                         helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers, case='Subjective') + ' not ' + \
                         random.choice(['form', 'sign', 'agree to']) + ' ' + \
                         random.choice(['an alliance', 'a joint military operation', 'military cooperation', 'a military coalition']) + ' against ' + \
                         helpers.listOfPowers(self.opponents, self.utterance.frompower, self.utterance.topowers) + '.'
        # (YES (PRP (NOT (ALY
        elif self.container.container.container.operator == 'YES':
          self.english = 'I ' + random.choice(['agree', 'concur']) + ' that ' + \
                         helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers, case='Subjective') + ' should not ' + \
                         random.choice(['form', 'sign', 'agree to']) + ' ' + \
                         random.choice(['an alliance', 'a joint military operation', 'military cooperation', 'a military coalition']) + ' against ' + \
                         helpers.listOfPowers(self.opponents, self.utterance.frompower, self.utterance.topowers) + '.'
        # (REJ (PRP (NOT (ALY
        elif self.container.container.container.operator == 'REJ':
          if random.choice([True, False]):
            self.english = 'I ' + random.choice(['disagree', 'reject']) + ' that ' + \
                           helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers, case='Subjective') + ' should not ' + \
                           random.choice(['form', 'sign', 'agree to']) + ' ' + \
                           random.choice(['an alliance', 'a joint military operation', 'military cooperation', 'a military coalition']) + ' against ' + \
                           helpers.listOfPowers(self.opponents, self.utterance.frompower, self.utterance.topowers) + '.'
          else:
            self.english = 'No, ' + helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers, case='Subjective') + ' ' + \
                           random.choice(['should be free to', 'should not be stopped from', 'should not be prevented from']) + ' ' + \
                           random.choice(['forming', 'signing', 'agreeing to']) + ' ' + \
                           random.choice(['an alliance', 'a joint military operation', 'military cooperation', 'a military coalition']) + ' against ' + \
                           helpers.listOfPowers(self.opponents, self.utterance.frompower, self.utterance.topowers) + '.'
        # (CCL (PRP (NOT (ALY
        elif self.container.container.container.operator == 'CCL':
          self.english = 'I wish to ' + random.choice(['cancel', 'retract', 'take back']) + ' my proposal that ' + \
                         helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers, case='Subjective') + ' ' + \
                         random.choice(['form', 'sign', 'agree to']) + ' ' + \
                         random.choice(['an alliance', 'a joint military operation', 'military cooperation', 'a military coalition']) + ' against ' + \
                         helpers.listOfPowers(self.opponents, self.utterance.frompower, self.utterance.topowers) + '.'
        # (HUH (PRP (NOT (ALY
        elif self.container.container.container.operator == 'HUH':
          self.english = 'I do not understand your proposal about an alliance.'
      elif self.container.container.operator == 'FCT':
        # (FCT (NOT (ALY
        if self.container.container.container is None:
          self.english = helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers, case='Subjective') + ' ' + \
                         random.choice(['are not in', 'do not have']) + ' ' + \
                         random.choice(['a current', 'an active', 'a']) + ' ' + \
                         random.choice(['alliance', 'joint military operation', 'military coalition']) + ' against ' + \
                         helpers.listOfPowers(self.opponents, self.utterance.frompower, self.utterance.topowers) + '.'
          self.english = self.english.replace(' a alliance', ' an alliance')
        # (HUH (FCT (NOT (ALY
        elif self.container.container.container.operator == 'HUH':
          self.english = 'I do not understand your statement about an alliance.'
    elif self.container.operator == 'NAR':
      if self.container.container.operator == 'PRP':
        # (PRP (NAR (ALY
        if self.container.container.container is None:
          self.english = 'I ' + random.choice(['doubt', 'don\'t think', 'do not think']) + ' that ' + \
                         helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers, case='Subjective') + ' should ' + \
                         random.choice(['form', 'sign', 'agree to']) + ' ' + \
                         random.choice(['an alliance', 'a joint military operation', 'military cooperation', 'a military coalition']) + ' against ' + \
                         helpers.listOfPowers(self.opponents, self.utterance.frompower, self.utterance.topowers) + '.'
        # (YES (PRP (NAR (ALY
        elif self.container.container.container.operator == 'YES':
          self.english = 'I ' + random.choice(['agree', 'concur']) + ' that ' + \
                         helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers, case='Subjective') + ' should not ' + \
                         random.choice(['form', 'sign', 'agree to']) + ' ' + \
                         random.choice(['an alliance', 'a joint military operation', 'military cooperation', 'a military coalition']) + ' against ' + \
                         helpers.listOfPowers(self.opponents, self.utterance.frompower, self.utterance.topowers) + '.'
        # (REJ (PRP (NAR (ALY
        elif self.container.container.container.operator == 'REJ':
          self.english = 'No, I ' + random.choice(['think', 'believe']) + ' that ' + \
                         helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers, case='Subjective') + \
                         ' should in fact be able to ' + random.choice(['form', 'sign', 'agree to', 'establish']) + ' ' + \
                         random.choice(['an alliance', 'a joint military operation', 'military cooperation', 'a military coalition']) + ' against ' + \
                         helpers.listOfPowers(self.opponents, self.utterance.frompower, self.utterance.topowers) + '.'
        # (CCL (PRP (NAR (ALY
        elif self.container.container.container.operator == 'CCL':
          self.english = 'I wish to ' + random.choice(['cancel', 'retract', 'take back']) + ' my proposal that ' + \
                         helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers, case='Subjective') + ' should not ' + \
                         random.choice(['form', 'sign', 'agree to']) + ' ' + \
                         random.choice(['an alliance', 'a joint military operation', 'military cooperation', 'a military coalition']) + ' against ' + \
                         helpers.listOfPowers(self.opponents, self.utterance.frompower, self.utterance.topowers) + '.'
        # (HUH (PRP (NAR (ALY
        elif self.container.container.container.operator == 'HUH':
          self.english = 'I do not understand your proposal about an alliance.'
      elif self.container.container.operator == 'FCT':
        # (FCT (NAR (ALY
        if self.container.container.container is None:
          self.english = 'It is unclear if ' + helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers, case='Subjective') + ' ' + \
                         random.choice(['are in', 'have']) + ' ' + \
                         random.choice(['an alliance', 'a joint military operation', 'military cooperation', 'a military coalition']) + ' against ' + \
                         helpers.listOfPowers(self.opponents, self.utterance.frompower, self.utterance.topowers) + '.'
        # (HUH (FCT (NAR (ALY
        elif self.container.container.container.operator == 'HUH':
          self.english = 'I do not understand your statement about an alliance.'
    elif self.container.operator == 'FCT':
      # (FCT (ALY
      if self.container.container is None:
        self.english = helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers, case='Subjective') + ' ' + \
                       random.choice(['are in', 'have']) + ' ' + \
                       random.choice(['an alliance', 'a joint military operation', 'military cooperation', 'a military coalition']) + ' against ' + \
                       helpers.listOfPowers(self.opponents, self.utterance.frompower, self.utterance.topowers) + '.'
      # (HUH (FCT (ALY
      elif self.container.container.operator == 'HUH':
        self.english = 'I do not understand your statement about an alliance.'
    else:
      self.english = self.formlistenglish()

    return self.english

  def formlistenglish(self): # type: () -> str
    """
    Creates a simple English statement about this alliance, without any context like proposals, negations, etc.
    Useful for lists of conjunctions or other contexts in which simplicity is valued over flavor.

    :return: the simple English statement
    :rtype: str

    """

    self.simpleenglish = helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers, case='Subjective') + ' ' + \
                         random.choice(['form', 'sign', 'agree to', 'establish']) + ' ' + \
                         random.choice(['an alliance', 'a joint military operation', 'military cooperation', 'a military coalition']) + ' against ' + \
                         helpers.listOfPowers(self.opponents, self.utterance.frompower, self.utterance.topowers) + '.'

    return self.simpleenglish

  def formclauseenglish(self): # type: () -> str
    """
    Creates a simple English statement about this alliance, without any context like proposals, negations, etc.
    Useful for lists of conjunctions or other contexts in which simplicity is valued over flavor.

    :return: the simple English statement
    :rtype: str

    """
    if self.container.operator == "NOT":  #For example, NOT ( PRP ( ALY
      self.simpleenglish = helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers,
                                                case='Subjective') + ' ' + \
                           random.choice(['will not form', 'will not sign', 'will not establish']) + ' ' + \
                           random.choice(['an alliance', 'a joint military operation', 'military cooperation',
                                          'a military coalition']) + ' against ' + \
                           helpers.listOfPowers(self.opponents, self.utterance.frompower, self.utterance.topowers)
    else:
      self.simpleenglish = helpers.listOfPowers(self.allies, self.utterance.frompower, self.utterance.topowers, case='Subjective') + ' ' + \
                         random.choice(['form', 'sign', 'agree to', 'establish']) + ' ' + \
                         random.choice(['an alliance', 'a joint military operation', 'military cooperation', 'a military coalition']) + ' against ' + \
                         helpers.listOfPowers(self.opponents, self.utterance.frompower, self.utterance.topowers)

    return self.simpleenglish

  def formDAIDE(self): # type () -> str
    """
    Create a DAIDE representation of this Message

    :return: the DAIDE message
    :rtype: str
    """

    return 'ALY (' + ' '.join(self.allies) + ') VSS (' + ' '.join(self.opponents) + ')'

class PressDMZ(PressMessage):
  """ The game-related content of a DMZ. """

  def __init__(self, utterance, container, thelists): # type: (PressUtterance, PressMessage, []) -> None
    """
    Initialize the message with an utterance

    :param utterance: the press utterance that this message is within the content for
    :type utterance: PressUtterance
    :param container: the press message that contains this one
    :type container: PressMessage
    :param thelists: the parsed, nested DAIDE statement
    :type thelists: []
    """

    super().__init__(utterance, container)
    if thelists is None or len(thelists) == 0:
      self.operator = 'DMZ'
      if random.choice([True, True, False]):
        self.powers = [curpower for curpower in helpers.powerlist if curpower in utterance.topowers or curpower == utterance.frompower]
      else:
        self.powers = random.sample(helpers.powerlist, random.randint(1, 3))
      self.provinces = random.sample(helpers.provincelist, random.randint(1, 3))
    elif len(thelists) == 3:
      self.operator = thelists[0]
      self.powers = thelists[1]
      self.provinces = thelists[2]

  def formenglish(self): # type () -> str
    """
    Creates an English expression about the DMZ in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    powersgloss = helpers.listOfPowers(self.powers, self.utterance.frompower, self.utterance.topowers)
    provincesgloss = helpers.listOfProvinces(self.provinces)
    if self.container.operator == 'PRP':
      # (PRP (DMZ
      if self.container.container is None:
        if 'you ' in powersgloss.lower() and 'and me' in powersgloss.lower():
          self.english = 'I ' + random.choice(['propose', 'request', 'offer']) + \
                         ' we ' + random.choice(['stay out of', 'create a DMZ in', 'create a demilitarized zone in', 'keep out of']) + ' ' + \
                         provincesgloss + '.'
        else:
          self.english = 'I ' + random.choice(['propose', 'request', 'offer']) + ' that ' + \
                         powersgloss + ' ' + random.choice(['stay out of', 'create a DMZ in', 'create a demilitarized zone', 'keep out of']) + ' ' + \
                         provincesgloss + '.'
      # (YES (PRP (DMZ
      elif self.container.container.operator == 'YES':
        self.english = 'I ' + random.choice(['agree to', 'concur with']) + ' ' + \
                       random.choice(['a DMZ in', 'a demilitarized zone in', 'keeping out of', 'staying out of']) + ' ' + \
                       provincesgloss + ', covering ' + powersgloss + '.'
      # (REJ (PRP (DMZ
      elif self.container.container.operator == 'REJ':
        self.english = 'I ' + random.choice(['reject', 'do not concur with', 'do not approve of']) + ' ' + \
                       random.choice(['a DMZ in', 'a demilitarized zone in', 'keeping out of', 'staying out of']) + ' ' + \
                       provincesgloss + '.'
      # (CCL (PRP (DMZ
      elif self.container.container.operator == 'CCL':
        self.english = 'I wish to ' + random.choice(['cancel', 'retract', 'take back']) + ' my proposal of ' + \
                       random.choice(['a DMZ in', 'a demilitarized zone in']) + ' ' + \
                       provincesgloss + '.'
      # (HUH (PRP (DMZ
      elif self.container.container.operator == 'HUH':
        self.english = 'I do not understand your DMZ proposal.'
    elif self.container.operator == 'NOT':
      if self.container.container.operator == 'PRP':
        # (PRP (NOT (DMZ
        if self.container.container.container is None:
          if random.choice([True, False]):
            self.english = 'I ' + random.choice(['propose', 'request', 'demand']) + ' that ' + \
                           powersgloss + ' have free movement into and through ' + \
                           provincesgloss + '.'
          else:
            self.english = 'I ' + random.choice(['propose', 'request', 'demand']) + ' that no ' + \
                           random.choice(['DMZ', 'demilitarized zone', 'safe zone']) + ' exist in ' + \
                           provincesgloss + '.'
        # (YES (PRP (NOT (DMZ
        elif self.container.container.container.operator == 'YES':
          self.english = 'I ' + random.choice(['agree', 'concur']) + ' that ' + \
                         powersgloss + ' have free movement into and through ' + \
                         provincesgloss + '.'
        # (REJ (PRP (NOT (DMZ
        elif self.container.container.container.operator == 'REJ':
          self.english = 'I ' + random.choice(['disagree with', 'reject']) + ' free movement into and through ' + \
                         provincesgloss + ' for ' + powersgloss + '.'
        # (CCL (PRP (NOT (DMZ
        elif self.container.container.container.operator == 'CCL':
          self.english = 'I wish to ' + random.choice(['cancel', 'retract', 'take back']) + ' my proposal that ' + \
                         provincesgloss + ' not enjoy a ' + random.choice(['DMZ', 'demilitarized zone', 'safe zone']) + \
                         ' with respect to ' + powersgloss + '.'
        # (HUH (PRP (NOT (DMZ
        elif self.container.container.container.operator == 'HUH':
          self.english = 'I do not understand your proposal about a DMZ.'
      elif self.container.container.operator == 'FCT':
        # (FCT (NOT (DMZ
        if self.container.container.container is None:
          self.english = powersgloss + ' ' + \
                         random.choice(['are not in', 'do not respect', 'do not have']) + ' ' + \
                         random.choice(['a current', 'an active', 'a']) + ' ' + \
                         random.choice(['DMZ', 'demilitarized zone', 'safe zone']) + ' in ' + \
                         provincesgloss + '.'
        # (HUH (FCT (NOT (DMZ
        elif self.container.container.container.operator == 'HUH':
          self.english = 'I do not understand your statement about a DMZ.'
    elif self.container.operator == 'NAR':
      if self.container.container.operator == 'PRP':
        # (PRP (NAR (DMZ
        if self.container.container.container is None:
          self.english = 'I ' + random.choice(['doubt', 'don\'t think', 'do not think']) + ' that ' + \
                         helpers.listOfPowers(self.powers, self.utterance.frompower, self.utterance.topowers, case='Subjective') + ' should ' + \
                         random.choice(['form', 'sign', 'agree to']) + ' a ' + \
                         random.choice(['DMZ', 'demilitarized zone', 'safe zone']) + ' in ' + \
                         provincesgloss + '.'
        # (YES (PRP (NAR (DMZ
        elif self.container.container.container.operator == 'YES':
          self.english = 'I ' + random.choice(['agree', 'concur']) + ' that ' + \
                         helpers.listOfPowers(self.powers, self.utterance.frompower, self.utterance.topowers, case='Subjective') + ' should not ' + \
                         random.choice(['form', 'sign', 'agree to']) + ' a ' + \
                         random.choice(['DMZ', 'demilitarized zone', 'safe zone']) + ' in ' + \
                         provincesgloss + '.'
        # (REJ (PRP (NAR (DMZ
        elif self.container.container.container.operator == 'REJ':
          self.english = 'No, I ' + random.choice(['think', 'believe']) + ' that ' + \
                         helpers.listOfPowers(self.powers, self.utterance.frompower, self.utterance.topowers, case='Subjective') + ' should not ' + \
                         ' should in fact be able to ' + random.choice(['form', 'sign', 'agree to', 'establish']) + ' a ' + \
                         random.choice(['DMZ', 'demilitarized zone', 'safe zone']) + ' in ' + \
                         provincesgloss + '.'
        # (CCL (PRP (NAR (DMZ
        elif self.container.container.container.operator == 'CCL':
          self.english = 'I wish to ' + random.choice(['cancel', 'retract', 'take back']) + ' my proposal that ' + \
                         helpers.listOfPowers(self.powers, self.utterance.frompower, self.utterance.topowers, case='Subjective') + ' should not ' + \
                         random.choice(['form', 'sign', 'agree to']) + ' a ' + \
                         random.choice(['DMZ', 'demilitarized zone', 'safe zone']) + ' in ' + \
                         provincesgloss + '.'
        # (HUH (PRP (NAR (DMZ
        elif self.container.container.container.operator == 'HUH':
          self.english = 'I do not understand your proposal about a DMZ.'
      elif self.container.container.operator == 'FCT':
        # (FCT (NAR (DMZ
        if self.container.container.container is None:
          self.english = 'It is unclear if ' + helpers.listOfPowers(self.powers, self.utterance.frompower, self.utterance.topowers, case='Subjective') + ' ' + \
                         random.choice(['are in', 'have']) + ' a ' + \
                         random.choice(['DMZ', 'demilitarized zone', 'safe zone']) + ' in ' + \
                         provincesgloss + '.'
        # (HUH (FCT (NAR (DMZ
        elif self.container.container.container.operator == 'HUH':
          self.english = 'I do not understand your statement about a DMZ.'
    elif self.container.operator == 'FCT':
      # (FCT (DMZ
      if self.container.container is None:
        self.english = helpers.listOfPowers(self.powers, self.utterance.frompower, self.utterance.topowers, case='Subjective') + ' ' + \
                       random.choice(['are in', 'have']) + ' ' + \
                       random.choice(['DMZ', 'demilitarized zone', 'safe zone']) + ' in ' + \
                       provincesgloss + '.'
      # (HUH (FCT (DMZ
      elif self.container.container.operator == 'HUH':
        self.english = 'I do not understand your statement about a DMZ.'
    else:
      self.english = self.formlistenglish()

    return self.english

  def formlistenglish(self): # type () -> str
    """
    Creates an English expression about the DMZ in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    self.simpleenglish = helpers.listOfPowers(self.powers, self.utterance.frompower, self.utterance.topowers, case='Subjective') + ' form a DMZ in ' + helpers.listOfProvinces(self.provinces) + '.'

    return self.simpleenglish

  def formclauseenglish(self): # type () -> str
    """
    Creates an English expression about the DMZ in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """
    if self.container.operator == "NOT":
      self.simpleenglish = helpers.listOfPowers(self.powers, self.utterance.frompower, self.utterance.topowers, case='Subjective') + ' will not form a DMZ in ' + helpers.listOfProvinces(self.provinces) + ''
    else:
      self.simpleenglish = helpers.listOfPowers(self.powers, self.utterance.frompower, self.utterance.topowers, case='Subjective') + ' form a DMZ in ' + helpers.listOfProvinces(self.provinces) + ''

    return self.simpleenglish

  def formDAIDE(self): # type () -> str
    """
    Create a DAIDE representation of this Message

    :return: the DAIDE message
    :rtype: str
    """

    return 'DMZ (' + ' '.join(self.powers) + ') (' + ' '.join(self.provinces) + ')'

class PressDraw(PressMessage):
  """ The game-related content of a draw. """

  def __init__(self, utterance, container, thelists): # type: (PressUtterance, PressMessage, []) -> None
    """
    Initialize the message with an utterance

    :param utterance: the press utterance that this message is within the content for
    :type utterance: PressUtterance
    :param container: the press message that contains this one
    :type container: PressMessage
    :param thelists: the parsed, nested DAIDE statement
    :type thelists: []
    """

    super().__init__(utterance, container)
    if thelists is None or len(thelists) == 0:
      self.operator = 'DRW'
      if random.choice([True, True, False]):
        self.powers = [curpower for curpower in helpers.powerlist if curpower in utterance.topowers or curpower == utterance.frompower]
      else:
        self.powers = None
      self.provinces = random.sample(helpers.provincelist, random.randint(1, 3))
    else:
      self.operator = thelists[0]
      if len(thelists) > 1:
        self.powers = thelists[1]
      else:
        self.powers = None

  def formenglish(self): # type () -> str
    """
    Creates an English expression about the draw in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    powersgloss = ''
    subjpowersgloxx = ''
    if self.powers is not None:
      powersgloss = helpers.listOfPowers(self.powers, self.utterance.frompower, self.utterance.topowers)
      subjpowersgloss = helpers.listOfPowers(self.powers, self.utterance.frompower, self.utterance.topowers, case='Subjective')

    if self.container.operator == 'PRP':
      # (PRP (DRW
      if self.container.container is None:
        if self.powers is None:
          self.english = 'I ' + random.choice(['propose', 'request', 'offer']) + ' we pursue a draw.'
        else:
          self.english = 'I ' + random.choice(['propose', 'request', 'offer']) + ' we pursue a draw between ' + powersgloss + '.'
      # (YES (PRP (DRW
      elif self.container.container.operator == 'YES':
        if self.powers is None:
          self.english = 'I ' + random.choice(['agree to', 'concur with']) + ' pursuing a draw.'
        else:
          self.english = 'I ' + random.choice(['agree to', 'concur with']) + ' pursuing a draw between ' + powersgloss + '.'
      # (REJ (PRP (DRW
      elif self.container.container.operator == 'REJ':
        if self.powers is None:
          self.english = 'I ' + random.choice(['reject', 'do not concur with', 'do not approve of', 'do not agree to']) + ' pursuing a draw.'
        else:
          self.english = 'I ' + random.choice(['reject', 'do not concur with', 'do not approve of', 'do not agree to']) + ' pursuing a draw between ' + powersgloss + '.'
      # (CCL (PRP (DRW
      elif self.container.container.operator == 'CCL':
        if self.powers is None:
          self.english = 'I wish to ' + random.choice(['cancel', 'retract', 'take back']) + ' my proposal of a draw.'
        else:
          self.english = 'I wish to ' + random.choice(['cancel', 'retract', 'take back']) + ' my proposal of a draw between ' + powersgloss + '.'
      # (HUH (PRP (DRW
      elif self.container.container.operator == 'HUH':
        self.english = 'I do not understand your draw proposal.'
    elif self.container.operator == 'NOT':
      if self.container.container.operator == 'PRP':
        # (PRP (NOT (DRW
        if self.container.container.container is None:
          if self.powers is None:
            self.english = 'I ' + random.choice(['propose', 'request', 'offer']) + ' we do not pursue a draw.'
          else:
            self.english = 'I ' + random.choice(['propose', 'request', 'offer']) + ' we do not pursue a draw between ' + powersgloss + '.'
        # (YES (PRP (NOT (DRW
        elif self.container.container.container.operator == 'YES':
          if self.powers is None:
            self.english = 'I ' + random.choice(['agree that', 'concur that']) + ' we should not pursue a draw.'
          else:
            self.english = 'I ' + random.choice(['agree that', 'concur that']) + ' we should not pursue a draw between ' + powersgloss + '.'
        # (REJ (PRP (NOT (DRW
        elif self.container.container.container.operator == 'REJ':
          if self.powers is None:
            self.english = 'I ' + random.choice(['still think', 'nevertheless believe']) + ' we should pursue a draw.'
          else:
            self.english = 'I ' + random.choice(['still think', 'nevertheless believe']) + ' we should pursue a draw between ' + powersgloss + '.'
        # (CCL (PRP (NOT (DRW
        elif self.container.container.container.operator == 'CCL':
          if self.powers is None:
            self.english = 'I wish to ' + random.choice(['cancel', 'retract', 'take back']) + ' my proposal that we do not draw.'
          else:
            self.english = 'I wish to ' + random.choice(['cancel', 'retract', 'take back']) + ' my proposal that ' + subjpowersgloss + ' not pursue a draw.'
        # (HUH (PRP (NOT (DRW
        elif self.container.container.container.operator == 'HUH':
          self.english = 'I do not understand your proposal about a draw.'
      elif self.container.container.operator == 'FCT':
        # (FCT (NOT (DRW
        if self.container.container.container is None:
          if self.powers is None:
            self.english = 'I am not pursuing a draw.'
          else:
            self.english = subjpowersgloss + ' are not pursuing a draw.'
        # (HUH (FCT (NOT (DRW
        elif self.container.container.container.operator == 'HUH':
          self.english = 'I do not understand your statement about a draw.'
    elif self.container.operator == 'NAR':
      if self.container.container.operator == 'PRP':
        # (PRP (NAR (DRW
        if self.container.container.container is None:
          if self.powers is None:
            self.english = 'It is ' + random.choice(['unclear', 'fuzzy', 'uncertain']) + ' that we should pursue a draw.'
          else:
            self.english = 'It is ' + random.choice(['unclear', 'fuzzy', 'uncertain']) + ' that ' + subjpowersgloss + ' should pursue a draw.'
        # (YES (PRP (NAR (DRW
        elif self.container.container.container.operator == 'YES':
          if self.powers is None:
            self.english = 'I ' + random.choice(['agree', 'concur']) + ' that it is ' + random.choice(['unclear', 'fuzzy', 'uncertain']) + ' that we should pursue a draw.'
          else:
            self.english = 'I ' + random.choice(['agree', 'concur']) + ' that it is ' + random.choice(['unclear', 'fuzzy', 'uncertain']) + ' that ' + subjpowersgloss + ' should pursue a draw.'
        # (REJ (PRP (NAR (DRW
        elif self.container.container.container.operator == 'REJ':
          if self.powers is None:
            self.english = 'No, I ' + random.choice(['think', 'believe']) + ' that we should pursue a draw.'
          else:
            self.english = 'No, I ' + random.choice(['think', 'believe']) + ' that ' + subjpowersgloss + ' should pursue a draw.'
        # (CCL (PRP (NAR (DRW
        elif self.container.container.container.operator == 'CCL':
          if self.powers is None:
            self.english = 'I wish to ' + random.choice(['cancel', 'retract', 'take back']) + ' my proposal regarding a draw.'
          else:
            self.english = 'I wish to ' + random.choice(['cancel', 'retract', 'take back']) + ' my proposal regarding a draw between ' + powersgloss + '.'
        # (HUH (PRP (NAR (DRW
        elif self.container.container.container.operator == 'HUH':
          self.english = 'I do not understand your proposal about a draw.'
      elif self.container.container.operator == 'FCT':
        # (FCT (NAR (DRW
        if self.container.container.container is None:
          if self.powers is None:
            self.english = 'It is unclear if we are in a good draw position.'
          else:
            self.english = 'It is unclear if ' + subjpowersgloss + ' are in a good draw position.'
        # (HUH (FCT (NAR (DRW
        elif self.container.container.container.operator == 'HUH':
          self.english = 'I do not understand your statement about a draw.'
    elif self.container.operator == 'FCT':
      # (FCT (DRW
      if self.container.container is None:
        if self.powers is None:
          self.english = 'We are in a good draw position.'
        else:
          self.english = subjpowersgloss + ' are in a good draw position.'
      # (HUH (FCT (DRW
      elif self.container.container.operator == 'HUH':
        self.english = 'I do not understand your statement about a draw.'
    else:
      self.english = self.formlistenglish()

    return self.english

  def formlistenglish(self): # type () -> str
    """
    Creates an English expression about the DMZ in the context of a sender, recipients and desired tone.

    :return: the simple English expression
    :rtype: str
    """

    if self.powers is None:
      self.simpleenglish = 'a draw'
    else:
      self.simpleenglish = 'a draw between ' + helpers.listOfPowers(self.powers, self.utterance.frompower, self.utterance.topowers)

    return self.simpleenglish

  def formclauseenglish(self): # type () -> str
    """
    Creates an English expression about the DMZ in the context of a sender, recipients and desired tone.

    :return: the simple English expression
    :rtype: str
    """

    if self.powers is None and self.container.operator == "NOT":
      self.simpleenglish = 'no draw'
    elif self.powers is None:
      self.simpleenglish = 'a draw'
    elif self.container.operator == "NOT":
      self.simpleenglish = 'no draw between ' + helpers.listOfPowers(self.powers, self.utterance.frompower, self.utterance.topowers)
    else:
      self.simpleenglish = 'a draw between ' + helpers.listOfPowers(self.powers, self.utterance.frompower, self.utterance.topowers)

    return self.simpleenglish

  def formDAIDE(self): # type () -> str
    """
    Create a DAIDE representation of this Message

    :return: the DAIDE message
    :rtype: str
    """

    if self.powers is None:
      return 'DRW'
    else:
      return 'DRW (' + ' '.join(self.powers) + ')'

class PressSolo(PressMessage):
  """ The game-related content of a solo win. """

  def __init__(self, utterance, container, thelists): # type: (PressUtterance, PressMessage, []) -> None
    """
    Initialize the message with an utterance

    :param utterance: the press utterance that this message is within the content for
    :type utterance: PressUtterance
    :param container: the press message that contains this one
    :type container: PressMessage
    :param thelists: the parsed, nested DAIDE statement
    :type thelists: []
    """

    super().__init__(utterance, container)
    if thelists is None or len(thelists) == 0:
      self.operator = 'SLO'
      if random.choice([True, True, False]):
        self.winner = [utterance.frompower]
      else:
        self.winner = [random.choice(helpers.powerlist)]
    elif len(thelists) == 2:
      self.operator = thelists[0]
      self.winner = thelists[1]

  def formenglish(self): # type () -> str
    """
    Creates an English expression about the solo win in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    winnergloss = helpers.listOfPowers(self.winner, self.utterance.frompower, self.utterance.topowers)
    if self.container.operator == 'PRP':
      # (PRP (SLO
      if self.container.container is None:
        if winnergloss == 'me':
          self.english = 'I am ' + random.choice(['in a good position for a solo win', 'going for a solo win', 'not catchable - watch my solo win', 'just a matter of turns away from winning']) + '.'
        elif winnergloss == 'you':
          self.english = 'You are ' + random.choice(['in a good position for a solo win', 'going for a solo win', 'not catchable - go for a solo win', 'just a matter of turns away from winning']) + '.'
        else:
          self.english = winnergloss + ' is ' + random.choice(['in a good position for a solo win', 'going for a solo win', 'not catchable - going for a solo win', 'just a matter of turns away from winning']) + '.'
      # (YES (PRP (SLO
      elif self.container.container.operator == 'YES':
        self.english = 'I ' + random.choice(['agree to', 'concur with']) + ' the likelihood of a solo win by ' + winnergloss + '.'
      # (REJ (PRP (SLO
      elif self.container.container.operator == 'REJ':
        self.english = 'I ' + random.choice(['disagree with', 'reject']) + ' the likelihood of a solo win by ' + winnergloss + '.'
      # (CCL (PRP (SLO
      elif self.container.container.operator == 'CCL':
        self.english = 'I wish to ' + random.choice(['cancel', 'retract', 'take back']) + ' my proposal of a solo win by ' + winnergloss + '.'
      # (HUH (PRP (SLO
      elif self.container.container.operator == 'HUH':
        self.english = 'I do not understand your solo win proposal.'
    elif self.container.operator == 'NOT':
      if self.container.container.operator == 'PRP':
        # (PRP (NOT (SLO
        if self.container.container.container is None:
          if winnergloss == 'me':
            self.english = 'I am ' + random.choice(['not in a good position for a solo win', 'not going for a solo win', 'not uncatchable - no solo win yet', 'still a ways from winning']) + '.'
          elif winnergloss == 'you':
            self.english = 'You are ' + random.choice(['not in a good position for a solo win', 'not going for a solo win', 'not uncatchable - no solo win yet', 'still a ways from winning']) + '.'
          else:
            self.english = winnergloss + ' is ' + random.choice(['not in a good position for a solo win', 'not going for a solo win', 'not uncatchable - no solo win yet', 'still a ways from winning']) + '.'
        # (YES (PRP (NOT (SLO
        elif self.container.container.container.operator == 'YES':
          if winnergloss == 'me':
            self.english = 'I agree I am ' + random.choice(['not in a good position for a solo win', 'not going for a solo win', 'not uncatchable - no solo win yet', 'still a ways from winning']) + '.'
          elif winnergloss == 'you':
            self.english = 'I agree you are ' + random.choice(['not in a good position for a solo win', 'not going for a solo win', 'not uncatchable - no solo win yet', 'still a ways from winning']) + '.'
          else:
            self.english = 'I agree ' + winnergloss + ' is ' + random.choice(['not in a good position for a solo win', 'not going for a solo win', 'not uncatchable - no solo win yet', 'still a ways from winning']) + '.'
        # (REJ (PRP (NOT (SLO
        elif self.container.container.container.operator == 'REJ':
          if winnergloss == 'me':
            self.english = 'I think I am ' + random.choice(['closer to a win than you think', 'going for a solo win anyway', 'nevertheless uncatchable', 'quite close to winning']) + '.'
          elif winnergloss == 'you':
            self.english = 'I think you are ' + random.choice(['closer to a win than you think', 'going for a solo win anyway', 'nevertheless uncatchable', 'quite close to winning']) + '.'
          else:
            self.english = 'I think ' + winnergloss + ' is ' + random.choice(['closer to a win than you think', 'going for a solo win anyway', 'nevertheless uncatchable', 'quite close to winning']) + '.'
        # (CCL (PRP (NOT (SLO
        elif self.container.container.container.operator == 'CCL':
          self.english = 'I wish to ' + random.choice(['cancel', 'retract', 'take back']) + ' my proposal that a solo win is not in the cards for ' + winnergloss + '.'
        # (HUH (PRP (NOT (SLO
        elif self.container.container.container.operator == 'HUH':
          self.english = 'I do not understand your proposal about a solo win.'
      elif self.container.container.operator == 'FCT':
        # (FCT (NOT (SLO
        if self.container.container.container is None:
          self.english = winnergloss + ' is not pursuing a solo win.'
        # (HUH (FCT (NOT (SLO
        elif self.container.container.container.operator == 'HUH':
          self.english = 'I do not understand your statement about a solo win.'
    elif self.container.operator == 'NAR':
      if self.container.container.operator == 'PRP':
        # (PRP (NAR (SLO
        if self.container.container.container is None:
          if winnergloss == 'me':
            self.english = 'I am ' + random.choice(['unsure about a solo win', 'on the fence about a solo win', 'not uncatchable - no solo win yet', 'still a ways from winning']) + '.'
          elif winnergloss == 'you':
            self.english = 'You are ' + random.choice(['unsure about a solo win', 'on the fence about a solo win', 'not uncatchable - no solo win yet', 'still a ways from winning']) + '.'
          else:
            self.english = winnergloss + ' is ' + random.choice(['unsure about a solo win', 'on the fence about a solo win', 'not uncatchable - no solo win yet', 'still a ways from winning']) + '.'
        # (YES (PRP (NAR (SLO
        elif self.container.container.container.operator == 'YES':
          if winnergloss == 'me':
            self.english = 'I agree I am ' + random.choice(['unsure about a solo win', 'on the fence about a solo win', 'not uncatchable - no solo win yet', 'still a ways from winning']) + '.'
          elif winnergloss == 'you':
            self.english = 'I agree you are ' + random.choice(['unsure about a solo win', 'on the fence about a solo win', 'not uncatchable - no solo win yet', 'still a ways from winning']) + '.'
          else:
            self.english = 'I agree ' + winnergloss + ' is ' + random.choice(['unsure about a solo win', 'on the fence about a solo win', 'not uncatchable - no solo win yet', 'still a ways from winning']) + '.'
        # (REJ (PRP (NAR (SLO
        elif self.container.container.container.operator == 'REJ':
          if winnergloss == 'me':
            self.english = 'I disagree - I am ' + random.choice(['pretty sure about a solo win', 'close to a solo win', 'uncatchable - solo win not far away', 'just a few moves from winning']) + '.'
          elif winnergloss == 'you':
            self.english = 'I disagree - you are ' + random.choice(['pretty sure about a solo win', 'close to a solo win', 'uncatchable - solo win not far away', 'just a few moves from winning']) + '.'
          else:
            self.english = 'I disagree - ' + winnergloss + ' is ' + random.choice(['pretty sure for a solo win', 'close to a solo win', 'uncatchable - solo win not far away', 'just a few moves from winning']) + '.'
        # (CCL (PRP (NAR (SLO
        elif self.container.container.container.operator == 'CCL':
          self.english = 'I wish to ' + random.choice(['cancel', 'retract', 'take back']) + ' my proposal that ' + \
                         winnergloss + ' is not clearly capable of a solo win.'
        # (HUH (PRP (NAR (SLO
        elif self.container.container.container.operator == 'HUH':
          self.english = 'I do not understand your proposal about a solo win.'
      elif self.container.container.operator == 'FCT':
        # (FCT (NAR (SLO
        if self.container.container.container is None:
          if winnergloss == 'me':
            self.english = 'It is unclear if I am ' + random.choice(['pretty sure for a solo win', 'close to a solo win', 'uncatchable', 'just a few moves from winning']) + '.'
          elif winnergloss == 'you':
            self.english = 'It is unlcear if you are ' + random.choice(['pretty sure for a solo win', 'close to a solo win', 'uncatchable', 'just a few moves from winning']) + '.'
          else:
            self.english = 'I it is unlcear if ' + winnergloss + ' is ' + random.choice(['pretty sure for a solo win', 'close to a solo win', 'uncatchable', 'just a few moves from winning']) + '.'
        # (HUH (FCT (NAR (SLO
        elif self.container.container.container.operator == 'HUH':
          self.english = 'I do not understand your statement about a solo win.'
    elif self.container.operator == 'FCT':
      # (FCT (SLO
      if self.container.container is None:
        if winnergloss == 'me':
          self.english = 'I am ' + random.choice(['pretty sure for a solo win', 'close to a solo win', 'uncatchable', 'just a few moves from winning']) + '.'
        elif winnergloss == 'you':
          self.english = 'You are ' + random.choice(['pretty sure for a solo win', 'close to a solo win', 'uncatchable', 'just a few moves from winning']) + '.'
        else:
          self.english = winnergloss + ' is ' + random.choice(['pretty sure for a solo win', 'close to a solo win', 'uncatchable', 'just a few moves from winning']) + '.'
      # (HUH (FCT (SLO
      elif self.container.container.operator == 'HUH':
        self.english = 'I do not understand your statement about a solo win.'
    else:
      self.english = self.formlistenglish()

    return self.english

  def formlistenglish(self): # type () -> str
    """
    Creates an English expression about the DMZ in the context of a sender, recipients and desired tone.

    :return: the simple English expression
    :rtype: str
    """

    self.simpleenglish = 'a solo win by ' + helpers.listOfPowers(self.winner, self.utterance.frompower, self.utterance.topowers)

    return self.simpleenglish

  def formclauseenglish(self):

    if self.container.operator == "NOT":
      self.simpleenglish = 'there will not be '
    else:
      self.simpleenglish = 'there will be '
    self.simpleenglish +=  'a solo win by ' + helpers.listOfPowers(self.winner, self.utterance.frompower, self.utterance.topowers)

    return self.simpleenglish

  def formDAIDE(self): # type () -> str
    """
    Create a DAIDE representation of this Message

    :return: the DAIDE message
    :rtype: str
    """

    return 'SLO (' + self.winner[0] + ')'

class PressAnd(PressMessage):
  """ The game-related content of a conjunction. """

  def __init__(self, utterance, container, thelists): # type: (PressUtterance, PressMessage, []) -> None
    """
    Initialize the message with an utterance

    :param utterance: the press utterance that this message is within the content for
    :type utterance: PressUtterance
    :param container: the press message that contains this one
    :type container: PressMessage
    :param thelists: the parsed, nested DAIDE statement
    :type thelists: []
    """

    super().__init__(utterance, container)
    self.conjuncts = []
    if thelists is None or len(thelists) == 0:
      self.operator = 'AND'
      for cconj in range(0, random.randint(2, 4)):
        conjword = random.choice(['PCE', 'ALY', 'DMZ', 'SLO', 'DRW', 'XDO', 'NOT', 'NAR'])
        self.conjuncts.append(randomFactory(utterance, self, conjword))
    elif len(thelists) > 1:
      self.operator = thelists[0]
      for cConj in range(1, len(thelists)):
        self.conjuncts.append(messageFactory(utterance, self, thelists[cConj]))

  def formenglish(self): # type () -> str
    """
    Creates an English expression about the conjunction in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    if self.container.operator == 'PRP':
      # (PRP (AND
      if self.container.container is None:
        self.english = 'I ' + random.choice(['propose', 'request', 'offer']) + \
                       ' all of the following: ' + self.formlistenglish()
      # (YES (PRP (AND
      elif self.container.container.operator == 'YES':
        self.english = 'I ' + random.choice(['agree to', 'concur with', 'will accept']) + ' all of the following: ' + self.formlistenglish()
      # (REJ (PRP (AND
      elif self.container.container.operator == 'REJ':
        self.english = 'I ' + random.choice(['reject', 'do not concur with', 'do not approve of', 'do not accept']) + \
                       ' all of the following: ' + self.formlistenglish()
      # (CCL (PRP (AND
      elif self.container.container.operator == 'CCL':
        self.english = 'I wish to ' + random.choice(['cancel', 'retract', 'take back']) + ' my proposal of the following: ' + self.formlistenglish()
      # (HUH (PRP (AND
      elif self.container.container.operator == 'HUH':
        self.english = 'I do not understand your list of proposals.'
    elif self.container.operator == 'NOT':
      if self.container.container.operator == 'PRP':
        # (PRP (NOT (AND
        if self.container.container.container is None:
          self.english = 'I do not ' + random.choice(['want', 'desire', 'support']) + ' the following: ' + self.formlistenglish()
        # (YES (PRP (NOT (AND
        elif self.container.container.container.operator == 'YES':
          self.english = 'I ' + random.choice(['agree', 'concur']) + ' that none of the following are desirable: ' + self.formlistenglish()
        # (REJ (PRP (NOT (AND
        elif self.container.container.container.operator == 'REJ':
          self.english = 'I ' + random.choice(['disagree', 'reject']) + ' that none of the following are desirable: ' + self.formlistenglish()
        # (CCL (PRP (NOT (AND
        elif self.container.container.container.operator == 'CCL':
          self.english = 'I wish to ' + random.choice(['cancel', 'retract', 'take back']) + ' my proposal rejecting the following: ' + self.formlistenglish()
        # (HUH (PRP (NOT (AND
        elif self.container.container.container.operator == 'HUH':
          self.english = 'I do not understand your list of proposals.'
      elif self.container.container.operator == 'FCT':
        # (FCT (NOT (AND
        if self.container.container.container is None:
          self.english = 'The following conditions are not true: ' + self.formlistenglish()
        # (HUH (FCT (NOT (AND
        elif self.container.container.container.operator == 'HUH':
          self.english = 'I do not understand your list of statements.'
    elif self.container.operator == 'NAR':
      if self.container.container.operator == 'PRP':
        # (PRP (NAR (AND
        if self.container.container.container is None:
          self.english = 'I ' + random.choice(['am ambivalent about', 'am unsure about', 'am not convinced of']) + ' the following: ' + self.formlistenglish()
        # (YES (PRP (NAR (AND
        elif self.container.container.container.operator == 'YES':
          self.english = 'I am also ' + random.choice(['ambivalent about', 'unsure about', 'not convinced of']) + ' the following: ' + self.formlistenglish()
        # (REJ (PRP (NAR (AND
        elif self.container.container.container.operator == 'REJ':
          self.english = 'No, I ' + random.choice(['reject', 'oppose']) + ' your ambivalence about: ' + self.formlistenglish()
        # (CCL (PRP (NAR (AND
        elif self.container.container.container.operator == 'CCL':
          self.english = 'I wish to ' + random.choice(['cancel', 'retract', 'take back']) + ' my ambivalence about the following: ' + self.formlistenglish()
        # (HUH (PRP (NAR (AND
        elif self.container.container.container.operator == 'HUH':
          self.english = 'I do not understand your list of proposals.'
      elif self.container.container.operator == 'FCT':
        # (FCT (NAR (AND
        if self.container.container.container is None:
          self.english = 'It is unclear if the following are true: ' + self.formlistenglish()
        # (HUH (FCT (NAR (AND
        elif self.container.container.container.operator == 'HUH':
          self.english = 'I do not understand your list of statements.'
    elif self.container.operator == 'FCT':
      # (FCT (AND
      if self.container.container is None:
        self.english = 'The following are all true: ' + self.formlistenglish()
      # (HUH (FCT (AND
      elif self.container.container.operator == 'HUH':
        self.english = 'I do not understand your list of statements.'
    else:
      self.english = self.formlistenglish()

    return self.english

  def formlistenglish(self): # type () -> str
    """
    Creates an English expression about the conjunction in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    self.simpleenglish = '<br><ul>'
    for curConj in self.conjuncts:
      self.simpleenglish += '<li>' + helpers.initcap(curConj.formlistenglish()) + '</li>'
    self.simpleenglish += '</ul>'

    return self.simpleenglish

  def formclauseenglish(self): # type: () -> str
    """
    Creates a simple English clause, without any context like proposals, negations, etc.
    Useful for conditional statements or other contexts in which simplicity is valued over flavor.

    :return: the simple English clause
    :rtype: str

    """

    self.simpleenglish = self.formlistenglish()

    return self.simpleenglish

  def formDAIDE(self): # type () -> str
    """
    Create a DAIDE representation of this Message

    :return: the DAIDE message
    :rtype: str
    """

    return 'AND ' + ' '.join(['(' + curconj.formDAIDE() + ')' for curconj in self.conjuncts])

class PressOr(PressMessage):
  """ The game-related content of a disjunction. """

  def __init__(self, utterance, container, thelists): # type: (PressUtterance, PressMessage, []) -> None
    """
    Initialize the message with an utterance

    :param utterance: the press utterance that this message is within the content for
    :type utterance: PressUtterance
    :param container: the press message that contains this one
    :type container: PressMessage
    :param thelists: the parsed, nested DAIDE statement
    :type thelists: []
    """

    super().__init__(utterance, container)
    self.disjuncts = []
    if thelists is None or len(thelists) == 0:
      self.operator = 'AND'
      for cdisj in range(0, random.randint(2, 4)):
        disjword = random.choice(['PCE', 'ALY', 'DMZ', 'SLO', 'DRW', 'XDO', 'NOT', 'NAR'])
        self.disjuncts.append(randomFactory(utterance, self, disjword))
    elif len(thelists) > 1:
      self.operator = thelists[0]
      for cDisj in range(1, len(thelists)):
        self.disjuncts.append(messageFactory(utterance, self, thelists[cDisj]))

  def formenglish(self): # type () -> str
    """
    Creates an English expression about the disjunction in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    if self.container.operator == 'PRP':
      # (PRP (ORR
      if self.container.container is None:
        self.english = 'I ' + random.choice(['propose', 'request', 'offer']) + \
                       ' that you choose one of the following options: ' + self.formlistenglish()
      # (YES (PRP (ORR
      elif self.container.container.operator == 'YES':
        self.english = 'I ' + random.choice(['agree to', 'concur with', 'will accept']) + ' one of the following: ' + self.formlistenglish()
      # (REJ (PRP (ORR
      elif self.container.container.operator == 'REJ':
        self.english = 'I ' + random.choice(['reject', 'do not concur with', 'do not approve of', 'do not accept']) + \
                       ' any of the following: ' + self.formlistenglish()
      # (CCL (PRP (ORR
      elif self.container.container.operator == 'CCL':
        self.english = 'I wish to ' + random.choice(['cancel', 'retract', 'take back']) + ' my proposal of a choice from the following: ' + self.formlistenglish()
      # (HUH (PRP (ORR
      elif self.container.container.operator == 'HUH':
        self.english = 'I do not understand your list of proposals.'
    elif self.container.operator == 'NOT':
      if self.container.container.operator == 'PRP':
        # (PRP (NOT (ORR
        if self.container.container.container is None:
          self.english = 'I do not ' + random.choice(['want', 'desire', 'support']) + ' any of the following: ' + self.formlistenglish()
        # (YES (PRP (NOT (ORR
        elif self.container.container.container.operator == 'YES':
          self.english = 'I ' + random.choice(['agree', 'concur']) + ' that none of the following are desirable: ' + self.formlistenglish()
        # (REJ (PRP (NOT (ORR
        elif self.container.container.container.operator == 'REJ':
          self.english = 'I ' + random.choice(['disagree', 'reject']) + ' that none of the following are desirable: ' + self.formlistenglish()
        # (CCL (PRP (NOT (ORR
        elif self.container.container.container.operator == 'CCL':
          self.english = 'I wish to ' + random.choice(['cancel', 'retract', 'take back']) + ' my proposal rejecting the following: ' + self.formlistenglish()
        # (HUH (PRP (NOT (ORR
        elif self.container.container.container.operator == 'HUH':
          self.english = 'I do not understand your list of proposals.'
      elif self.container.container.operator == 'FCT':
        # (FCT (NOT (ORR
        if self.container.container.container is None:
          self.english = 'One of the following conditions are not true: ' + self.formlistenglish()
        # (HUH (FCT (NOT (ORR
        elif self.container.container.container.operator == 'HUH':
          self.english = 'I do not understand your list of statements.'
    elif self.container.operator == 'NAR':
      if self.container.container.operator == 'PRP':
        # (PRP (NAR (ORR
        if self.container.container.container is None:
          self.english = 'I ' + random.choice(['am ambivalent about', 'am unsure about', 'am not convinced of']) + ' one of the following: ' + self.formlistenglish()
        # (YES (PRP (NAR (ORR
        elif self.container.container.container.operator == 'YES':
          self.english = 'I am also ' + random.choice(['ambivalent about', 'unsure about', 'not convinced of']) + ' one the following: ' + self.formlistenglish()
        # (REJ (PRP (NAR (ORR
        elif self.container.container.container.operator == 'REJ':
          self.english = 'No, I ' + random.choice(['reject', 'oppose']) + ' your ambivalence about any of the following: ' + self.formlistenglish()
        # (CCL (PRP (NAR (ORR
        elif self.container.container.container.operator == 'CCL':
          self.english = 'I wish to ' + random.choice(['cancel', 'retract', 'take back']) + ' my ambivalence about one of the following: ' + self.formlistenglish()
        # (HUH (PRP (NAR (ORR
        elif self.container.container.container.operator == 'HUH':
          self.english = 'I do not understand your list of proposals.'
      elif self.container.container.operator == 'FCT':
        # (FCT (NAR (ORR
        if self.container.container.container is None:
          self.english = 'It is unclear if each of the following are true: ' + self.formlistenglish()
        # (HUH (FCT (NAR (ORR
        elif self.container.container.container.operator == 'HUH':
          self.english = 'I do not understand your list of statements.'
    elif self.container.operator == 'FCT':
      # (FCT (ORR
      if self.container.container is None:
        self.english = 'One of the following is true: ' + self.formlistenglish()
      # (HUH (FCT (ORR
      elif self.container.container.operator == 'HUH':
        self.english = 'I do not understand your list of statements.'
    else:
      self.english = self.formlistenglish()

    return self.english

  def formlistenglish(self): # type () -> str
    """
    Creates an English expression about the disjunction in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    self.simpleenglish = '<br><ul>'
    for curDisj in self.disjuncts:
      self.simpleenglish += '<li>' + helpers.initcap(curDisj.formlistenglish()) + '</li>'
    self.simpleenglish += '</ul>'

    return self.simpleenglish

  def formclauseenglish(self): # type: () -> str
    """
    Creates a simple English clause, without any context like proposals, negations, etc.
    Useful for conditional statements or other contexts in which simplicity is valued over flavor.

    :return: the simple English clause
    :rtype: str

    """

    self.simpleenglish = self.formlistenglish()

    return self.simpleenglish

  def formDAIDE(self): # type () -> str
    """
    Create a DAIDE representation of this Message

    :return: the DAIDE message
    :rtype: str
    """

    return 'ORR ' + ' '.join(['(' + curdisj.formDAIDE() + ')' for curdisj in self.disjuncts])

class PressIf(PressMessage):
  """ The game-related content of a conditional. """

  def __init__(self, utterance, container, thelists): # type: (PressUtterance, PressMessage, []) -> None
    """
    Initialize the message with an utterance

    :param utterance: the press utterance that this message is within the content for
    :type utterance: PressUtterance
    :param container: the press message that contains this one
    :type container: PressMessage
    :param thelists: the parsed, nested DAIDE statement
    :type thelists: []
    """

    super().__init__(utterance, container)
    if thelists is None or len(thelists) == 0:
      self.operator = 'AND'
      anteword = random.choice(['PCE', 'ALY', 'DMZ', 'SLO', 'DRW', 'XDO', 'NOT', 'NAR'])
      self.antecedent = randomFactory(utterance, self, anteword)
      consword = random.choice(['PCE', 'ALY', 'DMZ', 'SLO', 'DRW', 'XDO', 'NOT', 'NAR'])
      self.consequent = randomFactory(utterance, self, consword)
      self.alternative = None
      if random.choice([True, False]):
        altword = random.choice(['PCE', 'ALY', 'DMZ', 'SLO', 'DRW', 'XDO', 'NOT', 'NAR'])
        self.alternative = randomFactory(utterance, self, altword)
    elif len(thelists) == 3:
      self.operator = thelists[0]
      self.antecedent = messageFactory(utterance, self, thelists[1])
      self.consequent = messageFactory(utterance, self, thelists[2])
      self.alternative = None
    elif len(thelists) == 5:
      self.operator = thelists[0]
      self.antecedent = messageFactory(utterance, self, thelists[1])
      self.consequent = messageFactory(utterance, self, thelists[2])
      self.alternative = messageFactory(utterance, self, thelists[4])

  def formenglish(self): # type () -> str
    """
    Creates an English expression about the conditional in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    if self.container.operator == 'PRP':
      # (PRP (IFF
      if self.container.container is None:
        if random.choice([True, False]):
          self.english = 'Here\'s my ' + random.choice(['proposal', 'proposed deal', 'offer']) + \
                         ': if ' + self.antecedent.formclauseenglish() + ', then ' + self.consequent.formclauseenglish() + '.'
        else:
          self.english = 'Would you consider ' + self.consequent.formclauseenglish() + ' if ' + self.antecedent.formclauseenglish() + '?'
        if self.alternative is not None:
          self.english += ' If not this, then perhaps ' + self.antecedent.formclauseenglish() + '?'
      # (YES (PRP (IFF
      elif self.container.container.operator == 'YES':
        self.english = 'I ' + random.choice(['agree to', 'concur with', 'will accept']) + ' ' + self.antecedent.formclauseenglish() + \
                       ' and when it\'s done, I will execute the following: ' + self.consequent.formclauseenglish()
      # (REJ (PRP (IFF
      elif self.container.container.operator == 'REJ':
        self.english = 'I ' + random.choice(['reject', 'do not concur with', 'do not approve of', 'do not accept']) + \
                       ' the condition that ' + self.antecedent.formclauseenglish() + ' should lead to ' + self.consequent.formclauseenglish()
      # (CCL (PRP (IFF
      elif self.container.container.operator == 'CCL':
        self.english = 'I wish to ' + random.choice(['cancel', 'retract', 'take back']) + ' my proposal that if ' + \
                       self.antecedent.formclauseenglish() + ' then ' + self.consequent.formclauseenglish()
        if self.alternative is not None:
          self.english += ' otherwise ' + self.alternative.formclauseenglish()
      # (HUH (PRP (IFF
      elif self.container.container.operator == 'HUH':
        self.english = 'I do not understand your quid pro quo.'
    elif self.container.operator == 'NOT':
      if self.container.container.operator == 'PRP':
        # (PRP (NOT (IFF
        if self.container.container.container is None:
          self.english = 'I do not ' + random.choice(['want', 'desire', 'support']) + ' the following trade: ' + \
                         self.antecedent.formclauseenglish() + ' for ' + self.consequent.formclauseenglish()
        # (YES (PRP (NOT (IFF
        elif self.container.container.container.operator == 'YES':
          self.english = 'I ' + random.choice(['agree', 'concur']) + ' that the following trade is not desirable: ' + \
                         self.antecedent.formclauseenglish() + ' for ' + self.consequent.formclauseenglish()
        # (REJ (PRP (NOT (IFF
        elif self.container.container.container.operator == 'REJ':
          self.english = 'I still want ' + self.consequent.formclauseenglish() + ' whether or not you want ' + self.antecedent.formclauseenglish()
        # (CCL (PRP (NOT (IFF
        elif self.container.container.container.operator == 'CCL':
          self.english = 'I wish to ' + random.choice(['cancel', 'retract', 'take back']) + ' my proposal rejecting ' + \
                         self.antecedent.formclauseenglish() + ' for ' + self.consequent.formclauseenglish()
        # (HUH (PRP (NOT (IFF
        elif self.container.container.container.operator == 'HUH':
          self.english = 'I do not understand your trade offer.'
      elif self.container.container.operator == 'FCT':
        # (FCT (NOT (IFF
        if self.container.container.container is None:
          self.english = 'It is not the case that if ' + self.antecedent.formclauseenglish() + ', then ' + self.consequent.formclauseenglish()
        # (HUH (FCT (NOT (IFF
        elif self.container.container.container.operator == 'HUH':
          self.english = 'I do not understand your statement about the trade.'
    elif self.container.operator == 'NAR':
      if self.container.container.operator == 'PRP':
        # (PRP (NAR (IFF
        if self.container.container.container is None:
          self.english = 'If ' + self.antecedent.formclauseenglish() + ', then maybe ' + self.consequent.formclauseenglish()
        # (YES (PRP (NAR (IFF
        elif self.container.container.container.operator == 'YES':
          self.english = 'I agree, it may be that if ' + self.antecedent.formclauseenglish() + ', then maybe ' + self.consequent.formclauseenglish()
        # (REJ (PRP (NAR (IFF
        elif self.container.container.container.operator == 'REJ':
          self.english = 'I disagree that if ' + self.antecedent.formclauseenglish() + ', then maybe ' + self.consequent.formclauseenglish()
        # (CCL (PRP (NAR (IFF
        elif self.container.container.container.operator == 'CCL':
          self.english = 'I wish to ' + random.choice(['cancel', 'retract', 'take back']) + ' my proposal of ' + \
                         self.antecedent.formclauseenglish() + ' for ' + self.consequent.formclauseenglish()
        # (HUH (PRP (NAR (IFF
        elif self.container.container.container.operator == 'HUH':
          self.english = 'I do not understand your proposal of a quid pro quo.'
      elif self.container.container.operator == 'FCT':
        # (FCT (NAR (IFF
        if self.container.container.container is None:
          self.english = 'It is unclear that if ' + self.antecedent.formclauseenglish() + ', then ' + self.consequent.formclauseenglish()
        # (HUH (FCT (NAR (IFF
        elif self.container.container.container.operator == 'HUH':
          self.english = 'I do not understand your statement about a trade.'
    elif self.container.operator == 'FCT':
      # (FCT (IFF
      if self.container.container is None:
        self.english = 'I believe that if ' + self.antecedent.formclauseenglish() + ', then ' + self.consequent.formclauseenglish()
        if self.alternative is not None:
          self.english += ' If not this, then ' + self.antecedent.formclauseenglish() + '.'
      # (HUH (FCT (IFF
      elif self.container.container.operator == 'HUH':
        self.english = 'I do not understand your statement about a trade.'
    else:
      self.english = self.formclauseenglish()

    return self.english

  def formlistenglish(self): # type () -> str
    """
    Creates an English expression about the conditional in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    self.simpleenglish = 'if ' + self.antecedent.formlistenglish() + ', then ' + self.consequent.formlistenglish()
    if self.alternative is not None:
      self.simpleenglish += ', otherwise ' + self.alternative.formlistenglish()

    return self.simpleenglish

  def formclauseenglish(self): # type: () -> str
    """
    Creates a simple English clause, without any context like proposals, negations, etc.
    Useful for conditional statements or other contexts in which simplicity is valued over flavor.

    :return: the simple English clause
    :rtype: str

    """

    self.simpleenglish = self.formlistenglish()

    return self.simpleenglish

  def formDAIDE(self): # type () -> str
    """
    Create a DAIDE representation of this Message

    :return: the DAIDE message
    :rtype: str
    """

    retval = 'IFF ' + '(' + self.antecedent.formDAIDE() + ') (' + self.consequent.formDAIDE() + ')'
    if self.alternative is not None:
      retval += ' ELS (' +  self.alternative.formDAIDE() + ')'

    return retval

class PressNot(PressMessage):
  """ The game-related content of a negation. """

  def __init__(self, utterance, container, thelists): # type: (PressUtterance, PressMessage, []) -> None
    """
    Initialize the message with an utterance

    :param utterance: the press utterance that this message is within the content for
    :type utterance: PressUtterance
    :param container: the press message that contains this one
    :type container: PressMessage
    :param thelists: the parsed, nested DAIDE statement
    :type thelists: []
    """

    super().__init__(utterance, container)
    self.proposition = PressMessage(utterance, self)
    if thelists is None or len(thelists) == 0:
      self.operator = 'NOT'
      propword = random.choice(['PCE', 'ALY', 'DMZ', 'SLO', 'DRW', 'XDO'])
      self.proposition = randomFactory(utterance, self, propword)
    elif len(thelists) == 2:
      self.operator = thelists[0]
      self.proposition = messageFactory(utterance, self, thelists[1])

  def formenglish(self): # type () -> str
    """
    Creates an English expression about the negation in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    self.english = self.proposition.formenglish()

    return self.english

  def formlistenglish(self): # type () -> str
    """
    Creates an English expression about the negation in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    self.simpleenglish = self.proposition.formclauseenglish() + '.' #+ ' is not happening'

    return self.simpleenglish

  def formclauseenglish(self):  # type () -> str
    """
    Creates an English expression about the negation in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    self.simpleenglish = self.proposition.formclauseenglish()

    return self.simpleenglish

  def formDAIDE(self): # type () -> str
    """
    Create a DAIDE representation of this Message

    :return: the DAIDE message
    :rtype: str
    """

    return 'NOT ' + '(' + self.proposition.formDAIDE() + ')'

class PressNar(PressMessage):
  """ The game-related content of missing evidence. """

  def __init__(self, utterance, container, thelists): # type: (PressUtterance, PressMessage, []) -> None
    """
    Initialize the message with an utterance

    :param utterance: the press utterance that this message is within the content for
    :type utterance: PressUtterance
    :param container: the press message that contains this one
    :type container: PressMessage
    :param thelists: the parsed, nested DAIDE statement
    :type thelists: []
    """

    super().__init__(utterance, container)
    self.proposition = PressMessage(utterance, self)
    if thelists is None or len(thelists) == 0:
      self.operator = 'NAR'
      propword = random.choice(['PCE', 'ALY', 'DMZ', 'SLO', 'DRW', 'XDO'])
      self.proposition = randomFactory(utterance, self, propword)
    elif len(thelists) == 2:
      self.operator = thelists[0]
      self.proposition = messageFactory(utterance, self, thelists[1])

  def formenglish(self): # type () -> str
    """
    Creates an English expression about the missing evidence in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    self.english = self.proposition.formenglish()

    return self.english

  def formlistenglish(self): # type () -> str
    """
    Creates an English expression about the missing evidence in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    self.simpleenglish = 'it is uncertain that ' + self.proposition.formlistenglish()

    return self.simpleenglish

  def formclauseenglish(self): # type () -> str
    """
    Creates an English expression about the missing evidence in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    self.simpleenglish = 'it is uncertain that ' + self.proposition.formclauseenglish()

    return self.simpleenglish

  def formDAIDE(self): # type () -> str
    """
    Create a DAIDE representation of this Message

    :return: the DAIDE message
    :rtype: str
    """

    return 'NAR ' + '(' + self.proposition.formDAIDE() + ')'

class PressMoveExecute(PressMessage):
  """ The game-related content of an executable move. """

  def __init__(self, utterance, container, thelists): # type: (PressUtterance, PressMessage, []) -> None
    """
    Initialize the message with an utterance

    :param utterance: the press utterance that this message is within the content for
    :type utterance: PressUtterance
    :param container: the press message that contains this one
    :type container: PressMessage
    :param thelists: the parsed, nested DAIDE statement
    :type thelists: []
    """

    super().__init__(utterance, container)
    if thelists is None or len(thelists) == 0:
      self.operator = 'XDO'
      detword = random.choice(['HLD', 'MTO', 'SUP', 'SUPMTO', 'CVYCTO', 'CVYVIA', 'RTO', 'DSB', 'BLD', 'REM', 'WVE'])
      self.details = randomFactory(utterance, self, detword)
    elif len(thelists) == 2:
      self.operator = thelists[0]
      self.details = messageFactory(utterance, self, thelists[1])

  def formenglish(self): # type () -> str
    """
    Creates an English expression about the executable move in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    if self.container.operator == 'PRP':
      # (PRP (XDO
      if self.container.container is None:
        self.english = 'I ' + random.choice(['propose', 'request', 'demand']) + ' this move: ' + self.details.formlistenglish()
      # (YES (PRP (XDO
      elif self.container.container.operator == 'YES':
        self.english = 'I ' + random.choice(['agree to', 'concur with', 'accept']) + ' the move: ' + self.details.formlistenglish()
      # (REJ (PRP (XDO
      elif self.container.container.operator == 'REJ':
        self.english = 'I ' + random.choice(['reject', 'do not concur with', 'do not approve of']) + ' the move: ' + self.details.formlistenglish()
      # (CCL (PRP (XDO
      elif self.container.container.operator == 'CCL':
        self.english = 'I wish to ' + random.choice(['cancel', 'retract', 'take back']) + ' my proposal of the move: ' + self.details.formlistenglish()
      # (HUH (PRP (XDO
      elif self.container.container.operator == 'HUH':
        self.english = 'I do not understand your move proposal.'
    elif self.container.operator == 'NOT':
      if self.container.container.operator == 'PRP':
        # (PRP (NOT (XDO
        if self.container.container.container is None:
          self.english = 'I do not want the following move to happen: ' + self.details.formlistenglish()
        # (YES (PRP (NOT (XDO
        elif self.container.container.container.operator == 'YES':
          self.english = 'I ' + random.choice(['agree', 'concur']) + ' that this move will not happen: ' + self.details.formlistenglish()
        # (REJ (PRP (NOT (XDO
        elif self.container.container.container.operator == 'REJ':
          self.english = 'I do not promise that I won\'t make this move: ' + self.details.formlistenglish()
        # (CCL (PRP (NOT (XDO
        elif self.container.container.container.operator == 'CCL':
          self.english = 'I wish to ' + random.choice(['cancel', 'retract', 'take back']) + ' my objection to the move: ' + self.details.formlistenglish()
        # (HUH (PRP (NOT (XDO
        elif self.container.container.container.operator == 'HUH':
          self.english = 'I do not understand your proposal about a move.'
      elif self.container.container.operator == 'FCT':
        # (FCT (NOT (XDO
        if self.container.container.container is None:
          self.english = 'It is unlikely that this move will occur: ' + self.details.formlistenglish()
        # (HUH (FCT (NOT (XDO
        elif self.container.container.container.operator == 'HUH':
          self.english = 'I do not understand your statement about a move.'
    elif self.container.operator == 'NAR':
      if self.container.container.operator == 'PRP':
        # (PRP (NAR (XDO
        if self.container.container.container is None:
          self.english = 'I am not sure about the move: ' + self.details.formlistenglish()
        # (YES (PRP (NAR (XDO
        elif self.container.container.container.operator == 'YES':
          self.english = 'I ' + random.choice(['agree', 'concur']) + ' that we should be hesitant about the move: ' + self.details.formlistenglish()
        # (REJ (PRP (NAR (XDO
        elif self.container.container.container.operator == 'REJ':
          self.english = 'No, I ' + random.choice(['think', 'believe']) + ' that we should be sure about the move: ' + self.details.formlistenglish()
        # (CCL (PRP (NAR (XDO
        elif self.container.container.container.operator == 'CCL':
          self.english = 'I wish to ' + random.choice(['cancel', 'retract', 'take back']) + ' my hesitance about the move: ' + self.details.formlistenglish()
        # (HUH (PRP (NAR (XDO
        elif self.container.container.container.operator == 'HUH':
          self.english = 'I do not understand your proposal about a move.'
      elif self.container.container.operator == 'FCT':
        # (FCT (NAR (XDO
        if self.container.container.container is None:
          self.english = 'It is unclear if this move will happen: ' + self.details.formlistenglish()
        # (HUH (FCT (NAR (XDO
        elif self.container.container.container.operator == 'HUH':
          self.english = 'I do not understand your statement about a move.'
    elif self.container.operator == 'FCT':
      # (FCT (XDO
      if self.container.container is None:
        self.english = 'This move will happen: ' + self.details.formlistenglish()
      # (HUH (FCT (XDO
      elif self.container.container.operator == 'HUH':
        self.english = 'I do not understand your statement about a move.'
    else:
      self.english = self.formlistenglish()

    return self.english

  def formlistenglish(self): # type () -> str
    """
    Creates an English expression about the missing evidence in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    self.simpleenglish = self.details.formlistenglish()

    return self.simpleenglish

  def formclauseenglish(self): # type () -> str
    """
    Creates an English expression about the missing evidence in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    self.simpleenglish = self.details.formclauseenglish()

    return self.simpleenglish

  def formDAIDE(self): # type () -> str
    """
    Create a DAIDE representation of this Message

    :return: the DAIDE message
    :rtype: str
    """

    return 'XDO ' + '(' + self.details.formDAIDE() + ')'

class PressHold(PressMessage):
  """ The game-related content of a hold. """

  def __init__(self, utterance, container, thelists): # type: (PressUtterance, PressMessage, []) -> None
    """
    Initialize the message with an utterance

    :param utterance: the press utterance that this message is within the content for
    :type utterance: PressUtterance
    :param container: the press message that contains this one
    :type container: PressMessage
    :param thelists: the parsed, nested DAIDE statement
    :type thelists: []
    """

    super().__init__(utterance, container)
    if thelists is None or len(thelists) == 0:
      self.operator = 'HLD'
      if random.choice([True, True, False]):
        if random.choice([True, False]):
          self.unit = [utterance.frompower, random.choice(helpers.unitlist), random.choice(helpers.provincelist)]
        else:
          self.unit = [random.choice(utterance.topowers), random.choice(helpers.unitlist), random.choice(helpers.provincelist)]
      else:
        self.unit = [random.choice(helpers.powerlist), random.choice(helpers.unitlist), random.choice(helpers.provincelist)]
    elif len(thelists) == 2:
      self.operator = thelists[1]
      self.unit = thelists[0]

  def formenglish(self): # type () -> str
    """
    Creates an English expression about the hold in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    self.english = self.formlistenglish()
    return self.english

  def formlistenglish(self): # type () -> str
    """
    Creates an English expression about the hold in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    self.simpleenglish = helpers.powerdict[self.unit[0]]['Objective'] + \
                         ' holds their ' + \
                         helpers.unitdict[self.unit[1]]['Objective'] + \
                         ' in ' + \
                         helpers.provincedict[self.unit[2]]['Objective'] + '.'

    if 'Expert' in self.utterance.tones:
      unittype = 'A'
      if self.unit[1] == 'FLT':
        unittype = 'F'
      self.simpleenglish += ' (' + unittype + ' ' + self.unit[2] + ' H).'

    return self.simpleenglish

  def formclauseenglish(self): # type () -> str
    """
    Creates an English expression about the hold in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """
    if self.container.container.operator == "NOT":
      self.simpleenglish = helpers.powerdict[self.unit[0]]['Objective'] + \
                           ' is free to move their ' + \
                           helpers.unitdict[self.unit[1]]['Objective'] + \
                           ' in ' + \
                           helpers.provincedict[self.unit[2]]['Objective'] + ''
    else:
      self.simpleenglish = helpers.powerdict[self.unit[0]]['Objective'] + \
                         ' holds their ' + \
                         helpers.unitdict[self.unit[1]]['Objective'] + \
                         ' in ' + \
                         helpers.provincedict[self.unit[2]]['Objective'] + ''

    if 'Expert' in self.utterance.tones:
      unittype = 'A'
      if self.unit[1] == 'FLT':
        unittype = 'F'
      self.simpleenglish += ' (' + unittype + ' ' + self.unit[2] + ' H)'

    return self.simpleenglish

  def formDAIDE(self): # type () -> str
    """
    Create a DAIDE representation of this Message

    :return: the DAIDE message
    :rtype: str
    """

    return '(' + ' '.join(self.unit) + ') HLD'

class PressMoveInto(PressMessage):
  """ The game-related content of a move. """

  def __init__(self, utterance, container, thelists): # type: (PressUtterance, PressMessage, []) -> None
    """
    Initialize the message with an utterance

    :param utterance: the press utterance that this message is within the content for
    :type utterance: PressUtterance
    :param container: the press message that contains this one
    :type container: PressMessage
    :param thelists: the parsed, nested DAIDE statement
    :type thelists: []
    """

    super().__init__(utterance, container)
    if thelists is None or len(thelists) == 0:
      self.operator = 'MTO'
      if random.choice([True, True, False]):
        if random.choice([True, False]):
          self.unit = [utterance.frompower, random.choice(helpers.unitlist), random.choice(helpers.provincelist)]
        else:
          self.unit = [random.choice(utterance.topowers), random.choice(helpers.unitlist), random.choice(helpers.provincelist)]
      else:
        self.unit = [random.choice(helpers.powerlist), random.choice(helpers.unitlist), random.choice(helpers.provincelist)]
      provlist = [curprov for curprov in helpers.provincelist if curprov != self.unit[2]]
      self.province = random.choice(provlist)
    elif len(thelists) == 3:
      self.operator = thelists[1]
      self.unit = thelists[0]
      self.province = thelists[2]

  def formenglish(self): # type () -> str
    """
    Creates an English expression about the move in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    self.english = self.formlistenglish()
    return self.english

  def formlistenglish(self): # type () -> str
    """
    Creates an English expression about the move in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    if len(self.unit) < 3:
      self.simpleenglish = 'Ahem.'
      return self.simpleenglish

    self.simpleenglish = helpers.powerdict[self.unit[0]]['Objective'] + \
                         ' moves their ' + \
                         helpers.unitdict[self.unit[1]]['Objective'] + \
                         ' from ' + \
                         helpers.provincedict[self.unit[2]]['Objective'] + \
                         ' to ' + \
                         helpers.provincedict[self.province]['Objective'] + '.'

    if 'Expert' in self.utterance.tones:
      unittype = 'A'
      if self.unit[1] == 'FLT':
        unittype = 'F'
      self.simpleenglish += ' (' + unittype + ' ' + self.unit[2] + ' -> ' + self.province + ').'

    return self.simpleenglish

  def formclauseenglish(self): # type () -> str
    """
    Creates an English expression about the move in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    if len(self.unit) < 3:
      self.simpleenglish = 'Ahem.'
      return self.simpleenglish


    if self.container.container.operator== "NOT":
      self.simpleenglish = helpers.powerdict[self.unit[0]]['Objective'] + \
                         ' does not move their ' + \
                         helpers.unitdict[self.unit[1]]['Objective'] + \
                         ' from ' + \
                         helpers.provincedict[self.unit[2]]['Objective'] + \
                         ' to ' + \
                         helpers.provincedict[self.province]['Objective'] + ''
    else:
      self.simpleenglish = helpers.powerdict[self.unit[0]]['Objective'] + \
                           ' moves their ' + \
                           helpers.unitdict[self.unit[1]]['Objective'] + \
                           ' from ' + \
                           helpers.provincedict[self.unit[2]]['Objective'] + \
                           ' to ' + \
                           helpers.provincedict[self.province]['Objective'] + ''

    if 'Expert' in self.utterance.tones:
      unittype = 'A'
      if self.unit[1] == 'FLT':
        unittype = 'F'
      self.simpleenglish += ' (' + unittype + ' ' + self.unit[2] + ' -> ' + self.province + ') '

    return self.simpleenglish

  def formDAIDE(self): # type () -> str
    """
    Create a DAIDE representation of this Message

    :return: the DAIDE message
    :rtype: str
    """

    return '(' + ' '.join(self.unit) + ') MTO ' + self.province

class PressSupportHold(PressMessage):
  """ The game-related content of a hold support. """

  def __init__(self, utterance, container, thelists): # type: (PressUtterance, PressMessage, []) -> None
    """
    Initialize the message with an utterance

    :param utterance: the press utterance that this message is within the content for
    :type utterance: PressUtterance
    :param container: the press message that contains this one
    :type container: PressMessage
    :param thelists: the parsed, nested DAIDE statement
    :type thelists: []
    """

    super().__init__(utterance, container)
    if thelists is None or len(thelists) == 0:
      self.operator = 'SUP'
      if random.choice([True, True, False]):
        if random.choice([True, False]):
          self.supporter = [utterance.frompower, random.choice(helpers.unitlist), random.choice(helpers.provincelist)]
        else:
          self.supporter = [random.choice(utterance.topowers), random.choice(helpers.unitlist), random.choice(helpers.provincelist)]
      else:
        self.supporter = [random.choice(helpers.powerlist), random.choice(helpers.unitlist), random.choice(helpers.provincelist)]
      if random.choice([True, True, False]):
        if random.choice([True, False]):
          self.supported = [utterance.frompower, random.choice(helpers.unitlist), random.choice(helpers.provincelist)]
        else:
          self.supported = [random.choice(utterance.topowers), random.choice(helpers.unitlist), random.choice(helpers.provincelist)]
      else:
        self.supported = [random.choice(helpers.powerlist), random.choice(helpers.unitlist), random.choice(helpers.provincelist)]
    elif len(thelists) == 3:
      self.operator = thelists[1]
      self.supporter = thelists[0]
      self.supported = thelists[2]

  def formenglish(self): # type () -> str
    """
    Creates an English expression about the hold support in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    self.english = self.formlistenglish()
    return self.english

  def formlistenglish(self): # type () -> str
    """
    Creates an English expression about the hold support in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    self.simpleenglish = helpers.powerdict[self.supporter[0]]['Objective'] + \
                         ' provides support with their ' + \
                         helpers.unitdict[self.supporter[1]]['Objective'] + \
                         ' in ' + \
                         helpers.provincedict[self.supporter[2]]['Objective'] + \
                         ' for ' + \
                         helpers.powerdict[self.supported[0]]['Objective'] + \
                         ' to hold their ' + \
                         helpers.unitdict[self.supported[1]]['Objective'] + \
                         ' in ' + \
                         helpers.provincedict[self.supported[2]]['Objective'] + '.'

    if 'Expert' in self.utterance.tones:
      supportertype = 'A'
      if self.supporter[1] == 'FLT':
        supportertype = 'F'
      supportedtype = 'A'
      if self.supported[1] == 'FLT':
        supportedtype = 'F'
      self.simpleenglish += ' (' + supportertype + ' ' + self.supporter[2] + ' S ' + supportedtype + ' ' + self.supported[2] + ' H).'

    return self.simpleenglish

  def formclauseenglish(self): # type () -> str
    """
    Creates an English expression about the hold support in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """
    if self.container.container.operator== "NOT":
      self.simpleenglish = helpers.powerdict[self.supporter[0]]['Objective'] + \
                           ' does not provide support with their ' + \
                           helpers.unitdict[self.supporter[1]]['Objective'] + \
                           ' in ' + \
                           helpers.provincedict[self.supporter[2]]['Objective'] + \
                           ' for ' + \
                           helpers.powerdict[self.supported[0]]['Objective'] + \
                           ' to hold their ' + \
                           helpers.unitdict[self.supported[1]]['Objective'] + \
                           ' in ' + \
                           helpers.provincedict[self.supported[2]]['Objective'] + ''
    else:
      self.simpleenglish = helpers.powerdict[self.supporter[0]]['Objective'] + \
                         ' provides support with their ' + \
                         helpers.unitdict[self.supporter[1]]['Objective'] + \
                         ' in ' + \
                         helpers.provincedict[self.supporter[2]]['Objective'] + \
                         ' for ' + \
                         helpers.powerdict[self.supported[0]]['Objective'] + \
                         ' to hold their ' + \
                         helpers.unitdict[self.supported[1]]['Objective'] + \
                         ' in ' + \
                         helpers.provincedict[self.supported[2]]['Objective'] + ''

    if 'Expert' in self.utterance.tones:
      supportertype = 'A'
      if self.supporter[1] == 'FLT':
        supportertype = 'F'
      supportedtype = 'A'
      if self.supported[1] == 'FLT':
        supportedtype = 'F'
      self.simpleenglish += ' (' + supportertype + ' ' + self.supporter[2] + ' S ' + supportedtype + ' ' + self.supported[2] + ' H) '

    return self.simpleenglish

  def formDAIDE(self): # type () -> str
    """
    Create a DAIDE representation of this Message

    :return: the DAIDE message
    :rtype: str
    """

    return '(' + ' '.join(self.supporter) + ') SUP (' + ' '.join(self.supported) + ')'

class PressSupportMove(PressMessage):
  """ The game-related content of a move support. """

  def __init__(self, utterance, container, thelists): # type: (PressUtterance, PressMessage, []) -> None
    """
    Initialize the message with an utterance

    :param utterance: the press utterance that this message is within the content for
    :type utterance: PressUtterance
    :param container: the press message that contains this one
    :type container: PressMessage
    :param thelists: the parsed, nested DAIDE statement
    :type thelists: []
    """

    super().__init__(utterance, container)
    if thelists is None or len(thelists) == 0:
      self.operator = 'SUP'
      if random.choice([True, True, False]):
        if random.choice([True, False]):
          self.supporter = [utterance.frompower, random.choice(helpers.unitlist), random.choice(helpers.provincelist)]
        else:
          self.supporter = [random.choice(utterance.topowers), random.choice(helpers.unitlist), random.choice(helpers.provincelist)]
      else:
        self.supporter = [random.choice(helpers.powerlist), random.choice(helpers.unitlist), random.choice(helpers.provincelist)]
      if random.choice([True, True, False]):
        if random.choice([True, False]):
          self.supported = [utterance.frompower, random.choice(helpers.unitlist), random.choice(helpers.provincelist)]
        else:
          self.supported = [random.choice(utterance.topowers), random.choice(helpers.unitlist), random.choice(helpers.provincelist)]
      else:
        self.supported = [random.choice(helpers.powerlist), random.choice(helpers.unitlist), random.choice(helpers.provincelist)]
      provlist = [curprov for curprov in helpers.provincelist if curprov != self.supporter[2] and curprov != self.supported[2]]
      self.province = random.choice(provlist)
    elif len(thelists) == 5:
      self.operator = thelists[1]
      self.supporter = thelists[0]
      self.supported = thelists[2]
      self.province = thelists[4]

  def formenglish(self): # type () -> str
    """
    Creates an English expression about the move support in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    self.english = self.formlistenglish()
    return self.english

  def formlistenglish(self): # type () -> str
    """
    Creates an English expression about the move support in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    if len(self.supporter) != 3 or len(self.supported) != 3:
      self.simpleenglish = 'Ahem.'
      return self.simpleenglish

    self.simpleenglish = helpers.powerdict[self.supporter[0]]['Objective'] + \
                         ' provides support with their ' + \
                         helpers.unitdict[self.supporter[1]]['Objective'] + \
                         ' in ' + \
                         helpers.provincedict[self.supporter[2]]['Objective'] + \
                         ' so ' + \
                         helpers.powerdict[self.supported[0]]['Objective'] + \
                         ' can move their ' + \
                         helpers.unitdict[self.supported[1]]['Objective'] + \
                         ' from ' + \
                         helpers.provincedict[self.supported[2]]['Objective'] + \
                         ' into ' + \
                         helpers.provincedict[self.province]['Objective'] + '.'

    if 'Expert' in self.utterance.tones:
      supportertype = 'A'
      if self.supporter[1] == 'FLT':
        supportertype = 'F'
      supportedtype = 'A'
      if self.supported[1] == 'FLT':
        supportedtype = 'F'
      self.simpleenglish += ' (' + supportertype + ' ' + self.supporter[2] + ' S ' + supportedtype + ' ' + self.supported[2] + ' -> ' + self.province + ').'

    return self.simpleenglish


  def formclauseenglish(self): # type () -> str
    """
    Creates an English expression about the move support in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    if len(self.supporter) != 3 or len(self.supported) != 3:
      self.simpleenglish = 'Ahem.'
      return self.simpleenglish


    if self.container.container.operator== "NOT":
      self.simpleenglish = helpers.powerdict[self.supporter[0]]['Objective'] + \
                         ' does not provide support with their ' + \
                         helpers.unitdict[self.supporter[1]]['Objective'] + \
                         ' in ' + \
                         helpers.provincedict[self.supporter[2]]['Objective'] + \
                         ' so ' + \
                         helpers.powerdict[self.supported[0]]['Objective'] + \
                         ' can move their ' + \
                         helpers.unitdict[self.supported[1]]['Objective'] + \
                         ' from ' + \
                         helpers.provincedict[self.supported[2]]['Objective'] + \
                         ' into ' + \
                         helpers.provincedict[self.province]['Objective'] + ''
    else:
      self.simpleenglish = helpers.powerdict[self.supporter[0]]['Objective'] + \
                           ' provides support with their ' + \
                           helpers.unitdict[self.supporter[1]]['Objective'] + \
                           ' in ' + \
                           helpers.provincedict[self.supporter[2]]['Objective'] + \
                           ' so ' + \
                           helpers.powerdict[self.supported[0]]['Objective'] + \
                           ' can move their ' + \
                           helpers.unitdict[self.supported[1]]['Objective'] + \
                           ' from ' + \
                           helpers.provincedict[self.supported[2]]['Objective'] + \
                           ' into ' + \
                           helpers.provincedict[self.province]['Objective'] + ''

    if 'Expert' in self.utterance.tones:
      supportertype = 'A'
      if self.supporter[1] == 'FLT':
        supportertype = 'F'
      supportedtype = 'A'
      if self.supported[1] == 'FLT':
        supportedtype = 'F'
      self.simpleenglish += ' (' + supportertype + ' ' + self.supporter[2] + ' S ' + supportedtype + ' ' + self.supported[2] + ' -> ' + self.province + ')'

    return self.simpleenglish

  def formDAIDE(self): # type () -> str
    """
    Create a DAIDE representation of this Message

    :return: the DAIDE message
    :rtype: str
    """

    return '(' + ' '.join(self.supporter) + ') SUP (' + ' '.join(self.supported) + ') MTO ' + self.province

class PressConvoy(PressMessage):
  """ The game-related content of a convoy. """

  def __init__(self, utterance, container, thelists): # type: (PressUtterance, PressMessage, []) -> None
    """
    Initialize the message with an utterance

    :param utterance: the press utterance that this message is within the content for
    :type utterance: PressUtterance
    :param container: the press message that contains this one
    :type container: PressMessage
    :param thelists: the parsed, nested DAIDE statement
    :type thelists: []
    """

    super().__init__(utterance, container)
    if thelists is None or len(thelists) == 0:
      self.operator = 'CVY'
      if random.choice([True, True, False]):
        if random.choice([True, False]):
          self.convoyunit = [utterance.frompower, random.choice(helpers.unitlist), random.choice(helpers.provincelist)]
        else:
          self.convoyunit = [random.choice(utterance.topowers), random.choice(helpers.unitlist), random.choice(helpers.provincelist)]
      else:
        self.convoyunit = [random.choice(helpers.powerlist), random.choice(helpers.unitlist), random.choice(helpers.provincelist)]
      if random.choice([True, True, False]):
        if random.choice([True, False]):
          self.convoyedunit = [utterance.frompower, random.choice(helpers.unitlist), random.choice(helpers.provincelist)]
        else:
          self.convoyedunit = [random.choice(utterance.topowers), random.choice(helpers.unitlist), random.choice(helpers.provincelist)]
      else:
        self.convoyedunit = [random.choice(helpers.powerlist), random.choice(helpers.unitlist), random.choice(helpers.provincelist)]
      provlist = [curprov for curprov in helpers.provincelist if curprov != self.convoyunit[2] and curprov != self.convoyedunit[2]]
      self.province = random.choice(provlist)
    elif len(thelists) == 5:
      self.operator = thelists[1]
      self.convoyunit = thelists[0]
      self.convoyedunit = thelists[2]
      self.province = thelists[4]

  def formenglish(self): # type () -> str
    """
    Creates an English expression about the convoy in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    self.english = self.formlistenglish()
    return self.english

  def formlistenglish(self): # type () -> str
    """
    Creates an English expression about the convoy in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    self.simpleenglish = helpers.powerdict[self.convoyunit[0]]['Objective'] + \
                         '\'s ' + \
                         helpers.unitdict[self.convoyunit[1]]['Objective'] + \
                         ' in ' + \
                         helpers.provincedict[self.convoyunit[2]]['Objective'] + \
                         ' convoys ' + \
                         helpers.powerdict[self.convoyedunit[0]]['Objective'] + \
                         '\'s ' + \
                         helpers.unitdict[self.convoyedunit[1]]['Objective'] + \
                         ' from ' + \
                         helpers.provincedict[self.convoyedunit[2]]['Objective'] + \
                         ' into ' + \
                         helpers.provincedict[self.province]['Objective'] + '.'

    if 'Expert' in self.utterance.tones:
      convoytype = 'F'
      convoyedtype = 'A'
      self.simpleenglish += ' (' + convoytype + ' ' + self.convoyunit[2] + ' C ' + convoyedtype + ' ' + self.convoyedunit[2] + ' -> ' + self.province + ').'

    return self.simpleenglish

  def formclauseenglish(self): # type () -> str
    """
    Creates an English expression about the convoy in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """
    if self.container.container.operator == "NOT":
      self.simpleenglish = helpers.powerdict[self.convoyunit[0]]['Objective'] + \
                           '\'s ' + \
                           helpers.unitdict[self.convoyunit[1]]['Objective'] + \
                           ' in ' + \
                           helpers.provincedict[self.convoyunit[2]]['Objective'] + \
                           ' does not convoy ' + \
                           helpers.powerdict[self.convoyedunit[0]]['Objective'] + \
                           '\'s ' + \
                           helpers.unitdict[self.convoyedunit[1]]['Objective'] + \
                           ' from ' + \
                           helpers.provincedict[self.convoyedunit[2]]['Objective'] + \
                           ' into ' + \
                           helpers.provincedict[self.province]['Objective'] + ''
    else:
      self.simpleenglish = helpers.powerdict[self.convoyunit[0]]['Objective'] + \
                         '\'s ' + \
                         helpers.unitdict[self.convoyunit[1]]['Objective'] + \
                         ' in ' + \
                         helpers.provincedict[self.convoyunit[2]]['Objective'] + \
                         ' convoys ' + \
                         helpers.powerdict[self.convoyedunit[0]]['Objective'] + \
                         '\'s ' + \
                         helpers.unitdict[self.convoyedunit[1]]['Objective'] + \
                         ' from ' + \
                         helpers.provincedict[self.convoyedunit[2]]['Objective'] + \
                         ' into ' + \
                         helpers.provincedict[self.province]['Objective'] + ''

    if 'Expert' in self.utterance.tones:
      convoytype = 'F'
      convoyedtype = 'A'
      self.simpleenglish += ' (' + convoytype + ' ' + self.convoyunit[2] + ' C ' + convoyedtype + ' ' + self.convoyedunit[2] + ' -> ' + self.province + ') '

    return self.simpleenglish

  def formDAIDE(self): # type () -> str
    """
    Create a DAIDE representation of this Message

    :return: the DAIDE message
    :rtype: str
    """

    return '(' + ' '.join(self.convoyunit) + ') CVY (' + ' '.join(self.convoyedunit) + ') CTO ' + self.province

class PressConvoyVia(PressMessage):
  """ The game-related content of a convoy over water. """

  def __init__(self, utterance, container, thelists): # type: (PressUtterance, PressMessage, []) -> None
    """
    Initialize the message with an utterance

    :param utterance: the press utterance that this message is within the content for
    :type utterance: PressUtterance
    :param container: the press message that contains this one
    :type container: PressMessage
    :param thelists: the parsed, nested DAIDE statement
    :type thelists: []
    """

    super().__init__(utterance, container)
    if thelists is None or len(thelists) == 0:
      self.operator = 'CTO'
      if random.choice([True, True, False]):
        if random.choice([True, False]):
          self.convoyedunit = [utterance.frompower, random.choice(helpers.unitlist), random.choice(helpers.provincelist)]
        else:
          self.convoyedunit = [random.choice(utterance.topowers), random.choice(helpers.unitlist), random.choice(helpers.provincelist)]
      else:
        self.convoyedunit = [random.choice(helpers.powerlist), random.choice(helpers.unitlist), random.choice(helpers.provincelist)]
      provlist = [curprov for curprov in helpers.provincelist if curprov != self.convoyedunit[2]]
      self.destination = random.choice(provlist)
      self.searoute = random.sample(helpers.sealist, random.randint(1, 4))
    elif len(thelists) == 5:
      self.operator = thelists[1]
      self.convoyedunit = thelists[0]
      self.destination = thelists[2]
      self.searoute = thelists[4]

  def formenglish(self): # type () -> str
    """
    Creates an English expression about the convoy over water in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    self.english = self.formlistenglish()
    return self.english

  def formlistenglish(self): # type () -> str
    """
    Creates an English expression about the convoy over water in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    self.simpleenglish = helpers.powerdict[self.convoyedunit[0]]['Objective'] + \
                         '\'s ' + \
                         helpers.unitdict[self.convoyedunit[1]]['Objective'] + \
                         ' in ' + \
                         helpers.provincedict[self.convoyedunit[2]]['Objective'] + \
                         ' moves by convoy to ' + \
                         helpers.provincedict[self.destination]['Objective'] + \
                         ' following this path: ' + \
                         helpers.listOfProvinces(self.searoute) + '.'

    return self.simpleenglish

  def formclauseenglish(self): # type () -> str
    """
    Creates an English expression about the convoy over water in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """
    if self.container.container.operator == "NOT":
      self.simpleenglish = helpers.powerdict[self.convoyedunit[0]]['Objective'] + \
                         '\'s ' + \
                         helpers.unitdict[self.convoyedunit[1]]['Objective'] + \
                         ' in ' + \
                         helpers.provincedict[self.convoyedunit[2]]['Objective'] + \
                         ' does not move by convoy to ' + \
                         helpers.provincedict[self.destination]['Objective'] + \
                         ' following this path: ' + \
                         helpers.listOfProvinces(self.searoute) + ''
    else:
      self.simpleenglish = helpers.powerdict[self.convoyedunit[0]]['Objective'] + \
                           '\'s ' + \
                           helpers.unitdict[self.convoyedunit[1]]['Objective'] + \
                           ' in ' + \
                           helpers.provincedict[self.convoyedunit[2]]['Objective'] + \
                           ' moves by convoy to ' + \
                           helpers.provincedict[self.destination]['Objective'] + \
                           ' following this path: ' + \
                           helpers.listOfProvinces(self.searoute) + ''

    return self.simpleenglish

  def formDAIDE(self): # type () -> str
    """
    Create a DAIDE representation of this Message

    :return: the DAIDE message
    :rtype: str
    """

    return '(' + ' '.join(self.convoyedunit) + ') CTO ' + self.destination + ' VIA (' + ' '.join(self.searoute) + ')'

class PressRetreat(PressMessage):
  """ The game-related content of a retreat. """

  def __init__(self, utterance, container, thelists): # type: (PressUtterance, PressMessage, []) -> None
    """
    Initialize the message with an utterance

    :param utterance: the press utterance that this message is within the content for
    :type utterance: PressUtterance
    :param container: the press message that contains this one
    :type container: PressMessage
    :param thelists: the parsed, nested DAIDE statement
    :type thelists: []
    """

    super().__init__(utterance, container)
    if thelists is None or len(thelists) == 0:
      self.operator = 'RTO'
      if random.choice([True, True, False]):
        if random.choice([True, False]):
          self.unit = [utterance.frompower, random.choice(helpers.unitlist), random.choice(helpers.provincelist)]
        else:
          self.unit = [random.choice(utterance.topowers), random.choice(helpers.unitlist), random.choice(helpers.provincelist)]
      else:
        self.unit = [random.choice(helpers.powerlist), random.choice(helpers.unitlist), random.choice(helpers.provincelist)]
      provlist = [curprov for curprov in helpers.provincelist if curprov != self.unit[2]]
      self.destination = random.choice(provlist)
    elif len(thelists) == 3:
      self.operator = thelists[1]
      self.unit = thelists[0]
      self.destination = thelists[2]

  def formenglish(self): # type () -> str
    """
    Creates an English expression about the retreat in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    self.english = self.formlistenglish()
    return self.english

  def formlistenglish(self): # type () -> str
    """
    Creates an English expression about the retreat in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    self.simpleenglish = helpers.powerdict[self.unit[0]]['Objective'] + \
                         '\'s ' + \
                         helpers.unitdict[self.unit[1]]['Objective'] + \
                         ' retreats from ' + \
                         helpers.provincedict[self.unit[2]]['Objective'] + \
                         ' to ' + \
                         helpers.provincedict[self.destination]['Objective'] + '.'

    return self.simpleenglish

  def formclauseenglish(self): # type () -> str
    """
    Creates an English expression about the retreat in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """
    if self.container.container.operator== "NOT":
      self.simpleenglish = helpers.powerdict[self.unit[0]]['Objective'] + \
                         '\'s ' + \
                         helpers.unitdict[self.unit[1]]['Objective'] + \
                         ' does not retreat from ' + \
                         helpers.provincedict[self.unit[2]]['Objective'] + \
                         ' to ' + \
                         helpers.provincedict[self.destination]['Objective'] + ''
    else:
      self.simpleenglish = helpers.powerdict[self.unit[0]]['Objective'] + \
                           '\'s ' + \
                           helpers.unitdict[self.unit[1]]['Objective'] + \
                           ' retreats from ' + \
                           helpers.provincedict[self.unit[2]]['Objective'] + \
                           ' to ' + \
                           helpers.provincedict[self.destination]['Objective'] + ''

    return self.simpleenglish

  def formDAIDE(self): # type () -> str
    """
    Create a DAIDE representation of this Message

    :return: the DAIDE message
    :rtype: str
    """

    return '(' + ' '.join(self.unit) + ') RTO ' + self.destination

class PressDisband(PressMessage):
  """ The game-related content of a disband. """

  def __init__(self, utterance, container, thelists): # type: (PressUtterance, PressMessage, []) -> None
    """
    Initialize the message with an utterance

    :param utterance: the press utterance that this message is within the content for
    :type utterance: PressUtterance
    :param container: the press message that contains this one
    :type container: PressMessage
    :param thelists: the parsed, nested DAIDE statement
    :type thelists: []
    """

    super().__init__(utterance, container)
    if thelists is None or len(thelists) == 0:
      self.operator = 'DSB'
      if random.choice([True, True, False]):
        if random.choice([True, False]):
          self.unit = [utterance.frompower, random.choice(helpers.unitlist), random.choice(helpers.provincelist)]
        else:
          self.unit = [random.choice(utterance.topowers), random.choice(helpers.unitlist), random.choice(helpers.provincelist)]
      else:
        self.unit = [random.choice(helpers.powerlist), random.choice(helpers.unitlist), random.choice(helpers.provincelist)]
    elif len(thelists) == 2:
      self.operator = thelists[1]
      self.unit = thelists[0]

  def formenglish(self): # type () -> str
    """
    Creates an English expression about the disband in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    self.english = self.formlistenglish()
    return self.english

  def formlistenglish(self): # type () -> str
    """
    Creates an English expression about the disband in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    self.simpleenglish = helpers.powerdict[self.unit[0]]['Objective'] + \
                         '\'s ' + \
                         helpers.unitdict[self.unit[1]]['Objective'] + \
                         ' in ' + \
                         helpers.provincedict[self.unit[2]]['Objective'] + \
                         ' retreats from the board.'

    return self.simpleenglish

  def formclauseenglish(self): # type () -> str
    """
    Creates an English expression about the disband in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """
    if self.container.container.operator== "NOT":
      self.simpleenglish = helpers.powerdict[self.unit[0]]['Objective'] + \
                         '\'s ' + \
                         helpers.unitdict[self.unit[1]]['Objective'] + \
                         ' in ' + \
                         helpers.provincedict[self.unit[2]]['Objective'] + \
                         ' does not retreat from the board'
    else:
      self.simpleenglish = helpers.powerdict[self.unit[0]]['Objective'] + \
                           '\'s ' + \
                           helpers.unitdict[self.unit[1]]['Objective'] + \
                           ' in ' + \
                           helpers.provincedict[self.unit[2]]['Objective'] + \
                           ' retreats from the board'

    return self.simpleenglish

  def formDAIDE(self): # type () -> str
    """
    Create a DAIDE representation of this Message

    :return: the DAIDE message
    :rtype: str
    """

    return '(' + ' '.join(self.unit) + ') DSB'

class PressBuild(PressMessage):
  """ The game-related content of a build. """

  def __init__(self, utterance, container, thelists): # type: (PressUtterance, PressMessage, []) -> None
    """
    Initialize the message with an utterance

    :param utterance: the press utterance that this message is within the content for
    :type utterance: PressUtterance
    :param container: the press message that contains this one
    :type container: PressMessage
    :param thelists: the parsed, nested DAIDE statement
    :type thelists: []
    """

    super().__init__(utterance, container)
    if thelists is None or len(thelists) == 0:
      self.operator = 'BLD'
      if random.choice([True, True, False]):
        if random.choice([True, False]):
          self.unit = [utterance.frompower, random.choice(helpers.unitlist), random.choice(helpers.supplylist)]
        else:
          self.unit = [random.choice(utterance.topowers), random.choice(helpers.unitlist), random.choice(helpers.supplylist)]
      else:
        self.unit = [random.choice(helpers.powerlist), random.choice(helpers.unitlist), random.choice(helpers.supplylist)]
    elif len(thelists) == 2:
      self.operator = thelists[1]
      self.unit = thelists[0]

  def formenglish(self): # type () -> str
    """
    Creates an English expression about the build in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    self.english = self.formlistenglish()
    return self.english

  def formlistenglish(self): # type () -> str
    """
    Creates an English expression about the build in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    self.simpleenglish = helpers.powerdict[self.unit[0]]['Objective'] + \
                         ' builds a new ' + \
                         helpers.unitdict[self.unit[1]]['Objective'] + \
                         ' in ' + \
                         helpers.provincedict[self.unit[2]]['Objective'] + \
                         '.'

    return self.simpleenglish

  def formclauseenglish(self):  # type () -> str
    """
    Creates an English expression about the build in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """
    if self.container.container.operator== "NOT":
      self.simpleenglish = helpers.powerdict[self.unit[0]]['Objective'] + \
                         ' does not build a new ' + \
                         helpers.unitdict[self.unit[1]]['Objective'] + \
                         ' in ' + \
                         helpers.provincedict[self.unit[2]]['Objective'] + \
                         ''
    else:
      self.simpleenglish = helpers.powerdict[self.unit[0]]['Objective'] + \
                           ' builds a new ' + \
                           helpers.unitdict[self.unit[1]]['Objective'] + \
                           ' in ' + \
                           helpers.provincedict[self.unit[2]]['Objective'] + \
                           ''

    return self.simpleenglish

  def formDAIDE(self): # type () -> str
    """
    Create a DAIDE representation of this Message

    :return: the DAIDE message
    :rtype: str
    """

    return '(' + ' '.join(self.unit) + ') BLD'

class PressRemove(PressMessage):
  """ The game-related content of a remove. """

  def __init__(self, utterance, container, thelists): # type: (PressUtterance, PressMessage, []) -> None
    """
    Initialize the message with an utterance

    :param utterance: the press utterance that this message is within the content for
    :type utterance: PressUtterance
    :param container: the press message that contains this one
    :type container: PressMessage
    :param thelists: the parsed, nested DAIDE statement
    :type thelists: []
    """

    super().__init__(utterance, container)
    if thelists is None or len(thelists) == 0:
      self.operator = 'REM'
      if random.choice([True, True, False]):
        if random.choice([True, False]):
          self.unit = [utterance.frompower, random.choice(helpers.unitlist), random.choice(helpers.provincelist)]
        else:
          self.unit = [random.choice(utterance.topowers), random.choice(helpers.unitlist), random.choice(helpers.provincelist)]
      else:
        self.unit = [random.choice(helpers.powerlist), random.choice(helpers.unitlist), random.choice(helpers.provincelist)]
    elif len(thelists) == 2:
      self.operator = thelists[1]
      self.unit = thelists[0]

  def formenglish(self): # type () -> str
    """
    Creates an English expression about the remove in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    self.english = self.formlistenglish()
    return self.english

  def formlistenglish(self): # type () -> str
    """
    Creates an English expression about the remove in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    self.simpleenglish = helpers.powerdict[self.unit[0]]['Objective'] + \
                         ' removes their ' + \
                         helpers.unitdict[self.unit[1]]['Objective'] + \
                         ' in ' + \
                         helpers.provincedict[self.unit[2]]['Objective'] + \
                         ' from the board.'

    return self.simpleenglish

  def formclauseenglish(self):  # type () -> str
    """
    Creates an English expression about the remove in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    if self.container.container.operator== "NOT":
      self.simpleenglish = helpers.powerdict[self.unit[0]]['Objective'] + \
                         ' does not their ' + \
                         helpers.unitdict[self.unit[1]]['Objective'] + \
                         ' in ' + \
                         helpers.provincedict[self.unit[2]]['Objective'] + \
                         ' from the board.'
    else:
      self.simpleenglish = helpers.powerdict[self.unit[0]]['Objective'] + \
                           ' removes their ' + \
                           helpers.unitdict[self.unit[1]]['Objective'] + \
                           ' in ' + \
                           helpers.provincedict[self.unit[2]]['Objective'] + \
                           ' from the board.'

    return self.simpleenglish

  def formDAIDE(self): # type () -> str
    """
    Create a DAIDE representation of this Message

    :return: the DAIDE message
    :rtype: str
    """

    return '(' + ' '.join(self.unit) + ') REM'

class PressWaive(PressMessage):
  """ The game-related content of a waive. """

  def __init__(self, utterance, container, thelists): # type: (PressUtterance, PressMessage, []) -> None
    """
    Initialize the message with an utterance

    :param utterance: the press utterance that this message is within the content for
    :type utterance: PressUtterance
    :param container: the press message that contains this one
    :type container: PressMessage
    :param thelists: the parsed, nested DAIDE statement
    :type thelists: []
    """

    super().__init__(utterance, container)
    if thelists is None or len(thelists) == 0:
      self.operator = 'WVE'
      if random.choice([True, True, False]):
        if random.choice([True, False]):
          self.power = utterance.frompower
        else:
          self.power = random.choice(utterance.topowers)
      else:
        self.power = random.choice(helpers.powerlist)
    elif len(thelists) == 2:
      self.operator = thelists[1]
      self.power = thelists[0]

  def formenglish(self): # type () -> str
    """
    Creates an English expression about the waive in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    self.english = self.formlistenglish()
    return self.english

  def formlistenglish(self): # type () -> str
    """
    Creates an English expression about the waive in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    self.simpleenglish = helpers.powerdict[self.power]['Objective'] + \
                         ' waives their build turn.'

    return self.simpleenglish

  def formclauseenglish(self): # type () -> str
    """
    Creates an English expression about the waive in the context of a sender, recipients and desired tone.

    :return: the English expression
    :rtype: str
    """

    if self.container.container.operator== "NOT":
      self.simpleenglish = helpers.powerdict[self.power]['Objective'] + \
                         ' does not waive their build turn.'
    else:
      self.simpleenglish = helpers.powerdict[self.power]['Objective'] + \
                           ' waives their build turn.'

    return self.simpleenglish

  def formDAIDE(self): # type () -> str
    """
    Create a DAIDE representation of this Message

    :return: the DAIDE message
    :rtype: str
    """

    return self.power + ' WVE'

def messageFactory(utterance, container, daidelists): # type: (PressUtterance, PressMessage, []) -> PressMessage
  """
  Creates the objects and subobjects corresponding to a nested DAIDE list

  :param utterance: the original DAIDE utterance
  :type utterance: PressUtterance
  :param container: the DAIDE message that contains this one
  :type container: PressMessage
  :param daidelists: the parsed nested DAIDE expression
  :type daidelists: []

  :return: a DAIDE message
  :rtype: PressMessage
  
  """

  if daidelists is None or len(daidelists) == 0:
    return PressMessage(utterance, container)

  if daidelists[0] == 'FCT':
    return PressFact(utterance, container, daidelists)
  elif daidelists[0] == 'PRP':
    return PressProposal(utterance, container, daidelists)
  elif daidelists[0] == 'YES':
    return PressAccept(utterance, container, daidelists)
  elif daidelists[0] == 'REJ':
    return PressReject(utterance, container, daidelists)
  elif daidelists[0] == 'CCL':
    return PressCancel(utterance, container, daidelists)
  elif daidelists[0] == 'HUH':
    return PressHuh(utterance, container, daidelists)
  elif daidelists[0] == 'BWX':
    return PressIgnore(utterance, container, daidelists)
  elif daidelists[0] == 'PCE':
    return PressPeace(utterance, container, daidelists)
  elif daidelists[0] == 'ALY':
    return PressAlliance(utterance, container, daidelists)
  elif daidelists[0] == 'DMZ':
    return PressDMZ(utterance, container, daidelists)
  elif daidelists[0] == 'DRW':
    return PressDraw(utterance, container, daidelists)
  elif daidelists[0] == 'SLO':
    return PressSolo(utterance, container, daidelists)
  elif daidelists[0] == 'ORR':
    return PressOr(utterance, container, daidelists)
  elif daidelists[0] == 'AND':
    return PressAnd(utterance, container, daidelists)
  elif daidelists[0] == 'IFF':
    return PressIf(utterance, container, daidelists)
  elif daidelists[0] == 'NOT':
    return PressNot(utterance, container, daidelists)
  elif daidelists[0] == 'NAR':
    return PressNar(utterance, container, daidelists)
  elif daidelists[0] == 'XDO':
    return PressMoveExecute(utterance, container, daidelists)
  elif len(daidelists) == 2 and daidelists[1] == 'HLD':
    return PressHold(utterance, container, daidelists)
  elif len(daidelists) == 3 and daidelists[1] == 'MTO':
    return PressMoveInto(utterance, container, daidelists)
  elif len(daidelists) == 3 and daidelists[1] == 'SUP':
    return PressSupportHold(utterance, container, daidelists)
  elif len(daidelists) == 5 and daidelists[1] == 'SUP' and daidelists[3] == 'MTO':
    return PressSupportMove(utterance, container, daidelists)
  elif len(daidelists) == 5 and daidelists[1] == 'CVY' and daidelists[3] == 'CTO':
    return PressConvoy(utterance, container, daidelists)
  elif len(daidelists) == 5 and daidelists[1] == 'CVY' and daidelists[3] == 'VIA':
    return PressConvoyVia(utterance, container, daidelists)
  elif len(daidelists) == 3 and daidelists[1] == 'RTO':
    return PressRetreat(utterance, container, daidelists)
  elif len(daidelists) == 2 and daidelists[1] == 'DSB':
    return PressDisband(utterance, container, daidelists)
  elif len(daidelists) == 2 and daidelists[1] == 'BLD':
    return PressBuild(utterance, container, daidelists)
  elif len(daidelists) == 2 and daidelists[1] == 'REM':
    return PressRemove(utterance, container, daidelists)
  elif len(daidelists) == 2 and daidelists[1] == 'WVE':
    return PressWaive(utterance, container, daidelists)
  else:
    return PressMessage(utterance, container)

def randomFactory(utterance, container, daideword): # type: (PressUtterance, PressMessage, str) -> PressMessage
  """
  Randomly constructs the objects and subobjects corresponding to a DAIDE word

  :param utterance: the original DAIDE utterance
  :type utterance: PressUtterance
  :param container: the DAIDE message that contains this one
  :type container: PressMessage
  :param daideword: the DAIDE keyword for this message (PRP, FCT, etc.)
  :type daideword: str

  :return: a randomly constructed DAIDE message
  :rtype: PressMessage
  
  """

  if daideword == 'FCT':
    return PressFact(utterance, container, None)
  elif daideword == 'PRP':
    return PressProposal(utterance, container, None)
  elif daideword == 'YES':
    return PressAccept(utterance, container, None)
  elif daideword == 'REJ':
    return PressReject(utterance, container, None)
  elif daideword == 'CCL':
    return PressCancel(utterance, container, None)
  elif daideword == 'HUH':
    return PressHuh(utterance, container, None)
  elif daideword == 'BWX':
    return PressIgnore(utterance, container, None)
  elif daideword == 'PCE':
    return PressPeace(utterance, container, None)
  elif daideword == 'ALY':
    return PressAlliance(utterance, container, None)
  elif daideword == 'DMZ':
    return PressDMZ(utterance, container, None)
  elif daideword == 'DRW':
    return PressDraw(utterance, container, None)
  elif daideword == 'SLO':
    return PressSolo(utterance, container, None)
  elif daideword == 'ORR':
    return PressOr(utterance, container, None)
  elif daideword == 'AND':
    return PressAnd(utterance, container, None)
  elif daideword == 'IFF':
    return PressIf(utterance, container, None)
  elif daideword == 'NOT':
    return PressNot(utterance, container, None)
  elif daideword == 'NAR':
    return PressNar(utterance, container, None)
  elif daideword == 'XDO':
    return PressMoveExecute(utterance, container, None)
  elif daideword == 'HLD':
    return PressHold(utterance, container, None)
  elif daideword == 'MTO':
    return PressMoveInto(utterance, container, None)
  elif daideword == 'SUP':
    return PressSupportHold(utterance, container, None)
  elif daideword == 'SUPMTO':
    return PressSupportMove(utterance, container, None)
  elif daideword == 'CVYCTO':
    return PressConvoy(utterance, container, None)
  elif daideword == 'CVYVIA':
    return PressConvoyVia(utterance, container, None)
  elif daideword == 'RTO':
    return PressRetreat(utterance, container, None)
  elif daideword == 'DSB':
    return PressDisband(utterance, container, None)
  elif daideword == 'BLD':
    return PressBuild(utterance, container, None)
  elif daideword == 'REM':
    return PressRemove(utterance, container, None)
  elif daideword == 'WVE':
    return PressWaive(utterance, container, None)
  else:
    return PressMessage(utterance, container)

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

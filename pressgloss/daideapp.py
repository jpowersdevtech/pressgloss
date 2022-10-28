# Standard library imports
import logging
import os
import sys
import random

# Third-party imports
import flask
from flask.wrappers import Response
from flask import Blueprint

# pressgloss imports
import pressgloss.core as PRESSGLOSS
import pressgloss.gamelog as GAMELOG
import pressgloss.helpers as helpers

landingpage = Blueprint('landingpage', __name__, template_folder='templates')
theapi = Blueprint('theapi', __name__, template_folder='templates')

@landingpage.route('/')
def index(): # type: () -> str
  """
  Publish the index.html from resources
  """

  return flask.render_template('index.html')

@theapi.route('/annotategamelog', methods=['POST'])
def annotategamelog(): # type: () -> Response
  """
  Annotate a Diplomacy game log with glosses for each message containing only DAIDE

  :return: A Flask Response with type JSON containing the game log with annotations.
  :rtype: Response
  """

  if flask.request.method == 'POST':
    reqdict = flask.request.get_json(force=True)
    results = GAMELOG.annotatelog(reqdict)
    return flask.jsonify(results)

  return flask.jsonify({})

@theapi.route('/daide2gloss', methods=['POST'])
def daide2gloss(): # type: () -> Response
  """
  Handle DAIDE input from the page.  This will be a single well-formed DAIDE expression.

  :return: A Flask Response with type JSON containing the gloss.
  :rtype: Response
  """

  if flask.request.method == 'POST':
    reqdict = flask.request.get_json(force=True)
    daidetext = reqdict['daidetext']
    thetones = reqdict['tones']
    results = {"gloss": PRESSGLOSS.daide2gloss(daidetext, thetones)}
    return flask.jsonify(results)

  return flask.jsonify({})

@theapi.route('/randomdaide', methods=['POST'])
def randomdaide(): # type: () -> Response
  """
  Generate a random DAIDE expression and English gloss

  :return: A Flask Response with type JSON containing the DAIDE and gloss.
  :rtype: Response
  """

  if flask.request.method == 'POST':
    reqdict = flask.request.get_json(force=True)
    tones = random.sample(helpers.tonelist, random.randint(1, 3))
    utterance = PRESSGLOSS.PressUtterance(None, tones)
    results = {"daide": utterance.daide, "gloss": utterance.english}
    return flask.jsonify(results)

  return flask.jsonify({})

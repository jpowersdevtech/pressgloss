# Standard library imports
import logging
import os
import sys

# Third-party imports
import flask
from flask.wrappers import Response
from flask import Blueprint

# pressgloss imports
import pressgloss.core as PRESSGLOSS

landingpage = Blueprint('landingpage', __name__, template_folder='templates')
theapi = Blueprint('theapi', __name__, template_folder='templates')

@landingpage.route('/')
def index(): # type: () -> str
  """
  Publish the index.html from resources
  """

  return flask.render_template('index.html')

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

  return flask.jsonify([])

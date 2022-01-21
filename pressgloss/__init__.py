# -*- coding: utf-8 -*-
""" pressgloss module

"""

# Third-party imports
import flask

__version__ = "0.0.1"

def create_app(): # type: () -> flask.Flask
  """
  Application context initialization.  This method MUST
  have this name.

  :return: the contextualized flask app
  :rtype: flask.Flask
  """

  app = flask.Flask(__name__, instance_relative_config=False)
  with app.app_context():
    from . import daideapp

    app.register_blueprint(daideapp.landingpage)
    app.register_blueprint(daideapp.theapi)

    return app

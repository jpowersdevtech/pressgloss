********************************
Pressgloss Library
********************************

A Python library for converting formal Diplomacy DAIDE Press language into
human-readable glosses with tone.  Some functions are exposed as JSON POST
API endpoints.

------------------------
Install and run the app:
------------------------

pip install -r requirements.txt

To start the Flask app locally,:

    python -m pressgloss --operation app

Then visit `http://127.0.0.1:5000/ <http://127.0.0.1:5000/>`_

---------
CLI:
---------

To translate a DAIDE expression:

    python -m pressgloss --operation translate --daide "FRM (ENG) (FRA ITA) (PRP (PCE (FRA ITA)))" --tones "Haughty,Urgent"

To generate 10 random DAIDE expressions, with glosses (random tones will also be selected):

    python -m pressgloss --operation random --number 10

To fine tune a model: 

    python -m pressgloss --operation finetune

To use a model to encode a DAIDE expression:

    python -m pressgloss --operation encode --model (optional) --english "I think this proposal will help us both out. I offer a peace treaty between us. I think our interests are aligned for the time being." --tones "Friendly"

To validate a model, either finetuned or few-shot: 

    python -m pressgloss --operation validate --model (optional)

To get the usage instructions:

    python -m pressgloss --help

---------
API:
---------

^^^^^^^^^^^^
/daide2gloss
^^^^^^^^^^^^

Translate a DAIDE expression into English using one or more tones.

**request**::

    {"daidetext": "FRM (FRA) (ITA) (PRP (PCE (FRA ITA)))",
     "tones": ["Friendly"]}

**response**::

    {"gloss": "I think this proposal will help us both out.
               I offer a peace treaty between us.
               I think our interests are aligned for the time being."}

^^^^^^^^^^^^^^^^
/annotategamelog
^^^^^^^^^^^^^^^^

Annotate a Diplomacy game log whose messages were largely in pure DAIDE to have English glosses in addition to the DAIDE.

**request**::

A JSON game log directly from the online diplomacy game hosted by the TACC team.

**response**::

Exactly the same game except that each message contains an English gloss of the DAIDE that was found there, or a note to explain why a gloss could not be generated.

^^^^^^^^^^^^
/randomdaide
^^^^^^^^^^^^

Randomly generate a valid DAIDE expression.  Good for testing.

**request**::

The request can be empty but must be POST.

**response**::

    {"daide": "FRM (FRA) (ITA) (PRP (PCE (FRA ITA)))",
     "gloss": "I think this proposal will help us both out.
               I offer a peace treaty between us.
               I think our interests are aligned for the time being."}

---------
Testing:
---------

To test, best to make sure coverage and unittest are installed, then from the
parent directory, run

    coverage run --source pressgloss -m unittest tests.test_basic

`DAIDE Specification <http://www.daide.org.uk/index.html>`_

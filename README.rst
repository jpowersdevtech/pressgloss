********************************
pressgloss Library
********************************

A Python library for converting formal Diplomacy Press language into human-readable
glosses with tone.

Easy use:
pip install -r requirements.txt

To run unit tests:
.\\test.bat or ./test.sh

To start the Flask app:

    python -m pressgloss --operation app

Then visit `http://127.0.0.1:5000/ <http://127.0.0.1:5000/>`_

To translate a DAIDE expression:

    python -m pressgloss --operation translate --daide "FRM (ENG) (FRA ITA) (PRP (PCE (FRA ITA)))" --tones "Haughty,Urgent"

To get the usage instructions:

    python -m pressgloss --help

To test, best to make sure coverage and unittest are installed, then from the
parent directory, run
coverage run --source pressgloss -m unittest tests.test_basic

`DAIDE Specification <http://www.daide.org.uk/index.html>`_

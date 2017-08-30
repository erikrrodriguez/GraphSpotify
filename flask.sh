#!/bin/bash

. venv/bin/activate

# Run once to install
#pip install --editable .

export FLASK_APP=GraphSpotify/GraphSpotify.py
export FLASK_DEBUG=true
flask run

#!/bin/bash

. venv/bin/activate

# Run once to install
#pip install --editable .

export FLASK_APP=GraphSpotify
export FLASK_DEBUG=true
flask run

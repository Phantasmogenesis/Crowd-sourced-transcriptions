#!/bin/s

. venv/bin/activate
export FLASK_APP=crowd-sourced
export FLASK_DEBUG=1
flask run -h localhost -p 8000
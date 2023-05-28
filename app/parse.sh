#!/bin/bash
# Redirect the python script errors to dev/null
# The error will be while the python script tries to access the not-ready yet database
./producer.sh > /dev/null & python3 parse.py 2> /dev/null
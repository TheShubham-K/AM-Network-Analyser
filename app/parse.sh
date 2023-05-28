#!/bin/bash
# Redirect errors to dev/null
# The sole error will be while the python script tries to access the not-ready yet database
./producer.sh > /dev/null & python3 parse.py
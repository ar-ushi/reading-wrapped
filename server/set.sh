#!/bin/bash

ENV=$1

FILE=.env.$ENV 

if [ -f "$FILE" ]; then
    echo "Setting environment to [ $ENV ]"
else
    echo "$FILE does not exisst"
    exit 1
fi

cp .env.$ENV .env
echo "Environment setup complete"
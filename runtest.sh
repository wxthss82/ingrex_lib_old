#!/bin/bash

until ./starttest.sh; do
    echo "Server 'startcomm' crashed with exit code $?. Respawning .." >&2
    sleep 1
done

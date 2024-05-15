#!/bin/bash

pid=$(pgrep -f "check.sh")
if [ -n "$pid" ]; then
  kill "$pid"
  echo "Script stopped."
fi

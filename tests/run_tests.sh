#!/usr/bin/env bash

HERE=`readlink -f $(dirname $0)`

export PYTHONPATH=$HERE/../src:$PYTHONPATH
export PATH=$HERE/../bin:$PATH

glados

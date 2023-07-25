#!/usr/bin/env bash

set -e
HERE=`readlink -f $(dirname $0)`

export PYTHONPATH=$HERE/../src:$PYTHONPATH
export PATH=$HERE/../bin:$PATH

glados turret -v

#turret -p 9101
#turret -p 9101 -c unit_tests/data/config1.json
#turret -p 9101 -c unit_tests/data/config2.json
#turret -p 9101 -c unit_tests/data/config3.json
#exit $?

#turret 
#exit $?

echo "[******************]"
echo "[* Running pylint *]"
echo "[******************]"
set +e
MIN_PYLINT_SCORE=9.0
pylint --rcfile=../.pylintrc ../src/glados > pylint.tmp
cat pylint.tmp | tail -n2
cat pylint.tmp
set -e

echo "[*****************]"
echo "[* Running black *]"
echo "[*****************]"
black -l 80 --diff ../src/glados > black.diff 2> /dev/null

echo "[****************]"
echo "[* Running mypy *]"
echo "[****************]"
mypy ../src/glados

echo "[**********************]"
echo "[* Running Unit Tests *]"
echo "[**********************]"
OMIT=../src/glados/__main__.py
coverage run -m pytest
COVERAGE_REPORT=.coverage.tmp
coverage report -m > $COVERAGE_REPORT

#exit $?

echo ""
echo "[********************]"
echo "[* Running Coverage *]"
echo "[********************]"
cat $COVERAGE_REPORT

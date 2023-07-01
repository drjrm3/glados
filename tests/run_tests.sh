#!/usr/bin/env bash

HERE=`readlink -f $(dirname $0)`

export PYTHONPATH=$HERE/../src:$PYTHONPATH
export PATH=$HERE/../bin:$PATH

glados turret -v

#turret 
#exit $?

echo "[******************]"
echo "[* Running pylint *]"
echo "[******************]"
MIN_PYLINT_SCORE=9.0
pylint --rcfile=../.pylintrc ../src/glados > pylint.tmp
cat pylint.tmp | tail -n2
cat pylint.tmp

echo "[**********************]"
echo "[* Running Unit Tests *]"
echo "[**********************]"
OMIT=../src/glados/__main__.py
coverage run -m unittest discover unit_tests -p "*test.py" -b
COVERAGE_REPORT=.coverage.tmp
coverage report -m > $COVERAGE_REPORT

echo ""
echo "[********************]"
echo "[* Running Coverage *]"
echo "[********************]"
cat $COVERAGE_REPORT

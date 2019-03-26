#!/usr/bin/env bash
set -x
# W0703: Catching too general exception
# C0111: missing-docstring
# E0401: import-error (we hook import cutter)
# E0611: No name X in module Y
# C0200: Consider using enumerate instead of iterating with range and len
# R0903: too-few-public-methods
# W0511: fixme
pylint --disable=W0511,R0903,C0200,E0611,W0703,C0111,I1101,E0401 \
       --ignore=autogen,plugin_interface.py cutterdrcov_plugin
lint1=$?
# C0413: wrong-import-position
# R0201: no-self-use (use method as function)
pylint --disable=C0413,C0111,R0201,R0903,E0401 unittest/*.py
lint2=$?
if [ $lint1 -ne 0 ]; then
	exit $lint1
fi
if [ $lint2 -ne 0 ]; then
	exit $lint2
fi

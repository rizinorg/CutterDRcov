#!/usr/bin/env bash
set -x

./scripts/lint.sh
lint_result=$?
coverage run -m unittest discover unittest
if [ $lint_result -ne 0 ]; then
	exit $lint_result
fi


#!/usr/bin/env bash
set -x

./scripts/lint.sh
python unittest

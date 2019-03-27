# CutterDRcov - DynamoRIO Coverage Visualizer for Cutter

![Screenshot](screanshots/overview.jpg?raw=true)

[![Build Status](https://travis-ci.org/oddcoder/CutterDRcov.svg?branch=master)](https://travis-ci.org/oddcoder/CutterDRcov)
[![codecov](https://codecov.io/gh/oddcoder/CutterDRcov/branch/master/graph/badge.svg)](https://codecov.io/gh/oddcoder/CutterDRcov)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/oddcoder/CutterDRcov.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/oddcoder/CutterDRcov/context:python)

## Introduction

CutterDrcov is code coverage plugin that visualize DynamoRIO
[drcov](http://dynamorio.org/docs/page_drcov.html) into [Cutter](https://cutter.re)
static analysis.

IDA or Binary ninja user? checkout
[lighthouse](https://github.com/gaasedelen/lighthouse)

## Installation
First, locate the folder used by cutter for loading plugins, you can find it
from inside cutter by going to *Edit menu* → *preferences* and finally
selecting *Plugins*.
![pathlocation](screanshots/path.jpg?raw=true)

Inside that folder you will want to go *python* folder,
[download](https://github.com/oddcoder/CutterDRcov/archive/master.zip) this
repository, and move *cutterdrcov_plugin* folder there.

## Usage

First you will need to get some drcov trace, you can get DynamoRIO from their
official repository [here](https://github.com/DynamoRIO/dynamorio/releases).

For example, on 64Bit linux to get coverage trace by issuing this shell command:

```sh
$ dynamoRIO/bin64/drrun -t drcov -- [program name] [arguments]
```
Finally you will need to load that trace into CutterDRcov!

![usage](screanshots/usage.gif?raw=true)

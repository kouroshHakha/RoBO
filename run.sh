#!/usr/bin/env bash

export NGSPICE_TMP_DIR=/tmp
source ./.pypath
export PYTHONHASHSEED=0
exec python $@
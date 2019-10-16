#!/bin/bash
# WSL restrictions force insanity with respect to paths when using Windows Docker Desktop
#
#./dockerrun.sh /c/Users/cfesler/src/kairos/proto /c/Users/cfesler/src/out

IN_DIR=$1
OUT_DIR=$2
docker run -ti --mount type=bind,source="${OUT_DIR}",target=/out --mount type=bind,source="${IN_DIR}",target=/in pb_uml:latest /bin/bash /gen_uml.sh

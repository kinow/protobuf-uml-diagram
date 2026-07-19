#!/usr/bin/env bash

set -euo pipefail

# Example:
# ./dockerrun.sh /home/kinow/proto /home/kinow/src/out

if (($# != 2)); then
    echo "Usage: $0 <input-dir> <output-dir>" >&2
    exit 1
fi

IN_DIR=$1
OUT_DIR=$2

docker run \
    --mount "type=bind,source=${OUT_DIR},target=/out" \
    --mount "type=bind,source=${IN_DIR},target=/in" \
    pb_uml:latest

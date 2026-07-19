#!/usr/bin/env bash

set -euo pipefail

PROTO_PATH="/in"
PYTHONPATH="/out/python"

echo "MODULE:${MODULE:-}"

mkdir -p "${PYTHONPATH}"

mapfile -d '' proto_files < <(find "${PROTO_PATH}" -name '*.proto' -print0)

if ((${#proto_files[@]} == 0)); then
    echo "No .proto files found in ${PROTO_PATH}" >&2
    exit 1
fi

protoc \
    --proto_path="${PROTO_PATH}" \
    -I=/usr/include \
    --python_out="${PYTHONPATH}" \
    "${proto_files[@]}"

export PYTHONPATH

for proto_file in "${proto_files[@]}"; do
    module="${proto_file#/in/}"
    module="${module//\//.}"
    module="${module%.proto}_pb2"

    protobuf-uml-diagram \
        --proto "${module}" \
        --output=/out \
        --format png

    protobuf-uml-diagram \
        --proto "${module}" \
        --output=/out \
        --format svg
done

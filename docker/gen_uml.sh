#!/bin/bash
PROTO_PATH="/in"
echo "MODULE:${MODULE}"
PYTHONPATH="/out/python"

mkdir -p ${PYTHONPATH}

protoc --proto_path=${PROTO_PATH} -I=/usr/include --python_out=${PYTHONPATH} $(find ${PROTO_PATH} -name '*.proto')

export PYTHONPATH
for p in $(find ${PROTO_PATH} -name '*.proto'); do
    p="${p/\/in\//}"
    p="${p/\//.}"
    p="${p/.proto/_pb2}"
    python protobuf_uml_diagram.py --proto ${p} --output=/out
done

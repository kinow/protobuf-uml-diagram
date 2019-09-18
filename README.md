[![Build Status](https://travis-ci.org/kinow/protobuf-uml-diagram.svg?branch=master)](https://travis-ci.org/kinow/protobuf-uml-diagram)
[![codecov](https://codecov.io/gh/kinow/protobuf-uml-diagram/branch/master/graph/badge.svg)](https://codecov.io/gh/kinow/protobuf-uml-diagram)


# Protobuf UML diagram

A tool to generate UML diagrams from Protobuf compiled .proto files.

_Usage_:

```bash
$ protobuf-uml-diagram --proto "cylc.flow.ws_messages_pb2" --output /tmp/
```

_Logging output_:

```bash
INFO:__main__:Importing compiled proto cylc.flow.ws_messages_pb2
INFO:__main__:Writing PNG diagram to /tmp/ws_messages_pb2.png
```

_Image output_:

![example output](example-output.png "Example output")

## Installation

```bash
$ git clone https://github.com/kinow/protobuf-uml-diagram.git
$ cd protobuf-uml-diagram
$ pip install .
$ protobuf-uml-diagram
```

## Alternative to installation

Generate UML diagrams from all (uncompiled) `.proto` files in a directory:

```
./dockerbuild.sh
./dockerrun.sh <path_containing_proto_files> <output_path>
```

## License

Apache License

[![PyPI](https://img.shields.io/pypi/v/protobuf-uml-diagram.svg?color=yellow)](https://pypi.org/project/protobuf-uml-diagram/)
[![License](https://img.shields.io/github/license/kinow/protobuf-uml-diagram.svg?color=lightgrey)](https://github.com/kinow/protobuf-uml-diagram/blob/master/LICENSE.txt)
[![CI](https://github.com/kinow/protobuf-uml-diagram/actions/workflows/main.yml/badge.svg?branch=master&event=push)](https://github.com/kinow/protobuf-uml-diagram/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/kinow/protobuf-uml-diagram/branch/master/graph/badge.svg)](https://codecov.io/gh/kinow/protobuf-uml-diagram)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/X8X1618T2)

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

![example output](https://raw.githubusercontent.com/kinow/protobuf-uml-diagram/master/example-output.png "Example output")

## Installation

```bash
$ pip install protobuf-uml-diagram
$ protobuf-uml-diagram
```

### Development

```bash
$ git clone https://github.com/kinow/protobuf-uml-diagram.git
$ cd protobuf-uml-diagram
$ pip install -e .
$ protobuf-uml-diagram
```

### Docker

Generate UML diagrams from all (not compiled) `.proto` files in a directory:

```
./dockerbuild.sh
./dockerrun.sh <path_containing_proto_files> <output_path>
```

## License

Apache License

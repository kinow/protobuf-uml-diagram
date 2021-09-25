#!/usr/bin/env python

# Copyright 2019 Bruno P. Kinoshita
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Generate UML diagrams with graphviz from Protobuf compiled Python modules."""

import logging
from importlib import import_module
from io import StringIO
from pathlib import Path
from string import Template
from types import ModuleType
from typing import List, Tuple, Union

import click
from google.protobuf.descriptor import Descriptor, FieldDescriptor
from google.protobuf.descriptor_pb2 import FieldDescriptorProto
from graphviz import Source

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

Text = Union[str, bytes]


# https://github.com/pallets/click/issues/405#issuecomment-470812067
class PathPath(click.Path):
    """A Click path argument that returns a pathlib Path, not a string"""

    def convert(self, value: Text, param: Text, ctx) -> Path:
        """Convert a text parameter into a ``Path`` object.
        :param value: parameter value
        :type value: Text
        :param param: parameter name
        :type param: Text
        :param ctx: context
        :type ctx: object
        :return: a ``Path`` object
        :rtype: Path
        """
        return Path(super().convert(value, param, ctx))


# -- UML diagram

# These are the protobuf types. 11 is the message type, meaning another type
TYPES_BY_NUMBER = {
    number: text.lower().replace("type_", "")
    for text, number in FieldDescriptorProto.Type.items()
}


LABELS_BY_NUMBER = {
    number: text.lower().replace("label_", "")
    for text, number in FieldDescriptorProto.Label.items()
}


def _process_module(proto_module: ModuleType) -> Tuple[List[str], List[str]]:
    """"
    :return: list of descriptors
    :rtype: List[Descriptor]
    """
    classes = []
    relationships = []
    for type_name, type_descriptor in proto_module.DESCRIPTOR.message_types_by_name.items():
        _process_descriptor(type_descriptor, classes, relationships)
    return classes, relationships


def _process_descriptor(descriptor: Descriptor, classes: list,
                        relationships: list) -> None:
    """
    :param descriptor: a Protobuf descriptor
    :type descriptor: Descriptor
    :param classes: list of classes
    :type classes: list
    """
    type_template_text = StringIO()
    this_node = descriptor.full_name
    type_template_text.write(
        f"""    \"{this_node}\"[label = "{{{this_node}|""")
    fields = []
    for _field in descriptor.fields:
        if _field.type == FieldDescriptor.TYPE_MESSAGE:
            that_node = _field.message_type.full_name

            # is it a repeated field?
            label = LABELS_BY_NUMBER[_field.label]
            if label == 'repeated':
                relationships.append(f"    \"{that_node}\"->\"{this_node}\" [dir=backward;arrowhead=odiamond,arrowtail=normal;headlabel=\"1\";taillabel=\"0..*\"]")
            else:
                relationships.append(f"    \"{this_node}\"->\"{that_node}\" [arrowhead=none;headlabel=\"1\";taillabel=\"1\"]")

            field_type = that_node  # so we replace the 'message' token by the actual name
        else:
            field_type = TYPES_BY_NUMBER[_field.type]

        fields.append(f"+ {_field.full_name}:{field_type}")

    # add fields
    type_template_text.write("\\n".join(fields))
    type_template_text.write("}\"]")
    classes.append(type_template_text.getvalue())

    type_template_text.close()

    # nested types
    for nested_descriptor in descriptor.nested_types:
        _process_descriptor(nested_descriptor, classes, relationships)
    # TODO: what about extension, enum, ...?


def _get_uml_template(proto_module: ModuleType) -> str:
    """
    Return the graphviz dot template for a UML class diagram.
    :param proto_module: protobuf module
    :type proto_module: ModuleType
    :return: UML template
    :rtype: str
    """
    classes, relationships = _process_module(proto_module)
    uml_template = Template("""
digraph "Protobuf UML class diagram" {
    fontname="Bitstream Vera Sans"
    fontsize=10
    node[shape=record,style=filled,fillcolor=gray95,fontname="Bitstream Vera Sans",fontsize=8]
    edge[fontname="Bitstream Vera Sans",fontsize=8]

$classes

$relationships
}""")
    return uml_template.substitute(
        classes="\n".join(classes),
        relationships="\n".join(relationships))


# -- Protobuf Python module load

def _module(proto: str) -> ModuleType:
    """
    Given a protobuf file location, it will replace slashes by dots, drop the
    .proto and append _pb2.

    This works for the current version of Protobuf, and loads this way the
    Protobuf compiled Python module.
    :param proto:
    :return: Protobuf compiled Python module
    :rtype: ModuleType
    """
    if proto.endswith('.proto'):
        no_extension = f'{proto[:-len(".proto")]}_pb2'
    else:
        no_extension = proto
    return import_module(no_extension.replace("/", "."))


# -- Diagram builder

class Diagram:
    """A diagram builder."""

    _proto_module: ModuleType = None
    _rendered_filename: str = None
    _file_format = "png"

    def from_file(self, proto_file: str):
        if not proto_file:
            raise ValueError("Missing proto file!")
        try:
            self._proto_module = _module(proto_file)
        except ModuleNotFoundError as e:
            logger.error(f'Failed to import {proto_file}')
            raise e
        logger.info(f"Imported: {proto_file}")
        return self

    def to_file(self, output: Path):
        if not output:
            raise ValueError("Missing output location!")
        uml_file = Path(self._proto_module.__file__).stem
        self._rendered_filename = str(output.joinpath(uml_file))
        return self

    def with_format(self, file_format: str):
        if not file_format:
            raise ValueError("Missing file format!")
        self._file_format = file_format
        return self

    def build(self):
        if not self._proto_module:
            raise ValueError("No Protobuf Python module!")
        if not self._rendered_filename:
            raise ValueError("No output location!")
        if not self._file_format:
            raise ValueError("No file format!")

        uml_template = _get_uml_template(self._proto_module)

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("UML template:")
            logger.debug(uml_template)

        src = Source(uml_template)
        src.format = self._file_format
        logger.info(
            f"Writing diagram to {self._rendered_filename}.{self._file_format}")
        src.render(filename=self._rendered_filename, view=False, cleanup=True)


# -- main method

@click.command()
@click.option('--proto', required=True,
              help='Compiled Python proto module (e.g. some.package.ws_compiled_pb2).')
@click.option('--output', type=PathPath(file_okay=False), required=True,
              help='Output directory.')
def main(proto: str, output: Path) -> None:
    Diagram() \
        .from_file(proto) \
        .to_file(output) \
        .build()


if __name__ == '__main__':
    main()

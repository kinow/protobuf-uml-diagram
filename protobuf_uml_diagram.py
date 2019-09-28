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

import logging
from importlib import import_module
from io import StringIO
from pathlib import Path

import click
from google.protobuf.descriptor_pb2 import FieldDescriptorProto
from graphviz import Source

from types import ModuleType

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# https://github.com/pallets/click/issues/405#issuecomment-470812067
class PathPath(click.Path):
    """A Click path argument that returns a pathlib Path, not a string"""

    def convert(self, value, param, ctx) -> Path:
        return Path(super().convert(value, param, ctx))


def _get_uml_filename(module_filename) -> str:
    """
    Return the UML file name, for a given Python module name.
    :param module_filename: e.g. cylc.flow.ws_messages_proto.pb2.
    :type module_filename: str
    :return: UML file name (e.g. ws_messages_proto).
    :rtype: str
    """
    return Path(module_filename).stem


def _get_message_mapping(types: dict) -> dict:
    """
    Return a mapping with the type as key, and the index number.
    :param types: a dictionary of types with the type name, and the message type
    :type types: dict
    :return: message mapping
    :rtype: dict
    """
    message_mapping = {}
    entry_index = 2  # based on the links found, they normally start with 2?
    for _type, message in types.items():
        message_mapping[_type] = entry_index
        entry_index += 1
    return message_mapping


def _get_uml_template(*, types: dict, type_mapping: dict, message_mapping: dict) -> str:
    """
    Return the graphviz dot template for a UML class diagram.
    :param types: protobuf types with indexes
    :param type_mapping: a mapping for the protobuf type indexes and the type text
    :param message_mapping: a dict with which messages were linked, for the relationships
    :return: UML template
    :rtype: str
    """
    relationships = []
    classes = []

    uml_template = """
        digraph "Protobuf UML class diagram" {
            fontname = "Bitstream Vera Sans"
            fontsize = 8

            node [
                fontname = "Bitstream Vera Sans"
                fontsize = 8
                shape = "record"
                style=filled
                fillcolor=gray95
            ]

            edge [
                fontname = "Bitstream Vera Sans"
                fontsize = 8

            ]

    CLASSES

    RELATIONSHIPS
        }
        """

    entry_index = 2
    for _type, message in types.items():
        type_template_text = StringIO()
        type_template_text.write(f"""    {entry_index}[label = "{{{_type}|""")
        fields = []
        for _field in message.fields:
            message_type = _field.message_type
            field_type = type_mapping[_field.type]  # this will be 'message' if referencing another protobuf message

            if message_type:
                this_node = message_mapping[_type]
                that_node = message_mapping[message_type.name]
                relationships.append(f"    {this_node}->{that_node}")
                field_type = message_type.name  # so we replace the 'message' token by the actual name

            fields.append(f"+ {_field.name}:{field_type}")

        # add fields
        type_template_text.write("\\n".join(fields))
        type_template_text.write("}\"]\n")
        entry_index += 1
        classes.append(type_template_text.getvalue())

        type_template_text.close()

    uml_template = uml_template.replace("CLASSES", "\n".join(classes))
    uml_template = uml_template.replace("RELATIONSHIPS", "\n".join(relationships))
    return uml_template


@click.command()
@click.option('--proto', required=True, help='Compiled Python proto module (e.g. some.package.ws_compiled_pb2).')
@click.option('--output', type=PathPath(file_okay=False), required=True, help='Output directory.')
def main(proto: str, output: Path) -> None:
    type_mapping={}
    message_mapping={}
    types={}
    proto_file=_module(proto)
    logger.info(f"Imported: {proto_file}")
    _build_mappings(proto_file, types, type_mapping, message_mapping)

    uml_template = _get_uml_template(types=types, type_mapping=type_mapping, message_mapping=message_mapping)

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("UML template:")
        logger.debug(uml_template)

    src = Source(uml_template)
    src.format = "png"
    rendered_filename = str(output.joinpath(_get_uml_filename(proto_file.__file__)))
    logger.info(f"Writing PNG diagram to {rendered_filename}.png")
    src.render(
        filename=rendered_filename,
        view=False,
        cleanup=True
    )


def _module(proto: str) -> ModuleType:
    return import_module(proto.replace(".proto", "_pb2").replace("/", "."))


def _build_mappings(proto_file, types:dict, type_mapping: dict, message_mapping: dict) -> None:

    # a mapping with values such as 1: 'double', 9: 'string', etc.
    # to find the text value of a type
    type_mapping.update({number: text.lower().replace("type_", "") for text, number in FieldDescriptorProto.Type.items()})

    # our compiled type actually includes .DESCRIPTOR where we can find
    # introspection data
    types.update(proto_file.DESCRIPTOR.message_types_by_name)

    message_mapping.update(_get_message_mapping(types))

    for _dep in proto_file.DESCRIPTOR.dependencies:
        _build_mappings(_module(_dep.name), types, type_mapping, message_mapping)


if __name__ == '__main__':
    main()

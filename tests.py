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

import os
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import ANY

import pytest

import protobuf_uml_diagram
from protobuf_uml_diagram import PathPath, Diagram


def test_path_path():
    """Test the converter used for the command line args."""
    path_path = PathPath()
    path = path_path.convert(value="blue", param="color", ctx=None)  # type: ignore
    assert isinstance(path, Path)


def test_from_file_raises():
    with pytest.raises(ValueError) as e:
        Diagram().from_file('')
    assert 'Missing proto file' in str(e.value)


def test_to_file_raises():
    with pytest.raises(ValueError) as e:
        Diagram().to_file(None)  # type: ignore
    assert 'Missing output location' in str(e.value)


def test_with_format_raises():
    with pytest.raises(ValueError) as e:
        Diagram().with_format(None)  # type: ignore
    assert 'Missing file' in str(e.value)


def test_build_raises():
    with pytest.raises(ValueError) as e:
        Diagram().build()
    assert 'No Protobuf' in str(e.value)

    with pytest.raises(ValueError) as e:
        Diagram() \
            .from_file('test_data.data_messages.proto') \
            .build()
    assert 'No output' in str(e.value)

    with pytest.raises(ValueError) as e:
        d = Diagram() \
            .from_file('test_data.data_messages.proto') \
            .to_file(Path('abc'))
        d._file_format = None
        d.build()
    assert 'No file format' in str(e.value)


def test_happy_path():
    with TemporaryDirectory() as tmpdir:
        tf = os.path.join(tmpdir, 'diagram.png')
        Diagram() \
            .from_file('test_data.data_messages.proto') \
            .to_file(Path(tf)) \
            .with_format('png') \
            .build()
        assert os.path.getsize(tf) > 0


def test_homonymous(mocker):
    """A test for when you have two 'subclasses' with same names."""
    spy = mocker.spy(protobuf_uml_diagram, '_get_field_name')
    with TemporaryDirectory() as tmpdir:
        tf = os.path.join(tmpdir, 'diagram.png')
        Diagram() \
            .from_file('test_data.issue_10.proto') \
            .to_file(Path(tf)) \
            .with_format('png') \
            .build()
        assert os.path.getsize(tf) > 0
    spy.assert_called_with(descriptor=ANY, full_names=True)


def test_homonymous_user_does_not_care(mocker):
    """A test for when you have two 'subclasses' with same names, but you do not care."""
    spy = mocker.spy(protobuf_uml_diagram, '_get_field_name')
    with TemporaryDirectory() as tmpdir:
        tf = os.path.join(tmpdir, 'diagram.png')
        Diagram() \
            .from_file('test_data.issue_10.proto') \
            .to_file(Path(tf)) \
            .with_format('png') \
            .with_full_names(False) \
            .build()
        assert os.path.getsize(tf) > 0
    spy.assert_called_with(descriptor=ANY, full_names=False)


def test_logs_module_not_found():
    with pytest.raises(ModuleNotFoundError) as e:
        Diagram() \
            .from_file('piracicaba') \
            .build()
    assert 'piracicaba' in str(e)


def test_contains_dot_proto_in_middle_of_the_name():
    """A test where the input data contains .proto, but doesn't end with it."""
    with TemporaryDirectory() as tmpdir:
        tf = os.path.join(tmpdir, 'diagram.png')
        Diagram() \
            .from_file('test_data.issue_27.proto.configs_data_pb2') \
            .to_file(Path(tf)) \
            .with_format('png') \
            .build()
        assert os.path.getsize(tf) > 0


def test_to_file_with_missing_protobuf():
    """A test where the protobuf module is missing."""
    with TemporaryDirectory() as tmpdir:
        tf = os.path.join(tmpdir, 'diagram.png')
        d = Diagram().from_file('test_data.issue_27.proto.configs_data_pb2')
        d._proto_module = None
        with pytest.raises(ValueError) as cm:
            d.to_file(Path(tf))
        assert str(cm.value) == 'Missing protobuf module!'


def test_to_file_with_protobuf_missing_file():
    """A test where the protobuf module is present but invalid (no file)."""
    with TemporaryDirectory() as tmpdir:
        tf = os.path.join(tmpdir, 'diagram.png')
        d = Diagram().from_file('test_data.issue_27.proto.configs_data_pb2')
        d._proto_module = {}
        with pytest.raises(ValueError) as cm:
            d.to_file(Path(tf))
        assert str(cm.value) == 'Missing protobuf module!'


def test_enum1():
    """Verify we can parse when an enum is part of a message."""
    with TemporaryDirectory() as tmpdir:
        tf = os.path.join(tmpdir, 'diagram.png')
        Diagram() \
            .from_file('test_data.pr116.enum1_pb2') \
            .to_file(Path(tf)) \
            .with_format('png') \
            .build()
        assert os.path.getsize(tf) > 0


def test_enum2():
    """Verify we can parse when an enum is outside a message."""
    with TemporaryDirectory() as tmpdir:
        tf = os.path.join(tmpdir, 'diagram.png')
        Diagram() \
            .from_file('test_data.pr116.enum2_pb2') \
            .to_file(Path(tf)) \
            .with_format('png') \
            .build()
        assert os.path.getsize(tf) > 0

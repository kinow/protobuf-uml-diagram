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

from protobuf_uml_diagram import _get_uml_filename, _get_message_mapping


def test_get_uml_filename():
    assert _get_uml_filename("/tmp/name/test.txt") == "test"


def test_get_message_mapping():
    d = {
        1: "blue",
        2: "red",
        3: "green"
    }
    r = _get_message_mapping(d)
    assert {1: 2, 2: 3, 3: 4} == r

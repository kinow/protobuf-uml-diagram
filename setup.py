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

import codecs
from os.path import join, dirname, abspath

from setuptools import setup

here = abspath(dirname(__file__))


def read(*parts):
    with codecs.open(join(here, *parts), 'r') as fp:
        return fp.read()


install_requires = [
    "click>=7.1,<8.1",
    "graphviz>=0.14,<0.18",
    "protobuf>=3.13,<3.19"
]

setup_requires = [
    'pytest-runner>=4.1,<5.4'
]

tests_require = [
    'codecov==2.1.*',
    'coverage>=5.3,<5.6',
    'pytest-cov>=2.10,<2.13',
    'pytest>=6.1,<6.3',
    'pycodestyle>=2.6,<2.8'
]

extras_require = {
    'tests': tests_require,
    'all': install_requires + tests_require
}

setup(
    version="0.8",
    name="protobuf-uml-diagram",
    description="Create UML diagrams from Protobuf proto files",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": ["protobuf-uml-diagram=protobuf_uml_diagram:main"]
    },
    py_modules=['protobuf_uml_diagram'],
    python_requires='>=3.7',
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require=extras_require,
    setup_requires=setup_requires,
)

# Changes

## 0.8 (??-??-202?)

- Added dependabot to GitHub repository [e56ca23711ac0344cbb51a3ff4f93f23c8d42a5f](https://github.com/kinow/protobuf-uml-diagram/commit/e56ca23711ac0344cbb51a3ff4f93f23c8d42a5f)
- Update coverage requirement from ==5.3.* to >=5.3,<5.6 [#15](https://github.com/kinow/protobuf-uml-diagram/pull/15)
- Update pytest requirement from ==6.1.* to >=6.1,<6.3 [#18](https://github.com/kinow/protobuf-uml-diagram/pull/18)
- Update graphviz requirement from ==0.14.* to >=0.14,<0.17 [#16](https://github.com/kinow/protobuf-uml-diagram/pull/16)
- Update pytest-runner requirement from ==4.1.* to >=4.1,<5.4 [#14](https://github.com/kinow/protobuf-uml-diagram/pull/14)
- Update protobuf requirement from ==3.13.* to >=3.13,<3.16 [#17](https://github.com/kinow/protobuf-uml-diagram/pull/17)
- Move to GitHub Actions [#19](https://github.com/kinow/protobuf-uml-diagram/issues/19)
- Update pycodestyle requirement from ==2.6.* to >=2.6,<2.8 #22 [#22](https://github.com/kinow/protobuf-uml-diagram/pull/22)
- Update pytest-cov requirement from ==2.10.* to >=2.10,<2.12 [#21](https://github.com/kinow/protobuf-uml-diagram/pull/21)
- Update protobuf requirement from <3.16,>=3.13 to >=3.13,<3.17 [#23](https://github.com/kinow/protobuf-uml-diagram/pull/23)
- Update click requirement from ==7.1.* to >=7.1,<8.1 [#24](https://github.com/kinow/protobuf-uml-diagram/pull/24)
- Update protobuf requirement from <3.17,>=3.13 to >=3.13,<3.18 [#25](https://github.com/kinow/protobuf-uml-diagram/pull/25)
- Update pytest-cov requirement from <2.12,>=2.10 to >=2.10,<2.13 [#26](https://github.com/kinow/protobuf-uml-diagram/pull/26)

## 0.7 (06-10-2020)

- Fix TypeError: main() got an unexpected keyword argument 'fullname'
[#13](https://github.com/kinow/protobuf-uml-diagram/issues/13)

## 0.6 (24-07-2020)

- Release to include `sdist` distribution archive in PYPI

## 0.5 (27-05-2020)

- Support homonyms, by using protobuf full name of each entity
[#10](https://github.com/kinow/protobuf-uml-diagram/issues/10)

## 0.4 (03-03-2020)

- More shellcheck fixes in Docker commands
- Added support to aggregations, showing when a field is "repeated"
- Updated example image and test (happy path)

## 0.3 (17-10-2019)

- Added test coverage report
- Added more tests, and graphviz to CI pipeline
- Fixed shellcheck issues in Docker commands
- Add builder option and validation for file format (default to PNG)
- Added support for nested messages (issue #1)

## 0.2 (30-09-2019)

- Added Dockerfile (thanks to Chris Fesler)
- Better support to Protobuf FieldDescriptor types
- Add comments to code
- Implemented a builder for parameters
- Updated setup.py to include metadata for PYPI
- Added more tests

## 0.1 (22-05-2019)

- Initial prototype code, not released to PYPI, used as script in a [project](https://cylc.github.io/)

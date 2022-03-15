FROM python:3.9-buster
RUN apt-get update && apt-get install -y curl graphviz \
  && curl -L https://github.com/protocolbuffers/protobuf/releases/download/v3.7.1/protoc-3.7.1-linux-x86_64.zip -o protoc-3.7.1.zip \
  && unzip protoc-3.7.1.zip -d protoc-3.7.1 \
  && mv protoc-3.7.1/bin/* /usr/local/bin/ \
  && mv protoc-3.7.1/include/* /usr/local/include/ \
  && pip install -U setuptools \
  && pip install "click==7.0.*" "graphviz==0.10.*" "protobuf==3.7.*"
ADD docker/gen_uml.sh /
ADD protobuf_uml_diagram.py /
CMD [ "/bin/bash", "./run.sh" ]

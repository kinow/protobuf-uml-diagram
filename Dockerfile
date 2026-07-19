FROM python:3.10

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        graphviz \
        unzip \
    && rm -rf /var/lib/apt/lists/*

# Install protoc.
# Keep this version aligned with the protobuf versions tested against.
ARG PROTOC_VERSION=33.0

RUN curl -LO "https://github.com/protocolbuffers/protobuf/releases/download/v${PROTOC_VERSION}/protoc-${PROTOC_VERSION}-linux-x86_64.zip" \
    && unzip "protoc-${PROTOC_VERSION}-linux-x86_64.zip" -d /tmp/protoc \
    && mv /tmp/protoc/bin/protoc /usr/local/bin/ \
    && mv /tmp/protoc/include/* /usr/local/include/ \
    && rm -rf /tmp/protoc "protoc-${PROTOC_VERSION}-linux-x86_64.zip"

WORKDIR /app

COPY . .

RUN python -m pip install --upgrade pip setuptools wheel \
    && python -m pip install .

COPY docker/gen_uml.sh /usr/local/bin/gen_uml.sh
RUN chmod +x /usr/local/bin/gen_uml.sh

CMD ["/usr/local/bin/gen_uml.sh"]

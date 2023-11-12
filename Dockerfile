FROM alpine

RUN apk add python3 py3-pip py3-cffi
RUN pip install cryptography
RUN pip install bcrypt


COPY src/ /app
WORKDIR /app

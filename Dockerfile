FROM alpine

RUN apk add python3 py3-pip py3-cffi
RUN pip install cryptography
RUN pip install bcrypt

EXPOSE 5068


COPY src/ /app
WORKDIR /app

CMD ["python", "Goodchain.py"]
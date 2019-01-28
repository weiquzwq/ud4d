FROM python:3-alpine3.7

WORKDIR /usr/src/app
RUN pip install --no-cache-dir ud4d \
    && apk add --no-cache udev \
    && apk add --no-cache bash

COPY keep_alive.py .

CMD [ "python", "keep_alive.py" ]

FROM python:3-alpine3.7

WORKDIR /usr/src/app
COPY . .

# use `pip install -e .` for local usage
RUN pip install -e . \
    && apk add --no-cache udev \
    && apk add --no-cache bash

COPY keep_alive.py .

CMD [ "python", "keep_alive.py" ]

FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    python3.13 \
    python-pip \
    git

RUN pip3 intsall PyYAML  

COPY feed.py /usr/bin/feed.py
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
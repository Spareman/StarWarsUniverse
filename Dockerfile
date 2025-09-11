FROM ubuntu:latest
LABEL authors="manhl"

ENTRYPOINT ["top", "-b"]
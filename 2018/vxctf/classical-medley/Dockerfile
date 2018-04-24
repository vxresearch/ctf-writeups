FROM ubuntu:latest
RUN useradd -m medley &&\
    apt-get update &&\
    apt-get install -y python-pip build-essential socat libgmp3-dev libmpfr-dev libmpc-dev &&\
    pip install pycrypto gmpy2 &&\
    apt-get autoremove -y build-essential
WORKDIR /home/medley
ADD nc .
USER medley
CMD socat TCP-LISTEN:10001,reuseaddr,fork EXEC:"stdbuf -i0 -o0 -e0 python main.py"
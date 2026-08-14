FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y openssh-client sshpass && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir ansible paramiko

RUN ansible-galaxy collection install cisco.ios

COPY . /app/

CMD ["ansible", "--version"]
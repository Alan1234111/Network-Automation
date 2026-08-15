FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y openssh-client sshpass && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.yml /app/

RUN pip install --no-cache-dir -r requirements.txt
RUN ansible-galaxy collection install -r requirements.yml

COPY . /app/

CMD ["ansible", "--version"]
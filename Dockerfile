FROM ubuntu:disco

COPY . /webrcon
WORKDIR /webrcon

RUN apt-get update && apt-get install -y python3 python3-pip git
RUN pip3 install pipenv
RUN env LANG=C.UTF-8 pipenv install --dev

CMD pipenv run app-prod

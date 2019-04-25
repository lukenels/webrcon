FROM python:3.7

ADD . /code
WORKDIR /code

RUN pip3 install pipenv
RUN env LANG=C.UTF-8 pipenv install --dev

CMD ["pipenv", "run", "app-prod"]

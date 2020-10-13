FROM python:3.8

RUN pip install pipenv

WORKDIR /var/task.layer
COPY Pipfile* ./
RUN pipenv lock -r >requirements.txt && pip install -r requirements.txt -t python

WORKDIR /var/task.function
COPY py py

CMD [ 'sh', '-c', 'exit 1']
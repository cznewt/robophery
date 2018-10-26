FROM python:3.6-slim

RUN \
    apt-get update && \
    apt-get install -y python3-dev python3-pip libxml2-dev libxslt1-dev libffi-dev build-essential libi2c-dev i2c-tools python-ftdi1 python-smbus && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && pip install pipenv

ADD Pipfile Pipfile.lock README.rst requirements.txt requirements_tests.txt setup.py /app/
WORKDIR /app
RUN pipenv install --system --deploy --dev
ADD robophery/ /app/robophery/

RUN useradd --system robophery && \
    python setup.py install && \
    chown -R robophery:robophery /app/

USER robophery

ENV PYTHONUNBUFFERED 1
ENV PROCESSES 1

CMD ["rp_manager"]

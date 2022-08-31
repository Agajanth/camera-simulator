FROM python:3.10

RUN mkdir /camera_simulator

RUN mkdir /tests

COPY /camera_simulator /camera_simulator

COPY /tests /camera_simulator

COPY pyproject.toml /camera_simulator

WORKDIR /camera_simulator

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip3 install poetry

RUN poetry config virtualenvs.create false

RUN poetry install

ENV PATH="/root/.poetry/bin:$PATH"

CMD ["pytest"]

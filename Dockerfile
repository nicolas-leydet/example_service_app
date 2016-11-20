FROM python:3.5

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

COPY simple_api ./simple_api

WORKDIR .
ENV PYTHONPATH .

ENTRYPOINT ["python"]
CMD ["simple_api/server.py"]

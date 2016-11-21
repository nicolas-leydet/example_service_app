FROM python:3.5

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

COPY knogget ./knogget

WORKDIR .
ENV PYTHONPATH .

ENTRYPOINT ["python"]
CMD ["knogget/server.py"]

FROM python:3.12.2
WORKDIR /code
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY flask /code
CMD ["python3", "-u", "server.py"]

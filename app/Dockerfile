FROM python:latest
WORKDIR /code
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY flask /code
CMD ["python3", "-u", "server.py"]

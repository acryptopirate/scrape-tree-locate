FROM python:3.9

RUN mkdir /code
WORKDIR /code

ADD main.py .
ADD requirements.txt .
RUN pip install -r requirements.txt
CMD ["python3.9", "main.py"]
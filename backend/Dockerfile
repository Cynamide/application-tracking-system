FROM python:3.11-slim-buster

WORKDIR /backend

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN pwd

RUN cd ..

RUN pwd

EXPOSE 5000

CMD [ "flask", "run","--host=0.0.0.0"]

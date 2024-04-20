FROM python:3.10

RUN mkdir /myplaner-app

WORKDIR /myplaner-app

COPY requirments.txt . 

RUN pip install -r requirments.txt

RUN pip install gunicorn

COPY . .

RUN chmod a+x docker/*.sh

# WORKDIR src

# CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000

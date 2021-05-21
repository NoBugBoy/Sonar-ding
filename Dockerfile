FROM python:3.8-slim-buster
WORKDIR /app
ADD ./ /app
RUN pip install -r requirement.txt
CMD [ "python", "/app/run.py" ]

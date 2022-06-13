FROM python:latest
WORKDIR /regim/
COPY . .
COPY wsgi.py .
RUN pip install -r ./requirements.txt
CMD [ "python", "wsgi.py" ]
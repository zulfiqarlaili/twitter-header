FROM python:3.8-slim-buster
WORKDIR /app
COPY . .
RUN pip3 install --no-cahce-dir -r requirement.txt
CMD [ "python", "update-header.py" ]
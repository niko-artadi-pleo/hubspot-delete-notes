#FROM python:3.9.13-alpine3.16
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

# install project dependencies
ADD requirements.txt .
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Add project files
ADD delete_notes.py .

CMD ["python3", "./delete_notes.py"]
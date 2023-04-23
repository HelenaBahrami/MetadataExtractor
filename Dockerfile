FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN groupadd -r nrtv && useradd -r -g nrtv nrtv

COPY ./metadata_extractor/ .

RUN chown -R nrtv:nrtv /app

RUN chmod +x /app/image_metadata_extractor.py

USER nrtv

ENTRYPOINT [ "python", "image_metadata_extractor.py" ]

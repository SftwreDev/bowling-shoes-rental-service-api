FROM python:3.12-slim-bookworm
ENV PYTHONUNBUFFERED 1
RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean

WORKDIR /code
# Install packages
COPY . .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app /code/app

COPY start /start
RUN chmod +x /start
CMD ["bash", "/start"]
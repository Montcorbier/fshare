FROM python:2.7

RUN apt-get update
RUN apt-get -y install rubygems ruby-full
RUN gem install --no-rdoc --no-ri sass -v 3.4.22
RUN gem install --no-rdoc --no-ri compass

RUN mkdir -p /app/fshare
COPY fshare/requirements.txt /app/fshare
WORKDIR /app

RUN pip install -r fshare/requirements.txt

COPY ./fshare /app
WORKDIR /app/website/static/website
RUN compass compile

WORKDIR /app

RUN ./manage.py collectstatic --noinput

CMD uwsgi \
	--http :8000 \
	--module fshare.wsgi \
	--socket fshare.sock


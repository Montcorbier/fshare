docker run -v `pwd`/fshare:/app -w /app/website/static/website fshare compass compile
docker run -v `pwd`/fshare:/static fshare ./manage.py collectstatic --noinput
docker run -v `pwd`/fshare:/static fshare ./manage.py migrate
docker run -v `pwd`/fshare:/app -w /app/website/static/website fshare compass compile
docker run -v `pwd`/fshare:/app -v `pwd`/static:/static fshare ./manage.py collectstatic --noinput
docker run -v `pwd`/fshare:/app fshare ./manage.py migrate
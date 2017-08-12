git pull origin master
docker build -t fshare .
sh scripts/build.sh
docker restart fshare
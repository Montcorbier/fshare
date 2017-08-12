docker run -it \
	-p 8000:8000 \
	-v `pwd`/fshare:/app \
	-v `pwd`/static:/static \
	-v /opt/sockets/fshare.sock:/app/fshare.sock \
	--name fshare \
	-d fshare
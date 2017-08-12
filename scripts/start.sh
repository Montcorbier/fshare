docker run -it \
	-p 8000:8000 \
	-v `pwd`/fshare:/app \
	-v `pwd`/static:/static \
	--name fshare \
	-d fshare
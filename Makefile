deploy:
	rsync -av --exclude=images \
	    --exclude=.git \
	    --exclude=images_annotated \
	    --exclude=bak_images \
	    --exclude=.idea \
	    --exclude=__pycache__ \
	    --exclude=*/__pycache__ \
	    -e ssh ./ pi@jesseraspberrypi.local:/home/pi/Documents/tree

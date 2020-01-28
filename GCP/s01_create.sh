gcloud compute instances create greenbuildings1\
		--zone=us-central1-a\
		--machine-type=n1-standard-2\
		--tags=http-server,https-server\
		--image=ubuntu-1604-xenial-v20190816 \
		--image-project=ubuntu-os-cloud\
		--boot-disk-size=12GB\
		--boot-disk-type=pd-standard\
		--boot-disk-device-name=greenbuildings1
		# --image=cos-73-11647-267-0\
		# --image-project=cos-cloud\



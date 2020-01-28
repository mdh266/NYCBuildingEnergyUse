gcloud compute firewall-rules create greenbuildings\
			 --direction=INGRESS \
			 --priority=1000 \
			 --network=default \
			 --action=ALLOW \
			 --rules=tcp:8888


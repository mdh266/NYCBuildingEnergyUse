Serve Model using MLflow:

	mlflow models serve --m XGBModel

Build & Serve Model With MLflow + Docker:

	mlflow models build-docker -m XGBModel -n xgbmodel

	docker run -ip 8000:8080 xgbmodel

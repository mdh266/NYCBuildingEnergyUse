# About
-------------
I originally started this project a while back with a goal of taking the 2016 NYC Benchmarking Law data about building energy usage and do something interesting with it. After a few iterations I thought it might be interesting to see if I could predict the emission of green house gases from buildings by looking at their age, and water consumption as well as other energy consumption metrics. In the end the point of this project was to build and deploy a model on the cloud using a real world dataset with outliers and missing values using state of the art tools such as,

* [Seaborn](http://seaborn.pydata.org/)
* [Scikit-Learn](https://scikit-learn.org)
* [XGBoost](https://xgboost.readthedocs.io/en/latest/)
* [BigQuery](https://cloud.google.com/bigquery)
* [MLflow](https://www.mlflow.org/) 
* [Docker](https://www.docker.com/)
* [Google Appe Engine](https://cloud.google.com/appengine)


## Notebook Overviews
--------------------------


### GreenBuildings1 : Exploratory Analysis & Outlier Removal
---------------------
In this first blogpost I will cover how to perform the basics of data cleaning including:

- Exploratory data analysis
- Identifying and removing outliers

In indentifying outliers I will cover both visual inspection as well a machine learning method called [Isolation Forests](https://en.wikipedia.org/wiki/Isolation_forest).  Since I will completing this project over multiple days and using [Google Cloud](https://cloud.google.com/), I will go over the basics of using [BigQuery](https://cloud.google.com/bigquery) for storing the datasets so I won't have to start all over again each time I work on it. At the end of this blogpost I will summarize the findings, and give some specific recommendations to reduce mulitfamily and office building energy usage.



### GreenBuildings2 : Imputing Missing Values With Scikit-Learn
---------------------
In this second post I cover [imputations techniques](https://en.wikipedia.org/wiki/Imputation_(statistics)#Regression) for missing data using Scikit-Learn's [impute module](https://scikit-learn.org/stable/modules/impute.html) using both point estimates (i.e. mean, median) using the **[SimpleImputer](https://scikit-learn.org/stable/modules/generated/sklearn.impute.SimpleImputer.html)** class as well as more complicated regression models (i.e. KNN) using the **[IterativeImputer](https://scikit-learn.org/stable/modules/generated/sklearn.impute.IterativeImputer.html)** class. The later requires that the features in the model are correlated.  This is indeed the case for our dataset and in our particular case we also need to [transform](https://en.wikipedia.org/wiki/Data_transformation_(statistics)) the feautres in order to discern a more meaningful and predictive relationship between them. As we will see, the transformation of the features also gives us much better results for imputing missing values.


### GreenBuildings3: Build & Deploy Models With MLflow, Docker & Google App Engine
---------------------
This last post will deal with model building and model deployment. Specifically I will build a model of New York City building green house gas emissions based on the building energy usage metrics. After I build a sufficiently accurate model I will convert the model to [REST API](https://restfulapi.net/) for serving and then deploy the REST API to the cloud. The processes of model development and deployment are made a lot easier with [MLflow](https://mlflow.org/) library. Specifically, I will cover using the [MLflow Tracking](https://www.mlflow.org/docs/latest/tracking.html) framework to log all the diffent models I developed as well as their performance. MLflow tracking acts a great way to memorialize and document the development process. I will then use [MLflow Models](https://www.mlflow.org/docs/latest/models.html) to convert the selected model into a [REST API](https://restfulapi.net/) for model servin and show how to the API to the cloud using [Docker](https://www.docker.com/) and [Google App Engine](https://cloud.google.com/appengine). 


### Using The Notebooks
----------------------

You can install the dependencies and access the first two notebook (`GreenBuildings1` & (`GreenBuildings2`) using <a href="https://www.docker.com/">Docker</a> by building the Docker image with the following:

	docker build -t greenbuildings .

Followed by running the command container:

	docker run -ip 8888:8888 -v `pwd`:/home/jovyan -t greenbuildings

See <a href="https://jupyter-docker-stacks.readthedocs.io/en/latest/index.html">here</a> for more info.  Otherwise without Docker, make sure to use Python 3.7 and install <a href="http://geopandas.org/">GeoPandas</a> (0.3.0) using <a href="https://conda.io/en/latest/">Conda</a> as well as the additional libraries listed in <code>requirements.txt</code>.  These can be installed with the command,

	pip install -r requirements.txt

The last notebook (`GreenBuildings3`) I ran locally on my machine with the dependencies in `requirements.txt`.


### The Dataset 
------------------

The NYC Benchmarking Law requires owners of large buildings to annually measure their energy and water consumption in a process called benchmarking. The law standardizes this process by requiring building owners to enter their annual energy and water use in the U.S. Environmental Protection Agency's (EPA) online tool, ENERGY STAR Portfolio Manager® and use the tool to submit data to the City. This data gives building owners about a building's energy and water consumption compared to similar buildings, and tracks progress year over year to help in energy efficiency planning.

I used the 2016 Benchmarking data which is disclosed publicly and can be found <a href="http://www.nyc.gov/html/gbee/html/plan/ll84_scores.shtml">here</a>.  


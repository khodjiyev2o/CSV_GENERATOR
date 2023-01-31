CSV GENERATOR
Online service for generating CSV files with fake (dummy) data using
Python and Django:


Visit the [Deployed Version](http://54.180.202.8/) 

## Getting Started

1. Clone the project from the Github repo :

````
git clone https://github.com/khodjiyev2o/CSV_GENERATOR
````

2. Go to the project directory -> ./CSV GENERATOR

3. Create virtual environment :

````
python3 -m venv venv
````

4. Activate virtual environment  : 

````
source\venv\bin\activate
````

if you are using Windows ,then :

````
venv\Scripts\activate
````
if UNIX/LINUX, then :
````
source venv\bin\activate
````
4. Create the .env file and fill out the missing values. You can look at all missing values in sample.env file:

For example: 
````
AWS_DEFAULT_REGION="sa-east-1"
````
5. Build  the docker image

````

$ docker build -t app .

````
6. Run the docker container

````

$  docker run --restart=always --name csv_generator -dp 80:8000 app 

````
6. Run the docker with volumes for auto-update after code changes
```
docker run --rm -it --mount src="$(pwd)",target=/usr/src/app,type=bind -dp 8000:8000  app

```

7. Open your browser and paste one of the urls :

* http://127.0.0.1:80
* http://localhost:80
* http://0.0.0.0:80
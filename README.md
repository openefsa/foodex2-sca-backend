<p align="center">
	<img src="https://www.efsa.europa.eu/themes/custom/efsa_theme/logo.svg" alt="European Food Safety Authority"/>
</p>

# FoodEx2 Smart Coding Application (back-end)
The FoodEx2 Smart Coding Application is designed and developed internally in the European Food Safety Authority (DATA and AMU units). This project aims to simplify the FoodEx2 coding process of food starting from a given free text description. More specifically this is possible thanks to the use of FoodEx2 dedicated text classification (single and multi-label) models trained on historycal data.

<p align="center">
    <img src="https://github.com/openefsa/foodex2-sca-frontend/blob/master/src/asset/icons/FE2_POSI_icon.jpg" alt="FoodEx2_SCA"/>
</p>

# For Developers
Find below all the steps needed to run the project.

## Prerequisites
* [Python 3.8](https://www.python.org/downloads/release/python-388/)

## Clone and install
Clone the project locally in your workspace using the following command:
```
git clone https://github.com/openefsa/foodex2-sca-back-end.git
```

Move inside the project's folder just cloned and install all the required dependencies (listed in the requirements.txt file). Create a **python virutal environment** using the command:
```
python -m venv venv
```

Make sure that the virtual environment it is enabled in your terminal or IDE (check [here](https://docs.python.org/3/tutorial/venv.html) for additional information) and hence, run the following command in order to install all the dependencies using the dedicated python pip package installer:
```
pip install -r requirements.txt
```

## Set up env variables 
The file _/api/private.py_ contains services for handling feedback that can be transmitted directly by the user. Feedback must be sent, via a dedicated api (see next section), to the [Azure Storage](https://docs.microsoft.com/en-us/azure/storage/). Once you have successfully created an account and a table (to collect feedback), set the following credentials in the file:
- ACCOUNT_KEY
- ACCOUNT_KEY
- TABLE_NAME
- SECRET CODE

_Note that it is also possible to use the application without the feedback engine and therefore Azure Table Storage is not required. To do this, just comment out all the code inside the file._


## Models
The FoodEx2 SCA back-end project makes use of various text classification models [Spacy](https://spacy.io/). For more information on what data and how these models were trained check the [wiki](https://github.com/openefsa/foodex2-sca-backend/wiki).

**Note that the project makes use of Kubernates which automatically downloads and exports all required templates to the _work-dir_ folder. For testing purposes, without using Kubernates, this can also be done _locally_ by changing the model path in the _api/public.py_ file (check the _todo_ comments). By doing so, you can manually create your own folder that will contain the models (which can be built manually or downloaded and extracted).**


## Serve FoodEx2 SCA Locally
Several APIs are available on the FoodEx2 Smart Coding Application (check the [wiki](https://github.com/openefsa/foodex2-sca-backend/wiki) for additional information). To expose them, you need to serve the project using Flask. Run the following command from the project folder:
```
python app.py
```

# Deployment
The following section describes how to deploy the FoodEx2 Smart Coding Application's back-end locally.

## Docker build
Install [Docker](https://docs.docker.com/get-docker/) and configure it on your local computer. From the main folder of the foodex2-sca-backend project run the following command:
```
docker build -t name:tag
```

This command will use the **DOCKERFILE**, present in the main folder, for creating the docker image. Check if the docker image is present by launching the following command:
```
docker images
```

After making sure that the docker image has been correcly created, run it with the following command:
```
docker run name:tag
```

## Kubernates deployment
Deploy the docker image created on kubernates by using the files present under the *"/manifest"* folder by running the following command:
```
kubectl deploy -f create ./manifest/deployment.yml
```

# Project Under Development

<p align="center">
	<img src="http://www.efsa.europa.eu/profiles/efsa/themes/responsive_efsa/logo.png" alt="European Food Safety Authority"/>
</p>

## FoodEx2 Smart Coding Application (back-end)
The FoodEx2 Smart Coding Application is designed and developed internally in the European Food Safety Authority (DATA and AMU units). This project aims to simplify the FoodEx2 coding process of food starting from a given free text description. More specifically this is possible thanks to the use of FoodEx2 dedicated text classification models trained on historycal data. Please note that the various model functionalities are exposed through APIs. 

<p align="center">
    <img src="src/icons/FE2_POSI.jpg" alt="FoodEx2_SCA"/>
</p>

## For Developers
### Prerequisites
* [Python](https://www.python.org/downloads/)

## Clone and install
Clone the project locally in your workspace using the following command:
```
git clone https://github.com/openefsa/foodex2-sca-back-end.git
```

Now, move inside the project's folder just cloned and install all the required dependencies (listed in the requirements.txt file). Run the following command in order to automatically install all the dependencies using python pip package installer:
```
pip install -r requirements.txt
```

### Serve FoodEx2 SCA Locally
In order to expose the available APIs provided, it is needed to serve the project using Flask. Run the following command from the project's folder:
```
python app.py
```

Now the APIs can be reached from the url shown by appending to it the specific API name of interest (e.g. https://localhost/predictAll).

## Models
The FoodEx2 SCA back-end project allows to obtain a series of FoodEx2 suggestions starting from the description of the food given in input. This is possible thanks to [Spacy](https://spacy.io/) text classification models. More precisely, we have initiated different Spacy [en_core_web_md](https://spacy.io/models/en#en_core_web_md) models, each specific for its role (check the [wiki](wiki) for additional information), which have been then trained using the historical data collected by EFSA. In the current version of the FoodEx2 SCA back-end, the data collected in consumption has been used.

## Deployment
The following section describes how to deploy the FoodEx2 Smart Coding Application's back-end locally.

### Docker build
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

### Kubernates deployment
Deploy the docker image created on kubernates by using the files present under the *"/manifest"* folder by running the following command:
```
kubectl deploy -f create ./manifest/deployment.yml
```
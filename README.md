# Project Under Development

<p align="center">
	<img src="http://www.efsa.europa.eu/profiles/efsa/themes/responsive_efsa/logo.png" alt="European Food Safety Authority"/>
</p>

## FoodEx2 Smart Coding Application (back-end)
The FoodEx2 Smart Coding Application is designed and developed internally in the European Food Safety Authority (DATA and AMU units). This project aims to simplify the FoodEx2 coding process of food starting from a given free text description. More specifically this is possible thanks to the use of FoodEx2 dedicated text classification (single and multi-label) models trained on historycal data.

<p align="center">
    <img src="https://github.com/openefsa/foodex2-sca-frontend/blob/master/src/asset/icons/FE2_POSI_icon.jpg" alt="FoodEx2_SCA"/>
</p>

## For Developers
Find below all the steps needed to run the project.

### Prerequisites
* [Python 3.8](https://www.python.org/downloads/release/python-388/)

### Clone and install
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

### Set up env variables 
The file _/api/private.py_ contains services for handling feedback that can be transmitted directly by the user. Feedback must be sent, via a dedicated api (see next section), to the [Azure Storage](https://docs.microsoft.com/en-us/azure/storage/). Once you have successfully created an account and a table (to collect feedback), set the following credentials in the file:
- ACCOUNT_KEY
- ACCOUNT_KEY
- TABLE_NAME
- SECRET CODE

_Note that it is also possible to use the application without the feedback engine and therefore Azure Table Storage is not required. To do this, just comment out all the code inside the file._


### Models
The FoodEx2 SCA back-end project makes use of various text classification models [Spacy](https://spacy.io/). For more information on what data and how these models were trained check the [wiki](wiki).

**Note that the project makes use of Kubernates which automatically downloads and exports all required templates to the _work-dir_ folder. For testing purposes, without using Kubernates, this can also be done _locally_ by changing the model path in the _api/public.py_ file (check the _todo_ comments). By doing so, you can manually create your own folder that will contain the models (which can be built manually or downloaded and extracted).**


### Serve FoodEx2 SCA Locally
Several APIs are available on the FoodEx2 Smart Coding Application. To expose them, you need to serve the project using Flask. Run the following command from the project folder:
```
python app.py
```

### Public APIs
Public APIs are freely accessible and therefore do not require authentication. Below you will find descriptions and the various parameters required for each of them:

**Replace hostname and port with the server name and activated port respectively (e.g. if running in local without specifying a port the default one would be localhost:5000).**

#### predict
This api allows to select a specific model, from the existing ones, and hence obtain FoodEx2 terms suggestiong based on the free text given as input.

##### call example
```
GET http://hostname:port/predict_all HTTP/1.1
content-type: application/json

{
    "text":"white chocolate",
    "model":"bt",
    "threshold": "0.1"
}
```

##### parameters
- Text: descrption of the food to encode
- Model: name of one of the available models. If using the official models than one of the follwoing can be chosen (BT, CAT, F01, F02, F03, F04, F06, F07, F08, F09, F10, F11, F12, F17, F18, F19, F20, F21, F22, F23, F24, F25, F26, F27, F28, F31, F32, F33)
- Threshold: filter those terms having a percentage of accuracy lower than the provided one.

#### predict_all
This api allows to get FoodEx2 term predictions for each exsisting model.

##### call example
```
GET http://hostname:port/predict_all HTTP/1.1
content-type: application/json

{
    "text":"white chocolate",
    "threshold": "0.1"
}
```

##### parameters
- Text: descrption of the food to encode;
- Threshold: filter those terms having a percentage of accuracy lower than the provided one.

### Private APIs
The private APIs require token authentication. Here the description and parameters required for each api:

#### post_feedback
This api allows to post feedback directly to the Azure storage table. The feedback collected will be used to retrain existing models with the aim of covering more unseen terms and add new examples to existing class.

##### call example
```
POST http://hostname:port/post_feedback HTTP/1.1
Content-Type: "application/json"
x-access-token: mysecretkey

{
    "desc": "hazelnuts",
    "code": "A034L"
}
```

##### parameters
- Desc: descrption of the food to submit as feedback
- code: FoodEx2 code which better rapresent the given description.

#### get_codes
This api allows to get a series of FoodEx2 codes which are not well described or which need further examples.

##### call example
```
POST http://hostname:port/get_codes HTTP/1.1
content-type: application/json
x-access-token: mysecretkey

{
    "n": 5
}
```

##### parameters
- n: number of FoodEx2 codes requested.

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
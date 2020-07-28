# Project Under Development

<p align="center">
	<img src="http://www.efsa.europa.eu/profiles/efsa/themes/responsive_efsa/logo.png" alt="European Food Safety Authority"/>
</p>

## FoodEx2 Smart Coding Application - Backend
The FoodEx2 Smart Coding Application is designed and developed internally in the European Food Safety Authority (DATA and AMU units). This project aim to simplify the FoodEx2 coding process of food and feed starting from a given free text description. More specifically this is possible thanks to the creation and hence the usage of FoodEx2 dedicated text classification models trained on historycal data. Please note that this project exposes the functionality provided by the models through APIs. 

<p align="center">
    <img src="src/icons/FE2_POSI.jpg" alt="FoodEx2_SCA"/>
</p>

## For Developers
### Prerequisites
* [Python] (https://www.python.org/downloads/)

## Clone and install
Clone the project locally in your workspace using the following command:
```
git clone https://github.com/openefsa/foodex2-sca-backend.git
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

## Deployment

### Docker build

### Kubernates deployment
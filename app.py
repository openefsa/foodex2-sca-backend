#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# *********************************************************************
# |                                                                    
# | File: \app.py
# | Description: <<desc here>>
# | Project: foodex_sca_backend
# | Created Date: 19th May 2020
# | Author: Alban Shahaj (shahaal)
# | Email: data.collection@efsa.europa.eu
# | -----------------------------------------------------------------  
# | Last Modified: Thursday, 24th June 2020
# | Modified By: Alban Shahaj (shahaal)
# | -----------------------------------------------------------------  
# | Copyright (c) 2020 European Food Safety Authority (EFSA)
# |                                                                    
# *********************************************************************
###


from flask import Flask
from flask_cors import CORS


# instantiate flask app
app = Flask(__name__)
# set app configuration from external file
app.config.from_object("config.ProductionConfig")
CORS(app)
# register api blueprint to flask app
from api import api as api_blueprint
app.register_blueprint(api_blueprint)

    

if __name__ == "__main__":
    # run flask app
    app.run(host="0.0.0.0")
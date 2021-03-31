#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# *********************************************************************
# |                                                                    
# | File: \__init__.py
# | Description: <<desc here>>
# | Project: api
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

import pathlib, os, sqlite3 as sq

from flask import Blueprint
from . import utils

api = Blueprint('api', __name__, template_folder='templates')

# create connection with local db
db_path = utils.check_db('MTX_12.0')
db__uri_path = pathlib.Path(os.path.abspath(db_path)).as_uri()
conn = sq.connect('{}?mode=ro'.format(db__uri_path), uri=True,check_same_thread=False)
# create cursor that will operate on db
c = conn.cursor()

# private and public apis must be imported after Blueprint initialisation
from . import private, public
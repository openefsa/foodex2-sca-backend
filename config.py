#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# *********************************************************************
# |                                                                    
# | File: \config.py
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

class Config:
    
    # heder where token will be passed to the request
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'x-access-token'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_SECURE = True


class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    SESSION_COOKIE_SECURE = False
    TESTING = True
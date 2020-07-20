#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# *********************************************************************
# |
# | File: \private.py
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


from flask import request

from . import api

from functools import wraps
import datetime
import json

# import azure table service
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity

from kubernetes import client, config

# load k8s configuration
try:
    config.load_incluster_config()
except config.ConfigException:
    try:
        config.load_kube_config()
    except config.ConfigException:
        raise Exception("Could not configure kubernetes python client")

v1 = client.CoreV1Api()
# pull secrets from cred in deafult namespace
secret = v1.read_namespaced_secret("creds", "default")
print(secret)

# initiate the table service
table_service = TableService(
    account_name=secret.BLOB_STORAGE_ACCOUNT_NAME,
    account_key=secret.BLOB_STORAGE_ACCOUNT_KEY
)

# if the table does not exsits than create it
tableName = secret.AZURE_TABLE_NAME
if not table_service.exists(tableName):
    table_service.create_table(tableName)


def authorisation_required(f):
    ''' method used to check if the user has permission to post feedbacks '''

    @wraps(f)
    def decorated(*args, **kwargs):
        key = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            # enable feedbacks if status code ok
            enable_feedbacks = (token == secret.FEEDBACK_API_SECRET_KEY)

        return f(enable_feedbacks, *args, **kwargs)

    return decorated


@api.route('/postFeedback', methods=['POST'])
@authorisation_required
def postFeedback(enable_feedbacks):
    # if current user is active
    if enable_feedbacks:
        # get the data from the request
        data = request.get_json()
        # populate the feedback entity
        feedback = Entity()
        feedback.PartitionKey = 'foodex2feedbacks'
        time = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
        feedback.RowKey = time
        feedback.description = data['desc']
        feedback.code = data['code']
        # insert the entity in the table
        table_service.insert_entity(tableName, feedback)
        return json.dumps({'message': 'Feedback sent correctly'})
    else:
        return json.dumps({'message': 'An error occured while sending the feedback please try the administrator.'})

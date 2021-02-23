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

from . import api, c

from functools import wraps
import datetime
import pandas as pd
import json
import os
import re

# import azure table service
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity

# TODO only debug
'''
os.environ["ACCOUNT_NAME"] = "account_name"
os.environ["ACCOUNT_KEY"] = "account_key"
os.environ["TABLE_NAME"] = "table_name"
os.environ["SECRET_KEY"] = "secret_key"
'''

# initiate the table service
table_service = TableService(
    account_name=os.environ['ACCOUNT_NAME'],
    account_key=os.environ['ACCOUNT_KEY']
)

# if the table does not exsits than create it
tableName = os.environ['TABLE_NAME']
if not table_service.exists(tableName):
    table_service.create_table(tableName)

# read unsure data (used by feedback engine)
unsureDf = pd.read_parquet(
    "api/asset/data/unsure_data/foodex_unsure_data.parquet")
query_terms = "SELECT termCode, termExtendedName FROM terms WHERE termCode IN (%s) LIMIT 100"
query_attrs = "SELECT code, label FROM attributes WHERE code IN (%s) LIMIT 100"


def join_intepretation(codes, descs):
    ''' return the interpretation joined by delimiters '''
    res = ""
    for index, code in enumerate(codes):
        if index == 0:
            res += descs[code]+" # "
        elif index % 2 == 1:
            res += descs[code]+" . "
        else:
            res += descs[code]+" $ "
    return res[:-3]


def authorisation_required(f):
    ''' method used to check if the user has permission to post feedbacks '''

    @wraps(f)
    def decorated(*args, **kwargs):
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            # enable feedbacks if status code ok
            enable_feedbacks = (token == os.environ['SECRET_KEY'])

        return f(enable_feedbacks, *args, **kwargs)

    return decorated


@api.route('/post_feedback', methods=['POST'])
@authorisation_required
def post_feedback(enable_feedbacks):
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
        return json.dumps({'message': 'An error occurred while sending the feedback please try the administrator.'})


@api.route('/get_codes', methods=['POST'])
@authorisation_required
def get_codes(enable_feedbacks):
    # if current user is active
    if enable_feedbacks:
        # get the data from the request
        dim = request.get_json().get("n")
        # return if asking a not valid number of codes
        if not(1 <= dim <= 100):
            return json.dumps({'message': 'Sorry can return only a minimum of one and a maximum of 100 FoodEx2 codes. Try again.'})
        # get randomly n records from the df (limited max to 100)
        sample = unsureDf.sample(n=dim)
        # initialise the returned json object
        json_obj = {}
        # build up the json obj
        for index, row in sample.iterrows():
            # get the full code
            full_code = row['BASETERM_AND_EXPLICIT']
            # split it by delimiters
            codes = re.split("[#$.]", full_code)
            # get the category codes and build the sql query
            attrs = tuple([i for i in codes if len(i) == 3])
            get_attrs = (query_attrs % ','.join('?'*len(attrs)))
            # get the term codes and build the sql query
            terms = tuple([i for i in codes if len(i) == 5])
            get_terms = (query_terms % ','.join('?'*len(terms)))

            descs = {}
            # if there are categories get the description in dict
            if(attrs):
                # execute query
                c.execute(get_attrs, [i for i in attrs])
                descs.update(dict(c.fetchall()))
            # if there are categories get the description in dict
            if(terms):
                c.execute(get_terms, [i for i in terms])
                descs.update(dict(c.fetchall()))

            # build full interpretation
            full_desc = join_intepretation(codes, descs)
            # fill the json obj at row index
            json_obj[index] = {
                'fullCode': full_code,
                'fullDesc': full_desc
            }

        return json_obj
    else:
        return json.dumps({'message': 'An error occurred while getting the codes please contact the administrator.'})

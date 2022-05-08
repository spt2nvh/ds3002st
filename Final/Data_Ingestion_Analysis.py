#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  6 20:21:36 2022

@author: shannontran
"""

!pip install schedule
!pip install pymongo
import json
import requests
import time
import schedule
from datetime import datetime, timedelta
from pymongo import MongoClient 
import pymongo


client = pymongo.MongoClient('localhost', 27017)
db = client['api_db_final1']
collection = db.create_collection('api_data_final1')
api_collection = db.get_collection("ap_data_final1")



def api_function():
    response = requests.request("GET", "https://4feaquhyai.execute-api.us-east-1.amazonaws.com/api/pi")
    data = response.text
    parse_json = json.loads(data)
    print(data)
    api_collection.insert_one(parse_json) # inserts API data into database collection

schedule.every().minute.at(":00").until(timedelta(hours=1)).do(api_function) # Runs api_function for 1 hour, every minute

onehour = time.time()+60*60
while True:
    schedule.run_pending()
    if time.time() > onehour:
        break


list(api_collection.find({}))




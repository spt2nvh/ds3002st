#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 20:43:07 2022

@author: shannontran
"""


# Import packages
import pandas as pd
import sqlite3
import csv
import json
import os
import sys

#%%

# Reading in data source:
os.chdir('/Users/shannontran/Documents/UVA Classes/STAT 2120/Data') # change directory to where file lives
data  = pd.read_csv('kickstarter.csv') # use pandas to read in csv

# Modifying data source:
data['percent_pledged'] = round((data.pledged / data.goal)*100, 4) #  creates new column for percent of goal actually pledged
data = data.drop(columns=['deadline', 'launched']) # removes columns containing dates

# Summary of data:
print("Number of columns", len(data.columns))
print("Number of rows:", len(data))



#%%

# Uses sys.argv[] to take user input in command line, to convert csv file to either json or sql db table
# Valid user input: either json or sql
# Invalid user input: no input, or anything besides "json" or "sql"


try:
    # Prints error/directions if no input is submitted
    if len(sys.argv) == 1:
        print("Pass in 'json' or 'sql'")
        
    arg = sys.argv[1].lower() # Converts any input into lowercase to control for variation in inputs
    
    # Converts csv to json file if "json" is inputted
    if arg == 'json':
        def csv_to_json(csvFile, jsonFile):
            data = []
            with open(csvFile, encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    data.append(row)
            with open(jsonFile, 'w',encoding='utf-8') as json_file:
                json_string = json.dumps(data)
                json_file.write(json_string)
        csvFile = r'/Users/shannontran/Documents/UVA Classes/STAT 2120/Data/kickstarter.csv'
        jsonFile = r'/Users/shannontran/Desktop/DS 3002/kickstarter.json' # creates new .json file in DS 3002 folder
        csv_to_json(csvFile, jsonFile)
        print("CSV file successfully saved as a JSON file to /Users/shannontran/Desktop/DS 3002!")
        
    # Converts csv to sql db table in kickstarter.db if "sql" is inputted
    elif arg == 'sql':
        data.to_csv("kickstarter1.csv", index=False) # saves modification to csv file
        conn = sqlite3.connect('kickstarter.db')
        cur = conn.cursor()

        cur.execute("""DROP TABLE IF EXISTS 'KSTable';""") # drops table if already exists
        # Creates db table
        cur.execute("""CREATE TABLE KSTable( 
           ID INT PRIMARY KEY,
           name TEXT,
           category TEXT,
           goal INT,
           pledged INT,
           status TEXT,
           number_backers INT,
           percent_pledged);
        """)
        conn.commit()
        
        # Inputs csv values into db table
        with open('kickstarter1.csv','r') as file:
            csv_reader = csv.reader(file)
            columns = next(csv_reader)
            list_of_rows = [tuple(row) for row in data.values]
            query = 'INSERT OR REPLACE INTO KSTable({0}) VALUES ({1})'
            query = query.format(','.join(columns), ','.join('?' * len(columns)))
            for x in csv_reader:
                cur.executemany(query, list_of_rows)
            conn.commit()
        print("CSV file successfully saved as SQL Database table to kickstarter.db!")
        
    # Prints error/directions if input is anything other than "json" or "sql"
    else:
        print("Please input either 'json' or 'sql'")
        
    # Prints error if there is an error in code or input
except:
    print("Error: invalid")
    
    
    
    
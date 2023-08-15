#!/usr/bin/env python
# coding: utf-8

# In[4]:


import json
import requests
import time
import math
import sys

from datetime import datetime


def print_time(strPrint):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(strPrint," =", current_time)

def post_request_with_json_file(url, json_file_path):
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            print("POST request successful!")
            #print("Response:")
            #print(response.json())
        else:
            print(f"POST request failed with status code: {response.status_code}")
            #print("Response:")
            #print(response.text)

        
    except IOError as e:
        print(f"Error reading the JSON file: {e}")
        print_time("End Time")
    except requests.exceptions.RequestException as e:
        print(f"Error making the request: {e}")
        print_time("End Time")


# In[5]:


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def send_post_request(url, payload):
    headers = {'Content-Type': 'application/json'}    
    response = requests.post(url, json=payload, headers=headers,verify=False)
    return response

def post_request_with_json_file(url, json_file_path):
    # Replace 'API_URL' with the actual API endpoint URL
    API_URL = url

    # Replace 'data.json' with the path to your JSON file
    data = read_json_file(json_file_path)
    row_count = 0
    batch_size = 100  # Number of rows to send in one batch

    for key, item in data.items():
        

        if key=='data':
            row_count=len(item)
            row_batch=0
            iterate=math.ceil(row_count/batch_size)

            if isinstance(item, list):
                for i in range(0,iterate):
                    print("BATCH ",i+1)
                    if i==0:
                        batch_from=i
                        batch_to= (i+1)*batch_size
                    elif i==(iterate-1):
                        batch_from=batch_to
                        batch_to=row_count
                    else:
                        batch_from=batch_to
                        batch_to= (i+1)*batch_size

                    print (batch_from+1,' - ', batch_to)
                    payload = {k: v for k, v in data.items() if k != 'data'}
                    payload['data']=item[batch_from:batch_to]
                    response = send_post_request(API_URL, payload)
                    print(f"Pausing for 10 seconds...")
                    time.sleep(10)

    print("All rows sent.")


if __name__ == "__main__":
    arg1 = sys.argv[1]


    print_time("Start Time")
    #api_url = "http://139.180.145.25:8000/match_akun"  # Replace with your API endpoint URL
    api_url = "http://127.0.0.1:8000/match_akun"  # Replace with your API endpoint URL
    print (api_url)

    json_file_path = arg1  # Replace with the path to your JSON file
    post_request_with_json_file(api_url, json_file_path)
    print_time("End Time")


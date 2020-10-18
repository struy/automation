#! /usr/bin/env python3
import json
import requests
import os


path = os.getcwd() + "/module_2/"+"data/feedback/"
external_ip  = requests.get('https://api.ipify.org').text
url  ="http://"+ external_ip +"/feedback/"
feedbacks = []


for filename in os.listdir(path):
    with open(path + filename, "r") as f:
        lines_names = ["title", "name", "date", "feedback"]
        lines = f.read().splitlines()
        feedback = dict(zip(lines_names, lines))
        response = requests.post(url, json=feedback)
        print(response.request.url, response.request.body)
        response.raise_for_status()
        response.close()
    



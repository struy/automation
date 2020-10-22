#!/usr/bin/env python3

import os
import requests


def descriptions_upload(path, url):
    """Example to send: 
    {"name": "Watermelon","weight": 500,
    "description": "Watermelon is good for relieving heat, eliminating annoyance and quenching thirst. It contains a lot of water, which is good for relieving the symptoms of acute fever immediately. The sugar and salt contained in watermelon can diuretic and eliminate kidney inflammation. Watermelon also
    contains substances that can lower blood pressure.", "image_name": "010.jpeg"} """
    lines_names = ["name", "weight", "description"]
    for filename in os.listdir(path):
        with open(path + filename, "r") as f:
            lines = f.read().splitlines()
            content = dict(zip(lines_names, lines))
            # TODO regex int
            temp = content['weight'].split(" ")
            if temp[0].isdigit():
                content['weight'] = int(temp[0]])
            content['image_name'] = filename[:-4]+".jpeg"
            print(content)
            response = requests.post(url, json=content)
            response.raise_for_status()
            response.close()


if __name__ == "__main__":
    descriptions_path = os.getcwd() + "/supplier-data/descriptions/"
    external_ip = requests.get('https://api.ipify.org').text
    upload_url = "http://" + external_ip + "/fruits/"
    descriptions_upload(descriptions_path, upload_url)

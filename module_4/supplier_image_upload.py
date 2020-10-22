#!/usr/bin/env python3

import os
import requests
from PIL import Image
import concurrent.futures

# TODO use shutil


IMAGES_PATH = os.getcwd() + "/supplier-data/images/"
external_ip = requests.get('https://api.ipify.org').text
UPLOAD_URL = "http://" + external_ip + "/upload/"

# Synchronous Approach


def upload_images(path, url):
    for filename in os.listdir(path):
        if filename.endswith(".jpeg"):
            with open(path+filename, 'rb') as opened:
                requests.post(url, files={'file': opened})


# Multithreaded Approach
def open_upload_images(filename):
    global IMAGES_PATH
    global UPLOAD_URL
    with open(IMAGES_PATH+filename, 'rb') as opened:
        requests.post(UPLOAD_URL, files={'file': opened})


def upload_images_with_treads(path, url):
    filenames = [filename for filename in os.listdir(
        path) if filename.endswith(".jpeg")]
    size = 5
    with concurrent.futures.ThreadPoolExecutor(size) as thp:
        thp.map(open_upload_images, filenames)


if __name__ == "__main__":
    upload_images(IMAGES_PATH, UPLOAD_URL)

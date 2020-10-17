#! /usr/bin/env python3

import os
from PIL import Image


SIZE = (128, 128,)
FROM = os.getcwd() + "/images/"
# origin path TO = "/opt/icons/"
TO = os.getcwd() + "/img2/"


for filename in os.listdir(FROM):
    # skip Apple system file
    if filename == '.DS_Store':
        continue
    #  Open an image
    with Image.open(FROM + filename) as im:
        # Rotate an image and   Resize an image
        new_im = im.rotate(-90).resize(SIZE)
        # Save an image in a specific format in a separate directory
        if new_im.mode != 'RGB':
            new_im = new_im.convert('RGB')
        new_im.save(TO+filename+".jpg", "jpeg")
        new_im.close()

#!/usr/bin/env python3

import os
from PIL import Image


PATH = os.getcwd() + "/supplier-data/images/"
SIZE = (600, 400,)
FORMAT = "jpeg"


def change_resolution_and_format(path,size,format):
    for filename in os.listdir(path):
        # skip Apple system file and JPEG files
        if filename.endswith(".tiff"):            
            #  Open an image
            with Image.open(path + filename) as im:
                #  Resize an image
                new_im = im.resize(size)
                # hange image format from .TIFF to .JPEG
                if new_im.mode != 'RGB':
                    new_im = new_im.convert('RGB')
                new_im.save(path+filename[:4]+format, format)
                new_im.close()


if __name__ == "__main__":
    change_resolution_and_format(PATH, SIZE, FORMAT)

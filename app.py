#!/usr/bin/python
# -*- coding: utf-8 -*-
from tkinter import *

# from threading import Thread

import subprocess  # Scrapy processor

import os
import urllib.request
import json
import datetime
from PIL import Image
from io import StringIO




# definations

def start_crawling():
    scrape()


def scrape():
    process = subprocess.Popen('scrapy runspider ./download_images/download_images/spiders/downimage.py -o output.json')
    process.wait()


def read_output_file():
    f = open('output.json',)
    data = json.load(f)

    for img_url in data[0]['image_urls']:
       DownloadImageFromURL(img_url)

    f.close()
    

#Download images from output file
def DownloadImageFromURL(url):
    response = urllib.request.urlretrieve(url)
    ImageExt = response[1].get_content_type()#image/png or image/jpg etc
    ImageExt = ImageExt.replace("image/", "") #png or jpg etc

    now = datetime.datetime.now()
    fileName = now.strftime("%m-%d-%Y,%H-%M-%S")
    
    urllib.request.urlretrieve(url, "output_images/"+fileName+"."+ImageExt)


# instanciate of window object

app = Tk()

# set app title

app.title('Scrapy Web Crawler')

# set app hight/Width

app.geometry('500x250')

# Config column

app.grid_columnconfigure(0, weight=1)

# label

input_label = Label(app, text='Enter URL', font=('bold', 10), pady=20)
input_label.grid(row=0, column=0, sticky=W)

# Entry

input_val = StringVar()
input_entry = Entry(app, textvariable=input_val, width=70)
input_entry.grid(row=0, column=1, sticky='we')

# submit button

submit_btn = Button(app, text='Start Crawling', width=10,
                    command=read_output_file)
submit_btn.grid(row=1, column=1, sticky=W)

# run app

app.mainloop()

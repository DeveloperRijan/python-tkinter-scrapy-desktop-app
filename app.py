#!/usr/bin/python
# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import messagebox

from threading import Thread
import subprocess  # Scrapy processor

import requests
import os
import json
import datetime


# instanciate of window object
app = Tk()

#global variables
submitted_url = StringVar()
submit_btn=''


def run_after_scrawler_finished():
    print("From Call Back")

# definations
def start_scraping_now():
    with subprocess.Popen('scrapy runspider -a filename=urls.txt ./download_images/download_images/spiders/downimage.py -o output.json',  stderr=None, shell=True)  as process:
        process.communicate()
        messagebox.showinfo("Success", "Crawler Processing Completed")
        
        #Show Button of Downloads + Start Over
        start_download_btn = Button(app, text='Download Images',
                    command=read_output_file)
        start_download_btn.place(x=180, y=50)

        scraping_start_over_btn = Button(app, text='Start Over',
                            command=scraping_start_over)
        scraping_start_over_btn.place(x=310, y=50)
    #process.wait()
    

#Thread name should be unique on each call...
def created_and_run_thread(threadName):
    threadName = Thread(target = start_scraping_now, args = (),)
    threadName.start()


def start_crawling():
    if os.path.exists("output.json"):
        os.remove("output.json")
    
    if(submitted_url.get() == ''):
        messagebox.showwarning("SORRY", "Please enter a valid URL")
        return False

    #Make button disbale
    if submit_btn["state"] != DISABLED:
        submit_btn["state"] = DISABLED

    #passing unique thread name
    current_time = datetime.datetime.now()
    threadName = current_time.strftime("%m-%d-%Y_%H-%M-%S")
    created_and_run_thread(threadName)



def scraping_start_over():
    pass


def start_downloading_process():
    f = open('output.json',)
    data = json.load(f)

    for row in data:
       for image_url in row["image_urls"]:
           DownloadImageFromURL(image_url)

    f.close()


thread_download = Thread(target = start_downloading_process, args = ())

def read_output_file():
    thread_download.start()
    

#Download images from output file
def DownloadImageFromURL(url):
    now = datetime.datetime.now()
    fileName = now.strftime("%m-%d-%Y_%H-%M-%S")
    
    r = requests.get(url)
    contentType = r.headers['content-type'] #image/png or image/jpg etc
    contentType = contentType.split("/") #["image", "png"]
    ext = contentType[1] #png or jpg etc
    allowed_types = ["png", "jpeg", "jpg", "gif", "svg"]

    if ext in allowed_types:
        with open("./output_images/"+fileName+"."+ext, "wb") as handler:
            handler.write(r.content)
    
    r.connection.close()




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
input_entry = Entry(app, textvariable=submitted_url, width=70)
input_entry.grid(row=0, column=1, sticky='we')

# submit button

submit_btn = Button(app, text='Start Crawling',
                    command=start_crawling)
submit_btn.place(x=75, y=50)



def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit crawler app?"):
        app.destroy()

app.protocol("WM_DELETE_WINDOW", on_closing)

# run app

app.mainloop()

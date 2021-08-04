#!/usr/bin/python
# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import messagebox

from threading import Thread
import subprocess  # Scrapy processor

import re
import requests
import os
import json
import datetime


# instanciate of window object
app = Tk()
app.resizable(False, False)

#global variables
input_entry=None
submitted_url = StringVar()
submit_btn=None
start_download_btn=None
scraping_start_over_btn=None



# definations
def start_scraping_now():
    #with subprocess.Popen('scrapy runspider -a filename=urls.txt ./download_images/download_images/spiders/downimage.py -o output.json',  stderr=None, shell=True)  as process:
    with subprocess.Popen('scrapy crawl downimage -o output.json',  stderr=None, shell=True)  as process:
        process.communicate()
        messagebox.showinfo("Success", "Crawler Processing Completed")
        
        #Show Button of Downloads + Start Over
        if(start_download_btn["state"] != NORMAL):
            start_download_btn["state"] = NORMAL
        
        if(scraping_start_over_btn["state"] != NORMAL):
            scraping_start_over_btn["state"] = NORMAL
    #process.wait()
    

#Thread name should be unique on each call...
def created_and_run_thread(threadName):
    threadName = Thread(target = start_scraping_now, args = (),)
    threadName.start()


#url validation regex
regex = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def start_crawling():
    with open("output.json", "w") : pass
    
    if(submitted_url.get() == ''):
        messagebox.showwarning("SORRY", "Please enter URL")
        return False
    
    #validate url
    if(re.match(regex, submitted_url.get()) is None):
        messagebox.showwarning("SORRY", "Please enter a valid URL")
        return False

    #Make button disbale
    if (submit_btn["state"] != DISABLED):
        submit_btn["state"] = DISABLED


    #set the submitted url into urls file
    with open("urls.txt", "w") as txt_url:
        txt_url.writelines(submitted_url.get())

    #passing unique thread name
    current_time = datetime.datetime.now()
    threadName = current_time.strftime("%m-%d-%Y_%H-%M-%S")
    created_and_run_thread(threadName)



def scraping_start_over():
    #disabled buttons
    if(start_download_btn['state'] != DISABLED):
        start_download_btn['state'] = DISABLED

    if(scraping_start_over_btn['state'] != DISABLED):
        scraping_start_over_btn['state'] = DISABLED
    
    if(submit_btn["state"] != NORMAL):
        submit_btn["state"] = NORMAL

    #clear text of entry/input
    input_entry.delete(0, 'end')



def start_downloading_process():
    if(os.stat("output.json").st_size == 0):
        messagebox.showwarning("SORRY", "Crawler response was empty ! might be your given url is not accessible or down, try again")
        #Enable submit button
        if(submit_btn['state'] != NORMAL):
            submit_btn['state']=NORMAL
        return False


    #load json result file
    f = open('output.json',)
    data = json.load(f)

    #check if there is no images
    if(not len(data[0]["image_urls"]) > 0):
        messagebox.showwarning("SORRY", "Crawler didn't find any images! try again or change url")
        #Enable submit button
        if(submit_btn['state'] != NORMAL):
            submit_btn['state']=NORMAL
        return False
    
    #else download images
    for row in data:
       for image_url in row["image_urls"]:
            try:
                now = datetime.datetime.now()
                fileName = now.strftime("%m-%d-%Y_%H-%M-%S")
                
                r = requests.get(image_url)
                contentType = r.headers['content-type'] #image/png or image/jpg etc
                contentType = contentType.split("/") #["image", "png"]
                ext = contentType[1] #png or jpg etc
                allowed_types = ["png", "jpeg", "jpg", "gif", "svg"]

                if ext in allowed_types:
                    with open("./output_images/"+fileName+"."+ext, "wb") as handler:
                        handler.write(r.content)
                
            except Exception as excp:
                print(f"Error to downloading image")
                continue

    

    f.close()
    r.connection.close()

    #if end then
    messagebox.showinfo("Success", "Images Downloading Completed")
    
    #clear text of entry/input
    input_entry.delete(0, 'end')

    #Enable submit button
    if(submit_btn['state'] != NORMAL):
        submit_btn['state']=NORMAL
    




def created_and_run_downloading_thread(threadName):
    threadName = Thread(target = start_downloading_process, args = ())
    threadName.start()

def read_output_file_and_download():
    #Make Buttons Disabled
    if(start_download_btn['state'] != DISABLED):
        start_download_btn['state'] = DISABLED
    if(scraping_start_over_btn['state'] != DISABLED):
        scraping_start_over_btn['state'] = DISABLED

    #passing unique thread name
    current_time = datetime.datetime.now()
    threadName = current_time.strftime("%m-%d-%Y_%H-%M-%S")
    created_and_run_downloading_thread(threadName)




# set app title

app.title('Web Crawler')

# set app hight/Width

app.geometry('500x170')

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

start_download_btn = Button(app, text='Download Images',
                    command=read_output_file_and_download)
start_download_btn.place(x=180, y=50)

scraping_start_over_btn = Button(app, text='Start Over',
                    command=scraping_start_over)
scraping_start_over_btn.place(x=310, y=50)



#make button by default disabled
if(start_download_btn['state'] != DISABLED):
    start_download_btn['state'] = DISABLED
if(scraping_start_over_btn['state'] != DISABLED):
    scraping_start_over_btn['state'] = DISABLED
    
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit crawler app?"):
        app.destroy()

app.protocol("WM_DELETE_WINDOW", on_closing)

# run app

app.mainloop()

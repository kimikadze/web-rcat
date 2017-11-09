#!/usr/bin/env python
# encoding: utf-8

# pythonspot.com
#import sys
#import time
import os
#sys.path.append('.')
from flask import Flask,Blueprint, render_template, redirect, request, flash, url_for, send_file
from macos.rcat.rcat_main import View

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")

def index():
    #return "hello"

    return render_template('rcat.html')




@app.route("/return-file/")
def return_file():
    #return send_file("/Users/Florian/Desktop/Flask/Webservice/rcat_app/relations.pdf")
    #print(os.path.basename(os.getcwd()))
    #print(os.getcwd())
    pdf_path = "/".join(([os.getcwd(), "relations.pdf"]))
    return send_file(pdf_path)


@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, "files/")
    #print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
    #for file in urllib.request.files.getlist("file"):

        #print(file)
        filename = file.filename
        destination = "/".join(([target, filename]))
        #print(destination)
        file.save(destination)

    #print(os.path.basename(os.getcwd()))
    os.chdir("../rcat/")
    View().main_PDF(text_file=destination, character_file="rcat/doc/character_lists/Goethe_Werther_74_characters.txt",
                  dist_parameter=[8, 5, 5],
                  remove_stopwords_in_context="n",
                  segments=5, lang=1, number_of_wc=3,
                  write_gephi_csv="n",
                  word_field = "N",
                  wf_cat="None",
                  lemmatisation="treetagger")


    return render_template('rcat_done.html')



    

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=50002)


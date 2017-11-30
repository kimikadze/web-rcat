#!/usr/bin/env python
# encoding: utf-8

# pythonspot.com
#import sys
#import time
import os
#sys.path.append('.')
from flask import Flask,Blueprint, render_template, redirect, request, flash, url_for, send_file
from rcat.rcat_main import rcat

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")

def index():
    #return "hello"

    return render_template('rcat.html')







@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, "files_upload/")
    #print(target)

    if not os.path.isdir(target):
        os.mkdir(target)



    #PROCESS FIRST FILE (TEXT)

    first_file = request.files.getlist("file")[0]

    filename = first_file.filename
    filename = str("1__"+filename)
    destination_first_file = "".join(([target, filename]))

    first_file.save(destination_first_file)

    #PROCESS SECOND FILE (CHARACTERS)

    second_file = request.files.getlist("file")[1]

    filename = second_file.filename
    filename = str("2__"+filename)
    destination_second_file = "".join(([target, filename]))

    second_file.save(destination_second_file)

    #GET DISTANCE PARAMETERS

    distance = int(request.form["distance"])
    words_before = int(request.form["before"])
    words_after = int(request.form["after"])

    #GET OTHER PARAMETERS

    stopwords_parameter = request.form["stopwords"]
    lemmatisation_parameter = request.form["lemmatisation"]
    #print(lemmatisation_parameter)
    wordcloud_parameter = int(request.form["word_clouds"])
    #print(wordcloud_parameter)
    language_parameter = request.form["language"]
    #segments_parameter = int(request.form["segments"])


    # RUN RCAT

    #print(os.path.basename(os.getcwd()))
    os.chdir("../rcat/")
    rcat().main_PDF(text_file=destination_first_file, character_file=destination_second_file,
                  dist_parameter=[distance, words_before, words_after],
                  remove_stopwords_in_context=stopwords_parameter,
                  segments=5, txt_language=language_parameter, number_of_wc=wordcloud_parameter,
                  write_gephi_csv="n",
                  word_field = "N",
                  wf_cat="None",
                  lemmatisation=lemmatisation_parameter)


    return render_template('rcat_done.html')


@app.route("/return-file/")
def return_file():
    #return send_file("/Users/Florian/Desktop/Flask/Webservice/rcat_app/relations.pdf")
    #print(os.path.basename(os.getcwd()))
    #print(os.getcwd())
    pdf_path = "/".join(([os.getcwd(), "relations.pdf"]))
    return send_file(pdf_path)
    

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=50001)


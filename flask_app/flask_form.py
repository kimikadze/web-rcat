#!/usr/bin/env python
# encoding: utf-8

# pythonspot.com
# import sys
# import time
import matplotlib
matplotlib.use('Agg')
import os
import uuid
import zipfile
import shutil



# sys.path.append('.')
from flask import Flask, Blueprint, render_template, redirect, request, flash, url_for, send_file, session

from rcat.rcat_main import rcat
from nocache import nocache

app = Flask(__name__)
app.secret_key = 'super secret key'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

###

@app.route("/")

def index():
    #return "hello"

    return render_template('rcat.html')



@app.route("/upload", methods=["POST"])
def upload():

    session_id = uuid.uuid1()
    #session_id = False
    print(session_id)
    session['session_id'] = session_id
    target = os.path.join(APP_ROOT, "data_user/%s_files_upload/" %session_id)
    #print(target)

    if not os.path.isdir(target):
        os.mkdir(target)



    #PROCESS FIRST FILE (TEXT)

    if_demo_txt = request.form["if_demo_txt"]


    if if_demo_txt == "werther":
        destination_first_file = "werther.txt"

    if if_demo_txt == "own_txt_file":
        first_file = request.files.getlist("file")[0]

        filename = first_file.filename
        filename = str("1__"+filename)
        destination_first_file = "".join(([target, filename]))

        first_file.save(destination_first_file)

    #PROCESS SECOND FILE (CHARACTERS)

    if_demo_characters = request.form["if_demo_characters"]

    if if_demo_characters == "werther_characters":
        destination_second_file = "werther_characters.txt"

    if if_demo_characters == "own_character_file":

        second_file = request.files.getlist("file")[1]

        filename = second_file.filename
        filename = str("2__"+filename)
        destination_second_file = "".join(([target, filename]))

        second_file.save(destination_second_file)

    #GET DISTANCE PARAMETERS

    distance = int(request.form["distance"])
    words_before = int(request.form["before"])
    words_after = int(request.form["after"])

    #STOPWORDS PARAMETER AND FILE
    stopwords_parameter = request.form["stopwords"]
    if stopwords_parameter=="own_stopwords":
        third_file = request.files.getlist("file")[2]
        filename = third_file.filename
        filename = str("3__" + filename)
        destination_third_file = "".join(([target, filename]))
        third_file.save(destination_third_file)
        #exception: if a file is uploaded, the path is given instead of the parameter from html
        stopwords_parameter=destination_third_file



    #GET OTHER PARAMETERS
    lemmatisation_parameter = request.form["lemmatisation"]
    #print(lemmatisation_parameter)
    wordcloud_parameter = int(request.form["word_clouds"])
    #print(wordcloud_parameter)
    language_parameter = request.form["language"]
    segments_parameter = int(request.form["segments"])


    #GET WORD FIELD PARAMETER
    wordfield_parameter = request.form["word_fields"]
    wf_cat_parameter = 0

    # GET WORD FIELD PARAMETER (WERTHER / NONE)
    if wordfield_parameter=="werther_emotions":
        fourth_file = "werther_emotions.txt"


    if wordfield_parameter=="N":
        wf_cat_parameter= "None"
        # pass

    #GET WORD FIELD PARAMETER (SINGLE)

    if wordfield_parameter=="single":
        fourth_file = request.files.getlist("file")[3]
        filename = fourth_file.filename
        filename = str("4__"+filename)
        destination_fourth_file = "".join(([target, filename]))
        fourth_file.save(destination_fourth_file)
        #print(destination_third_file)

        wf_cat_parameter = destination_fourth_file


    #GET WORD FIELD PARAMETER (MULTI)
    if wordfield_parameter=="multi":
        multi_wordfield_list = request.files.getlist("file")[3:]
        #print(request.files.getlist("file"))
        #print(multi_wordfield_list[1:])
        multi_file_list = []
        for index, word_field in enumerate(multi_wordfield_list[1:]):
            filename = word_field.filename
            #index_updated = index+4
            #print(index_updated)
            #index_updated_string = str(index_updated)
            filename = str("%s__" %str(index+4) + filename)
            destination_n_file = "".join(([target, filename]))
            word_field.save(destination_n_file)
            multi_file_list.append(destination_n_file)

        #print(multi_file_list)
        wf_cat_parameter = multi_file_list



    #FEATURES (PMI / SELECTION FOR WORD CLOUD FILTER)
    wc_context_parameter = request.form["wc_context_selection"]


    #FEATURES ADDITIONALLY (ZETA)
    #zeta_parameter = request.form["zeta"]


    #WORDS IN WORD CLOUD
    words_in_word_cloud_parameter = int(request.form["words_in_word_cloud"])

    #GET DEMO PARAMETERS
    if_demo_txt = request.form["if_demo_txt"]
    if_demo_characters = request.form["if_demo_characters"]

    # RUN RCAT

    #print(os.path.basename(os.getcwd()))
    #print("1")
    #print(os.getcwd())

    ############
    # if os.getcwd().endswith("/flask_app") == True:
    #     os.chdir("rcat/")
    # if os.getcwd().endswith("/rcat") == True:
    #     pass
    # else:
    #     print("multiple session path error")
    ##############


    # if if_demo_txt == "werther.txt" and if_demo_characters == "werther_characters.txt":
    #     rcat().main_PDF(text_file=destination_first_file,
    #                     character_file=destination_second_file,
    #                     dist_parameter=[distance, words_before, words_after],
    #                     remove_stopwords_in_context=stopwords_parameter,
    #                     segments=segments_parameter, txt_language=language_parameter,
    #                     number_of_wc=wordcloud_parameter,
    #                     write_gephi_csv="n",
    #                     word_field=wordfield_parameter,
    #                     wf_cat=wf_cat_parameter,
    #                     lemmatisation=lemmatisation_parameter,
    #                     sess_id=session_id,
    #                     word_cloud_context_selection=wc_context_parameter,
    #                     words_in_wc=words_in_word_cloud_parameter)  # ,
    #     # zeta_analysis=zeta_parameter)
	#

    rcat().main_PDF(text_file=destination_first_file,
                    character_file=destination_second_file,
                  dist_parameter=[distance, words_before, words_after],
                  remove_stopwords_in_context=stopwords_parameter,
                  segments=segments_parameter, txt_language=language_parameter,
                    number_of_wc=wordcloud_parameter,
                  write_gephi_csv="n",
                  word_field = wordfield_parameter,
                  wf_cat=wf_cat_parameter,
                  lemmatisation=lemmatisation_parameter,
                    sess_id=session_id,
                    word_cloud_context_selection = wc_context_parameter,
                    words_in_wc =words_in_word_cloud_parameter)#,
                    #zeta_analysis=zeta_parameter)

    if request.form["output"] == "PDF":
        return render_template('rcat_done_pdf.html')

    if request.form["output"] == "zip":
        path = os.path.join(APP_ROOT, "data_user/%s_temp_folder/" %session_id)
        os.chdir(os.path.join(APP_ROOT, "data_user/%s_temp_folder_zip/" %session_id))
        shutil.make_archive("rCat", "zip", path)

        return render_template('rcat_done_zip.html')



@app.route("/return-file-pdf/")
@nocache
def return_file():
    #return send_file("/Users/Florian/Desktop/Flask/Webservice/rcat_app/relations.pdf")
    #print(os.path.basename(os.getcwd()))
    #print(os.getcwd())

    session_id = session['session_id']
    pdf_path = "/".join(([os.getcwd(), "data_user/%s_temp_folder/relations.pdf" %session_id]))
    return send_file(pdf_path)


# @app.route("/return-file-zip/")
# @nocache
# def return_file():
#     #return send_file("/Users/Florian/Desktop/Flask/Webservice/rcat_app/relations.pdf")
#     #print(os.path.basename(os.getcwd()))
#     #print(os.getcwd())
#
#     session_id = session['session_id']
#     zip_path = os.path.join(APP_ROOT, "data_user/%s_temp_folder_zip/rCat.zip" %session_id)
#     return send_file(zip_path)

if __name__ == "__main__":
   # app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
#    sess.init_app(app)
    #app.debug = True
    #app.run(host='54.37.75.43', debug=True) #HOST FOR SERVER
    app.run(host='0.0.0.0',port=50022)



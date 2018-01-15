# web-rcat

# rCAT
This page describes the tool for the relational character analysis tool. The purpose of rCAT is to extract relations of entities in a text and generate a pdf report. Relational information about entities can be helpful to get an insight into the text structure in terms of relations of entities. For more details about the implementation see the abstract: Barth, Florian and Kim, Evgeny and Murr, Sandra and Klinger, Roman (2018). "A Reporting Tool for Relational Visualization and Analysis of Character Mentions in Literature" (DHd 2018 Köln).

# Installation
There are some major dependencies the tool needs. Follow the installation instructions from the relevant pages: 
  - Python v.3.6 and higher. It is better if you get Anaconda distribution (https://www.anaconda.com/download) 
  -Graphviz, a vizualization package (http://www.graphviz.org/Download.php). 
 - LaTex (https://www.latex-project.org/get/). 
 - Flask Web framework (http://flask.pocoo.org/).
 - Treetaggerwrapper (http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/) 

In addition, there are other dependecies as well as Python wrappers that should also be installed via "pip" command:
```sh
$ pip install pylatex
$ pip install numpy
$ pip install nltk
$ pip install graphviz
$ pip install wordcloud 
$ pip install treetaggerwrapper
```
If you use Anaconda python distribution, you may skip numpy and nltk as they are preinstalled. 
The next step is to get necessary libraries from NLTK package. In terminal, type:

```sh
$ python
```
```sh
A python environment will open. 
$ Python 3.6.1 |Anaconda custom (x86_64)| (default, May 11 2017, 13:04:09) 
[GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import nltk
>>> nltk.download()
```
A window opens: select "popular packages" and download them. Close the window after the download process is finished.

Clone this repository, navigate to the directory "flask_app" within "web-rcat" folder. Then start the program as: 
```sh
$ python flask_form.py
```
You will see the following status:

```sh
 * Running on http://0.0.0.0:50029/ (Press CTRL+C to quit)
 ```
 Open the url in your browser. This will lead you to the main page of the tool. Now you can start working with it!
 
 # Working with rCAT
 TBD

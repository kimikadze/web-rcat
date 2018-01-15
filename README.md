# rCAT
This page describes the tool for the relational character analysis tool. The purpose of rCAT is to extract relations of entities in a text and generate a pdf report. Relational information about entities can be helpful to get an insight into the text structure in terms of relations of entities. For more details about the implementation and citation see the abstract: Barth, Florian and Kim, Evgeny and Murr, Sandra and Klinger, Roman (2018). "A Reporting Tool for Relational Visualization and Analysis of Character Mentions in Literature". Abstract presented at DHd 2018 Conference. Köln, Germany.

### Installation
There are some major dependencies the tool needs. Follow the installation instructions from the relevant pages: 
 - Python v.3.6 and higher. It is better if you get Anaconda distribution (https://www.anaconda.com/download) 
 - Graphviz, a vizualization package (http://www.graphviz.org/Download.php). 
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
 
 ### Working with rCAT
 
 The web interface has the following fields: 

 ##### Select text file: 
 Click Choose file to select the text you want to analyze. The file should be in a plain text format.

 ##### Select character file: 
 Click Choose file to select the text with character names.   

> The file with character names should be formatted as follows: 
> each line starts with a canonical name for a single character. 
> Separated by tab are aliases of this character. 
> Each character and list of his/her aliases should be entered on separate lines.

##### Specify relation distance: 
This should be an integer. How many words between mentions of two characters are considered as proximity. Default is 10.

##### Specify words before : 
This should be an integer. How many words before the mention of the first character to include into the contextual analysis. Default is 8.

##### Specify words after: 
This should be an integer. How many words after the mention of the second character to include into the contextual analysis. Default is 8.

##### Remove stop words (y/n)?: 
Remove stop words from contextual analysis or no. Default Yes. 

##### Lemmatization 
This option will lemmatize each word in the text (cast it to its base form). This option is especially usefull when working with relatively short texts. 

##### Word clouds to show 
Parameter that defines how many word clouds will be generated. This should be an integer. This option will show only n-top word clouds for each character and character pair. Default is 5. 

##### Text language
German, English

##### Segments: 
This should be an integer. Number of segments into which the book should be splitted to track the word field development of the story. Default is 10. 

#####  Analyze with word fields: 
There are two ways in which you can provide word fields.
>Single category: One plain text file with one word per line. The tool will then use this words to characterize characters, relations between characters, and plot the development of these word field in a single plot. 
Multi-category: Multiple files structured as described above. Files names correspond to the categories of the word fields. The tool will plot the development of these word fields in multiple plots. Warning: multi-category word clouds are not currently supported. 

##### Filter word clouds by:
You can filter the words appearing the word cloud either by the most freq words or by pointwise mutual information. 

##### Choose the amount of words in the word clouds: 
How many words should each word cloud consist of.

##### Perform Zeta analysis:
This is a stylometry parameter that measure that computes prefered and avoided terms for a target group compared to a comparison group. 


##### Run analysis: 
Run the program. 

The program will analyze the text and generates a pdf report that you can download by clicking Download on a page you are redireted.

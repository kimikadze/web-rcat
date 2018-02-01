from nltk import word_tokenize
#import treetaggerwrapper
import re
import treetaggerwrapper
import os

class text_reader:

    def __init__(self):
        pass

    def read_text_file(self, txt_file):
        with open(txt_file, encoding='utf-8') as txt_data:
            txt = txt_data.read()
        return txt


    def tokenize_lemmatize_text(self, txt, lemmatize="n", text_language= "German"):#,remove_stopwords == "n"):
        # tokenizes text

        # so far: don't use stop word removal here since this cuts out all personal pronouns of the text that we
        # potentially want to use for establishing character relations; either by generalisation (Werther == I) or
        # by coreference resolution


        # TOKENISATION WITH NLTK.WORD_TOKENIZE

        # if lemmatize == "n":
		#
        #     text_tokenized = word_tokenize(txt, language=text_language)
        #     text_tokenized_stripped = list()
        #     #remove all punctation from false tokenized words
        #     for word in text_tokenized:
        #         #print(word)
        #         if (word != "." and word != "!" and word != "?" and word != "," and word != ":" and word != "–" and word != "'" and word != "»" and word != "«" and word != "’"):
        #             text_tokenized_stripped += [word.strip(".")]
		#
        #     return text_tokenized_stripped


        # TOKENIZATION AND LEMMATIZATION WITH TREETAGGER

        exlude_from_text = [".", "!", "?", ",", ":", "-", "'", "»", "«", "’"]


        if lemmatize == "n" and text_language=="MHG":
            print(os.getcwd())
            output = os.popen("../../treetagger/cmd/tree-tagger-middle-high-german > output.txt")
            output.read()
            output.close()
            with open("output.txt") as f:
                for i in f:
                    print(i)





        if lemmatize == "n" and text_language=="German":
            tt = treetaggerwrapper.TreeTagger(TAGLANG='de')
            txt_pos = tt.tag_text(txt)

            txt_word_pos_lemma = list()
            for word_pos_lemma in txt_pos:
                txt_word_pos_lemma_split = re.split("\t", word_pos_lemma)
                txt_word_pos_lemma += [txt_word_pos_lemma_split]

            text_lemmatized = list()
            for i in txt_word_pos_lemma:
                if i[0] not in exlude_from_text:
                    text_lemmatized += [i[0]]
            return text_lemmatized



        if lemmatize == "n" and text_language=="English":
            tt = treetaggerwrapper.TreeTagger(TAGLANG='en')
            txt_pos = tt.tag_text(txt)

            txt_word_pos_lemma = list()
            for word_pos_lemma in txt_pos:
                txt_word_pos_lemma_split = re.split("\t", word_pos_lemma)
                txt_word_pos_lemma += [txt_word_pos_lemma_split]

            text_lemmatized = list()
            for i in txt_word_pos_lemma:
                if i[0] not in exlude_from_text:
                    text_lemmatized += [i[0]]
            return text_lemmatized



        if lemmatize == "treetagger" and text_language== "German":
            tt = treetaggerwrapper.TreeTagger(TAGLANG='de')
            txt_pos = tt.tag_text(txt)

            txt_word_pos_lemma = list()
            for word_pos_lemma in txt_pos:
                txt_word_pos_lemma_split = re.split("\t", word_pos_lemma)
                txt_word_pos_lemma += [txt_word_pos_lemma_split]

            text_lemmatized = list()
            for i in txt_word_pos_lemma:
                if (i[2] == '<unknown>' or i[2] == '@card@'):
                    text_lemmatized += [i[0]]
                if (i[2]) == "Sie|sie":
                    text_lemmatized += ["sie"]
                else:
                    if i[2] not in exlude_from_text:
                        text_lemmatized += [i[2]]

            #print(text_lemmatized)
            return text_lemmatized


        if lemmatize == "treetagger" and text_language== "English":
            tt = treetaggerwrapper.TreeTagger(TAGLANG='en')
            txt_pos = tt.tag_text(txt)

            txt_word_pos_lemma = list()
            for word_pos_lemma in txt_pos:
                txt_word_pos_lemma_split = re.split("\t", word_pos_lemma)
                txt_word_pos_lemma += [txt_word_pos_lemma_split]

           # print(txt_word_pos_lemma)
            text_lemmatized = list()
            for i in txt_word_pos_lemma:
                if (i[2] == '<unknown>' or i[2] == '@card@'):
                    text_lemmatized += [i[0]]
                else:
                    if i[2] not in exlude_from_text:
                        text_lemmatized += [i[2]]

            #print(text_lemmatized)
            return text_lemmatized



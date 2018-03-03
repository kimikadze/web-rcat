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


    def tokenize_lemmatize_text(self, txt, txt_file, lemmatize="n", text_language= "German"):#,remove_stopwords == "n"):
        # tokenizes text

        # so far: don't use stop word removal here since this cuts out all personal pronouns of the text that we
        # potentially want to use for establishing character relations; either by generalisation (Werther == I) or
        # by coreference resolution




        # TOKENIZATION AND LEMMATIZATION WITH TREETAGGER

        exlude_from_text = [".", "!", "?", ",", ":", "-", "'", "»", "«", "’", "“", '"']


        if lemmatize == "n" and text_language=="MHG":
            #print(os.getcwd())
            #output = os.popen("echo '%s' | ../../treetagger/cmd/tree-tagger-middle-high-german > output.txt" %txt)
            output = os.popen("cat '%s' | ../../treetagger/cmd/tree-tagger-middle-high-german > output.txt" %txt_file)


            output.read()
            output.close()


            with open("output.txt") as f:
                #lines = f.readlines()
                token_pos_lemma_complete_text = list()
                for line in f:
                    token_pos_lemma = line.strip().split("\t")
                    if token_pos_lemma[0] not in exlude_from_text:
                        token_pos_lemma_complete_text.append(token_pos_lemma[0])


                #print(token_pos_lemma_complete_text)
                return token_pos_lemma_complete_text


        if lemmatize == "treetagger" and text_language=="MHG":
            #print(os.getcwd())

            #output = os.popen("echo '%s' | ../../treetagger/cmd/tree-tagger-middle-high-german > output.txt" %txt)
            output = os.popen("cat '%s' | ../../treetagger/cmd/tree-tagger-middle-high-german > output.txt" %txt_file)



            output.read()
            output.close()

            with open("output.txt") as f:
                #lines = f.readlines()
                token_pos_lemma_complete_text = list()
                for line in f:
                    token_pos_lemma = line.strip().split("\t")
                    if (token_pos_lemma[2] == '<unknown>' or token_pos_lemma[2] ==  '@card@'):
                        token_pos_lemma_complete_text.append(token_pos_lemma[0])

                    else:
                        if token_pos_lemma[2] not in exlude_from_text:
                            token_pos_lemma_complete_text.append(token_pos_lemma[2])

                #print(token_pos_lemma_complete_text)
                return token_pos_lemma_complete_text




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
            print(text_lemmatized)
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
                try:
                    if (i[2] == '<unknown>' or i[2] == '@card@'):
                        text_lemmatized += [i[0]]
                    if (i[2]) == "Sie|sie":
                        text_lemmatized += ["sie"]
                    else:
                        if i[2] not in exlude_from_text:
                            text_lemmatized += [i[2]]
                except IndexError:
                    pass



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
                try:
                    if (i[2] == '<unknown>' or i[2] == '@card@'):
                        text_lemmatized += [i[0]]
                    else:
                        if i[2] not in exlude_from_text:
                            text_lemmatized += [i[2]]
                except IndexError:
                    pass
                continue

            #print(text_lemmatized)
            return text_lemmatized



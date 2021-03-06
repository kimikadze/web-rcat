import matplotlib.cbook
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os
import re


class WordField:

    def __init__(self, word_field, wf_cat, segments):
        # self.dictionary = pickle.load(open(dictionary,'rb'))
        self.word_field = word_field # multi or single
        self.wf_cat = wf_cat
        self.split_value = segments


    def read_text_file(self, txt_file):
        with open(txt_file,'r', encoding="utf-8") as txt_data:
            txt = txt_data.read()
            txt = np.array(txt.split())
            self.text_lenght = len(txt)
            chunks = np.array_split(txt, self.split_value)

            return chunks

    def score(self, chunks):
        FieldDict = {}
        Sequence = {}
        if self.word_field == "single" or self.word_field == "werther_emotions":
            for line in open(self.wf_cat, 'r', encoding="utf-8"):
                line = line.strip()
                FieldDict[line] = 1

            Sequence = {"Word field": []}
            normalization = 10000  # normalization value for calculating the score -- adaptable
            for n, chunk in enumerate(chunks):
                Counts = {}
                Field_seq = {}
                Field_seq[n] = 0
                for token in chunk:
                    if token in FieldDict:
                        if not token in Counts:
                            Counts[token] = 1
                        else:
                            Counts[token] += 1
                for value in Counts.values():
                    Field_seq[n] += (value * normalization)/(self.text_lenght * len(FieldDict))
                for score in Field_seq.values():
                    Sequence["Word field"].append(score)

        elif self.word_field == "multi":
            FieldDict = {}
            normalization = 10000
            for filename in self.wf_cat:
                filename = filename.split('/')[-1]
                #print(("xxx 111"))
                #print(filename)
                filename = re.match("[0-9]__(.*?)\.", filename).group(1)

                #filename = filename.split('.')[-2]
                FieldDict[filename] = []
            #for root, dirs, files in os.walk(self.word_field):
            for filename in self.wf_cat:
                for line in open(filename,encoding="utf-8"):
                    line = line.strip()
                    #print("aaa")
                    #print(filename)
                    filename_x = filename.split('/')[-1]
                    filename_y = re.match("[0-9]__(.*?)\.", filename_x).group(1)
                    #print(("xxx 222"))
                    #print(filename)

                    #filename = filename.split('.')[-2]
                    if filename_y in FieldDict:
                        FieldDict[filename_y].append(line)

            for key in FieldDict.keys():
                Sequence[key] = []
            for chunk in chunks:
                Counts = {}
                for token in chunk:
                    if token not in Counts:
                        Counts[token] = 1
                    else:
                        Counts[token] += 1
                Field_seq = {}
                for key in FieldDict.keys():
                    Field_seq[key] = 0
                for k,v in Counts.items():
                    for key,value in FieldDict.items():
                        if k in value:
                            if not key in Field_seq:
                                Field_seq[key] = round((v*normalization)/(self.text_lenght*len(key)),4)
                            else:
                                Field_seq[key] += round((v*normalization)/(self.text_lenght*len(key)),4)
                for w,score in Field_seq.items():
                    Sequence[w].append(score)
        return Sequence


    def plot_wordfield(self, sequence):

        font = {'family': 'sans', 'weight': 'normal', 'size': 12}
        plt.rc('font', **font)
        fig = plt.figure(figsize=(10, 10))
        fig.subplots_adjust(bottom=0.05)
        N = self.split_value
        bin = np.arange(N)

        for n,(field,development) in enumerate(sequence.items()):
            colors = np.random.rand(3)
            plt.subplot(len(sequence),1, n+1)
            plt.plot(development,c=colors, linewidth=2)
            plt.title(field)
            plt.subplots_adjust(hspace=1)
            plt.yticks([])
            plt.xlim([0,bin.size-1])
            plt.xticks([])

        # plt.show()
        with PdfPages('data/temp_folder/word_field.pdf') as pdf:
            pdf.savefig(fig)
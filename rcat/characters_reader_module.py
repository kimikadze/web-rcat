from nltk import word_tokenize
from stanfordcorenlp import StanfordCoreNLP
import codecs
import io
# from corenlp_pywrap import pywrap
# from corenlp_pywrap import pywrap
import os
import re
import pprint




class characters_reader:


##### a) use list

    def __init__(self):
        pass

    def read_characters(self, char_file):
        with open(char_file, encoding='UTF-8') as char_data:
            doc = char_data.readlines()
            character_list = list()
            for line in doc:
                splitted_line = line.split("\t")
                splitted_line[-1] = splitted_line[-1].strip()
                splitted_line[0] = splitted_line[0].strip("\ufeff")
                character_list += [splitted_line]
            return character_list

    # reads the characters line by line
    # (each line contains one character, with tabstop separated synonyms)

###########################################################################################################

    def tokenize_characters(self, character_list):
        characters_list_tokenized = list()
        for single_character_list in character_list:
            new_single_char_list = list()
            for i in single_character_list:
                new_single_char_list += [word_tokenize(i)]
            characters_list_tokenized += [new_single_char_list]
        #Problem: sometimes tokenisation includes dotes with single characters: ["Graf", "R."] sometimes not: ["N.", "N", "."]
        #remove all dots:
        characters_list_tokenized_without_dots = list()
        for single_character_list in characters_list_tokenized:
            new_single_char_list_2 = list()
            for synonym_liste in single_character_list:
                # get all indices for elements that contain only "." and remove these elements:
                remove_indices = [item for item in range(len(synonym_liste)) if synonym_liste[item] == "."]
                # return only that indices that should not be removed:
                new_single_char_list_2 += [[i for j, i in enumerate(synonym_liste) if j not in remove_indices]]
            characters_list_tokenized_without_dots += [new_single_char_list_2]

        characters_list_tokenized_without_dots_stripped = list()
        for single_character_list in characters_list_tokenized_without_dots:
            new_single_char_list = list()
            for synonym_liste in single_character_list:
                new_synonym_list = list()
                for i in synonym_liste:
                    new_synonym_list += [i.strip(".")]
                new_single_char_list += [new_synonym_list]
            characters_list_tokenized_without_dots_stripped += [new_single_char_list]

        return characters_list_tokenized_without_dots_stripped

    # tokenizes characters

    ## data scheme:
    ## [ [ [char_a], [a_synonym_1], [a_synonym_2_token_i, a_synonym_2_token_ii], ... ], [ [char_b], ... ] ]


############################################################################
############################################################################



##### b) use core NLP


    def ner_stanfordcorenlp_wrapper(txt):
        #first start server with:
        #java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer
        # (in directory of stanfordcorenlp)



        #nlp = StanfordCoreNLP(r"/Users/Florian/Applications/SourceTree/rCat/stanford-corenlp-full-2016-10-31 symlink")
        #nlp = StanfordCoreNLP(r"/Applications/stanford-corenlp-full-2016-10-31/")
        nlp = StanfordCoreNLP(r"/Applications/stanford-corenlp-full-2016-10-31/", lang="de")


        #with io.open(txt, "r", encoding="utf-8") as file:
        #with codecs.open(txt, "r", encoding="utf-8") as file:
        #with open(txt, "r", encoding="utf-8") as file:
        with open(txt, "r", encoding="latin") as file:

            text_rar = file.read()
            #print(type(text_rar))
            #print(str(text_rar))

            print("Running Stanford Core NLP...")
            print(nlp.word_tokenize(text_rar))



    # def ner_pywrap(text):
    #     #first start server with:
    #     #java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer
    #     # (in directory of stanfordcorenlp)
    #
    #     with open(text, "r", encoding="latin") as file:
    #     #with open(text, "r", encoding="utf-8") as file:
    #
    #         text_rar = file.read()
    #         #text_rar.encode('latin-1')
    #         full_annotator_list = ["tokenize", "cleanxml", "ssplit", "pos", "lemma", "ner", "regexner", "truecase", "parse",
    #                                "depparse", "dcoref", "relation", "natlog", "quote"]
    #         ner_annotator_list = ["tokenize", "ssplit", "pos", "lemma", "ner"]
    #         cn = pywrap.CoreNLP(url='http://localhost:9000', annotator_list=ner_annotator_list)
    #         out = cn.basic(text_rar, out_format='json')
    #         print(out.text)


    def ner_corenlp_direct(txt):
        #get current directory:
        app_directory = os.getcwd()
        ##print(app_directory)

        #os.chdir("stanford-corenlp-full-2016-10-31 symlink")
        os.chdir("/Applications/stanford-corenlp-full-2016-10-31/")
        #output = os.popen('java -mx3g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLP -props StanfordCoreNLP-german.properties -file %s/werther_adaptations/Lenz_Der_Waldbruder_ein_Pendant_zu_Werthers_Leiden_kindle.txt -outputFormat conll' % app_directory)
        output = os.popen('java -mx3g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLP -props StanfordCoreNLP-german.properties -file _text/Dep_Parse_de_Kopie.txt -outputFormat conll')
        for line in output:
            print(line)
        output.read()
        output.close()

        os.chdir("/Applications/stanford-corenlp-full-2016-10-31/")
        with open("Dep_Parse_de_Kopie.txt.conll") as f:
            lines = f.readlines()
            print(lines)




###### c) use Weblicht-API to write NER to file

    def weblicht_ner(txt, folder):
        #os.chdir("weblicht")
        output = os.popen("curl -X POST -F chains=@weblicht/weblicht_ner_chain_german.xml -F content=@%s/%s\
            -F apikey=0000015edeabbcc6k37uGuo/kTwD5CMLLcN0xCM0lreYPPOVq9a52+BggmE= https://weblicht.sfs.uni-tuebingen.de/WaaS/api/1.0/chain/process > weblicht/output/%s.tcf" % (folder, txt, txt))
        for i in output:
            print(i)
        output.read()
        output.close()

    def tcf_reader(tcf_file):
        with open("weblicht/output/%s.tcf" % tcf_file) as f:
            #get tokens
            lines = f.readlines()
            #tokens = []
            tokens = {}
            ner_ids = []
            for line in lines:
                finding = re.findall('<tc:token ID="(.*)">(.*)</tc:token>', line)
                if len(finding) > 0:
                    tokens[finding[0][0]] = finding[0][1]


                #if len(finding) > 0:
                    #tokens += finding

                #get ner id
                finding_ner = re.findall('<tc:entity tokenIDs="(.*)" class="(.*)"></tc:entity>', line)
                if len(finding_ner) > 0:
                    #print(finding_ner)
                    #print(re.split(" ",finding_ner[0][0]))
                    ner_ids += [[re.split(" ",finding_ner[0][0]), finding_ner[0][1]]]

        #solve ner_ids
        ner = []
        for entity_id_with_tag in ner_ids:
            entity_with_proper_names = []
            for ner_id in entity_id_with_tag[0]:
                entity_with_proper_names += [tokens[ner_id]]
            entity_with_proper_names_and_tag = [entity_with_proper_names, entity_id_with_tag[1]]
            ner.append(entity_with_proper_names_and_tag)


        #get unique
        ner_unique = []
        for entity in ner:
            if entity not in ner_unique:
                ner_unique.append(entity)

        return ner_unique

        #print(ner_unique)


    def write_PER_to_file(ner, filename):
        with open("weblicht/output/%s_PER.txt" %filename, mode="w") as f:
            for entity in ner:
                if entity[1] == "PER":
                    for token in entity[0]:
                        f.write(token + " ")
                    f.write("\n")


    # def main_write_weblicht_PER(txt, folder):
    #
    #     characters_reader.weblicht_ner(txt, folder)
    #     NERs = characters_reader.tcf_reader(txt)
    #     characters_reader.write_PER_to_file(NERs, filename=txt)


    def main_write_all_files_in_folder(folder):
        for txt in os.listdir(folder):
            characters_reader.weblicht_ner(txt, folder)
            NERs = characters_reader.tcf_reader(txt)
            characters_reader.write_PER_to_file(NERs, filename=txt)

            # print(i)
            #characters_reader.main_write_weblicht_PER(i)


#run single functions
#characters_reader.main_write_all_files_in_folder("Texte_Perutz")

















































#for i in os.listdir("werther_adaptations"):
#    #print(i)
#    characters_reader.main_write_weblicht_PER(i)


# for i in os.listdir("Texte_Perutz"):
#     #print(i)
#     characters_reader.main_write_weblicht_PER(i)








#characters_reader.weblicht_ner("2003_Bönisch_Dana_Rocktage.txt")
#NERs = characters_reader.tcf_reader("2003_Bönisch_Dana_Rocktage.txt")
#characters_reader.write_PER_to_file(NERs)


#characters_reader.ner_stanfordcorenlp_wrapper("werther_adaptions/2003_Bönisch, Dana_Rocktage.txt")
# characters_reader.ner_stanfordcorenlp_wrapper("werther_adaptations/2003_Bönisch, Dana_Rocktage.txt")
# characters_reader.ner_stanfordcorenlp_wrapper("werther_adaptations/Nicolai_Freuden des jungen Werthers, Leiden und Freuden Werthers des Mannes_kindle.txt")
# characters_reader.ner_stanfordcorenlp_wrapper("werther_adaptations/1910_Jacobowski, Ludwig_Werther der Jude_ohne Zeilenumbrüche.txt")
#characters_reader.ner_stanfordcorenlp_wrapper("werther_adaptations/Dilan/1910_Jacobowski, Ludwig_Werther der Jude_ohne Zeilenumbrüche_latin.txt")

#characters_reader.ner_pywrap("werther_adaptations/1939_Mann_Lotte in Weimar_konvertiert.txt")
#characters_reader.ner_pywrap("werther_adaptations/Dilan/1910_Jacobowski, Ludwig_Werther der Jude_ohne Zeilenumbrüche_latin.txt")


#characters_reader.ner_corenlp_direct("1910_Jacobowski, Ludwig_Werther der Jude_ohne Zeilenumbrüche.txt")











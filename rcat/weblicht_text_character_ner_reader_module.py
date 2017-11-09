import os
import re



class weblicht_text_character_ner_reader:
    def __init__(self):
        pass



    def weblicht_tcf(filepath):
        # os.chdir("weblicht")

        filename_without_path = re.findall(".*/(.*)/(.*.txt)", filepath)
        print(filepath)

        output = os.popen("curl -X POST -F chains=@rcat/weblicht/weblicht_ner_chain_german.xml -F content=@rcat/doc/texts/Goethe_Die_Leiden_des_jungen_Werthers_1774.txt\
            -F apikey=0000015edeabbcc6k37uGuo/kTwD5CMLLcN0xCM0lreYPPOVq9a52+BggmE= https://weblicht.sfs.uni-tuebingen.de/WaaS/api/1.0/chain/process > rcat/test_folder/%s.tcf" % (
            filename_without_path[0][1]))
            #filepath, filename_without_path[0][1]))
        for i in output:
            print(i)
        output.read()
        output.close()

    def tcf_reader(tcf_file):
        with open(tcf_file) as f:

            lines = f.readlines()

            weblicht_data_holder = {}

            tokens = {}
            lemmas = {}

            ner_ids = []
            for line in lines:
                finding = re.findall('<tc:token ID="(.*)">(.*)</tc:token>', line)
                if len(finding) > 0:
                    tokens[finding[0][0]] = finding[0][1]


            weblicht_data_holder["tokens"] = tokens


            for line in lines:
                finding = re.findall('<tc:lemma ID="l_(.*)" tokenIDs="(.*)">(.*)</tc:lemma>', line)
                if len(finding) > 0:
                    ###lemmas["%s_%s" (finding[0][0],finding[0][1])] = finding[0][2]
                    lemma = int(finding[0][0])
                    lemma_plus_one = str(lemma+1)
                    lemma_plus_one_with_l = str("l"+lemma_plus_one)
                    ###token = finding[0][1]
                    lemmas[lemma_plus_one_with_l] = finding[0][2]

            weblicht_data_holder["lemmas"] = lemmas

            return weblicht_data_holder


    def build_lemmatized_text(weblicht_data_holder):

        lemmas = weblicht_data_holder["lemmas"]
        print(len(lemmas))
        tokens = weblicht_data_holder["tokens"]
        print(len(tokens))

        lemmatized_text = list()

        for index in range(len(lemmas)):
            if lemmas["l%s" %(index+1)] in ["&lt;unknown&gt;", "@card@", "@ord@"]:
                lemmatized_text.append(tokens["t%s" %(index+1)])
            else:
                lemmatized_text.append(lemmas["l%s" %(index+1)])

        return lemmatized_text




#data_holder = weblicht_text_character_ner_reader.tcf_reader("test_folder/Goethe_Die_Leiden_des_jungen_Werthers_1774.txt.tcf")
#weblicht_text_character_ner_reader.build_lemmatized_text(data_holder)







































        #         finding_ner = re.findall('<tc:entity tokenIDs="(.*)" class="(.*)"></tc:entity>', line)
        #         if len(finding_ner) > 0:
        #             # print(finding_ner)
        #             # print(re.split(" ",finding_ner[0][0]))
        #             ner_ids += [[re.split(" ", finding_ner[0][0]), finding_ner[0][1]]]
        #
        # # solve ner_ids
        # ner = []
        # for entity_id_with_tag in ner_ids:
        #     entity_with_proper_names = []
        #     for ner_id in entity_id_with_tag[0]:
        #         entity_with_proper_names += [tokens[ner_id]]
        #     entity_with_proper_names_and_tag = [entity_with_proper_names, entity_id_with_tag[1]]
        #     ner.append(entity_with_proper_names_and_tag)
        #
        # # get unique
        # ner_unique = []
        # for entity in ner:
        #     if entity not in ner_unique:
        #         ner_unique.append(entity)
        #
        # return ner_unique
        #
        # # print(ner_unique)



#weblicht_text_character_ner_reader.weblicht_tcf("Goethe_Die_Leiden_des_jungen_Werthers_1774.txt", "texts")

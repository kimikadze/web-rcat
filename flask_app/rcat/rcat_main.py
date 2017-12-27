import os
from tkinter import *
from tkinter import filedialog, messagebox

from rcat.characters_reader_module import characters_reader
#from characters_reader_module import characters_reader

from rcat.network_generator_module import network_generator
#from network_generator_module import network_generator

from rcat.network_parameters_module import network_parameters
#from network_parameters_module import network_parameters

from rcat.relations_module import relations
#from relations_module import relations

from rcat.text_reader_module import text_reader
#from text_reader_module import text_reader

from rcat.word_field_module import WordField
#from word_field_module import WordField

from rcat.pdf_latex_module import pdf_latex
#from pdf_latex_module import pdf_latex



class rcat(object):

    def __init__(self):
        pass


    def data_holder(self, text__file, character__file, temporary_path=str(),
                    distance_parameter=[5, 3, 3], del_stopwords_in_context="n", segments=int(10),
                    number_of_wc=str(), write_gephi_csv = str(), word_field=str(), wf_cat=str(), lemmatisation="n",
                    language="German",choose__method=str()):

        # holder = dict(character_relations=0, character_relations_context=0, text_file=0, character_file=0,
        #               tokenized_text=0, characters=0, parameter=0, network_parameters=0,
        #               single_character_context=0, segments=0, lemmatisation=0, lang=0, number_of_wc=0, word_field=0, wf_cat=0)


        if word_field != "N":

            start_wf = WordField(word_field=word_field, wf_cat=wf_cat, segments=segments)
            chunked = start_wf.read_text_file(txt_file=text__file)
            scores = start_wf.score(chunked)
            start_wf.plot_wordfield(scores)
        else:
            pass

        if lemmatisation != "weblicht":
            txt = text_reader().read_text_file(txt_file=text__file)
            txt_tokenized = text_reader().tokenize_lemmatize_text(txt, lemmatize=lemmatisation, text_language=language)

            characters = characters_reader().read_characters(char_file=character__file)
            characters_tokenized = characters_reader().tokenize_characters(characters)

            # print("compute character relations...")
            character_positions = relations().find_character_positions(txt_tokenized, characters_tokenized)
            character_pairs = relations().build_character_pairs(characters, characters_tokenized)
            character_relations = relations().build_relations(character_positions, character_pairs,
                                                              distance_for_relation=distance_parameter[0])

            # print("find context for characters...")
            #print(os.getcwd())
            character_relations_context = relations().count_context_words(character_relations, txt_tokenized,
                                                                          words_before=distance_parameter[1],
                                                                          words_after=distance_parameter[2],
                                                                          delete_stopwords_in_context=del_stopwords_in_context,
                                                                          word_field=word_field, wf_cat=wf_cat,
                                                                          stop_words="./data/stopwords/stopwords_de_except_ich.txt")
                                                                            #stop_words="./data/stopwords/Stoppwortliste_mittelhochdeutsch_erweitert_with_character_names_ONEWORD.txt")
                                                                          #stop_words="./data/stopwords/Stoppwortliste_mittelhochdeutsch_erweitert_with_character_names_underscore.txt")

            single_character_context = relations().count_context_words_for_single_characters(character_positions,
                                                                                             characters,
                                                                                             txt_tokenized, delete_stopwords_in_context=del_stopwords_in_context,
                                                                                             word_field=word_field,
                                                                                             wf_cat=wf_cat,
                                                                                             stop_words="./data/stopwords/stopwords_de_except_ich.txt")
                                                                                             #stop_words="./data/stopwords/Stoppwortliste_mittelhochdeutsch_erweitert_with_character_names_ONEWORD.txt")
                                                                                            #stop_words = "./data/stopwords/Stoppwortliste_mittelhochdeutsch_erweitert_with_character_names_underscore.txt")




            holder = {"character_relations": character_relations,
                      "character_relations_context": character_relations_context,
                      "text_file": text__file, "character_file": character__file, "tokenized_text": txt_tokenized,
                      "characters": characters, "parameter": distance_parameter,
                      "network_parameters": 0, "single_character_context": single_character_context,
                      "segments": segments, "lang": "./data/stopwords/stopwords_de_except_ich.txt", "number_of_wc": number_of_wc, "word_field": word_field,
                      "wf_cat": wf_cat}


            netw_parameters = network_parameters().calculate_network_parameters(holder["character_relations"],
                                                                                holder["characters"])

            # print("build network...")

            network_generator.build_and_plot_graph_vis_col(holder["character_relations"], netw_parameters,number_of_wc,temppath=temporary_path)

            holder["network_parameters"] = netw_parameters



        return holder



    def main_PDF(self,
                 text_file,
                 character_file,
                 dist_parameter,
                 remove_stopwords_in_context,
                 segments,
                 number_of_wc=3,
                 write_gephi_csv="n",
                 word_field=str(),
                 wf_cat=str(),
                 lemmatisation="n",
                 txt_language="German",
                 choose_method="graphvis_col",
                 sess_id=False,
                 word_cloud_context_selection = "MFW",
                 words_in_wc = 12):

        dirpath = os.getcwd()
        if sess_id==False:
            dirpath = os.path.join(dirpath, "data/temp_folder")
        else:
            dirpath = os.path.join(dirpath, "data_user/%s_temp_folder" %sess_id)
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
                #dirpath = os.path.join(dirpath, "data_user/%s_temp_folder" %sess_id)

        d_holder = self.data_holder(text_file,
                                    character_file,
                                    dirpath,
                                    dist_parameter,
                                    remove_stopwords_in_context,
                                    segments,
                                    number_of_wc,
                                    write_gephi_csv,
                                    word_field,
                                    wf_cat,
                                    lemmatisation,
                                    language=txt_language,
                                    choose__method=choose_method)


        # print("writing PDF...")
        pdf = pdf_latex().initialize()
        pdf_latex().write_header(pdf)
        pdf_latex().network_figure(pdf, dirpath, method=choose_method)
        pdf_latex().write_data_input(pdf, d_holder)
        pdf_latex().write_netork_parameters(pdf, d_holder)
        pdf_latex().write_word_cloud_single_character(pdf, d_holder, number_of_wc=number_of_wc, tpath=dirpath, wc_context_selection=word_cloud_context_selection, words_in_word_cloud = words_in_wc)
        pdf_latex().write_word_cloud(pdf, d_holder, number_of_wc=number_of_wc, tpath=dirpath, wc_context_selection=word_cloud_context_selection, words_in_word_cloud = words_in_wc)
        pdf_latex().write_wordfield_curve(pdf, d_holder, wf_cat)
        pdf_latex().word_field_curve(pdf, wf_cat)
        pdf_latex().write_prgramm_statments(pdf)
        pdf_latex().finalize(pdf, s_id=sess_id)
        # print("PDF complete")

        #messagebox.showinfo("Status", "Analysis is complete. PDF report is generated.")

        if write_gephi_csv == "y":
            csv_line_data = network_generator.build_csv_lines_for_gephi(d_holder["character_relations"], weight="log")
            network_generator.write_gephi_data_to_csv(csv_line_data)
            #messagebox.showinfo("Information", "Gephi input is genereated")




# if __name__ == "__main__":
#
#
#     rcat().main_PDF(text_file="/Users/Florian/Applications/SourceTree/web-rcat/flask_app/data/CRETA_internal/Werther/Goethe_Die_Leiden_des_jungen_Werthers_1774.txt", character_file="/Users/Florian/Applications/SourceTree/web-rcat/flask_app/data/CRETA_internal/Werther/Goethe_Werther_74_characters.txt",
#                   dist_parameter=[8, 5, 5],
#                   remove_stopwords_in_context="n",
#                   segments=5, txt_language="German", number_of_wc=3,
#                   write_gephi_csv="n",
#                   word_field = "N",
#                   wf_cat="None",
#                   lemmatisation="n")
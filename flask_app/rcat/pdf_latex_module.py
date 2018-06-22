import matplotlib
matplotlib.use('Agg')
import operator
import os
import re
import shutil
import numpy as np
import time
import datetime
import matplotlib.pyplot as plt
from operator import itemgetter

from pylatex import Document, Section, Itemize, Subsection, Command, PageStyle, Head, MiniPage, Foot, LargeText, \
    MediumText, LineBreak, simple_page_number, Figure, NoEscape, Tabular, MultiColumn, MultiRow, Package
from pylatex.utils import bold

import os

from rcat.wordcloud_module import word_cloud
from rcat.feature_module import features
#from wordcloud_module import word_cloud


class pdf_latex:
    def __init__(self):
        pass
        # geometry_options = {"margin": "0.7in"}
        # self.doc == Document(geometry_options=geometry_options)

    def initialize(self):
        geometry_options = {"margin": "0.7in"}
        # doc = Document("multirow",geometry_options=geometry_options)
        doc = Document(geometry_options=geometry_options)
        return doc

    def write_prgramm_statments(self, doc):
        section1 = Section("rCat, v.0.1", numbering=False)
        section1.append(
            "This program is developed by Florian Barth and Evgeny Kim with the help of Roman Klinger and Sandra Murr. It is part of the Center for Reflected Text Analytics (CRETA) at the Universtiy of Stuttgart.\n\nFeel free to contact us:")

        list = Itemize()
        list.add_item("rcat@ims.uni-stuttgart.de")

        section1.append(list)
        doc.append(section1)

    def network_figure(self, doc, temp_path, method="graphvis_col"):

        if method == "networkx":
            with doc.create(Figure(position='h!')) as network_pic:
                network_pic.add_image(os.path.join(temp_path, "graph_networkx.png"), width='240px')
                network_pic.add_caption('Network')

        if method == "graphvis":
            with doc.create(Figure(position='h!')) as network_pic:
                network_pic.add_image(os.path.join(temp_path, "network.pdf"))
                network_pic.add_caption('Network')

        if method == "graphvis_col":
            with doc.create(Figure(position='h!')) as network_pic:
                network_pic.add_image(os.path.join(temp_path,"network.pdf"))
                #network_pic.add_image("network.pdf")
                network_pic.add_caption('Network')

    def visualize_zeta(self, doc, zeta_edge_pair_results, path, top_n_results=10):
        # def visualize_zeta(self, edge_pair_result, top_n_results=10):

        section = Section("Zeta Scores for Pairs with highest edge weights")
        section.append("Zeta score is a stylometry measure that measures preferred and avoided terms in the context of character pairs.")

        for index, edge_pair_result in enumerate(zeta_edge_pair_results):
            #features().visualize_zeta(zeta_results[index], name_for_figure="zeta_pair_%s" %index, path=dirpath)

            #subsection = Subsection("Zeta Scores for Pairs with highest edge weights", numbering=False)


            subsection = Subsection("Edge Pair: %s -- %s" %(edge_pair_result["name_target"],edge_pair_result["name_comparison"]), numbering=False)

            #Target (Character A)

            # the following index [::-1] inverts the list for the figure
            objects = [el[0] for el in edge_pair_result["zeta_scores_target_sorted"][0:top_n_results]][::-1]
            y_pos = np.arange(len(objects))
            performance = [el[1] for el in edge_pair_result["zeta_scores_target_sorted"][0:top_n_results]][::-1]

            plt.barh(y_pos, performance, align='center', alpha=0.5)
            plt.yticks(y_pos, objects)
            plt.xlabel('Zeta Score')
            plt.title('%s-context' % edge_pair_result["name_target"])
            # plt.show()
            # plt.savefig("zeta.pdf", bbox_inches='tight')

            #print(path)
            plt.savefig("%s/zeta_pair_%s_a_target.pdf" % (path, index),bbox_inches='tight')

            target_pic = Figure(position="H")
            target_pic.add_image(os.path.join(path, "zeta_pair_%s_a_target.pdf" % index), width='240px')
            target_pic.add_caption("Prefered terms in context of %s (compared to %s)" % (edge_pair_result["name_target"],edge_pair_result["name_comparison"]))
            #wordcloud_pic.add_caption('word cloud of "%s -- %s"' % (

            subsection.append(target_pic)


            ################ Comparison (Character B)

            objects = [el[0] for el in edge_pair_result["zeta_scores_comparison_sorted"][0:top_n_results]][::-1]
            y_pos = np.arange(len(objects))
            performance = [el[1] for el in edge_pair_result["zeta_scores_comparison_sorted"][0:top_n_results]][::-1]

            plt.barh(y_pos, performance, align='center', alpha=0.5)
            plt.yticks(y_pos, objects)
            plt.xlabel('Zeta Score')
            plt.title('%s-context' % edge_pair_result["name_comparison"])
            # plt.show()
            # plt.savefig("zeta.pdf", bbox_inches='tight')
            plt.savefig("%s/zeta_pair_%s_b_comparison.pdf" % (path, index),bbox_inches='tight')

            comparison_pic = Figure(position="H")
            comparison_pic.add_image(os.path.join(path, "zeta_pair_%s_b_comparison.pdf" % index), width='240px')
            comparison_pic.add_caption("Prefered terms in context of %s (compared to %s)" % (edge_pair_result["name_comparison"], edge_pair_result["name_target"]))


            subsection.append(comparison_pic)

            #subsection.append(subsubsection)

            section.append(subsection)
        doc.append(section)


    def word_field_curve(self,doc,wf_cat=str()):
        #print(wf_cat)
        if wf_cat == "None":
            pass
        else:
            with doc.create(Figure(position='H')) as emoarc:
                print(os.getcwd())
                emoarc.add_image("/".join(([os.getcwd(), "data/temp_folder/word_field.pdf"])))
                emoarc.add_caption("Word field development in the current text")

    def write_wordfield_curve(self,doc,dta_holder,wf_cat=str()):
        if wf_cat == "None":
            pass
        else:
            with doc.create(Section("Word field development", numbering=True)) as wordField:
                wordField.append("Word field development in the current book. The plot(s) below show how the presence of certain terms\
                    change with the narrative, from beginning to end.")

    def write_data_input(self, doc, dta_holder):
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        with doc.create(Section("Data Input", numbering=True)):
            with doc.create(Subsection("Statistics", numbering=False)):
                with doc.create(Itemize()) as itmize:
                    itmize.add_item("timestamp: %s" %st )
                    itmize.add_item('analyzed text: "%s"' % dta_holder["text_file"].split('/')[-1])
                    itmize.add_item("length of text: %s tokens" % len(dta_holder["tokenized_text"]))
                    # itmize.add_item("number of characters: %s" % len(dta_holder["characters"]))
                    characters_with_at_least_one_degree = 0
                    for degree_list in dta_holder["network_parameters"][3]:
                        if degree_list[1] != 0:
                            characters_with_at_least_one_degree += 1
                    itmize.add_item(
                        "number of characters (with at least one degree): %s" % str(characters_with_at_least_one_degree))
            with doc.create(Subsection("Input parameters",numbering=False)):
                with doc.create(Itemize()) as itmize:
                    itmize.add_item("distance measure: %s" % dta_holder["parameter"][0])
                    itmize.add_item("context measure 1 (words before Character 1): %s" % dta_holder["parameter"][1])
                    itmize.add_item("context measure 2 (words after Character 2): %s" % dta_holder["parameter"][2])

                # doc.append(\newline)
                # text_file = re.search(".*/(.*)", dta_holder["text_file"])
                # character_file = re.search(".*/(.*)", dta_holder["character_file"])

                # itmize.add_item('command line input: "python main.py -t %s -c %s -d %s -b %s -a %s"' % (
                # text_file.group(1), character_file.group(1), dta_holder["parameter"][0], dta_holder["parameter"][1],
                # dta_holder["parameter"][2]))

    def write_weighted_degrees(self, doc, dta_holder):

        with doc.create(Section("weighted degrees", numbering=False)):
            index = 1
            for weigthed_degree_tuple in dta_holder["network_parameters"][4]:
                with doc.create(Subsection("%s" % weigthed_degree_tuple[0], numbering=False)):
                    doc.append(weigthed_degree_tuple[1])




    def write_word_cloud(self, doc, dta_holder, tpath, number_of_wc, head_of_file_name = "wordcloud", wc_context_selection="MFW", words_in_word_cloud = 12):

        # import float package for -> Figure(position="H")
        doc.packages.append(Package('float'))

        #section = Section("Word Cloud for character pairs", numbering=True)

        if wc_context_selection=="PMI":
            section = Section("Word Cloud for character pairs (method: pointwise mutual information", numbering=True)
            section.append("These word clouds were constructed based on pointwise mutual information (PMI). PMI is a measure of how strongly each term is associated with the character pair. ")
        if wc_context_selection=="MFW":
            section = Section("Word Cloud for character pairs (method: most frequent contexts words", numbering=True)
            section.append("These word clouds were constructed based on most frequent words. They show the most frequent words that appear in the context of the character pair. ")


        network_parameters = dta_holder["network_parameters"]
        edge_weights = network_parameters[6]
        edge_weights_sorted = sorted(edge_weights, key=operator.itemgetter(2), reverse=True)

        ### here we iterate over all context_terms in "character_relations_context"
        ### it is done with the index since a numbering for the word cloud file is necessary
        # for relation in dta_holder["character_relations_context"]:


        if wc_context_selection == "PMI":
            #print(dta_holder["character_relations_context"])
            PMI_all_pairs = features().PMI(context_words=dta_holder["character_relations_context"])
            #print(PMI_all_pairs[0:3])
            # for i in PMI_all_pairs[0:3]:
            #     print(i)

            for edge_pair_list in edge_weights_sorted[0:number_of_wc]:
                for index, character_context_dic in enumerate(PMI_all_pairs):
                    #print(index)
                    if character_context_dic["character_names"][0] == edge_pair_list[0] and character_context_dic["character_names"][1] == edge_pair_list[1]:
                        #print(index, character_context_dic["character_names"], character_context_dic["PMI"])

                        if len(character_context_dic["PMI"][0:words_in_word_cloud]) == 0:
                            text_string = "<<empty_word_cloud>>"
                        if len(character_context_dic["PMI"][0:words_in_word_cloud]) > 0:
                            text_string = str()
                            # for word_freq_tuple in relation["tf_sorted_list"][0:10]:
                            #print(index,character_context_dic["character_names"],character_context_dic["PMI"][0:12])
                            for word_freq_list in character_context_dic["PMI"][0:words_in_word_cloud]:


                                if round(word_freq_list[1]) < 10:
                                    if round(word_freq_list[1]) > 0:
                                        for i in range(round(word_freq_list[1])):
                                            text_string += "%s " %word_freq_list[0]
                                    if round(word_freq_list[1]) <= 0:
                                        text_string += "%s " % word_freq_list[0]

                                if round(word_freq_list[1]) >= 10:
                                    for i in range(9):
                                        text_string += "%s " % word_freq_list[0]

                            #print(text_string)

                        word_cloud.generate_wordcloud_simple(text=text_string, ending_number=index, temppath=tpath, file_name_head = head_of_file_name)
                        # wc = word_cloud.generate_wordcloud_simple(text=str(text_string))

                        #######

                        wordcloud_pic = Figure(position="H")
                        wordcloud_pic.add_image(os.path.join(tpath, "wordcloud%s.png" % index),
                                                width='240px')  # , placement="center")
                        # wordcloud_pic.add_image(wc, width='240px')#, placement="center")

                        # wordcloud_pic.add_caption('word cloud of "%s -- %s"' % (relation["character_names"][0], relation["character_names"][1]))
                        wordcloud_pic.add_caption('word cloud of "%s -- %s"' % (
                        dta_holder["character_relations_context"][index]["character_names"][0],
                        dta_holder["character_relations_context"][index]["character_names"][1]))

                        # subs.append(wordcloud_pic)
                        # section.append(subs)

                        section.append(wordcloud_pic)

            doc.append(section)

        if wc_context_selection=="MFW":

            #BETTER WITH ENUMERATE (CHANGE, IF HAVE SOME TIME)
            # for edge_pair_list in edge_weights_sorted[0:number_of_wc]:
            #     for index, character_context_dic in enumerate(dta_holder["character_relations_context"]):
            #         #print(index)
            #         if character_context_dic["character_names"][0] == edge_pair_list[0] and character_context_dic["character_names"][1] == edge_pair_list[1]:
            #             print(index, character_context_dic["character_names"], character_context_dic["tf_sorted_list"])
			#

            for edge_pair_list in edge_weights_sorted[0:number_of_wc]:

                for index in range(len(dta_holder["character_relations_context"])):
                    if dta_holder["character_relations_context"][index]["character_names"][0] == edge_pair_list[0] and dta_holder["character_relations_context"][index]["character_names"][1] == edge_pair_list[1]:


                            #print(dta_holder["character_relations_context"][index]["tf_sorted_list"][0:12])

                            if len(dta_holder["character_relations_context"][index]["tf_sorted_list"][0:words_in_word_cloud]) == 0:
                                text_string = "<<empty_word_cloud>>"
                            if len(dta_holder["character_relations_context"][index]["tf_sorted_list"][0:words_in_word_cloud]) > 0:
                                text_string = str()
                                # for word_freq_tuple in relation["tf_sorted_list"][0:10]:
                                for word_freq_tuple in dta_holder["character_relations_context"][index]["tf_sorted_list"][0:words_in_word_cloud]:



                                    if word_freq_tuple[1] < 10:
                                        for i in range(word_freq_tuple[1]):
                                            text_string += "%s " % word_freq_tuple[0]

                                    if word_freq_tuple[1] >= 10:
                                        for i in range(9):
                                            # print(i)
                                            text_string += "%s " % word_freq_tuple[0]

                            #print(text_string)

                            word_cloud.generate_wordcloud_simple(text=text_string, ending_number=index, temppath=tpath, file_name_head = head_of_file_name)
                            # wc = word_cloud.generate_wordcloud_simple(text=str(text_string))

                            #######

                            wordcloud_pic = Figure(position="H")
                            wordcloud_pic.add_image(os.path.join(tpath, "wordcloud%s.png" % index),
                                                    width='240px')  # , placement="center")
                            # wordcloud_pic.add_image(wc, width='240px')#, placement="center")

                            # wordcloud_pic.add_caption('word cloud of "%s -- %s"' % (relation["character_names"][0], relation["character_names"][1]))
                            wordcloud_pic.add_caption('word cloud of "%s -- %s"' % (
                            dta_holder["character_relations_context"][index]["character_names"][0],
                            dta_holder["character_relations_context"][index]["character_names"][1]))

                            # subs.append(wordcloud_pic)
                            # section.append(subs)

                            section.append(wordcloud_pic)

            doc.append(section)



    def write_word_cloud_single_character(self, doc, dta_holder, tpath, number_of_wc, head_of_file_name = "wordcloud_for_single_character", wc_context_selection="MFW", words_in_word_cloud = 12):


        doc.packages.append(Package('float'))
        if wc_context_selection=="PMI":
            section = Section("Word Cloud for single characters (method: pointwise mutual information", numbering=True)
            section.append("These word clouds were constructed based on pointwise mutual information (PMI). PMI is a measure of how strongly each term is associated with each character mention. ")
        if wc_context_selection=="MFW":
            section = Section("Word Cloud for single characters (method: most frequent contexts words", numbering=True)
            section.append("These word clouds were constructed based on most frequent words. They show the most frequent words that appear around character mention. ")


        network_parameters = dta_holder["network_parameters"]
        weighted_degrees = network_parameters[5]
        weighted_degrees_sorted = sorted(weighted_degrees, key=operator.itemgetter(1), reverse=True)

        if wc_context_selection == "PMI":

            character_names_with_highest_degree = list()
            for weighted_degree in weighted_degrees_sorted[0:number_of_wc]:
                character_names_with_highest_degree += [weighted_degree[0]]


            for index, context_dic in enumerate(dta_holder["single_character_context"]):
                if len(context_dic["tf_sorted_list"][0:words_in_word_cloud]) == 0:
                    text_string = "<<empty_word_cloud>>"
                if len(context_dic["tf_sorted_list"][0:words_in_word_cloud]) > 0:
                    #print(context_dic)
                    text_string = str()
                    # for word_freq_tuple in relation["tf_sorted_list"][0:10]:
                    for word_freq_tuple in context_dic["tf_sorted_list"][0:words_in_word_cloud]:

                        if word_freq_tuple[1] < 10:
                            for i in range(word_freq_tuple[1]):
                                text_string += "%s " % word_freq_tuple[0]

                        if word_freq_tuple[1] >= 10:
                            for i in range(9):
                                # print(i)
                                text_string += "%s " % word_freq_tuple[0]
                                # print(text_string)

                word_cloud.generate_wordcloud_simple(text=text_string, ending_number=index, temppath=tpath,
                                                     file_name_head=head_of_file_name)
                #wc = word_cloud.generate_wordcloud_simple(text=str(text_string))

                wordcloud_pic = Figure(position="H")
                wordcloud_pic.add_image(os.path.join(tpath, "wordcloud_for_single_character%s.png" % index),
                                        width='240px')  # , placement="center")

                wordcloud_pic.add_caption('word cloud of "%s"' % (dta_holder["single_character_context"][index]["character_names"]))

                section.append(wordcloud_pic)

            doc.append(section)

        if wc_context_selection == "MFW":

            character_names_with_highest_degree = list()
            for weighted_degree in weighted_degrees_sorted[0:number_of_wc]:
                character_names_with_highest_degree += [weighted_degree[0]]

            for index in range(0, len(dta_holder["single_character_context"])):


                if dta_holder["single_character_context"][index]["character_names"] in character_names_with_highest_degree:

                    if len(dta_holder["single_character_context"][index]["tf_sorted_list"][0:words_in_word_cloud]) == 0:
                        text_string = "<<empty_word_cloud>>"
                    if len(dta_holder["single_character_context"][index]["tf_sorted_list"][0:words_in_word_cloud]) > 0:
                    #print(dta_holder["single_character_context"][index]["tf_sorted_list"][0:12])

                        text_string = str()
                        # for word_freq_tuple in relation["tf_sorted_list"][0:10]:
                        for word_freq_tuple in dta_holder["single_character_context"][index]["tf_sorted_list"][0:words_in_word_cloud]:


                            #print(word_freq_tuple)

                            # for i in range(word_freq_tuple[1]):
                            #     text_string += "%s " % word_freq_tuple[0]

                            if word_freq_tuple[1] < 10:
                                for i in range(word_freq_tuple[1]):
                                    text_string += "%s " % word_freq_tuple[0]

                            if word_freq_tuple[1] >= 10:
                                for i in range(9):
                                    #print(i)
                                    text_string += "%s " % word_freq_tuple[0]

                    #print(text_string)

                    word_cloud.generate_wordcloud_simple(text=text_string, ending_number=index, temppath=tpath, file_name_head = head_of_file_name)
                    # wc = word_cloud.generate_wordcloud_simple(text=str(text_string))

                    #######

                    wordcloud_pic = Figure(position="H")
                    wordcloud_pic.add_image(os.path.join(tpath, "wordcloud_for_single_character%s.png" % index),
                                            width='240px')  # , placement="center")

                    wordcloud_pic.add_caption('word cloud of "%s"' % (
                        dta_holder["single_character_context"][index]["character_names"]))

                    # subs.append(wordcloud_pic)
                    # section.append(subs)

                    section.append(wordcloud_pic)

            doc.append(section)



        # section1 = Section("rCat, v.0.1", numbering=False)
        # section1.append(
        #     "This program is developed by Florian Barth and Evgeny Kim with the help of Roman Klinger and Sandra Murr. It is part of the Center for Reflected Text Analytics (CRETA) at the Universtiy of Stuttgart.\n\nFeel free to contact us:")

        # list = Itemize()
        # list.add_item("rcat@ims.uni-stuttgart.de")

        # section1.append(list)
        # doc.append(section1)




    def write_netork_parameters(self, doc, dta_holder):
        with doc.create(Section("Network Parameters", numbering=True)) as section1:
            section1.append("Here you can get information about the network parameters.")
            with doc.create(Subsection("Definitions",numbering=False)):
                with doc.create(Itemize()) as definitions:
                    definitions.add_item("Average degree: The degree of a node is the number of edges connected to it. It measures the number of connections to other characters. Average degree is calculated\
                        on a probability of two nodes being connected.")
                    definitions.add_item("SD degree: Standard deviation of all degrees.")
                    definitions.add_item("Density: Graph density is the ratio of the number of edges to the number of possible edges.")
                    definitions.add_item("Weighted degree: Sum of weights of incident edges. Measures the number of interactions of a character.")
            with doc.create(Subsection("Current network parameters",numbering=False)):
                with doc.create(Itemize()) as itmize:
                    itmize.add_item("average degree: %s" % dta_holder["network_parameters"][0])
                    itmize.add_item("sd degree: %s" % dta_holder["network_parameters"][1])
                    itmize.add_item("density: %s" % dta_holder["network_parameters"][2])
                # itmize.add_item("degrees for single characters: %s" %dta_holder["network_parameters"][3])

        # pdf_latex().write_table_degrees(doc, dta_holder)

        subsection1 = Subsection("Degrees", numbering=False)

        # table1 = Tabular('|c|c|c|c|')
        table1 = Tabular('|c|c|c|')

        table1.add_hline()
        table1.add_row(("Character (Node)", "degree", "weighted degree"))
        table1.add_hline()
        degree_list_weigthed_degree_tuple = zip(dta_holder["network_parameters"][3],dta_holder["network_parameters"][4])
        sorted_degree_list_weigthed_degree_tuple = sorted(degree_list_weigthed_degree_tuple, key=lambda x: x[1][1], reverse=True)
        #for degree_list, weigthed_degree_tuple in zip(dta_holder["network_parameters"][3],
        #                                              dta_holder["network_parameters"][4]):
        for degree_list, weigthed_degree_tuple in sorted_degree_list_weigthed_degree_tuple:
            if degree_list[0] == weigthed_degree_tuple[0]:
                table1.add_row(degree_list[0], degree_list[1], weigthed_degree_tuple[1])
                table1.add_hline()
            else:
                print("characters for degree and weighted degree don't match!")

        subsection1.append(table1)
        doc.append(subsection1)

        subsection2 = Subsection("Weights for Edges", numbering=False)
        table2 = Tabular("|c|c|")
        table2.add_hline()
        table2.add_row("Character Pair (Edge)", "Weight")
        table2.add_hline()
        #print(dta_holder["character_relations"])
        sorted_relations = sorted(dta_holder["character_relations"], key=operator.itemgetter(4), reverse=True)
        #print(sorted_relations)
        #for relation in dta_holder["character_relations"]:
        for relation in sorted_relations[0:50]:
            if sorted_relations[4] != 0:
                table2.add_row("%s -- %s" % (relation[2][0], relation[2][1]), len(relation[3]))
                table2.add_hline()

        subsection2.append(table2)
        doc.append(subsection2)

    def write_header(self, doc):
        # def write_header(self):

        # Add document header
        header = PageStyle("header")
        # Create left header
        with header.create(Head("L")):
            header.append("Center for Reflected Text Analytics (CRETA)\nUniversity of Stuttgart")
            # header.append(LineBreak())
            # header.append("R3")
        ## Create center header
        # with header.create(Head("C")):
        #    header.append("Company")
        # Create right header
        with header.create(Head("R")):
            header.append(NoEscape(r'\today'))
        ## Create left footer
        # with header.create(Foot("L")):
        #    header.append("Left Footer")
        ## Create center footer
        with header.create(Foot("C")):
            header.append(simple_page_number())
        ## Create right footer
        # with header.create(Foot("R")):
        #    header.append("Right Footer")

        doc.preamble.append(header)
        doc.change_document_style("header")

        # Add Heading
        with doc.create(MiniPage(align='c')):
            doc.append(LargeText(bold("rCAT v0.1")))
            doc.append(LineBreak())
            doc.append(MediumText(bold("Relational Character Analysis Tool")))

        return doc

    def finalize(self, doc, s_id):
       # if s_id==False:
       #     doc.generate_pdf("data_user/relations", clean_tex=True)
       # else:
        doc.generate_pdf("data_user/%s_temp_folder/relations" %s_id, clean_tex=True)

    ## OLD FUNCTIONS


    # def write_weights_for_connections(self, doc, dta_holder):
    #
    #     # with doc.create(Section("weights for edges", numbering = False)):
    #     #     index = 1
    #     #     for relation in dta_holder["character_relations"]:
    #     #         with doc.create(Subsection("%s" %relation[2],numbering=False)):
    #     #             doc.append(len(relation[3]))
    #     #         index += 1
    #
    #     section1 = Section("Weights for Edges")
    #     table1 = Tabular("|c|c|")
    #     table1.add_hline()
    #     table1.add_row("Edge (Character Pair)", "Weight")
    #     table1.add_hline()
    #     for relation in dta_holder["character_relations"]:
    #         if len(relation[3]) != 0:
    #             table1.add_row("%s -- %s" % (relation[2][0], relation[2][1]), len(relation[3]))
    #             table1.add_hline()
    #
    #     section1.append(table1)
    #     doc.append(section1)


    # def write_table_weighted_degrees(self,doc, dta_holder):
    #     section = Section("weighted degrees table", numbering = False)
    #     table1 = Tabular('|c|c|')
    #     table1.add_hline()
    #     table1.add_row(("character", "weighted degree"))
    #     table1.add_hline()
    #     for weigthed_degree_tuple in dta_holder["network_parameters"][4]:
    #         table1.add_row(weigthed_degree_tuple[0], weigthed_degree_tuple[1])
    #         table1.add_hline()
    #
    #     section.append(table1)
    #     doc.append(section)

    # def write_table_degrees(self,doc, dta_holder):
    #     section = Section("degrees table", numbering = False)
    #     table1 = Tabular('|c|c|')
    #     table1.add_hline()
    #     table1.add_row(("character", "degree"))
    #     table1.add_hline()
    #     for degree_list in dta_holder["network_parameters"][3]:
    #         table1.add_row(degree_list[0], degree_list[1])
    #         table1.add_hline()
    #
    #     section.append(table1)
    #     doc.append(section)

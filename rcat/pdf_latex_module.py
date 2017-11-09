from pylatex import Document, Section, Itemize, Subsection, Command, PageStyle, Head, MiniPage, Foot, LargeText, \
    MediumText, LineBreak, simple_page_number, Figure, NoEscape, Tabular, MultiColumn, MultiRow, Package
from pylatex.utils import bold
from rcat.wordcloud_module import word_cloud

import os
import operator
import shutil

import re


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
            "This program is developed by Dr. Roman Klinger, Sandra Murr, Evgeny Kim and Florian Barth. It is part of the Center for Reflected Text Analytics (CRETA) at the Universtiy of Stuttgart.\n\nFeel free to contact us:")

        list = Itemize()
        list.add_item("roman.klinger@ims.uni-stuttgart.de")
        list.add_item("sandra.murr@ilw.uni-stuttgart.de")
        list.add_item("evgeny.kim@ims.uni-stuttgart.de")
        list.add_item("florianbarth@ilw.uni-stuttgart.de")

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

    def word_field_curve(self,doc,wf_cat=str()):
        if wf_cat == "None":
            pass
        else:
            with doc.create(Figure(position='H')) as emoarc:
                emoarc.add_image("rcat/word_field.pdf")
                emoarc.add_caption("Word field development in the current text")

    def write_wordfield_curve(self,doc,dta_holder,wf_cat=str()):
        if wf_cat == "None":
            pass
        else:
            with doc.create(Section("Word field development", numbering=True)):
                with doc.create(Itemize()) as itmize:
                    itmize.add_item('Word field development in the current book.')

    def write_data_input(self, doc, dta_holder):
        with doc.create(Section("Data Input", numbering=True)):
            with doc.create(Itemize()) as itmize:
                itmize.add_item('analyzed text: "%s"' % dta_holder["text_file"].split('/')[-1])
                itmize.add_item("length of text: %s tokens" % len(dta_holder["tokenized_text"]))
                # itmize.add_item("number of characters: %s" % len(dta_holder["characters"]))

                characters_with_at_least_one_degree = 0
                for degree_list in dta_holder["network_parameters"][3]:
                    if degree_list[1] != 0:
                        characters_with_at_least_one_degree += 1
                itmize.add_item(
                    "number of characters (with at least one degree): %s" % str(characters_with_at_least_one_degree))

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

    def write_word_cloud(self, doc, dta_holder, tpath, number_of_wc, head_of_file_name = "wordcloud"):

        # import float package for -> Figure(position="H")
        doc.packages.append(Package('float'))

        section = Section("Word Cloud for character pairs", numbering=True)

        network_parameters = dta_holder["network_parameters"]
        edge_weights = network_parameters[6]
        edge_weights_sorted = sorted(edge_weights, key=operator.itemgetter(2), reverse=True)

        ### here we iterate over all context_terms in "character_relations_context"
        ### it is done with the index since a numbering for the word cloud file is necessary
        # for relation in dta_holder["character_relations_context"]:
        for edge_pair_list in edge_weights_sorted[0:number_of_wc]:

            for index in range(len(dta_holder["character_relations_context"])):
                if dta_holder["character_relations_context"][index]["character_names"][0] == edge_pair_list[0] and dta_holder["character_relations_context"][index]["character_names"][1] == edge_pair_list[1]:


                        #print(dta_holder["character_relations_context"][index]["tf_sorted_list"][0:12])

                        if len(dta_holder["character_relations_context"][index]["tf_sorted_list"][0:12]) == 0:
                            text_string = "<<empty_word_cloud>>"
                        if len(dta_holder["character_relations_context"][index]["tf_sorted_list"][0:12]) > 0:
                            text_string = str()
                            # for word_freq_tuple in relation["tf_sorted_list"][0:10]:
                            for word_freq_tuple in dta_holder["character_relations_context"][index]["tf_sorted_list"][0:12]:

                                #for i in range(word_freq_tuple[1]):
                                #     text_string += "%s " % word_freq_tuple[0]

                                #print(word_freq_tuple)

                                if word_freq_tuple[1] < 7:
                                    for i in range(word_freq_tuple[1]):
                                        text_string += "%s " % word_freq_tuple[0]

                                if word_freq_tuple[1] >= 7:
                                    for i in range(6):
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



    def write_word_cloud_single_character(self, doc, dta_holder, tpath, number_of_wc,head_of_file_name = "wordcloud_for_single_character"):


        doc.packages.append(Package('float'))
        section = Section("Word Cloud for single characters", numbering=True)

        network_parameters = dta_holder["network_parameters"]
        weighted_degrees = network_parameters[5]
        weighted_degrees_sorted = sorted(weighted_degrees, key=operator.itemgetter(1), reverse=True)


        character_names_with_highest_degree = list()
        for weighted_degree in weighted_degrees_sorted[0:number_of_wc]:
            character_names_with_highest_degree += [weighted_degree[0]]

        for index in range(0, len(dta_holder["single_character_context"])):


            if dta_holder["single_character_context"][index]["character_names"] in character_names_with_highest_degree:

                if len(dta_holder["single_character_context"][index]["tf_sorted_list"][0:12]) == 0:
                    text_string = "<<empty_word_cloud>>"
                if len(dta_holder["single_character_context"][index]["tf_sorted_list"][0:12]) > 0:
                #print(dta_holder["single_character_context"][index]["tf_sorted_list"][0:12])

                    text_string = str()
                    # for word_freq_tuple in relation["tf_sorted_list"][0:10]:
                    for word_freq_tuple in dta_holder["single_character_context"][index]["tf_sorted_list"][0:12]:


                        #print(word_freq_tuple)

                        # for i in range(word_freq_tuple[1]):
                        #     text_string += "%s " % word_freq_tuple[0]

                        if word_freq_tuple[1] < 7:
                            for i in range(word_freq_tuple[1]):
                                text_string += "%s " % word_freq_tuple[0]

                        if word_freq_tuple[1] >= 7:
                            for i in range(6):
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








    def write_netork_parameters(self, doc, dta_holder):
        with doc.create(Section("Network Parameters", numbering=True)) as section1:
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
        for degree_list, weigthed_degree_tuple in zip(dta_holder["network_parameters"][3],
                                                      dta_holder["network_parameters"][4]):
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
        for relation in dta_holder["character_relations"]:
            if len(relation[3]) != 0:
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
            doc.append(LargeText(bold("rCat v0.1")))
            doc.append(LineBreak())
            doc.append(MediumText(bold("Program for Relational Semantics")))

        return doc

    def finalize(self, doc):
        doc.generate_pdf("relations", clean_tex=True)

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

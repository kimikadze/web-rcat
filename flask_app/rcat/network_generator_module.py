# import networkx as nx

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import math
import os

import operator

#from graph_tool.all import *


class network_generator:

    def __init__(self):
        pass

    # def build_networkx(relations, temppath):
    #
    #     g = nx.Graph()
    #
    #     for i in range(len(relations)):
    #         #print(relations[i])
    #         if len(relations[i][3]) > 0:
    #             #print(relations[i][2], len(relations[i][3]))
    #             #g.add_edge(relations[i][2][0], relations[i][2][1], weight= len(relations[i][3]))
    #             g.add_edge(relations[i][2][0], relations[i][2][1], weight=math.log2(len(relations[i][3]) + 1))
    #
    #
    #     edges = g.edges()
    #     weights = [g[u][v]['weight'] for u, v in edges]
    #
    #     # Fruchtermann Rheingold:
    #     #pos = nx.spring_layout(g)
    #     # Eigenvector:
    #     #pos = nx.spectral_layout(g)
    #     # Random Layout:
    #     pos = nx.random_layout(g)
    #
    #     d = nx.degree(g)
    #
    #     nx.draw_networkx(g, pos, with_labels=True, nodelist=d.keys(), node_size=[v * 50 for v in d.values()],
    #             edges=edges, width=weights)#, node_color = color_map) #,edge_color=weights)
    #     plt.savefig(os.path.join(temppath,"graph_networkx.png"))
    #     #plt.savefig("graph_networkx.png")
    #     #plt.show()



    #def build_and_plot_graph_vis(relations, temppath=False, method="sfdp"):
    def build_and_plot_graph_vis(relations, temppath=False, method="fdp"):

        # options for method = ["neato", "sfdp"]


        graph_data = list()
        graph_data += ["graph {"]

        graph_data += ["node [shape=ellipse style=filled]"]
        for i in range(len(relations)):
            if len(relations[i][3]) > 0:
                # for j in range(len(relations[i][3])):
                string = str()
                string += relations[i][2][0].strip(". ").replace(".", "").replace(" ", "_") + ' -- ' + \
                          relations[i][2][1].strip(". ").replace(".", "").replace(" ",
                                                                                  "_") + '[penwidth= %s]' % math.log2(
                    len(relations[i][3]) + 1)
                graph_data += [string]
        graph_data += ["}"]


        if temppath==False:
            data = open("network.dot", mode="w")
            for i in graph_data:
                data.write(i + "\n")
            data.close()

            #launch_graphvis
            output = os.popen("%s -Tpdf network.dot -o network.pdf" %method)
            output.read()
            output.close()


        else:
            app_directory = os.getcwd()
            os.chdir(temppath)
            data = open("network.dot", mode="w")
            for i in graph_data:
                data.write(i + "\n")
            data.close()
            os.chdir(app_directory)


            #print(temppath)

            #launch_graphvis
            output = os.popen("%s -Tpdf %s/network.dot -o %s/network.pdf" %(method, temppath, temppath))


            output.read()
            output.close()


            #def build_graph_tool_network(self, relations):

        #g = Graph()



    def build_and_plot_graph_vis_col(relations, network_parameters, number_of_wc, temppath=False, method="fdp"):

        # options for method = ["neato", "sfdp"]


        graph_data = list()
        graph_data += ["graph {"]



        # take the 3 highest degrees and write specific colour and shape for their nodes:
        weighted_degrees = network_parameters[4]
        weighted_degrees_sorted =  sorted(weighted_degrees, key=operator.itemgetter(1), reverse=True)
        #print(weighted_degrees_sorted)
        for character_degree_pair in weighted_degrees_sorted[0:number_of_wc]:
            graph_data += ["%s [shape=ellipse style=filled fillcolor=red]" %character_degree_pair[0].strip(". ").replace(".", "").replace(" ", "_")]
            # » .strip(". ").replace(".", "").replace(" ", "_") « replaces white space white underscore since graphvis needs this


        # write all other nodes

        graph_data += ["node [shape=ellipse style=filled fillcolor=green]"]
        for i in range(len(relations)):
            if len(relations[i][3]) > 0:
                # for j in range(len(relations[i][3])):
                string = str()
                string += relations[i][2][0].strip(". ").replace(".", "").replace(" ", "_") + ' -- ' + \
                          relations[i][2][1].strip(". ").replace(".", "").replace(" ",
                                                                                  "_") + '[penwidth= %s]' % math.log2(
                    len(relations[i][3]) + 1)
                graph_data += [string]
        graph_data += ["}"]

        if temppath == False:
            data = open("network.dot", mode="w")
            for i in graph_data:
                data.write(i + "\n")
            data.close()

            # launch_graphvis
            output = os.popen("%s -Tpdf network.dot -o network.pdf" % method)
            output.read()
            output.close()


        else:
            app_directory = os.getcwd()
            os.chdir(temppath)
            data = open("network.dot", mode="w", encoding="utf-8")
            for i in graph_data:
                data.write(i + "\n")
            data.close()
            os.chdir(app_directory)

            # print(temppath)

            # launch_graphvis
            output = os.popen("%s -Tpdf %s/network.dot -o %s/network.pdf" % (method, temppath, temppath))

            output.read()
            output.close()


######################## ONLY WRITE DATA TO FILE
###########################################################

############# write graphvis data to file

    def build_graphvis(relations):
        # HIER WIRD GEWICHTUNG IM NETZWERK BERECHNET
        graph_data = list()
        graph_data += ["graph {"]
        graph_data += ["node [shape=ellipse style=filled]"]
        for i in range(len(relations)):
            if len(relations[i][3]) > 0:
                # for j in range(len(relations[i][3])):
                string = str()
                string += relations[i][2][0].strip(". ").replace(".", "").replace(" ", "_") + ' -- ' + relations[i][2][1].strip(". ").replace(".", "").replace(" ", "_") + '[penwidth= %s]' % math.log2(len(relations[i][3]) + 1)
                graph_data += [string]
        graph_data += ["}"]

        return graph_data

    def write_doc_file(graph_data):
        data = open("network_file_only.dot", mode="w")
        for i in graph_data:
            data.write(i + "\n")
        data.close()


############# write gephi data to file

    def build_csv_lines_for_gephi(relations, weight="counts"):
        csv_lines = ["source;Target;Weight;Type"]
        for i in range(len(relations)):
            if len(relations[i][3]) > 0:
                string = str()
                if weight=="counts":
                    string += relations[i][2][0].strip(". ").replace(".", "").replace(" ", "_") + ';' + relations[i][2][1].strip(". ").replace(".", "").replace(" ", "_") + ';%s' % len(relations[i][3]) + ";undirected"
                    csv_lines += [string]
                if weight=="log":
                    string += relations[i][2][0].strip(". ").replace(".", "").replace(" ", "_") + ';' + relations[i][2][1].strip(". ").replace(".", "").replace(" ", "_") + ';%s' % math.log2(len(relations[i][3]) + 1) + ";undirected"
                    csv_lines += [string]

        return csv_lines

    def write_gephi_data_to_csv(csv_lines, temppath=False):
        with open("%s/network_data_for_gephi.csv" %temppath, mode="w", encoding="utf-8") as file:
            print(temppath)
            for line in csv_lines:
                file.write(line + "\n")


        #print(relations[0:3])









from os import path
from wordcloud import WordCloud, STOPWORDS
import os


class word_cloud:

    def __init__(self):
        pass


    #def generate_wordcloud_simple(text, ending_number=None):
    def generate_wordcloud_simple(text, ending_number, temppath, file_name_head):
        #print(text)
        #text = 'all your base are belong to us all of your base base base'
        wordcloud = WordCloud(background_color="white",
                              relative_scaling=1.0, collocations=False, height=800, width=1600
                              #stopwords={'to', 'of'}  # set or space-separated string
                              ).generate(text)
        #plt.imshow(wordcloud)
        #plt.axis("off")
        #plt.show()


        wordcloud.to_file(os.path.join(temppath,"%s%s.png" % (file_name_head, ending_number)))

        # if ending_number==True:
        #     wordcloud.to_file("wordcloud%s.png" %ending_number)
        # else:
        #     wordcloud.to_file("wordcloud.png")

        #return wordcloud






    def generate_wordcloud(network_paramters, tempath):

        d = path.dirname(__file__)

        # Read the whole text.
        text = open(path.join(d, 'constitution.txt')).read()

        # Read the whole text.
        text = open(path.join(d, 'constitution.txt')).read()

        # Generate a word cloud image
        wordcloud = WordCloud().generate(text)

        # Display the generated image:
        # the matplotlib way:
        import matplotlib.pyplot as plt
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")

        # lower max_font_size
        wordcloud = WordCloud(max_font_size=40).generate(text)
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.show()

        #The pil way (if you don't have matplotlib)
        image = wordcloud.to_image()
        image.show()





# dirpath = tempfile.mkdtemp()
# rCat().data_holder(text__file="texts_werther_adaptations/Nicolai_Freuden_des_jungen_Werthers_Leiden_und_Freuden_Werthers_des_Mannes_kindle.txt", character__file="character_lists_werther_adaptations/1775_Nicolai_Werther_characters.txt", temporary_path=dirpath, distance_parameter=[8, 2, 2])
#
# #rCat.main_PDF(text_file ="texts_werther_adaptations/Nicolai_Freuden_des_jungen_Werthers_Leiden_und_Freuden_Werthers_des_Mannes_kindle.txt", character_file= "character_lists_werther_adaptations/1775_Nicolai_Werther_characters.txt",dist_parameter=[8, 2, 2])
#
#
# nw_parameters =
# wordcloud.generate_wordcloud()

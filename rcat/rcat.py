import os
from macos.rcat.text_reader_module import text_reader
from macos.rcat.characters_reader_module import characters_reader
from macos.rcat.relations_module import relations
from macos.rcat.network_generator_module import network_generator
from macos.rcat.pdf_latex_module import pdf_latex
from macos.rcat.network_parameters_module import network_parameters
from macos.rcat.word_field_module import WordField
from macos.rcat.weblicht_text_character_ner_reader_module import weblicht_text_character_ner_reader
from tkinter import *
from tkinter import filedialog, messagebox


class View(object):

    def __init__(self):
        self.parent = Tk()
        self.parent.title("rCAT v.1.0")
        self.initialize_ui()

    def clear_screen(self):
        self.frame.destroy()
        self.initialize_ui()

    def main_loop(self):
        mainloop()

    def background(self, list, color):
        for i in list:
            i.config(background=color)

    def initialize_ui(self):
        bg_main = 'LightSteelBlue1'
        bg_other = 'LightSteelBlue1'
        bg_entry = 'azure2'
        fontconf = ("Helvetica", 14)

        self.frame = Frame(self.parent)
        self.frame.pack()
        self.frame.configure(background=bg_main)

        menu = Menu(self.parent)
        self.parent.config(menu=menu)
        subMenu = Menu(menu)
        menu.add_cascade(label="Menu", menu=subMenu)
        subMenu.add_command(label="Exit", command=lambda: self.parent.quit())


        var0 = StringVar()
        L0 = Label(self.frame, text="Book", font=fontconf)
        L0.grid(row=1, column=0)
        self.E0 = Entry(self.frame, bd=5, textvariable=var0, background=bg_entry)
        self.E0.insert(END, "Open file...")
        self.E0.grid(row=1, column=2)

        var1 = StringVar()
        L1 = Label(self.frame, text="Characters", font=fontconf)
        L1.grid(row=2, column=0)
        self.E1 = Entry(self.frame, bd=5, textvariable=var1, background=bg_entry)
        self.E1.insert(END, "Open file...")
        self.E1.grid(row=2, column=2)

        var2 = StringVar()
        L2 = Label(self.frame, text="Distance measure", font=fontconf)
        L2.grid(row=3, column=0)
        self.E2 = Entry(self.frame, bd=5, textvariable=var2, background=bg_entry)
        self.E2.insert(END, int(10))
        self.E2.grid(row=3, column=2)

        var3 = StringVar()
        L3 = Label(self.frame, text="Context measure 1", font=fontconf)
        L3.grid(row=4, column=0)
        self.E3 = Entry(self.frame, bd=5, textvariable=var3, background=bg_entry)
        self.E3.insert(END, int(8))
        self.E3.grid(row=4, column=2)

        var4 = StringVar()
        L4 = Label(self.frame, text="Context measure 2", font=fontconf)
        L4.grid(row=5, column=0)
        self.E4 = Entry(self.frame, bd=5, textvariable=var4, background=bg_entry)
        self.E4.insert(END, int(8))
        self.E4.grid(row=5, column=2)

        var5 = StringVar()
        L5 = Label(self.frame, text="Remove stop words?(y/n)", font=fontconf)
        L5.grid(row=6, column=0)
        self.E5 = Entry(self.frame, bd=5, textvariable=var5, background=bg_entry)
        self.E5.insert(END, "y")
        self.E5.grid(row=6, column=2)

        var6 = StringVar()
        L6 = Label(self.frame, text="Segments", font=fontconf)
        L6.grid(row=9, column=0)
        self.E6 = Entry(self.frame, bd=5, textvariable=var6, background=bg_entry)
        self.E6.insert(END, int(10))
        self.E6.grid(row=9, column=2)

        var7 = StringVar()
        L7 = Label(self.frame, text="Word clouds to show", font=fontconf)
        L7.grid(row=8, column=0)
        self.E7 = Entry(self.frame, bd=5, textvariable=var7, background=bg_entry)
        self.E7.insert(END, int(5))
        self.E7.grid(row=8, column=2)

        var8 = StringVar()
        L8 = Label(self.frame, text="Write a csv file for Gephi?(y/n)", font=fontconf)
        L8.grid(row=7, column=0)
        self.E8 = Entry(self.frame, bd=5, textvariable=var8, background=bg_entry)
        self.E8.insert(END, "n")
        self.E8.grid(row=7, column=2)

        var81 = StringVar()
        L81 = Label(self.frame, text="Lemmatisation?(n/treetagger/weblicht)", font=fontconf)
        L81.grid(row=10, column=0)
        self.E81 = Entry(self.frame, bd=5, textvariable=var81, background=bg_entry)
        self.E81.insert(END, "n")
        self.E81.grid(row=10, column=2)

        var9 = StringVar()
        L9 = Label(self.frame, text="Analyze with word fields", font=fontconf)
        L9.grid(row=11, column=0)
        self.E9 = Entry(self.frame, bd=5, textvariable=var9, background=bg_entry)
        self.E9.insert(END, "")
        self.E9.grid(row=11, column=2)

        # =========================================================================

        open1 = Button(self.frame,
                       text="Open",
                       command=lambda: self.on_open(self.E0),
                       highlightbackground=bg_main,
                       font=fontconf)
        open1.grid(row=1, column=4)

        open2 = Button(self.frame,
                       text="Open",
                       command=lambda: self.on_open(self.E1),
                       highlightbackground=bg_main,
                       font=fontconf)
        open2.grid(row=2, column=4)

        open3 = Button(self.frame,
                       text="Select file",
                       command=lambda: self.on_open(self.E9),
                       highlightbackground=bg_main,
                       font=fontconf)
        open3.grid(row=11, column=4)

        open4 = Button(self.frame,
                       text="Select folder",
                       command=lambda: self.open_dir(self.E9),
                       highlightbackground=bg_main,
                       font=fontconf)
        open4.grid(row=12, column=4)

        # =============================================================================
        radio_lang = IntVar()
        radio_lang1 = IntVar()

        L10 = Label(self.frame, text="Book language", font=fontconf)
        L10.grid(row=13, column=0)

        Radiobutton(self.frame,
                    text="German",
                    variable=radio_lang,
                    value=1,
                    background=bg_main,
                    font=fontconf).grid(row=13, column=1)
        Radiobutton(self.frame,
                    text="English",
                    variable=radio_lang,
                    value=2,
                    background=bg_main,
                    font=fontconf).grid(row=14, column=1)
        Radiobutton(self.frame,
                    text="MHG",
                    variable=radio_lang,
                    value=3,
                    background=bg_main,
                    font=fontconf).grid(row=15, column=1)

        Radiobutton(self.frame,
                    text="Single category",
                    variable=radio_lang1,
                    value=1, background=bg_main,
                    font=fontconf).grid(row=11, column=5)
        Radiobutton(self.frame,
                    text="Multi-category",
                    variable=radio_lang1,
                    value=2, background=bg_main,
                    font=fontconf).grid(row=12, column=5)

        # =========================================================================
        run_button = Button(self.frame,
                            text="Run",
                            command=lambda: self.collect_args(var0,
                                                              var1,
                                                              var2,
                                                              var3,
                                                              var4,
                                                              var5,
                                                              var6,
                                                              var7,
                                                              var8,
                                                              var81,
                                                              var9,
                                                              radio_lang,
                                                              radio_lang1),
                            highlightbackground=bg_main,
                            font=fontconf)
        run_button.grid(row=13, column=2)

    # ****** Status bar *******************
    #     self.stateVar = StringVar()
    #     self.stateVar.set("Status bar...")
    #     status_font = ("Helvetica", 14, "italic")
    #
    #     self.status = Label(self.frame,
    #                    textvariable=self.stateVar,
    #                    font=status_font,
    #                    background=bg_other,
    #                    bd=3)
    #     self.status.grid(row=16, columnspan=15, sticky=W)

    # ****** Status bar *******************

        self.background([L0, L1, L2, L3, L4, L5, L6, L7, L8, L81, L9, L10], bg_other)

    def change_status(self, text):
        """Callled when the status changes """
        self.stateVar.set(text)

    def collect_args(self, var0, var1, var2, var3, var4, var5, var6, var7, var8, var81, var9, r1, r2):

        Arguments = dict()
        Arguments["Book"] = var0.get()
        Arguments["Characters"] = var1.get()
        Arguments["Distance measure"] = int(var2.get())
        Arguments["Context measure 1"] = int(var3.get())
        Arguments["Context measure 2"] = int(var4.get())
        Arguments["Remove stop words?(y/n)"] = var5.get()
        Arguments["Segments"] = int(var6.get())
        Arguments["Word clouds to show"] = int(var7.get())
        Arguments["Write a csv file for Gephi?(y/n)"] = var8.get()
        Arguments["Lemmatisation?(weblicht)"] = var81.get()
        Arguments["Language"] = ""
        Arguments["Analyze with word fields"] = ""
        Arguments["WF category"] = ""

        if r1.get() == 1:
            Arguments["Language"] = "rcat/stopwords/stopwords_de.txt"
        elif r1.get() == 2:
            Arguments["Language"] = "rcat/stopwords/stopwords_en.txt"
        elif r1.get() == 3:
            Arguments["Language"] = "rcat/stopwords/Stoppwortliste_mittelhochdeutsch_erweitert.txt"

        if r2.get() == 1:
            Arguments["WF category"] = "single"
            Arguments["Analyze with word fields"] = var9.get()
        elif r2.get() == 2:
            Arguments["WF category"] = "multi"
            Arguments["Analyze with word fields"] = var9.get()
        else:
            Arguments["Analyze with word fields"] = "N"
            Arguments["WF category"] = "None"

        arg = Arguments
        self.main_PDF(arg["Book"],
                      arg["Characters"],
                      [arg["Distance measure"],
                       arg["Context measure 1"],
                       arg["Context measure 2"]],
                      arg["Remove stop words?(y/n)"],
                      arg["Segments"],
                      arg["Word clouds to show"],
                      arg["Write a csv file for Gephi?(y/n)"],
                      arg["Analyze with word fields"],
                      arg["WF category"],
                      arg["Lemmatisation?(weblicht)"],
                      arg["Language"])

    def data_holder(self, text__file, character__file, temporary_path=str(),
                    distance_parameter=[5, 3, 3], del_stopwords_in_context="n", segments=int(10),
                    number_of_wc=str(), write_gephi_csv = str(), word_field=str(), wf_cat=str(), lemmatisation="n",
                    lang=str(),choose_method=str()):

        holder = dict(character_relations=0, character_relations_context=0, text_file=0, character_file=0,
                      tokenized_text=0, characters=0, parameter=0, network_parameters=0,
                      single_character_context=0, segments=0, lemmatisation=0, lang=0, number_of_wc=0, word_field=0, wf_cat=0)

        if word_field != "N":
            self.word_f(word_field,
                        wf_cat,
                        segments,
                        text__file)
        else:
            pass

        if lemmatisation != "weblicht":
            txt = text_reader().read_text_file(txt_file=text__file)
            txt_tokenized = text_reader().tokenize_lemmatize_text(txt, lemmatisation)
            call = self.tok(txt_tokenized,
                             character__file,
                             distance_parameter,
                             del_stopwords_in_context,
                             word_field,lang)

            holder['character_relations'] = call[0]
            holder['characters'] = call[1]
        if lemmatisation == "weblicht":
            # ****** temporary stub until weblicht is fixed *******
            #messagebox.showinfo("Error", "Lemmatisation with Weblicht failed. Falling back to no-lemmatization method")
            txt = text_reader().read_text_file(txt_file=text__file)
            txt_tokenized = text_reader().tokenize_lemmatize_text(txt)
            call = self.tok(txt_tokenized,
                             character__file,
                             distance_parameter,
                             del_stopwords_in_context,
                             word_field,lang)

            holder['character_relations'] = call[0]
            holder['characters'] = call[1]
            # ****** end of stub *************

            # filename_without_path = re.findall(".*/(.*)/(.*.txt)",text__file)
            #
            # #print(filename_without_path)
            # #print(filename_without_path)
            # #print(text__file)
            #
            # weblicht_text_character_ner_reader.weblicht_tcf(filepath=text__file)
            #
            # #print(os.getcwd())
            # tcf_data = weblicht_text_character_ner_reader.tcf_reader("rcat/test_folder/%s.tcf" %filename_without_path[0][1])
            # txt_tokenized = weblicht_text_character_ner_reader.build_lemmatized_text(tcf_data)

            # print(txt_tokenized)
            # ***** the commendted code don't work yet 

        # print("calculate network parameters...")
        netw_parameters = network_parameters().calculate_network_parameters(holder["character_relations"],
                                                                            holder["characters"])

        # print("build network...")

        network_generator.build_and_plot_graph_vis_col(holder["character_relations"], netw_parameters,number_of_wc,temporary_path)

        holder = {"character_relations": call[0],
                  "character_relations_context": call[2],
                  "text_file": text__file, "character_file": character__file, "tokenized_text": txt_tokenized,
                  "characters": call[1], "parameter": distance_parameter,
                  "network_parameters": netw_parameters, "single_character_context": call[3],
                  "segments": segments, "lang": lang, "number_of_wc": number_of_wc, "word_field": word_field,
                  "wf_cat": wf_cat}

        return holder


    def word_f(self,word_field,wf_cat,segments,text__file):
        start_wf = WordField(word_field=word_field, wf_cat=wf_cat, segments=segments)
        chunked = start_wf.read_text_file(txt_file=text__file)
        scores = start_wf.score(chunked)
        start_wf.plot_wordfield(scores)

    def tok(self,txt_tokenized,character__file,distance_parameter,del_stopwords_in_context,word_field,lang):

        # print("reading text file...")
        # print("reading character file...")
        characters = characters_reader().read_characters(char_file=character__file)
        characters_tokenized = characters_reader().tokenize_characters(characters)

        # print("compute character relations...")
        character_positions = relations().find_character_positions(txt_tokenized, characters_tokenized)
        character_pairs = relations().build_character_pairs(characters, characters_tokenized)
        character_relations = relations().build_relations(character_positions, character_pairs,
                                                          distance_for_relation=distance_parameter[0])

        # print("find context for characters...")
        character_relations_context = relations().count_context_words(character_relations, txt_tokenized,
                                                                      words_before=distance_parameter[1],
                                                                      words_after=distance_parameter[2],
                                                                      delete_stopwords_in_context=del_stopwords_in_context,
                                                                      word_field=word_field, stop_words=lang)

        single_character_context = relations().count_context_words_for_single_characters(character_positions,
                                                                                         characters, txt_tokenized,
                                                                                         word_field=word_field,
                                                                                         stop_words=lang)
        return character_relations, characters, character_relations_context, single_character_context


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
                 lang=str(),
                 choose_method="graphvis_col"):

        dirpath = os.getcwd()
        dirpath = os.path.join(dirpath, "rcat/test_folder")

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
                                    lang,
                                    choose_method)

        # print("writing PDF...")
        pdf = pdf_latex().initialize()
        pdf_latex().write_header(pdf)
        pdf_latex().network_figure(pdf, dirpath, method=choose_method)
        pdf_latex().write_data_input(pdf, d_holder)
        pdf_latex().write_netork_parameters(pdf, d_holder)
        pdf_latex().write_word_cloud_single_character(pdf, d_holder, number_of_wc=number_of_wc, tpath=dirpath)
        pdf_latex().write_word_cloud(pdf, d_holder, number_of_wc=number_of_wc, tpath=dirpath)
        pdf_latex().write_wordfield_curve(pdf, d_holder, wf_cat)
        pdf_latex().word_field_curve(pdf, wf_cat)
        pdf_latex().write_prgramm_statments(pdf)
        pdf_latex().finalize(pdf)
        # print("PDF complete")

        messagebox.showinfo("Status", "Analysis is complete. PDF report is generated.")

        if write_gephi_csv == "y":
            csv_line_data = network_generator.build_csv_lines_for_gephi(d_holder["character_relations"], weight="log")
            network_generator.write_gephi_data_to_csv(csv_line_data)
            messagebox.showinfo("Information", "Gephi input is genereated")

    def open_dir(self, element):
        root_dir = filedialog.askdirectory()
        element.delete(0, END)
        element.insert(END, root_dir)

    def on_open(self, element):
        global current_file
        home = os.path.expanduser('rcat/doc/')
        f_types = [("text files", "txt"), ("All files", "*")]
        dlg = filedialog.Open(filetypes=f_types, initialdir=home)
        fl = dlg.show()
        if fl != '':
            current_file = os.path.abspath('%s' % fl)
            element.delete(0, END)
            element.insert(END, current_file)
        else:
            pass


if __name__ == "__main__":
    view = View()
    view.main_loop()

    # View().main_PDF(text_file="/Users/Florian/Applications/SourceTree/rcat_github/macos/rcat/rcat/doc/texts/Goethe_Die_Leiden_des_jungen_Werthers_1774.txt", character_file="/Users/Florian/Applications/SourceTree/rcat_github/macos/rcat/rcat/doc/character_lists/Goethe_Werther_74_characters.txt",
    #               dist_parameter=[8, 5, 5],
    #               remove_stopwords_in_context="n",
    #               segments=5, lang=1, number_of_wc=3,
    #               write_gephi_csv="n",
    #               word_field = "N",
    #               wf_cat="None",
    #               lemmatisation="treetagger")
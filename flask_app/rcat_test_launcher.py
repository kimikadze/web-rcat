from flask_app.rcat.rcat_main import rcat



rcat().main_PDF(text_file="/Users/Florian/Applications/SourceTree/web-rcat/flask_app/data/CRETA_internal/Werther/Goethe_Die_Leiden_des_jungen_Werthers_1774.txt", character_file="/Users/Florian/Applications/SourceTree/web-rcat/flask_app/data/CRETA_internal/Werther/Goethe_Werther_74_characters.txt",
				dist_parameter=[10, 8, 8],
				remove_stopwords_in_context="n",
				segments=5, txt_language="German", number_of_wc=3,
				write_gephi_csv="n",
				word_field = "N",
				wf_cat="None",
				lemmatisation="n",
				word_cloud_context_selection = "PMI")
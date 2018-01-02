import operator
import math


class features:

	def __init__(self):
		pass





	def zeta(self, dta_holder, number_of_word_clouds, mode="single_character_context"):#context_single_characters, context_pairs):



		if mode=="single_character_context":
			weighted_degrees = dta_holder["network_parameters"][5]
			weighted_degrees_sorted = sorted(weighted_degrees, key=operator.itemgetter(1), reverse=True)

			for weighted_degree in weighted_degrees_sorted[0:number_of_word_clouds]:

				character_name_of_degree = weighted_degree[0]

				dic_with_current_character_name = [dic["words_before_after_pair"] for dic in dta_holder["single_character_context"] if dic["character_names"] == character_name_of_degree]


				#if weighted_degree ==

				print(weighted_degree)
				print(dic_with_current_character_name)
				#print(len(dic_with_current_character_name))

				#print(list(map(operator.itemgetter("character_names"), dta_holder["single_character_context"])))

				#map_obj = map(operator.itemgetter("character_names"), dta_holder["single_character_context"])

				#for i in map_obj:
				#	print(i)
				#print(dta_holder["single_character_context"]["character_names"])

				#if weighted_degree[0] == dta_holder["single_character_context"]["character_names"]:
					#print(dta_holder["single_character_context"]["character_names"])


	#def PMI(self, context_words, tokenized_text_no_stopword_removal, divide_by="sum_of_context_words"):
	def PMI(self, context_words):

		complete_vektor = dict()
		for dic in context_words:
			for word in dic["tf_dic"]:
				if word in complete_vektor:
					complete_vektor[word] = complete_vektor[word] + dic["tf_dic"][word]
				elif word not in complete_vektor:
					complete_vektor.update({word: dic["tf_dic"][word]})

		wortsumme = sum([complete_vektor[j] for j in complete_vektor])

		# if divide_by == "sum_of_context_words":
		# 	wortsumme = sum([complete_vektor[j] for j in complete_vektor])
		# if divide_by == "text_length":
		# 	wortsumme = len(tokenized_text_no_stopword_removal)

		# Test for all words of "Werther"-novel:
		# wortsumme = 35140

		PMIs_for_each_pair = list()
		for pair in range(len(context_words)):
			PMIs_for_each_word_with_pair = dict()
			for word in context_words[pair]["tf_dic"]:
				P_pair_word = context_words[pair]["tf_dic"][word] / wortsumme
				word_in_pair = context_words[pair]["tf_dic"][word]
				P_pair = sum([context_words[pair]["tf_dic"][j] for j in context_words[pair]["tf_dic"]]) / wortsumme
				counts_word = 0
				for dic in context_words:
					if word in dic["tf_dic"]:
						counts_word += dic["tf_dic"][word]
				P_word = counts_word / wortsumme
				PMI_pair_word = math.log2(P_pair_word / (P_pair * P_word))
				PMIs_for_each_word_with_pair.update({word: PMI_pair_word})
				# PMIs_for_each_word_with_pair.update({word: [PMI_pair_word,  P_pair_word, P_pair, P_word]})
				# PMIs_for_each_word_with_pair.update({word: [PMI_pair_word, word_in_pair, counts_word, wortsumme]})

				# i)
				# PMIs_for_each_word_with_pair_ranked = sorted(PMIs_for_each_word_with_pair.items(), key=operator.itemgetter(1), reverse=True)
				# ii)
				# PMIs_for_each_word_with_pair_ranked = sorted(PMIs_for_each_word_with_pair.items(), key=lambda x: x[1], reverse=True)
				# iii)
				dictlist = list()
				for key, value in PMIs_for_each_word_with_pair.items():
					temp = [key, value]
					dictlist.append(temp)
				PMIs_for_each_word_with_pair_ranked = sorted(dictlist, key=operator.itemgetter(1), reverse=True)

			#PMIs_for_each_pair += [[context_words[pair]["character_names"], PMIs_for_each_word_with_pair_ranked]]
			PMIs_for_each_pair += [{"character_names": context_words[pair]["character_names"], "PMI": PMIs_for_each_word_with_pair_ranked}]
		return PMIs_for_each_pair


	#


	# OLD STRUCTURE (LIST)
	# returns list with for each pair:
	#  1. character-pair, 2. Tuples with (words, PMIs) [ranked], 3. Dictionary with all words, PMIs [unranked]

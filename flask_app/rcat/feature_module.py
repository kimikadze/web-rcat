import operator
import math
import matplotlib.pyplot as plt; plt.rcdefaults()



class features:

	def __init__(self):
		pass



	def get_values_for_zeta(self, character_name, dta_holder, method="non_overlapping"):#, delete_stopwords_in_context="n", stop_words="./data/stopwords/stopwords_de_except_ich.txt"):
		# idea: every slice of context arround a character is considered as "document"

		#DOKUMENT FREQUENCIES (count_term_in_each_context_slice)
		dokument_freqs = {}
		dic_for_current_character_name = [dic for dic in dta_holder["single_character_context"] if dic["character_names"] == character_name]

		if method=="overlapping":
			# overlapping counts each occurence of a context term in a slice of context – even if
			# context slices are so close to each other, that a term is counted twice (or more)
			for unique_context_token in dic_for_current_character_name[0]["tf_sorted_list"]:
				df_unique_context_token = 0
				for context_slice in dic_for_current_character_name[0]["indices_before_after_pair_for_each_context_slice"]:

					#if delete_stopwords_in_context=="y":
					#	if unique_context_token[0] in [dta_holder["tokenized_text"][index] for index in context_slice if dta_holder["tokenized_text"][index] not in dta_holder["stopwords"]]:
					#		df_unique_context_token += 1
					#if delete_stopwords_in_context == "n":
					if unique_context_token[0] in [dta_holder["tokenized_text"][index] for index in context_slice]:
						df_unique_context_token += 1

				dokument_freqs[unique_context_token[0]] = df_unique_context_token


		if method=="non_overlapping":
			#print(dic_for_current_character_name)
			dokument_freqs = dic_for_current_character_name[0]["tf_dic"]

		#AMOUNT OF SLICES (N; amount of docs)
		amount_of_slices = len(dic_for_current_character_name[0]["indices_before_after_pair_for_each_context_slice"])

		values_for_zeta = {"dokument_freqs":dokument_freqs, "amount_of_slices":amount_of_slices}

		return values_for_zeta

	def calculate_zeta(self, values_for_zeta_target, values_for_zeta_comparison, dta_holder, remove_stopwords_in_context="n"):

		keys_target = list(values_for_zeta_target["dokument_freqs"].keys())
		keys_comparison = list(values_for_zeta_comparison["dokument_freqs"].keys())
		token_keys_from_both = keys_target + keys_comparison

		if remove_stopwords_in_context=="y":
			token_keys_from_both = [key_in_list for key_in_list in token_keys_from_both if key_in_list not in dta_holder["stopwords"]]

		values_for_zeta_target["partition_value"] = {}
		values_for_zeta_comparison["partition_value"] = {}

		#print(token_keys_from_both)
		#token_keys_from_both = list(set([values_for_zeta_target["dokument_freqs"].keys()] + [values_for_zeta_comparison["dokument_freqs"].keys()]))

		for token_key in token_keys_from_both:
			#print(token_key)

			try:
				target_partition = values_for_zeta_target["dokument_freqs"][token_key] / values_for_zeta_target["amount_of_slices"]
			except KeyError:
				target_partition = 0

			values_for_zeta_target["partition_value"][token_key] = target_partition

		for token_key in token_keys_from_both:
			try:
				comparison_partition = values_for_zeta_comparison["dokument_freqs"][token_key] / values_for_zeta_comparison["amount_of_slices"]
			except KeyError:
				comparison_partition = 0

			values_for_zeta_comparison["partition_value"][token_key] = comparison_partition

		zeta_scores_target = {}
		zeta_scores_comparison = {}
		# zeta_scores_target = list()
		# zeta_scores_comparison = list()
		for token_key in token_keys_from_both:
			zeta_scores_target[token_key] = values_for_zeta_target["partition_value"][token_key] - values_for_zeta_comparison["partition_value"][token_key]
			zeta_scores_comparison[token_key] = values_for_zeta_comparison["partition_value"][token_key] - values_for_zeta_target["partition_value"][token_key]

		zeta_scores_target_sorted = sorted(zeta_scores_target.items(), key=operator.itemgetter(1), reverse=True)
		#print(zeta_scores_target_sorted)
		zeta_scores_comparison_sorted = sorted(zeta_scores_comparison.items(), key=operator.itemgetter(1), reverse=True)
		#print(zeta_scores_comparison_sorted)


		results = {"zeta_scores_target_sorted": zeta_scores_target_sorted, "zeta_scores_comparison_sorted":zeta_scores_comparison_sorted}

		return results

####################
		# 	zeta_scores[token_key] = target_partition - comparison_partition
		#
		# zeta_scores_sorted = sorted(zeta_scores.items(), key=operator.itemgetter(1), reverse=True)
		#
		#print(zeta_scores_sorted)




	def zeta(self, dta_holder, number_of_word_clouds, remove_stopwords_in_context):#, mode="single_character_context"):#context_single_characters, context_pairs):

		network_parameters = dta_holder["network_parameters"]
		edge_weights = network_parameters[6]
		edge_weights_sorted = sorted(edge_weights, key=operator.itemgetter(2), reverse=True)

		edge_pair_results = list()

		for edge_pair_list in edge_weights_sorted[0:number_of_word_clouds]:
			#print(edge_pair_list)
			name_target = edge_pair_list[0]
			#print(name_a)
			name_comparison = edge_pair_list[1]
			values_target = features().get_values_for_zeta(character_name=name_target,dta_holder=dta_holder)
			values_comparison = features().get_values_for_zeta(character_name=name_comparison,dta_holder=dta_holder)
			#print("a", values_a)
			#print("b", values_b)

			#print(features().calculate_zeta(values_for_zeta_target=values_target, values_for_zeta_comparison=values_comparison, dta_holder=dta_holder))

			edge_pair_result = features().calculate_zeta(values_for_zeta_target=values_target, values_for_zeta_comparison=values_comparison, dta_holder=dta_holder, remove_stopwords_in_context=remove_stopwords_in_context)
			edge_pair_result["name_target"] = name_target
			edge_pair_result["name_comparison"] = name_comparison
			#edge_pair_results.append(features().calculate_zeta(values_for_zeta_target=values_target, values_for_zeta_comparison=values_comparison, dta_holder=dta_holder))

			edge_pair_results.append(edge_pair_result)

		return edge_pair_results



			#print(edge_pair_list)










############
		# if mode=="single_character_context":
		#
		# 	weighted_degrees = dta_holder["network_parameters"][5]
		# 	weighted_degrees_sorted = sorted(weighted_degrees, key=operator.itemgetter(1), reverse=True)
		#
		# 	#for weighted_degree in weighted_degrees_sorted[0:number_of_word_clouds]:
		# 	for weighted_degree in weighted_degrees_sorted[0:2]:
		#
		#
		# 		zeta_parameter_dic_for_partition = {}
		#
		# 		character_name_of_degree = weighted_degree[0]
		#
		# 		dic_for_current_character_name = [dic for dic in dta_holder["single_character_context"] if dic["character_names"] == character_name_of_degree]
		#
		# 		for unique_context_token in dic_for_current_character_name[0]["tf_sorted_list"]:
		# 			df_unique_context_token = 0
		# 			for context_slice in dic_for_current_character_name[0]["indices_before_after_pair_for_each_context_slice"]:
		# 				#print(unique_context_token[0])
		# 				#print([dta_holder["tokenized_text"][index] for index in context_slice])
		# 				if unique_context_token[0] in [dta_holder["tokenized_text"][index] for index in context_slice]:
		# 					#print("yes")
		# 					df_unique_context_token += 1
		# 				#else:
		# 				#	print("no")
		# 			zeta_parameter_dic_for_partition[unique_context_token[0]] = df_unique_context_token
		#
		# 		print(zeta_parameter_dic_for_partition)


#######################

					#print([dta_holder["tokenized_text"][index] for index in context_slice])

					#if unique_context_token in
				#if unique_context_token in context_slice
				#[indice for indice in dic_for_current_character_name[0]["indices_before_after_pair_for_each_context_slice"]]:

			#print(weighted_degree)



			#if weighted_degree ==

			#print(weighted_degree)
			#print(dic_with_indices_for_current_character_name)["indices_before_after_pair_for_each_context_slice"]
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
			#print(pair)
			#print(context_words[pair]["character_names"])
			PMIs_for_each_word_with_pair = dict()
			for word in context_words[pair]["tf_dic"]:
				#print(word)
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

			# BUILD RANKED PMI LIST
			dictlist = list()
			for key, value in PMIs_for_each_word_with_pair.items():
				temp = [key, value]
				dictlist.append(temp)
			PMIs_for_each_word_with_pair_ranked = sorted(dictlist, key=operator.itemgetter(1), reverse=True)

			PMIs_for_each_pair += [{"character_names": context_words[pair]["character_names"], "PMI": PMIs_for_each_word_with_pair_ranked}]
		# for i,j in enumerate(PMIs_for_each_pair):
		# 	print(i)
		# 	print(j)
		return PMIs_for_each_pair





	# OLD STRUCTURE (LIST)
	# returns list with for each pair:
	#  1. character-pair, 2. Tuples with (words, PMIs) [ranked], 3. Dictionary with all words, PMIs [unranked]

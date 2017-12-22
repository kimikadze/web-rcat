import operator
import math


class features:

	def __init__(self):
		pass

	def PMI(self, context_words, tokenized_text_no_stopword_removal, divide_by="sum_of_context_words"):
		complete_vektor = dict()
		for dic in context_words:
			for word in dic[2]:
				if word in complete_vektor:
					complete_vektor[word] = complete_vektor[word] + dic[2][word]
				elif word not in complete_vektor:
					complete_vektor.update({word: dic[2][word]})

		if divide_by == "sum_of_context_words":
			wortsumme = sum([complete_vektor[j] for j in complete_vektor])
		if divide_by == "text_length":
			wortsumme = len(tokenized_text_no_stopword_removal)

		# Test for all words of "Werther"-novel:
		# wortsumme = 35140

		PMIs_for_each_pair = list()
		for pair in range(len(context_words)):
			PMIs_for_each_word_with_pair = dict()
			for word in context_words[pair][2]:
				P_pair_word = context_words[pair][2][word] / wortsumme
				word_in_pair = context_words[pair][2][word]
				P_pair = sum([context_words[pair][2][j] for j in context_words[pair][2]]) / wortsumme
				counts_word = 0
				for dic in context_words:
					if word in dic[2]:
						counts_word += dic[2][word]
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

			PMIs_for_each_pair += [[context_words[pair][1], PMIs_for_each_word_with_pair_ranked]]

		return PMIs_for_each_pair

	# returns list with for each pair:
	#  1. character-pair, 2. Tuples with (words, PMIs) [ranked], 3. Dictionary with all words, PMIs [unranked]

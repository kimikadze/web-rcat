import operator
import os
from itertools import chain


class relations:
    def __init__(self):
        pass

    def find_character_positions(self, text_tokenized, characters_tokenized):
        characters_indices = list()
        for character_list in characters_tokenized:
            character_index = list()
            for character_synonym in character_list:
                if len(character_synonym) == 1:
                    character_index += [[item] for item in range(len(text_tokenized)) if
                                        text_tokenized[item] == character_synonym[0]]
                elif len(character_synonym) > 1:
                    for word_index in range(len(text_tokenized)):
                        if text_tokenized[word_index:word_index + (len(character_synonym))] == character_synonym:
                            character_index += [[i for i in range(word_index, word_index + (len(character_synonym)))]]
            characters_indices += [character_index]
        return characters_indices
        # finds token positions (indices in txt) for each character
        ## scheme:
        ##       char_1                  char_2
        ## [ [ [1], [8, 9], ... ], [ [12], [22, 23], ... ], ... ]

    ###########################################################################################################


    def build_character_pairs(self, character_list, characters_list_tokenized_without_dots_stripped):
        character_names = [character_list[i][0] for i in range(len(character_list))]
        character_pairs = list()
        for index_a in range(0, len(character_names)):
            for index_b in range(index_a + 1, len(character_names)):
                character_pairs += [[character_names[index_a], character_names[index_b]]]

        character_names_indices = [i for i in range(len(characters_list_tokenized_without_dots_stripped))]
        character_pairs_indices = list()
        for index_a in range(0, len(character_names_indices)):
            for index_b in range(index_a + 1, len(character_names_indices)):
                character_pairs_indices += [[character_names_indices[index_a], character_names_indices[index_b]]]

        return character_pairs_indices, character_pairs
        # builds all possible combinations of character pairs
        ## scheme: [ [char_1, char_2], [char_1, char_3], ... ]

    ###########################################################################################################

    def build_relations(self, character_position, char_pairs, distance_for_relation=10):
        entity_potitions_with_relations = list()
        for i in range(len(char_pairs[1])):
            indices_a = character_position[char_pairs[0][i][0]]
            indices_b = character_position[char_pairs[0][i][1]]
            index_matches_where_char_a_is_in_window_of_b = list()
            for index_b_list in indices_b:
                if len(index_b_list) == 1:
                    for index_a_list in indices_a:
                        if (len(index_a_list) == 1 and index_a_list[0] in [i for i in range( \
                                    index_b_list[0] - distance_for_relation,
                                        index_b_list[0] + distance_for_relation + 1)]):
                            index_matches_where_char_a_is_in_window_of_b += [[[index_a_list[0]], [index_b_list[0]]]]
                        elif (len( \
                                index_a_list) > 1 and (index_a_list[0] in [i for i in range( \
                                    index_b_list[0] \
                                        - distance_for_relation, index_b_list[0] + distance_for_relation + 1)] \
                                                               or index_a_list[-1] in \
                                    [i for i in range(index_b_list[0] - distance_for_relation, index_b_list[0] + \
                                            distance_for_relation + 1)])):
                            index_matches_where_char_a_is_in_window_of_b += [[index_a_list, [index_b_list[0]]]]
                elif len(index_b_list) > 1:
                    for index_a_list in indices_a:
                        if (len( \
                                index_a_list) == 1 and index_a_list[0] in [i for i in range( \
                                    index_b_list[0] - distance_for_relation,
                                    index_b_list[-1] + distance_for_relation + 1)]):
                            index_matches_where_char_a_is_in_window_of_b += [[[index_a_list[0]], index_b_list]]
                        elif (len( \
                                index_a_list) > 1 and (index_a_list[0] in [i for i in range( \
                                    index_b_list[0] - distance_for_relation, index_b_list[-1] + \
                                    distance_for_relation + 1)] or index_a_list[-1] in [i for i in range( \
                                    index_b_list[0] - distance_for_relation,
                                    index_b_list[0] + distance_for_relation + 1)])):
                            index_matches_where_char_a_is_in_window_of_b += [[index_a_list, index_b_list]]
            entity_potitions_with_relations += zip([i], [char_pairs[0][i]], [char_pairs[1][i]],
                                                   [index_matches_where_char_a_is_in_window_of_b])
            # entity_potitions_with_relations += [index_matches_where_char_a_is_in_window_of_b]

        return entity_potitions_with_relations

        # finds indices of context terms for all possible combinations
        # gives: 1. index, 2. Pair indices, 3. Pair Name, 4. Entity positions that have a relation

        ## scheme:
        ##    pair-index    character-indices   character-names         index positions of pairs
        ## [  ( 0,          [0, 1],             ["char_1", "char_2"],   [ [ [8, 9], [12] ], ... ] ) ,
        ##    ( 1,          [0, 2],             ["char_1", "char_3"],   [ ...                   ] ) , ... ]

    ###########################################################################################################

    def count_context_words_for_single_characters(self, character_positions, character_list, tokenized_text,
                                                  words_before=8, words_after=8,
                                                  delete_stopwords_in_context="n", word_field=str(), wf_cat=str(), stop_words=str()):

        context = list()

        #print(character_positions)
        #print(tokenized_text[7960])

        for j in range(len(character_positions)):
            words_before_after_character_positions_for_character = list()

            # zb: Vorkommensliste (mehrere Token potentiell) in WERTHER:
            for character_occurance_list in character_positions[j]:
                words_before_after_character_positions_for_character += [[i for i in range(character_occurance_list[0] - words_before, character_occurance_list[0])] + [i for i in range(character_occurance_list[-1] + 1, character_occurance_list[-1] + 1 + words_after)]]

            #print(words_before_after_character_positions_for_character)

            words_before_after_character_positions_for_character_chained = list(chain.from_iterable(words_before_after_character_positions_for_character))
            #print(words_before_after_character_positions_for_character_chained)

            words_before_after_character_positions_for_character_sorted = sorted(list(set(words_before_after_character_positions_for_character_chained)))
            #words_before_after_character_positions_for_character = list()

            if delete_stopwords_in_context == "n":
                words_before_after_pair = list()
                for index_number in words_before_after_character_positions_for_character_sorted:
                    if index_number in range(0, len(tokenized_text)):
                        words_before_after_pair += [tokenized_text[index_number]]

            if delete_stopwords_in_context != "n":
                # with open(stop_words, "r", encoding="utf-8") as dt:
                #     stop_dt = dt.readlines()
                #     stop_dt = [i.strip() for i in stop_dt]

                words_before_after_pair = list()
                for index_number in words_before_after_character_positions_for_character_sorted:
                    if index_number in range(0, len(tokenized_text)):
                        if tokenized_text[index_number].lower() not in stop_words:
                            words_before_after_pair += [tokenized_text[index_number]]

            if not word_field == "N":
                try:
                    with open(wf_cat, encoding="utf-8") as wf:
                        wordf = wf.readlines()
                        wordf = [i.strip() for i in wordf]
                        words_before_after_pair = [word for word in words_before_after_pair if word in wordf]
                #except IsADirectoryError:
                except TypeError:
                    wordf = []
                    #for root, dirs, files in os.walk(wf_cat):
                    for filename in wf_cat:
                        for line in open(filename, encoding="utf-8"):
                            line = line.strip()
                            wordf.append(line)
                    words_before_after_pair = [word for word in words_before_after_pair if word in wordf]

            #words_before_after_pair_ALL.append(words_before_after_pair)
            word_counts_for_pair = dict()
            for word in words_before_after_pair:
                if word not in word_counts_for_pair:
                    word_counts_for_pair[word] = words_before_after_pair.count(word)

            word_counts_for_pair_ranked = sorted(word_counts_for_pair.items(), key=operator.itemgetter(1),
                                                 reverse=True)

            context += [{"character_names": character_list[j][0],
                         "tf_dic": word_counts_for_pair,
                         "tf_sorted_list": word_counts_for_pair_ranked,
                         "indices_before_after_pair_for_each_context_slice": words_before_after_character_positions_for_character}]

        return context

    ###########################################################################################################

    def count_context_words(self, relations, tokenized_text, words_before=8, words_after=8,
                            delete_stopwords_in_context="n",  word_field=str(), wf_cat=str(), stop_words=str()):
        context = list()
        for j in range(len(relations)):
            words_before_between_after_pair_indices = list()
            for pair in relations[j][3]:
                if pair[0][0] < pair[1][0]:
                    words_before_between_after_pair_indices \
                        += [i for i in range(pair[0][0] - words_before, pair[0][0])] \
                           + [i for i in range(pair[0][-1] + 1, pair[1][0])] + \
                           [i for i in range(pair[1][-1] + 1, pair[1][-1] + 1 + words_after)]
                elif pair[0][0] > pair[1][0]:
                    words_before_between_after_pair_indices += [i for i in range( \
                        pair[1][0] - words_before, pair[1][0])] + [i for i in range( \
                        pair[1][-1] + 1, pair[0][0])] + [i for i in
                                                         range(pair[0][-1] + 1, pair[0][-1] + 1 + words_after)]
            words_before_between_after_pair_indices_sort = sorted(
                list(set(words_before_between_after_pair_indices)))

            if delete_stopwords_in_context == "n":
                words_before_between_after_pair = list()
                for index_number in words_before_between_after_pair_indices_sort:
                    if index_number in range(0, len(tokenized_text)):
                        words_before_between_after_pair += [tokenized_text[index_number]]

            if delete_stopwords_in_context != "n":
                #print(os.getcwd())
                # with open(stop_words, "r", encoding="utf-8") as dt:
                #     stop_dt = dt.readlines()
                #     stop_dt = [i.strip() for i in stop_dt]

                words_before_between_after_pair = list()
                for index_number in words_before_between_after_pair_indices_sort:
                    if index_number in range(0, len(tokenized_text)):
                        if tokenized_text[index_number].lower() not in stop_words:
                            words_before_between_after_pair += [tokenized_text[index_number]]
                #print(words_before_between_after_pair)

            if not word_field == "N":
                try:
                    with open(wf_cat, encoding="utf-8") as wf:
                        wordf = wf.readlines()
                        wordf = [i.strip() for i in wordf]
                        words_before_between_after_pair = [word for word in words_before_between_after_pair if
                                                           word in wordf]
                #except IsADirectoryError:
                except TypeError:
                    wordf = []
                    #for root, dirs, files in os.walk(wf_cat):
                    for filename in wf_cat:
                        for line in open(filename, encoding="utf-8"):
                            line = line.strip()
                            wordf.append(line)
                    words_before_between_after_pair = [word for word in words_before_between_after_pair if
                                                       word in wordf]

            word_counts_for_pair = dict()
            for word in words_before_between_after_pair:
                if word not in word_counts_for_pair:
                    word_counts_for_pair[word] = words_before_between_after_pair.count(word)

            # print(word_counts_for_pair)
            word_counts_for_pair_ranked = sorted(word_counts_for_pair.items(), key=operator.itemgetter(1),
                                                 reverse=True)

            # OLD: as list:
            # context += zip([relations[j][1]], [relations[j][2]], [word_counts_for_pair],
            #               [word_counts_for_pair_ranked])

            # NEW as list with dictionaries
            context += [{"character_indices": relations[j][1], "character_names": relations[j][2],
                         "tf_dic": word_counts_for_pair, "tf_sorted_list": word_counts_for_pair_ranked}]

        return context

        # gives for each pair:
        # 1. Pair indices,
        # 2. Pair Name,
        # 3. words_before_between_after_pair_indices for each pair (dictionary)
        # 4. words_before_between_after_pair_indices for each pair (tuples, ranked)



        ## scheme for OLD (as list):
        ## character-indices    character-names        dictionary with tf          list sorted by tf
        ## [ ( [0, 1],          ["char_1", "char_2"],  {"w1": 4, "w2": 10, ...},   [("w2", 10), ("w1", 4), ...]), ... ]

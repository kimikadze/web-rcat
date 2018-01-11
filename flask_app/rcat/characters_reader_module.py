from nltk import word_tokenize

class characters_reader:


##### read characters via character list

    def __init__(self):
        pass

    def read_characters(self, char_file):
        with open(char_file, encoding='UTF-8') as char_data:
            doc = char_data.readlines()
            character_list = list()
            for line in doc:
                splitted_line = line.split("\t")
                splitted_line[-1] = splitted_line[-1].strip()
                splitted_line[0] = splitted_line[0].strip("\ufeff")
                character_list += [splitted_line]
            return character_list

    # reads the characters line by line
    # (each line contains one character, with tabstop separated synonyms)

###########################################################################################################

    def tokenize_characters(self, character_list):
        characters_list_tokenized = list()
        for single_character_list in character_list:
            new_single_char_list = list()
            for i in single_character_list:
                new_single_char_list += [word_tokenize(i)]
            characters_list_tokenized += [new_single_char_list]
        #Problem: sometimes tokenisation includes dotes with single characters: ["Graf", "R."] sometimes not: ["N.", "N", "."]
        #remove all dots:
        characters_list_tokenized_without_dots = list()
        for single_character_list in characters_list_tokenized:
            new_single_char_list_2 = list()
            for synonym_liste in single_character_list:
                # get all indices for elements that contain only "." and remove these elements:
                remove_indices = [item for item in range(len(synonym_liste)) if synonym_liste[item] == "."]
                # return only that indices that should not be removed:
                new_single_char_list_2 += [[i for j, i in enumerate(synonym_liste) if j not in remove_indices]]
            characters_list_tokenized_without_dots += [new_single_char_list_2]

        characters_list_tokenized_without_dots_stripped = list()
        for single_character_list in characters_list_tokenized_without_dots:
            new_single_char_list = list()
            for synonym_liste in single_character_list:
                new_synonym_list = list()
                for i in synonym_liste:
                    new_synonym_list += [i.strip(".")]
                new_single_char_list += [new_synonym_list]
            characters_list_tokenized_without_dots_stripped += [new_single_char_list]

        return characters_list_tokenized_without_dots_stripped

    # tokenizes characters

    ## data scheme:
    ## [ [ [char_a], [a_synonym_1], [a_synonym_2_token_i, a_synonym_2_token_ii], ... ], [ [char_b], ... ] ]


############################################################################
############################################################################



class relations:
    def __init__(self):
        pass

    def find_character_positions(text_tokenized, characters_tokenized):
        characters_indices = dict()
        for index, character_list in enumerate(characters_tokenized):
            character_index = list()
            for character_synonym in character_list:
                if len(character_synonym) == 1:
                    character_index += [[item] for item in range(len(text_tokenized)) if
                                        text_tokenized[item] == character_synonym[0]]
                elif len(character_synonym) > 1:
                    for word_index in range(len(text_tokenized)):
                        if text_tokenized[word_index:word_index + (len(character_synonym))] == character_synonym:
                            character_index += [[i for i in range(word_index, word_index + (len(character_synonym)))]]
            # characters_indices[index] = list()
            characters_indices[index] = character_index
        return characters_indices
        # finds token positions (indices in txt) for each character
        ## scheme:


        # {
        #   0: [ [ [1], [8, 9], ... ]           ## character 0 (first element)
        #   1:  [ [12], [22, 23], ... ]         ## character 1 (second element)
        #   ...
        #   n: [ [ [99], [103, 104], ... ]      ## last character
        # }
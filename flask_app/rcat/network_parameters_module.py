import statistics

class network_parameters:

    def __init__(self):
        pass

    def calculate_network_parameters(self, relations, characters):
        unique_pairs_that_have_connection = list()
        for i in range(len(relations)):
            if len(relations[i][3]) > 0:
                unique_pairs_that_have_connection += [relations[i][2]]
        character_names = list()
        for i in range(len(characters)):
            character_names += [characters[i][0]]
        counter = list()
        counter = [0] * len(character_names)
        for i in range(len(character_names)):
            counter[i] = 0
            for pair in unique_pairs_that_have_connection:
                if (pair[0] == character_names[i] or pair[1] == character_names[i]):
                    counter[i] += 1
        degrees_for_each_character = list()
        for (i, j) in zip(character_names, counter):
            degrees_for_each_character += [[i, j]]
        remove_indices = [item for item in range(len(degrees_for_each_character)) if degrees_for_each_character[item][1] == 0]
        degrees_for_each_characters_that_have_connection = [i for j, i in enumerate(degrees_for_each_character) if j not in remove_indices]

        #average_degree_1 = sum(counter) / len(degrees_for_each_characters_that_have_connection)

        counter_without_zeros = [i for j, i in enumerate(counter) if j not in remove_indices]
        average_degree = statistics.mean(counter_without_zeros)
        sd_degree = statistics.stdev(counter_without_zeros)

        realised_connections = sum(counter_without_zeros)
        possible_connections = (len(degrees_for_each_characters_that_have_connection) - 1) * len(degrees_for_each_characters_that_have_connection)
        density = realised_connections / possible_connections

        #print(average_degree, sd_degree, density, degrees_for_each_characters_that_have_connection)

        #weighted edges
        weighted_degrees_for_each_characters_that_have_connection = []
        weighted_degrees_with_zeros = []
        #for i in range(0, len(character_names)):
        for name in character_names:
            weighted_degree = 0
            for index in range(0, len(relations)):
                if name in relations[index][2]:# and len([relations[i][3]]) != 0:
                ##if name in relations[index][2] and relations[index[3]] != 0:
                    weighted_degree += len(relations[index][3])
                #if character_names[i] in [relations[i][2]] and len([relations[i][3]]) != 0:
                #    weighted_degree += len(relations[i][3])
            if weighted_degree != 0:
                weighted_degrees_for_each_characters_that_have_connection += [[name, weighted_degree]]

            weighted_degrees_with_zeros += [[name, weighted_degree]]


        character_a_character_b_edge_weight = list()
        for relation in relations:
            if len(relation[3]) != 0:
                character_a_character_b_edge_weight += [[relation[2][0], relation[2][1], len(relation[3])]]
        #print(character_a_character_b_edge_weight)


        #print(weighted_degrees)
        #print(degrees_for_each_characters_that_have_connection)
        return average_degree, sd_degree, density, degrees_for_each_characters_that_have_connection, weighted_degrees_for_each_characters_that_have_connection, weighted_degrees_with_zeros, character_a_character_b_edge_weight



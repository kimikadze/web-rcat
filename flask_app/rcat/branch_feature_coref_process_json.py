import json
dist = 8

from pprint import pprint

with open("../data/coref_json/Werther_IH.json") as f:
	data = json.load(f)
	#pprint(data)

for n, dict in enumerate(data[0:100]):
	print(n, dict)

# entities_list = list()
# for i in data:
# 	if "entities" in i:
# 	#if i["entities"] == True:
# 		#print(i["entities"])
# 		entities_list += i["entities"]
# n = max(entities_list)
#
#
# positions = dict()
# for i in range(n+1):
# 	#print(i)
# 	positions[i] = list()
#
# #pprint(positions)
#
# for index, token_dic in enumerate(data):
# 	if "entities" in token_dic:



		# for entity_number in token_dic["entities"]:
		# 	token_dic[entity_number] +=
		#
		# 	try:
		# 		while
		#print(token_dic)












#print(n)









#for i in data:
#	print(i)


#def chunks(1,dist):
#	for dict in range(0,len(data), dist):

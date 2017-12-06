import uuid
import os




my_id = uuid.uuid1()
print(my_id)



# with open("output/%s_relations.txt" %my_id, mode="w") as f:
# 	f.write("File under this session: %s" %my_id)
# with open("output/%s_gephi.txt" %my_id, mode="w") as f:
# 	f.write("Gephi-file under this session: %s" %my_id)


#folder = str(my_id)

if not os.path.exists(str(my_id)):
    os.makedirs(str(my_id))
with open("%s/%s_file.txt" %(my_id, my_id), mode="w") as f:
	f.write("test")
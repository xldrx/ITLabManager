import jsonpickle
names=[]
with open("hostnames.txt","r") as fp:
	names = fp.readlines()

list = []
for i in range(1,25):
	list.append({"PhysicalName":"pc%02d"%i, "NetworkAddress":"172.16.1.%d"%i, "VirtualName":names[i-1]})
print jsonpickle.encode(list,False)

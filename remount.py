import os, jsonpickle
import sys

baseCommand = 'ssh root@%s -o StrictHostKeyChecking=no -o ConnectTimeout=2 "mount -a"'

list = []
with open("Hosts.json","r") as fp:
	file = fp.read()
	list = jsonpickle.decode(file)

start = 0
end = len(list)

if len(sys.argv)>1:
	nums = str.split(sys.argv[1],"-")
	start = int(nums[0])-1
	if len(nums)>1: end = int(nums[1])
	else: end = start+1

for host in list[start:end]:
	address = host["NetworkAddress"]
	command = baseCommand % address
	print "==> %s:%-14s @%s" % (host["PhysicalName"], host["VirtualName"], address)
	result = os.system(command)
	print

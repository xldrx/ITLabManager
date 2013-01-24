#! /usr/bin/env python -u
# coding=utf-8

import os
import jsonpickle

__author__ = 'xl'
import argparse

actions={
    "Hostname":"hostname -f;hostname -A;hostname -I;",
    "SetVirtualName":"echo {vname} > /etc/hostname;hostname {vname};hostname",
    "Whoami":"who am i",
    "ListScratch":"ls -la /scratch",
    "Remount":"mount -a",
    "SSH": None,
    "Uname": "uname -a",
    "VIVersion": "vi --version | head -n 1",
    }



def setupParser():
    parser = argparse.ArgumentParser(description="Test Arg Parsing in Python", prog="xlManager")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-c", "--Command", help="Command to run on each computers", dest="command")
    group.add_argument("-a", "--action", help="Action to run on each computers", choices=actions.keys())

    parser.add_argument("-t","--TargetComputerRange", help="Range number of target computers (e.g. 2 or 1-10)", dest="target")
    parser.add_argument("-v", "--verbose", help="Verbose the output", action="store_true", dest="verbose")
    parser.add_argument("-q", "--quiet", help="Will hide all errors", action="store_true", dest="quiet")
    parser.add_argument("--test", help="Will not actually run any command", dest="test", action="store_true")
    parser.add_argument("-ct","--ConnectTimeout", help="Connection Timeout", dest="connectTimeout", type=int, default=1)
    parser.add_argument("-k", "--key", help="Key file for connecting targets. (default is ./keys/id_rsa)", default="./keys/id_rsa", dest="sshkey")

    return parser

def parse(parser=None):
    if not parser: parser=setupParser()
    return parser.parse_args()

class HostClass(object):
    def __init__(self, vname, pname, address, num):
        self.vname = vname
        self.pname = pname
        self.address = address
        self.num0 = num
        self.num1 = num+1

    def __repr__(self):
        ret = u"["
        for row in self.__dict__:
            ret+="%s: %s, "%(row,self.__dict__[row])

        ret+="]"

        return ret


def compileString(basecommand, host):
    return basecommand.format(**host.__dict__)

def readListFile():
    list = []
    with open("conf/Hosts.json","r") as fp:
    	file = fp.read()
    	list = jsonpickle.decode(file)
    return list

def readList():
    list = readListFile()
    ret = []
    for i,l in enumerate(list):
        host = HostClass(l["VirtualName"], l["PhysicalName"], l["NetworkAddress"], i)
        ret.append(host)

    return ret

def MakeSSHCommand(baseCommand=None, args=None):
    ret = 'ssh root@{address} -o StrictHostKeyChecking=no '
    ret += '-o ConnectTimeout=%s ' %(args.connectTimeout if args else 1)
    ret += ('-i "%s" ' %args.sshkey) if args else " "
    ret += '"%s" ' % baseCommand if baseCommand else " "
    ret += "2> /dev/null " if args and args.quiet else " "

    return ret

def Run(baseCommand=None, args=None, list=None):
    errorList = []

    if not list:
        list = readList()

    baseCommand = MakeSSHCommand(baseCommand, args)
    start = 0
    end = len(list)

    if args.target:
    	nums = str.split(args.target,"-")
    	start = int(nums[0])-1
    	if len(nums)>1: end = int(nums[1])
    	else: end = start+1

    for host in list[start:end]:
    	print "==> %s:%-14s @%s" % (host.pname, host.vname, host.address)
        command = compileString(baseCommand, host)

        if args.verbose:
            print "::: Running [%s]" % command

    	if args.test:
            print "::: In real will run [%s]" % command
        else:
    	    result = os.system(command)
            if args.verbose:
                print "::: Returned (%s)" % result
            if result != 0:
                errorList.append((host, result))
            pass

        print

    if len(errorList)>0:
        print ">>> There were some errors when run commands on following computer(s)"
        for host, errorCode in errorList:
            print compileString("* {pname}: {vname:14} {address:17}", host),
            print "returned ", errorCode

def Main():
    args=parse()
    if args.action:
        Run(actions[args.action], args)
    else:
        Run(args.command, args)

    print "\n\n>>> By Sayed Hadi Hashemi - info@xldrx.com <<<\n"

Main()
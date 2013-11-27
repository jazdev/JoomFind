#!/usr/bin/python

import os

def tests():
	urlfile = "urls.txt"
	os.system('python ../src/JoomFind.py -f urls.txt --verbose')

if __name__=="__main__":
	tests()

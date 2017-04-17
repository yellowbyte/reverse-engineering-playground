#!/usr/bin/env python

import sys
import struct

def main():
	print "---------- zeroSection2 ----------"

	#open the file as stream of binary in read and write 
	filePath = sys.argv[1]
	theFile = open(filePath, "r+b")
	contents = theFile.read()

	#figure out size of section headers table 
	start =  struct.unpack("i", contents[32:36])[0]
	entrySize = struct.unpack("i", contents[46:48]+b'\x00\x00')[0]
	entryNum = struct.unpack("i", contents[48:50]+b'\x00\x00')[0]
	totalSize = entrySize * entryNum

	#zero out the whole section headers table 
	theFile.seek(start)
	theFile.write(b'\x00' * totalSize)
	
	#zero out section headers info. from ELF Header 
	offsets = [0x20, 0x2e, 0x30]
	bytes = 4
	for i in range(len(offsets)): 
		if i == 1: #from index 1 and on, btyes to update is 2 
			bytes = 2
		theFile.seek(offsets[i])	
		theFile.write(b'\x00' * bytes)
			
	

main()

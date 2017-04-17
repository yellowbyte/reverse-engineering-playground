#!/usr/bin/env python

import sys 
import struct

def main(): 
	print "---------- zeroSection ----------"

	#read the content of the file in binary 
	filePath = sys.argv[1]
	theFile = open(filePath, "r+b")

	#zero out e_shoff, pointer to start of section header table
	theFile.seek(0x20)
	theFile.write(b'\x00\x00\x00\x00')

	#zero out e_shentsize, e_shnum, e_shstrndx	
	rest = [0x2e, 0x30, 0x32] #e_shentsize (size of a section header table entry), e_shnum (number of entries in the section header table), e_shstrndx (index of section header table entry)
	for offset in rest: 
		theFile.seek(offset)
		theFile.write(b'\x00\x00')

	theFile.close()

main()

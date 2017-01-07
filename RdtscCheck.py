import idautils
import idaapi

def main():
	print "--------------- RdtscCheck ---------------"
	
	current = MinEA()
	end = MaxEA()
	found = 0

	while current < end: 
		current = FindBinary(current, SEARCH_DOWN|SEARCH_NEXT, '0f 31')
		if current != BADADDR and  SegName(current) == ".text": 
			print hex(current), GetDisasm(current)
			found = 1
	if found == 0: 
		print "*** No rdtsc instruction found"

main()
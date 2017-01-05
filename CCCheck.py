import idautils
import idaapi

def main():
	print "--------------- CCCheck ---------------"
	
	current = MinEA()
	end = MaxEA()
	found = 0

	while current < end: 
		current = FindBinary(current, SEARCH_DOWN|SEARCH_NEXT, 'CC')
		if current != BADADDR and  SegName(current) == ".text": 
			print hex(current), GetDisasm(current)
			found = 1
	if found == 0: 
		print "*** No 0xCC byte found"

main()

def main():
	print "---------- nopsled ----------"
	
	start = SelStart()
	end = SelEnd()
	if start == end: #user did not select multiple lines. User only wants to nop current instruction
		start = ScreenEA()
		end = NextHead(start)
	while start < end: 
		PatchByte(start, 0x90)	
		start += 1
	print hex(start), hex(end), type(start)

main()

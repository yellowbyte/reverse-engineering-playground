import idautils
import idaapi

def main():
	print "--------------- Deobfuscate ---------------"

	mask = [0xc1, 0x8f, 0x04, 0x08]
	ea = ScreenEA()
	maxAddr = MaxEA()
	i = 0
	check = 0 

	while ea < maxAddr: 
		PatchByte(ea, Byte(ea) ^ mask[i])
		i = (i+1) % 4
		ea = NextAddr(ea)


main()
import idautils
import idaapi


def findArguments(funcAddr, parentAddr): 
	"""
	find the number of arguments for a function 
	"""
	funcAddr = PrevHead(funcAddr, parentAddr)
	argNum = 0

	while GetMnem(funcAddr) != "call" and GetMnem(funcAddr)[0] != "j" and funcAddr != parentAddr: #while the instruction is not a call or jcc or pass the start of a function
		if GetMnem(funcAddr) == "mov" and "esp" in GetOpnd(funcAddr, 0): #a mov instruction that updates the stack. In GCC compiled 32-bits binary, mov instruction is used to put function arguments on stack instead of push instruction
			argNum += 1
		funcAddr = PrevHead(funcAddr, parentAddr)

	return argNum

def main():
	print "--------------- LocFuncAnalyzer ---------------"

	data = [0, 1, 2, 3, 4, 5]

	for func in idautils.Functions():
		flags = GetFunctionFlags(func)
		codeRef = 0
		dataRef = 0
		NotLocalFunc = False
		
		if SegName(func) != ".text" or GetFunctionName(func).lstrip("_") == "start": # Ignore library functions and start 
			continue 
		for addr in idautils.XrefsTo(func, 1):
			if SegName(addr.frm) != ".text" or GetFunctionName(addr.frm).lstrip("_") == "start": #if it's not called from .text section then it's not a local function created by the programmer 
				NotLocalFunc = True
				break
			if addr.type in data: 
				dataRef += 1
			else: 
				codeRef += 1
				refAddr = addr.frm
				refParentAddr = GetFunctionAttr(addr.frm, FUNCATTR_START)
		if NotLocalFunc:
			continue

		#If execution gets here, then it is a function that we are interested in
		print "*** ", GetFunctionName(func)
		print "Number of Arguments: ", findArguments(refAddr, refParentAddr)
		print "Code References: ", codeRef
		print "Data References: ", dataRef





main()

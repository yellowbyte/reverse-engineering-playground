from idc import *

def initialPattern(instr_addr, structures): 
	'''find the initial pattern that signals a possible input pin being used, output pin being used, or I2C communication'''
	instruction = GetDisasm(instr_addr)
	for struct in structures.keys(): 
		if(structures[struct] in instruction and ("LDR" in instruction or "MOV" in instruction)):
			return instruction.split()[1][:-1]+" "+hex(instr_addr)+" "+struct #1: reg, 2: addr, 3: struct
	return ""

def PatternEnd(instruction):
	'''initial pattern already found. Figure out if current instruction is where the pattern ends. And if it is, print the type of pattern'''
	global identify
	global reg
	global address
	global struct_type

	if(reg in instruction and ("STR" not in instruction and "LDR" not in instruction)): #Not the immediate value for the struct (pattern matching fails) 
		identify = False
		result = initialPattern(addr, structures)
		if(len(result) != 0):
			reg, address, struct_type = result.split()
	elif(reg in instruction and "STR" in instruction): #pattern confirms (output) 
		identify = False
		print("   struct:"+struct_type+" address: "+address+" (writing to register)")
	elif (reg in instruction and "LDR" in instruction): #pattern confirms (input)
		identify = False
		print("   struct:"+struct_type+" address: "+address+" (reading from register)")

def Analyze():
	'''main routine. NOTE: makes sure to update the structures dictionary on line 39 to the chip that the binary is compiled for'''
	print("------------------------------BEGIN--------------------------------")

	#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!IMPORTANT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	#The structures dictionary needs to be updated to the peripheral boundary addresses for the chip that the binary is compiled for
	#On the STM32F0 Discovery Board the chip is a STM32F0. The peripheral boundary addresses can be find on page 45 of the 
	#Reference Manual(http://datasheet.octopart.com/STM32F072CBT6-STMicroelectronics-datasheet-21772404.pdf). 
	#Also note that on the structures below, I didn't include all the structure addresses, I only include the one that I am interested in.  
	structures = {"RCC":"0x40021000", "GPIOC":"0x48000800", "GPIOA":"0x48000000"}

	functions = {}
	begin = ScreenEA() 
	identify = False #begin identifying form (pattern matching)
	valid = {}

	global identify
	global reg
	global address
	global struct_type

	for funcAddr in Functions(SegStart(begin), SegEnd(begin)): 
		functions[GetFunctionName(funcAddr)] = funcAddr #a function dictionary is created to support pattern matching in another function 

	for funcAddr in Functions(SegStart(begin), SegEnd(begin)):
		print("Inside Function: "+GetFunctionName(funcAddr)+" ("+hex(funcAddr)+")")
		addresses = list(FuncItems(funcAddr)) #return list of instructions in the function  
		for addr in addresses:
			instruction = GetDisasm(addr)
			if("STR" in instruction and "#0x28" in instruction):
				print("~~~~~~~~~~ Possible I2C communication ~~~~~~~~~~")
			if(identify): #already matched the initial line for the pattern. Now checks if the pattern exists
				if("sub" in instruction): #pattern matching continues onto another function
					func = instruction.split()[1] #function name
					func_addresses = list(FuncItems(functions[func]))
					for fe in func_addresses: 
						PatternEnd(GetDisasm(fe))
				PatternEnd(instruction)
			else:  #start of pattern matching hasn't been identified yet
				result = initialPattern(addr, structures)
				if(len(result) != 0):
					reg, address, struct_type = result.split()
					identify = True

if __name__ == '__main__':
	Analyze()
import idautils
import idaapi

MalFunc = {
	"CheckRemoteDebuggerPresent" : "Checks to see if a specific process (including your own) is being debugged", 
	"IsDebuggerPresent" : "Checks to see if the current process is being debugged",
	"MapVirtualKey" : "Translates a virtual-key code into a character value. Used by keylogging malware",
	"GetTickCount" : "Retrieves the number of milliseconds since bootup",
	"EnableExecuteProtectionSupport" : "Used to modify the Data Execution Protection (DEP) settings of the host, making it more susceptible to attack", 
	"GetTickCount" : "Retrieves the number of milliseconds since bootup. Used to gather timing information",
	"IsDebuggerPresent" : "Checks to see if the current process is being debugged", 
}

def main(): 
	print "--------------- MalCheck ---------------"

	functions = [GetFunctionName(i) for i in idautils.Functions()]
	badFunc = [i for i in functions if i in MalFunc.keys()]

	if(len(badFunc) == 0):
		print "no low-hanging fruits detected"
	else: 
		for i in badFunc: 
			print i, ":", AntiDebugFunc[i]

if __name__ == '__main__': 
	main()
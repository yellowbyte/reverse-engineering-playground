# IDAPython_Scripts
Either general IDAPython scripts I made to aid me in everyday reversing or IDAPython scripts I made targeting a specific executable (e.g. deobfuscate a specific routine that is unlikely to appear in other executables). All IDAPython scripts I made from now on will be placed here. 

### CCCheck ###
The 0xCC byte is the byte representing int 3, or software breakpoint. When you make a software breakpoint on an instruction, the debugger replaces the first byte of the instruction to 0xCC. When the CPU hits the int 3 instruction, the OS will signal SIGTRAP to the debugged program. But since the program is being debugged, the debugger will catch it instead, effectively halting the execution temporatory. The 0xCC byte can also be added to the program itself by the original software developers to thwart off people trying to reverse engineer their program since running the program under a debugger will stop it at random 0xCC instructions. This script checks the .text section for the 0xCC bytes and prints the addresses of where the 0xCC bytes are located if they exist. Being able to quickly identify where all the manually added 0xCC bytes are makes the initial dynamic analysis process smoother. 

### Deobfuscate ###
Deobfuscates a portion of the code and data for a crackme by Tosh. This script will directly patch the bytes in IDA so IDA will show the correct deobfuscated listing rather than writing the deobfuscated listing to a separate file. This enhances static analysis and makes solving this crackme challenge a lot faster. Full write-up of this particular crackme can be viewed on my blog (http://yellowbyte.blogspot.com/2017/01/elf-anti-debug-root-me-cracking.html).

### FindMain ###
In a stripped ELF executable, automatically find and rename main as "main." 

### MalCheck ###
Checks an executable for usage of API that has a high chance of being used maliciously or for anti-reversing purposes such as IsDebuggerPresent. It's always a good idea to check for low-hanging fruits before doing any deeper analysis. The "potentially malicious" functions that I came up with are from the book "Practical Malware Analysis."

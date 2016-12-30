# IDAPython-Scripts
Either general IDAPython scripts I made to aid me in everyday reversing or IDAPython scripts I made targeting a specific executable (e.g. deobfuscate a specific routine that is unlikely to appear in other executables). All IDAPython scripts I made from now on will be placed here. 

### MalCheck ###
Checks an executable for usage of API that has a high chance of being used maliciously or for anti-reversing purposes such as IsDebuggerPresent. It's always a good idea to check for low-hanging fruits before doing any deeper analysis. The "potentially malicious" functions that I came up with are from the book "Practical Malware Analysis."

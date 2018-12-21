Given a file containing shellcode, it will wrap it into an executable binary so an analyst can perform live debugging on the shellcode.

Example:
python shc2exe.py -a x86 sample_shc_32

__NOTE__: currently only support shellcode for x86 and x86-64 ISA.

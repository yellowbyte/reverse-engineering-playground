### [shc2exe](https://github.com/yellowbyte/reverse-engineering-playground/blob/master/shellcode_analysis/shc2exe.py) 
Given a file containing shellcode, it will wrap it into an executable binary so an analyst can perform live debugging on the shellcode.
```bash
python shc2exe.py -a x86 sample_shc_32
```
The sample provided shellcodes, sample_shc_32 and sample_shc_64, are taken from [shell-storm](http://shell-storm.org/shellcode/) and note that it currently only support shellcode for x86 and x86-64 ISA.

#!/usr/bin/env python2

import os
import sys
import glob
import lief
import click
import struct

from capstone import *

CURRENT_DIR = os.getcwd()

MD_32 = Cs(CS_ARCH_X86, CS_MODE_32)
MD_64 = Cs(CS_ARCH_X86, CS_MODE_64)

TEMPLATE_32 = "section .text\n" \
"global _start\n" \
"\n" \
"_start:\n{}" \
"\n" \
"xor ebx, ebx\n" \
"mov eax, 0x1\n" \
"int 0x80\n" \

TEMPLATE_64 = ".intel_syntax noprefix\n" \
".global _start\n" \
".text\n" \
"\n" \
"_start:\n{}" \
"\n" \
"xor rdi, rdi\n" \
"mov rax, 0x3c\n" \
"syscall\n" \


class BinaryBuilder:
    """    
    This class builds an executable binary from shellcode
    """    

    def __init__(self, shellcode, executable_name, arch):
        self.shc = shellcode
        self.name = executable_name
        self.arch = {
            "MD": MD_32 if arch=="x86" else MD_64,
            "template": TEMPLATE_32 if arch=="x86" else TEMPLATE_64,
            "extension": ".asm" if arch=="x86" else ".s",
            "assemble": "nasm -f elf32 -o {0}.o {0}.asm" if arch=="x86" else
                "gcc -c {0}.s", # Why GCC instead of NASM for x86-64:
                                # Capstone incorrectly disassembled some x86-64
                                # mov instruction as `movabs` instead of just 
                                # `mov`. `movabs` is valid AT&T syntax but not
                                # valid Intel syntax. Capstone is disassembling
                                # all other instruction as Intel syntax but with
                                # just the caveat of that mov instruction in AT&T.
                                # NASM can only assemble Intel syntax assembly, thus
                                # failed to assemble when it encountered `movabs`
            "link": "ld -m elf_i386 -o {0} {0}.o" if arch=="x86" else
                "ld -o {0} {0}.o"
        }
        self.filename = os.path.join(
            CURRENT_DIR, 
            self.name+self.arch["extension"])
        self._disasm = None
        self._assembly = None
        self._binary = None
        self._shc_disasm()
        self._inject()
        self._compile()
        self._parse_binary()

    @property
    def shellcode(self):
        """
        Disassembled shellcode
        """
        return self._disasm
    
    @property
    def assembly(self):
        """
        Content of a compilable assembly file with the shellcode injected
        """
        return self._assembly

    @property
    def va(self):
        """
        Virtual Address pointing to the beginning of the injected shellcode
        """
        return hex(self._binary.header.entrypoint)

    @staticmethod
    def to_disk(content, filename):
        """
        Save data to file on disk
        """
        with open(filename, "w") as f:
            f.write(content)

    def _shc_disasm(self):
        """
        Disassemble shellcode
        """
        self._disasm = "\n".join(map(
            lambda i: i.mnemonic+" "+i.op_str, 
            self.arch["MD"].disasm(self.shc, 0x1000)))

    def _inject(self):
        """
        Inject assembly snippet into assembly template
        """
        self._assembly = self.arch["template"].format(
            self._disasm)

    def _parse_binary(self): 
        self._binary = lief.parse(self.name)

    def _compile(self):
        """
        Create executable binary
        """
        self.to_disk(self.assembly, self.filename)

        # compile to object file
        os.system(self.arch["assemble"].format(
            self.name))

        # assemble to get executable
        os.system(self.arch["link"].format(
            self.name))
        self._cleanup()

    def _cleanup(self):
        """
        Delete artifacts left by the compilation process
        """
        for f in glob.glob(os.path.join(CURRENT_DIR, self.name+".*")):
            os.remove(f)


def get_shellcode(filepath):
    """
    Get shellcode from file and then sanitize it for usage
    """
    with open(filepath) as shellcode_file:
        _bytes = shellcode_file.read().strip().split(r"\x")
        _bytes = [struct.pack("B",int(b,16)) for b in _bytes if b]
        shellcode = "".join(_bytes)
    return shellcode

@click.command()
@click.argument("path", required=True)
@click.argument("filename", default="executable", required=False)
@click.option("--arch", "-a", default="x86", help="What is the target ISA?")
def main(path, arch, filename):
    """
    *** CURRENTLY ONLY SUPPORT X86 and X86-64 ***
    """
    shellcode = get_shellcode(path)

    _bin = BinaryBuilder(shellcode, filename, arch)
    print("Inserted shellcode is at address: {}".format(_bin.va))

if __name__ == "__main__":
    main()

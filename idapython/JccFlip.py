def setup():
    # There are many equivalences in the jcc instructions. Because of that my list is a lot shorter than the actual list
    # showing all available jcc instructions. For example, JLE and JNG are equivalent, thus their representation in hex,
    # 7e, are equal. Also, my list doesn't include the more obscure jcc instructions such as those that jump depending
    # on the parity, sign, and overflow flags. 
    jumpMirror = {
        0x77:0x72, #JA:JB
        0x73:0x76, #JAE:JBE
        0x74:0x75, #JE:JNE
        0x7f:0x7c, #JG:JL
        0x7d:0x7e, #JGE:JLE	
        0x76:0x73, #JNA:JNB
        0x72:0x77, #JNAE:JNBE
        0x75:0x74, #JNZ:JZ
    }

    # Add in the pairs in reverse order. For example, the jumpMirror will match JA to JB but not JB to JA. This fixes that
    for key in jumpMirror.keys():
        jumpMirror[jumpMirror[key]] = key


def main():
    print '---------- ConditionalFlip ----------'

    setup()
    ea = ScreenEA()
    PatchByte(ea, jumpMirror[Byte(ea)])	


main()

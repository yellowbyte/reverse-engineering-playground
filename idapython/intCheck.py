def main():
    print '---------- intCheck ----------'

    current = MinEA()
    end = MaxEA()
    found = False
    
    while current < end:
        current = FindBinary(current, SEARCH_DOWN|SEARCH_NEXT, 'cd')
        if current != BADADDR and SegName(current) == '.text' and Byte(current+1) != 0x80:
            print hex(current), GetDisasm(current)
            found = True
    if found:
        print '*** No manually added interrupt found'


main()

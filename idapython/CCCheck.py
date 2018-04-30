import idautils
import idaapi


def main():
    print '--------------- CCCheck ---------------'

    current = MinEA()
    end = MaxEA()
    found = False

    while current < end: 
        current = FindBinary(current, SEARCH_DOWN|SEARCH_NEXT, 'CC')
        if current != BADADDR and SegName(current) == '.text': 
            print hex(current), GetDisasm(current)
            found = True

    if found: 
        print '*** No 0xCC byte found'


main()

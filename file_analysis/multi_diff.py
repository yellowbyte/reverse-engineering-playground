"""
Use it as commandline tool or import it as library
"""
import sys


class MultiDiff(object):
    """
    Class to do multiple binary files diff-ing
    """

    def __init__(self, binaries_data, desired_amount_same=1):
        self.desired_amount_same = desired_amount_same
        self.binaries_data = binaries_data
        self.__mutual_bytes = None
        self.__current_size = None
        self.__data = None

    @property
    def mutual_bytes(self):
        """
        Get mutual bytes across all the files
        """
        if (self.__mutual_bytes is not None) and (self.__data == self.binaries_data):
            # Previously have already calculated
            return self.__mutual_bytes
        self.__mutual_bytes = list()
        self.__current_size = 0
        self.__data = self.binaries_data

        read_from = self.__data[0]
        for i, current_index_bytes in enumerate(zip(*self.__data)):
            one_sample = current_index_bytes[0]
            # XOR-ing 2 same bytes will equal 0
            not_all_same = any(map(lambda x: x^one_sample, current_index_bytes[1:]))
            if not not_all_same: # mutual byte detected
                self.__current_size += 1
            else:
                if self.__current_size >= self.desired_amount_same:
                    start, end = (i-self.__current_size, i)
                    self.__mutual_bytes.append((start, read_from[start:end]))
                self.__current_size = 0
        return self.__mutual_bytes

    def add_binary(self, binary_data):
        """
        Add another binary to diff against
        """
        self.binaries_data += binary_data

    def pretty_print(self):
        """
        Output to stdout the mutual bytes in a human-friendly format
        """
        for offset, matched_bytes in self.mutual_bytes:
            _bytes = ''.join(format(x, '02x') for x in matched_bytes)
            print('0x{:x}: {}'.format(offset, _bytes))


if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print 'Need to specify at least 2 files'
    files = sys.argv[1:]
    files_contents = list()
    for f in files:
        with open(f, 'rb') as current_file:
            files_contents.append(bytearray(current_file.read()))
    bins_analysis = MultiDiff(files_contents)
    bins_analysis.pretty_print()

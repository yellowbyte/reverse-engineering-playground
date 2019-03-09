#!/usr/bin/env python2

from __future__ import division

import matplotlib.pyplot as plt

class FrequencyAnalysis:
    """
    Frequency analysis of bytes in a file
    """

    def __init__(self, _bytes):
        self.bytes = _bytes

    @property
    def distribution(self):
        analysis =  [0] * 256
        for b in bytearray(self.bytes):
            analysis[b] += 1
        return analysis

    def display_graph(self, exclude=list()):
        desired_distribution = self.distribution
        # Normalize distribution
        desired_distribution = map(lambda x:(x/max(desired_distribution))*100,
                                   desired_distribution)
        for b in exclude:
            desired_distribution[b] = 0
        plt.hist(range(256), 
                 bins=range(256), 
                 weights=desired_distribution, 
                 edgecolor='black')
        plt.show()

    def display_text(self, num=3):
        print('Top '+str(num)+' Highest Frequency Bytes Are:')

        distribution = self.distribution
        tops = sorted(list(enumerate(distribution)), 
                      key=lambda x:x[1], 
                      reverse=True)[:num]
        for b in tops:
            print('0x{:x}: {}'.format(b[0],b[1]))
        return sorted(self.distribution, reverse=True)[:num]


if __name__ == '__main__':
    filepath = raw_input('Path To File: ')
    with open(filepath, 'rb') as f:
        _bin = f.read()
    file_analysis = FrequencyAnalysis(_bin)
    file_analysis.display_text(5)
    file_analysis.display_graph()

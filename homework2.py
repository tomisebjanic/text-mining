from unidecode import unidecode
from collections import Counter
import re
from itertools import combinations
import sklearn.cluster as cl
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from numpy import dot
from sklearn.metrics.pairwise import cosine_similarity
from scipy.cluster.hierarchy import ward, dendrogram, complete, average
import matplotlib.pyplot as plt


__author__ = 'tomisebjanic'


class TextMining:
    linkages = {"min": min, "max": max}
    def __init__(self):
        # self.languages = ['grk', 'por', 'fin', 'hng', 'chn', 'jpn', 'eng', 'ger', 'slo', 'slv', 'czc', 'dns', 'dut', 'blg', 'rus', 'ruw', 'swd', 'nrn']
        self.languages = ['grk', 'por', 'fin', 'hng', 'chn', 'jpn', 'eng', 'ger', 'slo', 'slv', 'czc']
        self.k = 2
        self.docs = {}  # holds numbers of occurencies of n-grams in text
        self.ngrams = {} # holds n-grams
        self.vector_distances = {}  # holds vector distances for each language
        self.data = {}
        # self.clusters = [[i] for i in self.languages]
        self.clusters = [[i] for i in range(len(self.languages))]
        self.linkage = self.linkages["max"]
        for lan in self.languages:
            self.docs[lan] = self.parse_file('ready/'+lan+'.txt')

        for i in self.docs:
            self.data[i] = Counter(self.generate_ngrams(self.docs[i]))
            self.ngrams[i] = list(Counter(self.generate_ngrams(self.docs[i])))
            self.docs[i] = list(Counter(self.generate_ngrams(self.docs[i])).values())

        for i in self.docs:
            self.docs[i] = list(map(float, self.docs[i]))

        self.vector_distances = {lan: (sum(vi**2 for vi in self.docs[lan]))**0.5 for lan in self.docs}

    def flatten_list(self, lst):
        return [item for sublist in lst for item in sublist]

    def parse_file(self, file_name):
        f = open(file_name, encoding='utf-8').read()
        return re.sub("\s\s+", " ", unidecode(f.replace("\n", " ").replace("\r", "").replace("\t", "").lower()))

    def generate_ngrams(self, xs):
        for i in range(len(xs)-(self.k-1)):
            yield xs[i:i+self.k]

    def flatten(self, lst):
        i=0
        while i<len(lst):
            while True:
                try:
                    lst[i:i+1] = lst[i]
                except (TypeError, IndexError):
                    break
            i += 1
        return lst

    def dot_produkt(self, x, y):
        return sum(v1*y.get(k1, 0) for k1, v1, in x.items())

    # Row distance (or whatever)
    def cos_dist(self, lan1, lan2):
        return 1 - (self.dot_produkt(self.data[self.languages[lan1]], self.data[self.languages[lan2]]) / (self.vector_distances[self.languages[lan1]] * self.vector_distances[self.languages[lan2]]))

    def cluster_distance(self, c1, c2):
        return self.linkage(self.cos_dist(e1, e2) for e1 in self.flatten(c1) for e2 in self.flatten(c2))

    def closest_clusters(self):
        return min((self.cluster_distance(*c), c) for c in combinations(self.clusters, 2))

    def do_mining(self):
        Z = []
        while len(self.clusters) > 1:
            dist, clusters = self.closest_clusters()
            # new_cluster = [clusters[0], clusters[1]]
            Z.append([self.clusters.index(clusters[0]), self.clusters.index(clusters[1]), dist, len(self.flatten([clusters[0], clusters[1]]))])
            del self.clusters[self.clusters.index(clusters[0])]
            del self.clusters[self.clusters.index(clusters[1])]
            self.clusters.append([clusters[0], clusters[1]])
            print(dist, [clusters[0], clusters[1]])


        dendrogram(Z)
        plt.show()



        # Z = [[0, 4, 0.015, 2],
        #     [1, 2, 0.1, 2],
        #     [3, 5, 0.2, 3],
        #     [6, 7, 0.4, 7]]
        # dendrogram(Z)
        #
        # plt.show()
        # print(0)
        # exit(0)




def flat(lst):
    i=0
    while i<len(lst):
        while True:
            try:
                lst[i:i+1] = lst[i]
            except (TypeError, IndexError):
                break
        i += 1
    return lst

# print(flat([1,[2],3]))


tm = TextMining()
tm.do_mining()
# print(tm.closest_clusters())

filenames = ['ready/eng.txt',
             'ready/ger.txt',
             'ready/slo.txt',
             'ready/slv.txt',
             'ready/czc.txt',
             'ready/dns.txt',
             'ready/dut.txt',
             'ready/blg.txt',
             'ready/src1.txt',
             'ready/src3.txt',
             'ready/rus.txt',
             'ready/ruw.txt',
             'ready/swd.txt',
             'ready/nrn.txt',
             'ready/grk.txt',
             'ready/por.txt',
             'ready/fin.txt',
             'ready/hng.txt',
             'ready/chn.txt',
             'ready/jpn.txt']

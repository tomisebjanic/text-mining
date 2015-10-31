from unidecode import unidecode
from collections import Counter
import re
from itertools import combinations
from scipy.cluster.hierarchy import dendrogram
import matplotlib.pyplot as plt


__author__ = 'tomisebjanic'


class TextMining:
    linkages = {"min": min, "max": max}

    def __init__(self):
        # self.languages = ['grk', 'por', 'fin', 'hng', 'chn', 'jpn', 'eng', 'ger', 'slo', 'slv', 'czc', 'dns', 'dut', 'blg', 'rus', 'ruw', 'swd', 'nrn']
        self.languages = ['grk', 'por', 'fin', 'hng', 'chn', 'jpn', 'eng', 'ger', 'slo', 'slv', 'czc']
        self.k = 2
        self.docs, self.data = {}, {}
        self.clusters = [[i] for i in range(len(self.languages))]
        self.clusters_copy = [[i] for i in range(len(self.languages))]
        self.linkage = self.linkages["max"]
        self.docs = {lan: self.parse_file('ready/'+lan+'.txt') for lan in self.languages}
        for i in self.docs:
            self.data[i] = Counter(self.generate_ngrams(self.docs[i]))
            self.docs[i] = list(map(float, Counter(self.generate_ngrams(self.docs[i])).values()))
        self.vector_distances = {lan: (sum(vi**2 for vi in self.docs[lan]))**0.5 for lan in self.docs}

    def parse_file(self, file_name):
        f = open(file_name, encoding='utf-8').read()
        return re.sub("\s\s+", " ", unidecode(f.replace("\n", " ").replace("\r", "").replace("\t", "").lower()))

    def generate_ngrams(self, xs):
        for i in range(len(xs)-(self.k-1)):
            yield xs[i:i+self.k]

    def flatten(self, lst):
        new_list = []
        for item in lst:
            if isinstance(item, list):
                new_list.extend(self.flatten(item))
            else:
                new_list.append(item)
        return new_list

    def dot_produkt(self, x, y):
        return sum(v1*y.get(k1, 0) for k1, v1, in x.items())

    def cos_dist(self, lan1, lan2):
        return 1 - (self.dot_produkt(self.data[self.languages[lan1]], self.data[self.languages[lan2]]) / (self.vector_distances[self.languages[lan1]] * self.vector_distances[self.languages[lan2]]))

    def cluster_distance(self, c1, c2):
        return self.linkage(self.cos_dist(e1, e2) for e1 in self.flatten(c1) for e2 in self.flatten(c2))

    def closest_clusters(self):
        return min((self.cluster_distance(*c), c) for c in combinations(self.clusters, 2))

    def do_mining(self):
        z = []
        while len(self.clusters) > 1:
            dist, cl = self.closest_clusters()
            z.append([self.clusters_copy.index(cl[0]), self.clusters_copy.index(cl[1]), dist, len(self.flatten(list(cl)))])
            del self.clusters[self.clusters.index(cl[0])]
            del self.clusters[self.clusters.index(cl[1])]
            self.clusters.append(list(cl))
            self.clusters_copy.append(list(cl))
            print(dist, cl)

        dendrogram(z, labels=self.languages, orientation='right', distance_sort='ascending')
        plt.show()


tm = TextMining()
tm.do_mining()

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
        self.languages = ['grk', 'por', 'fin', 'hng', 'chn', 'jpn', 'eng', 'ger', 'slo', 'slv', 'czc', 'dns', 'dut', 'blg', 'rus', 'ruw', 'swd', 'nrn', 'mkj', 'spn', 'src4', 'src5', 'itn']
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
        return sum(vx*y.get(kx, 0) for kx, vx, in x.items())

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

        dendrogram(z, labels=self.languages, orientation='top', distance_sort='ascending')
        plt.xlabel('Cluster Distances')
        plt.ylabel('Languages')
        plt.title('Language Similarity')
        plt.show()

    def recognize_language(self, file):
        article = Counter(self.generate_ngrams(self.parse_file(file)))
        article_distance = (sum(vi**2 for vi in list(map(float, Counter(article).values()))))**0.5
        distances = {lan: 1 - ((self.dot_produkt(self.data[lan], article)) / (self.vector_distances[lan] * article_distance)) for lan in self.data}
        print('File', file, 'is in', min(distances, key=distances.get), 'language.')




tm = TextMining()
# tm.do_mining()
tm.recognize_language('articles/slv.txt')
tm.recognize_language('articles/eng.txt')
tm.recognize_language('articles/ger.txt')
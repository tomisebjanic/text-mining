from itertools import combinations

avg = lambda lst: sum(list(lst))/len(list(lst))


class Clustering:
    linkages = {"min": min, "max": max, "average": avg}

    def __init__(self, file_name, linkage="max"):
        """Read data from file."""
        # print("Opening", file_name)
        f = open(file_name)
        self.header = f.readline().strip().split("\t")[1:]
        self.data = []
        self.ids = []
        for line in f:
            row = line.strip().split("\t")
            self.ids.append(row[0])
            self.data.append([None if (x == "?" or not len(x)) else float(x)
                              for x in row[1:]])
        self.clusters = [[i] for i in range(len(self.data))]
        self.linkage = self.linkages[linkage]

    def row_distance(self, r1, r2):
        """Distance between rows with indices r1 and r2."""
        return (sum((x-y)**2 for x, y in zip(self.data[r1], self.data[r2])))**0.5

    def cluster_distance(self, c1, c2):
        # c1, c2 = list of clusters
        """Distance between two clusters."""
        # to znamo, uporabimo self.linkage (1 vrstica)
        return self.linkage(self.row_distance(e1, e2) for e1 in c1 for e2 in c2)

    def closest_clusters(self):
        """Return two closest clusters."""
        # to tudi znamo (1 vrstica), nekaj podobnega temu spodaj
        return min((self.cluster_distance(*c), c) for c in combinations(self.clusters, 2))


    def run(self):
        """Perform hierarchical clustering."""
        joining = []
        while len(self.clusters) > 2:
            # naredimo nekaj z self.clusters
            # recimo, kličemo clusest_clusters
            # dodamo k joining
            dist, clusters = self.closest_clusters()
            # print(dist, clusters)
            joining = [clusters[0], clusters[1]]
            # del self.clusters[clusters[0][0]]
            # del self.clusters[clusters[1][0]-1]
            self.clusters = [x for x in self.clusters if x not in clusters] + [joining[0] + joining[1]]
            # potem pa:
            # si zapomnemo (v en seznam) katera dve skupini smo združili
            # naredimo nov seznam, kjer sta ti dve skupini združeni
            # self.clusters postane seznam brez teh dveh posamičnih skupin ampak z novo skupino

            # recimo uporabim nekaj kot spodaj
            # [x for x in c if x not in pair] + [pair[0] + pair[1]]
        print(0)

hc = Clustering("grades.txt")
hc.run()
print(hc.clusters)
# print(hc.row_distance(0, 1))
# print(hc.cluster_distance([0], [1]))
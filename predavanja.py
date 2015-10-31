#simpl 20min.

from collections import Counter


s = "Perica reze raci rep in se rezi perotu" 

#radi bi meli generator ki bo vracal terke
def kmers(xs, k=2):
	for i in range(len(xs)-(k-1)):
		yield xs[i:i+k]

print(Counter(kmers(s)))

# .union pa te fore tuj obstajajo
# 



docs = {"jap" : [10, 0, 20, 0, 40], "slo" : [2,4,2,5,6]}

neka = { language: sqrt(sum(vi**2 for vi in docs[language])) for language in docs} #to mi naredi za vse dokumente

print(neka)

#p.values() # da frekvence iz countera
#
#dolzine ||x|| in ||y|| zracunaj samo 1x - v bistvi vse zracunaj samo 1x.
#
#nucaj unije (mnozice pa te fore)
#
#polek cos razdalje se uporablja tudi Jaccaro

def to_freq(s1):
	s = unidecode(s1.lower())
	return Counter("%s%s" % (s[i],s[i+1]) for i in range(len(s)-1))

def len_vektor(a):
	return sqrt(sum(x**2 for x in a.values()))

def dot_product(x,y):
	return sum(v1*y.get(k1,0) for k1,v1 in x.items())

def cos_dist(x,y):
	return dot_product(x,y) / (len_vektor(x) * len_vektor(y))
#simpl 20min.

from collections import Counter
from math import sqrt

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
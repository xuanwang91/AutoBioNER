import string
import numpy as np
from sklearn.cluster import KMeans
import sys
import os

corpusName = sys.argv[1]
folder = '../../data/'+corpusName+'/'

id2ent = dict()
with open(folder+'entity2id.txt') as fin:
	for line in fin:
		tokens = line.strip().split()
		id2ent[tokens[1]] = tokens[0]

enttypes = ['CHEMICAL', 'DISEASE']

for enttype in enttypes:
	ent2emb = dict()
	with open(folder+'entity_word2vec.emb') as fin:
		for line in fin:
			tokens = line.strip().split()
			if tokens[0] not in id2ent:
				continue
			ent = id2ent[tokens[0]]
			if not ent.startswith(enttype):
				continue
			ent2emb[ent] = np.array(tokens[1:])

	print(len(ent2emb))

	entlist = []
	emblist = []
	for ent in ent2emb:
		entlist.append(ent)
		emblist.append(ent2emb[ent])

	kmeans = KMeans(n_clusters=10, random_state=0).fit(np.array(emblist))

	seedlist = [[] for _ in range(10)]
	for ent, label in zip(entlist, kmeans.labels_):
		seedlist[int(label)].append(ent)

	try:
		os.mkdir(folder+enttype)
	except:
		pass

	for idx in range(10):
		with open(folder+enttype+'/seed'+str(idx)+'.txt', 'w') as fout:
			for ent in seedlist[idx]:
				fout.write(ent+'\n')
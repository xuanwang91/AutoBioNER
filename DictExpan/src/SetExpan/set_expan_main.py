import util
import set_expan
import time
import random
import os
from collections import defaultdict

## Setting global versions
FLAGS_USE_TYPE=True

## Loading Corpus
data = "bc5"
print('dataset:%s' % data)
folder = '../../data/'+data+'/'
start = time.time()
print('loading eid and name maps')
eid2ename, ename2eid = util.loadEidToEntityMap(folder+'entity2id.txt') #entity2id.txt
print('loading eid and skipgram maps')
eid2patterns, pattern2eids = util.loadFeaturesAndEidMap(folder+'eidSkipgramCounts.txt') #eidSkipgramCount.txt
print('loading skipgram strength map')
eidAndPattern2strength = util.loadWeightByEidAndFeatureMap(folder+'eidSkipgram2TFIDFStrength.txt', idx=-1) #(eid, feature, weight) file
if (FLAGS_USE_TYPE):
	print('loading eid and type maps')
	eid2types, type2eids = util.loadFeaturesAndEidMap(folder+'eidTypeCounts.txt') #eidTypeCount.txt
	print('loading type strength map')
	eidAndType2strength = util.loadWeightByEidAndFeatureMap(folder+'eidType2TFIDFStrength.txt', idx=-1) #(eid, feature, weight) file
end = time.time()
print("Finish loading all dataset, using %s seconds" % (end-start))

## Start set expansion
enttypes = ['CHEMICAL', 'DISEASE']

dict_core_expand = defaultdict(list)
dict_full_expand = []
with open(folder+'dict_core.txt', 'r') as f:
	for line in f:
		segments = line.strip().split('\t')
		dict_core_expand[segments[0].upper()].append(segments[1])

with open(folder+'dict_full.txt', 'r') as f:
	for line in f:
		dict_full_expand.append(line.strip())

for enttype in enttypes:
	try:
		os.mkdir(folder+enttype)
	except:
		pass
		
	for seedSetNo in range(10):
		print('===================Seed Set '+str(seedSetNo)+'===================')
		seeds = []
		MRR = dict()
		with open(folder+enttype+'/seed'+str(seedSetNo)+'.txt', 'r') as fin:
			for line in fin:
				token  = line.strip().lower()
				if token in ename2eid:
					seeds.append(token)
			num_iter = int(len(seeds)/5)
			if num_iter <= 1:
				continue
			for idx in range(num_iter):
				print('SEED_SAMPLE #'+str(idx))
				userInput = random.sample(seeds, 10)
				seedEidsWithConfidence = [(ename2eid[ele], 0.0) for ele in userInput]

				negativeSeedEids = set()
				for ele in eid2ename:
					if not eid2ename[ele].startswith('PHRASE_'):
						negativeSeedEids.add(ele)

				expandedEidsWithConfidence = set_expan.setExpan(
						seedEidsWithConfidence=seedEidsWithConfidence,
						negativeSeedEids=negativeSeedEids,
						eid2patterns=eid2patterns,
						pattern2eids=pattern2eids,
						eidAndPattern2strength=eidAndPattern2strength,
						eid2types=eid2types,
						type2eids=type2eids,
						eidAndType2strength=eidAndType2strength,
						eid2ename=eid2ename,
						FLAGS_VERBOSE=True,
						FLAGS_DEBUG=True
				)
				for idx, ele in enumerate(expandedEidsWithConfidence):
					if ele[0] not in MRR:
						MRR[ele[0]] = 0.0
					MRR[ele[0]] += 1/(idx+1)

			MRR_sorted = sorted(MRR.items(), key=lambda kv: kv[1], reverse=True)

			with open(folder+enttype+'/seed'+str(seedSetNo)+'.txt', 'w') as fout:
				for ele, mrr in MRR_sorted:
					fout.write(eid2ename[ele] + '\t' + str(mrr) + '\n')

	print('===================Generating Expanded Dictionary: '+enttype+'===================')
	for seed_file in os.listdir(folder+enttype):        
		with open(folder+enttype+'/'+seed_file, 'r') as f:
			for line in f:
				entity = ' '.join(line.strip().split('\t')[0].split('_')[1:])
				if len(entity)<3 or entity.isdigit():
					continue
				dict_core_expand[enttype].append(entity)
				dict_full_expand.append(entity)

print('===================Output Expanded Dictionaries===================')                
with open(folder+'dict_core_expand.txt', 'w') as f:
	for tp in dict_core_expand:
		for ent in dict_core_expand[tp]:
			f.write('\t'.join((tp,ent)))
			f.write('\n')
with open(folder+'dict_full_expand.txt', 'w') as f:
	for ent in dict_full_expand:
		f.write(ent)
		f.write('\n') 
        

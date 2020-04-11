import json
import sys
import string

corpusName = sys.argv[1]
file_path = "../../data/"+corpusName+"/"

typeset = ['CHEMICAL', 'DISEASE', 'PHRASE']
entityset = dict()
with open(file_path+'sentences.json.raw.tmp', 'r') as fin, open(file_path+'sentences.json', 'w') as fou1, open(file_path+'entity2id.txt', 'w') as fou2:
	for line in fin:
		js = json.loads(line)
		js['entityMentions'] = []
		for idx, token in enumerate(js['tokens']):
			for etype in typeset:
				if token.startswith(etype):
					if token not in entityset:
						entityset[token] = len(entityset)
					ent = dict()
					ent['text'] = token
					ent['start'] = idx
					ent['end'] = idx
					ent['type'] = 'phrase'
					ent['entityId'] = entityset[token]
					js['entityMentions'].append(ent)
		json.dump(js, fou1)
		fou1.write('\n')
	for entity in entityset:
		fou2.write(entity+'\t'+str(entityset[entity])+'\n')

import sys
import re

corpusName = sys.argv[1]
file_path = "../../data/"+corpusName+"/"

typeset = ['CHEMICAL', 'DISEASE', 'PHRASE']
sentence = []
phrase_flag = 0
with open(file_path+'input_text_matched.txt', 'r') as fin, open(file_path+'corpus.txt', 'w') as fout:
    for line in fin:
        if line == '\n':
            if sentence != []:
                sentence_new = []
                for token in ''.join(sentence).strip().split():
                    if token.split('_')[0] in typeset:
                        token_new = re.sub('[^0-9a-zA-Z]+', '_', token).strip('_')
                        sentence_new.append(token_new)
                    else:
                        sentence_new.append(token)
                fout.write(' '.join(sentence_new))
                fout.write('\n')
                sentence = []           
                phrase_flag = 0
            continue
            
        segments = line.strip().split()
        if segments[0] in ['<s>', '<eof>']:
            continue
        if segments[2] != 'None':
            if phrase_flag == 1:
                sentence[-1] = ' '+sentence[-1][1:]
                phrase_flag = 0
            if segments[1] == 'I':
                sentence.append(' '+segments[2].upper()+'_'+segments[0])
            else:
                sentence.append('_'+segments[0])
        else:
            if segments[3] == 'D':
                if phrase_flag == 0:
                    sentence.append(' '+'PHRASE_'+segments[0])
                    phrase_flag = 1
                else:
                    sentence.append('_'+segments[0])
            else:
                if phrase_flag == 1:
                    sentence[-1] = ' '+sentence[-1][1:]
                    phrase_flag = 0
                sentence.append(' '+segments[0])

#!/bin/bash
data=bc5
path=$(pwd)

echo ${green}===Corpus Formatting===${reset}
python3 corpusFormat.py $data

echo ${green}===Running Stanford CoreNLP Tool===${reset}
## Download stanford coreNLP toolkit to specified folder if it doesn't exist
if [ ! -d ../tools/CoreNLP/stanford-corenlp ]; then
	wget -O ../tools/CoreNLP/stanford-corenlp.zip http://nlp.stanford.edu/software/stanford-corenlp-full-2017-06-09.zip
	unzip ../tools/CoreNLP/stanford-corenlp.zip -d ../tools/CoreNLP/
	mv ../tools/CoreNLP/stanford-corenlp-full-2017-06-09/ ../tools/CoreNLP/stanford-corenlp/
	rm -f ../tools/CoreNLP/stanford-corenlp.zip
fi
python3 parseAutoPhraseOutput.py $data 1

python3 nerProc.py $data

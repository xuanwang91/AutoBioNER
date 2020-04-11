# Input: a tokenized corpus. e.g., data/bc5/input_text.txt; a core dictionary, e.g., data/bc5/dict_core.txt; a full dictionary, e.g., data/bc5/dict_full.txt
# Output: expanded dictionaries. e.g., data/bc5/dict_core_expand.txt, data/bc5/dict_core_full.txt

# Need to start CoreNLP
# Download the Stanford CoreNLP Toolkit to src/tools/CoreNLP/
# cd src/tools/CoreNLP/stanford-corenlp
# java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer

# need to change the corpus (data, RAW_TEXT, DICT_CORE, DICT_FULL) name in run.sh 
# need to change the corpus (data) name in src/corpusProcessing/corpusProcess.sh

#!/bin/bash
data=bc5
path=$(pwd)
RAW_TEXT="data/bc5/input_text.txt"
DICT_CORE="data/bc5/dict_core.txt"
DICT_FULL="data/bc5/dict_full.txt"
TRAINING_SET="data/bc5/input_text_matched.txt"

echo ${green}===Dictionary Matching===${reset}
bin/generate $RAW_TEXT $DICT_CORE $DICT_FULL $TRAINING_SET

cd src/corpusProcessing/
./corpusProcess.sh

cd ../dataProcessing/
./dataProcess.sh

cd ../SetExpan/
python3 set_expan_main.py

# Distantly Supervised Biomedical Named Entity Recognition with Dictionary Expansion

This project provides the **AutoBioNER** framework for distantly supervised biomedical named entity recognition (BioNER).

The whole framework consists of two parts: **Dictionary Expansion** and
**Neural Model Training**.

## Required Inputs
- Tokenized Raw Texts: e.g., DictExpan/data/bc5/input_text.txt
  - One token per line.
  - An empty line means the end of a sentence.
- Two Dictionaries
  - Core Dictionary w/ Type Info: e.g., DictExpan/data/bc5/dict_core.txt
    - Two columns (i.e., Type, Tokenized Surface) per line.
    - Tab separated.
    - How to obtain: from domain-specific dictionaries.
  - Full Dictionary w/o Type Info: e.g., DictExpan/data/bc5/dict_full.txt
    - One tokenized high-quality phrases per line.
    - How to obtain: from domain-specific dictionaries and high-quality phrase mining tool on domain-specific corpus (e.g., [AutoPhrase](https://github.com/shangjingbo1226/AutoPhrase))

## Dictionary Expansion
```
cd DictExpan/
```

### Start Stanford CoreNLP
```
# Download the Stanford CoreNLP Toolkit to src/tools/CoreNLP/
cd src/tools/CoreNLP/stanford-corenlp
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer
```

### Run Dictionary Expansion
```
# Need to change the corpus (data, RAW_TEXT, DICT_CORE, DICT_FULL) name in run.sh
# Need to change the corpus (data) name in src/corpusProcessing/corpusProcess.sh
# Need to change the corpus (data) name in src/dataProcessing/dataProcess.sh
# Need to change the corpus (data) name in src/SetExpan/set_expan_main.py
./run.sh
```

### Output
Two expanded dictionaries:
- Expanded core dictionary: e.g., DictExpan/data/bc5/dict_core_expand.txt
- Expanded full dictionary: e.g., DictExpan/data/bc5/dict_full_expand.txt


## Neural Model Training
After the **Dictionary Expansion** step, take the tokenized raw corpus (DictExpan/data/bc5/input_text.txt), expanded core dictionary (DictExpan/data/bc5/dict_core_expand.txt) and expanded full dictionary (DictExpan/data/bc5/dict_full_expand.txt) as the input to **AutoNER**.

The details of the **Neural Model Training** can be found in the [AutoNER](https://github.com/shangjingbo1226/AutoNER) repository.

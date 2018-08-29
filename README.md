# sentence similarity's README

## Tips：
stanford-parser-python中的my_main_parser1来自水论文。 虽然LSA分分钟能秒杀它,但是还是可以用来处理sentence similarity:)
you can adjust these parameters or you can combine the two scores

## how to get the similarity
(based on the special Corpus (from msr para))
1. get the first score, look at semantic-lsa/lsa_parser.py
2. get the second score, look at my_main_parser1.py

## install

1. install python, pip
2. install jpype, nltk (download all data), gensim and so on...
3. modify file 'parser.py' 
	stanford_parser_home = 'your file location'

## semantic-lsa/lsa_parser.py
Based on LSA

## stanfor-parser-python/src/stanford_parser/my_main_parser1.py

"sentence similarity" use the formation of 'objects-specified(NN)' and 'objects-property(JJ, RB)' and 'object-behavior(VB)'.

1. use the stanford parse, get the sentence's structure
2. get sentence's specified objects
2.1 get 'NN' list as feature1
2.2 get 'JJ RB' list as feature2
2.3 get 'VB' list as feature3
2.4 set coefficients and combine feature1, feature2, feature3 and get feature4
3. set threshold and start testing......

## how to use
look at readme

# Thx

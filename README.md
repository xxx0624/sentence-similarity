#sentence similarity's README

##install

1. install python, pip
2. install jpype, nltk (download all data)
3. modify file 'parser.py' 
	stanford_parser_home = 'your file location'

## the algorithm details

"sentence similarity" use the formation of 'objects-specified(NN)' and 'objects-property(JJ, RB)' and 'object-behavior(VB)'.

1. use the stanford parse, get the sentence's structure
2. get sentence's specified objects
2.1 get 'NN' list as feature1
2.2 get 'JJ RB' list as feature2
2.3 get 'VB' list as feature3
2.4 set coefficients and combine feature1, feature2, feature3 and get feature4
3. set threshold and start testing......

## how to use

please look at stanford-parser-python-r22186/src/stanford_parser/my_main_parser.py
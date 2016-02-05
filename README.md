#sentence similarity's README

##install

(refer to stanford-parser-python-r22186's README)

We developed a python interface to the Stanford Parser.  It uses JPype
to create a Java virtual machine and convert between python and Java.
Most of the code is about getting the Stanford Dependencies, but it's
easy to add API to call any method on the parser.

JPype is included; you can set compile it by running "rake setup" in
3rdParty/jpype.  The Stanford Parser can be downloaded and installed
by running "rake download; rake setup" in 3rdParty/stanford-parser".
Otherwise set the environment variable STANFORD_PARSER_HOME to the
location of the installed directory.  It loads the grammar file from
the unzipped version, because the load is a few seconds faster.  If
you haven't gunzipped the .ser file you will get an error.

To see how to use it, look at parser_test.py.

## the details

"sentence similarity" use the formation of 'objects-specified(NN)' and 'objects-property(JJ, RB)' and 'object-behavior(VB)'.

1. use the stanford parse, get the sentence's structure
2. get sentence's specified objects
2.1 get 'NN' list as feature1
2.2 get 'JJ RB' list as feature2
2.3 get 'VB' list as feature3
2.4 set coefficients and combine feature1, feature2, feature3 and get feature4
3. set threshold and start testing......

## how to use

please look at stanford-parser-python-r22186/src/stanford_parser/test_parser.py

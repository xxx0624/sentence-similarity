#Tips:
1. 3 features: NN(object-specified), JJ & RB(object-property), VB(object-behavior)
2. combine these features: a*score(NN) + b*score(JJ&RB) + c*score(VB)
3. set a threshold and if the last score is larger than the threshold, it is true otherwise false.
<<<<<<< HEAD
4. set the path of line 81 in parser.py
=======
>>>>>>> 9bb1cbbc65add14411e9a27d65862c2547014e1f

##Results:
a	b	c	threshold	percision(msr-train)

0.6	0.2	0.2	0.1			66.6753

0.3	0.1	0.6	0.1			68.3984

0.2	0.2	0.6	0.1			67.9449

0.1	0.3	0.6	0.1			67.6126

0.5	0.3	0.2	0.1			64.9666

<<<<<<< HEAD
0.5	0.2	0.3	0.1			66.6055
=======
0.5	0.2	0.3	0.1			66.6055
>>>>>>> 9bb1cbbc65add14411e9a27d65862c2547014e1f

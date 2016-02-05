#coding:utf-8

from __future__ import division
from parser import Parser
import logging
from nltk.corpus import wordnet as wn
from math import e as mathe
import codecs, sys

reload(sys)
sys.setdefaultencoding('utf-8')


class myParser(object):

	'''
	rtype: dict
		{'dog':'NN', ...}
	'''
	def parser(self, sentence):
		if sentence == "":
			logging.warning('your sentence \"' + sentence + "\"" + 'is empty!')
			return None
		stand = Parser()
		#sentence = "the girl I met was your sister. and these dogs are very happy. those cats and food is good and the rain is dont like it"
		standoffTokens, posTags = stand.parseToStanfordDependencies(sentence)

		parse_dict = {}
		for word, tag in zip(standoffTokens, posTags):
			parse_dict[word.text] = tag

		return parse_dict


class myWordNet(object):
	def __init__(self):
		self.none_lcs = "NONE_LCS"
		self.max_default = 10

	def logging_warning(self, content = ""):
		if content == "":
			logging.warning('the msg ' + '\"' + content + '\"' + 'is empty')

	#word = 'dogs'
	def get_min_depth_from_wordnet(self, word):
		self.logging_warning(content = word)
		word_synsets = wn.synsets(word)
		return word_synsets[0].min_depth()

	#word = 'dogs'
	def get_max_depth_from_wordnet(self, word):
		self.logging_warning(content = word)
		word_synsets = wn.synsets(word)
		return word_synsets[0].max_depth()

	#word1 = 'dogs'
	#word2 = 'cats'
	def get_lcs_from_wordnet(self, word1, word2):
		self.logging_warning(content = word1)
		self.logging_warning(content = word2)
		word1_synsets = wn.synsets(word1)
		word2_synsets = wn.synsets(word2)
		if len(word1_synsets) == 0 or len(word2_synsets) == 0:
			return self.none_lcs
		lcs = word1_synsets[0].lowest_common_hypernyms(word2_synsets[0])
		if len(lcs) == 0:
			return self.none_lcs
		else:
			return lcs[0]

	#word1 = 'dogs'
	#word2 = 'cats'
	def get_shortest_distance_from_wordnet(self, word1, word2):
		self.logging_warning(content = word1)
		self.logging_warning(content = word2)
		word1_synsets = wn.synsets(word1)
		word2_synsets = wn.synsets(word2)
		if len(word1_synsets) == 0 or len(word2_synsets) == 0:
			dis = self.max_default
			return dis
		dis = word1_synsets[0].shortest_path_distance(word2_synsets[0])
		return dis

class Analysis(object):
	def __init__(self):
		self.alpha = 0.25
		self.beta = 0.25
		self.max_default = 10

	#word1 = 'dogs'
	#word2 = 'cats'
	def cal_w1_w2_similar(self, word1, word2):
		my_wordnet = myWordNet()
		dis = my_wordnet.get_shortest_distance_from_wordnet(word1, word2)
		if dis == None:
			dis = self.max_default
		lcs = my_wordnet.get_lcs_from_wordnet(word1, word2)
		lcs_depth = 0
		if isinstance(lcs, str):
			lcs_depth = 0
		else:
			lcs_depth = lcs.min_depth()
			#word1 = cats
			#word2 = cat
			if wn.synsets(word1)[0].lemma_names()[0] == wn.synsets(word2)[0].lemma_names()[0]:
				lcs_depth = 1
		ans = (mathe**(self.alpha*lcs_depth) - 1.0) / (mathe**(self.alpha*dis) + mathe**(self.beta*lcs_depth) - 2)
		return ans

	'''
	word = 'dogs'
	word_list = ['this', 'is',...]
	return the max simiarity
	'''
	def cal_word_wordlist_maxsimilar(self, word, word_list):
		max_simi = 0
		for i in word_list:
			max_simi = max(max_simi, self.cal_w1_w2_similar(word, i))
		return max_simi

	'''
	my_dict = {'cats':'NN', ...}
	tag = 'NN'
	return these items that value contains the tag in the dict
	'''
	def get_tag(self, my_dict, tag):
		tag_list = []
		for item in my_dict:
			if tag in my_dict[item]:
				tag_list.append(item)
		return tag_list

	def union_all(self, list1, list2):
		mp = {}
		ans_list = []
		for li in list1:
			if li in mp:
				pass
			else:
				ans_list.append(li)
				mp[li] = 1
		for li in list2:
			if li in mp:
				pass
			else:
				ans_list.append(li)
				mp[li] = 1
		return ans_list

	'''
	== param ==
	all_words = ['this', 'is', 'a', 'cat']
	word_list1 = ['this', 'a']
	word_list2 = ['is', 'cat']

	== return word_list1's vector==
	[1, x, y, 1]
	'''
	def get_vector(self, all_words, word_list1, word_list2):
		vector_list = []
		mp = {}
		for item in word_list1:
			if item not in mp:
				mp[item] = 1
		for item in all_words:
			if item in mp:
				vector_list.append(1.0)
			else:
				simi = self.cal_word_wordlist_maxsimilar(item, word_list1)
				vector_list.append(simi)
		return vector_list

	def get_2sentence_vector_tag(self, sentence1,sentence2, tag_list):
		my_parser = myParser()
		analysis = Analysis()
		dict_1 = my_parser.parser(sentence1)
		dict_2 = my_parser.parser(sentence2)

		tag_word_1 = []
		for tag in tag_list:
			tag_word_1 = tag_word_1 + analysis.get_tag(dict_1, tag)
		tag_word_2 = []
		for tag in tag_list:
			tag_word_2 = tag_word_2 + analysis.get_tag(dict_2, tag)
		tag_word_all = analysis.union_all(tag_word_1, tag_word_2)

		#vector = [1, 0.1, ...]
		vector_1 = analysis.get_vector(tag_word_all, tag_word_1, tag_word_2)
		vector_2 = analysis.get_vector(tag_word_all, tag_word_2, tag_word_1)
		return vector_1, vector_2

class myMath(object):

	def __init__(self):
		self.eps = 1e-8
	
	def my_cos(self, v1, v2):
		if len(v1) != len(v2):
			logging.warning('the two vectors\' len are not the same!(return eps)')
			return self.eps
		up = 0
		sum1 = 0
		sum2 = 0
		for i in range(len(v1)):
			up += v1[i] * v2[i]
			sum1 += v1[i]*v1[i]
			sum2 += v2[i]*v2[i]
		if sum1 * sum2 == 0:
			logging.warning('the two vectors\' sum is 0!(reset to eps)')
			sum1 = 1.0
			sum2 = self.eps
		#print 'up:', up, ' sum1:', sum1, ' sum2:', sum2
		return up / (sum1*sum2)

	def combine_3feature(self, feature1, feature2, feature3, a, b, c):
		return a * feature1 + b * feature2 + c * feature3

	def final_judge(self, score, threshold):
		if score > threshold:
			return True
		else:
			return False


def pre_solve(sentence):
	return sentence.replace(unicode('’', 'utf-8'), '\'')


def solve(sentence1, sentence2, a, b, c, threshold):
	#sentence1 = 'this cats are very cute.'
	#sentence2 = 'that cat is very beautiful.'
	analysis = Analysis()
	#nn: object-specified
	#jj rb: object-property
	#vb: object-behavior
	v_os_1, v_os_2 = analysis.get_2sentence_vector_tag(sentence1, sentence2, ['NN'])
	#print 'object-specified:', v_os_1, v_os_2
	v_op_1, v_op_2 = analysis.get_2sentence_vector_tag(sentence1, sentence2, ['JJ', 'RB'])
	#print 'object-property:', v_op_1, v_op_2
	v_ob_1, v_ob_2 = analysis.get_2sentence_vector_tag(sentence1, sentence2, ['VB'])
	#print 'object-behavior:', v_ob_1, v_ob_2

	res = myMath()
	#feature1
	sim_os = res.my_cos(v_os_1, v_os_2)
	#feature2
	sim_op = res.my_cos(v_op_1, v_op_2)
	#feature3
	sim_ob = res.my_cos(v_ob_1, v_ob_2)
	#overall feature
	sim_overall = res.combine_3feature(sim_os, sim_op, sim_ob, a, b, c)
	#print sim_os, sim_op, sim_ob, sim_overall

	if res.final_judge(sim_overall, threshold):
		return "1"
	else:
		return "0"

		

class main_parser(object):

	def main_solve(self, a, b, c, threshold, file_name):
		yes_cnt = 0
		all_cnt = 0
		fopen = codecs.open('../../../Corpus/'+file_name, 'r')
		try:
			line = fopen.readline()
			line = fopen.readline()
			while line :
				#start ...
				print yes_cnt+1, '/', 1+all_cnt, ' = ', (yes_cnt+1)*1.0/(1+all_cnt)
				parts = line.strip().split('	')
				label = parts[0].strip()
				sentence1 = parts[3].strip()
				#sentence1 = 'Sixteen days later, as superheated air from the shuttle\'s reentry rushed into the damaged wing, "there was no possibility for crew survival,\" the board said.'
				sentence1 = pre_solve(sentence1)
				sentence2 = parts[4].strip()
				#sentence2 = 'Sixteen days later, as superheated air from the shuttle’s re-entry rushed into the damaged wing, ‘‘there was no possibility for crew survival,’’ the board said.'
				sentence2 = pre_solve(sentence2)
				solve_label = solve(sentence1, sentence2, a, b, c, threshold)
				if solve_label == label:
					yes_cnt += 1
				all_cnt += 1
				#end...
				line = fopen.readline()
				#break
		finally:
			fopen.close()
		
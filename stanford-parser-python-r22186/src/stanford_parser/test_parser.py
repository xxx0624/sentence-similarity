from __future__ import division
from parser import Parser
import logging
from nltk.corpus import wordnet as wn
from math import e as mathe


class myParser(object):

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

	def logging_warning(self, content = ""):
		if content == "":
			logging.warning('the msg ' + '\"' + content + '\"' + 'is empty')

	def get_min_depth_from_wordnet(self, word):
		self.logging_warning(content = word)
		word_synsets = wn.synsets(word)
		return word_synsets[0].min_depth()

	def get_max_depth_from_wordnet(self, word):
		self.logging_warning(content = word)
		word_synsets = wn.synsets(word)
		return word_synsets[0].max_depth()

	def get_lcs_from_wordnet(self, word1, word2):
		self.logging_warning(content = word1)
		self.logging_warning(content = word2)
		word1_synsets = wn.synsets(word1)
		word2_synsets = wn.synsets(word2)
		return word1_synsets[0].lowest_common_hypernyms(word2_synsets[0])[0]

	def get_shortest_distance_from_wordnet(self, word1, word2):
		self.logging_warning(content = word1)
		self.logging_warning(content = word2)
		word1_synsets = wn.synsets(word1)
		word2_synsets = wn.synsets(word2)
		dis = word1_synsets[0].shortest_path_distance(word2_synsets[0])
		return dis

class Analysis(object):
	def __init__(self):
		self.alpha = 0.25
		self.beta = 0.25

	def cal_w1_w2_similar(self, word1, word2):
		my_wordnet = myWordNet()
		dis = my_wordnet.get_shortest_distance_from_wordnet(word1, word2)
		lcs = my_wordnet.get_lcs_from_wordnet(word1, word2)
		lcs_depth = lcs.min_depth()
		ans = (mathe**(self.alpha*dis) - 1.0) / (mathe**(self.alpha*dis) + mathe**(self.beta*lcs_depth) - 2)
		return ans

	def cal_word_wordlist_maxsimilar(self, word, word_list):
		max_simi = 0
		for i in word_list:
			max_simi = max(max_simi, self.cal_w1_w2_similar(word, i))
		return max_simi

	def get_tag(self, dict1, tag):
		nn_list = []
		for item in dict1:
			if tag in dict1[item]:
				nn_list.append(item)
		return nn_list

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




if __name__ == '__main__':
	sentence1 = 'this cats are very cute.'
	sentence2 = 'i like these dogs.'
	my_parser = myParser()
	analysis = Analysis()
	dict_1 = my_parser.parser(sentence1)
	nn_1 = analysis.get_tag(dict_1, 'NN')
	jj_rb_1 = analysis.get_tag(dict_1, 'JJ') + analysis.get_tag(dict_1, 'RB')
	vb_1 = analysis.get_tag(dict_1, 'VB')

	dict_2 = my_parser.parser(sentence2)
	nn_2 = analysis.get_tag(dict_2, 'NN')
	jj_rb_2 = analysis.get_tag(dict_2, 'JJ') + analysis.get_tag(dict_2, 'RB')
	vb_2 = analysis.get_tag(dict_2, 'VB')

	#nn-all = ['cats', 'dogs']
	nn_all = analysis.union_all(nn_1, nn_2)
	jj_rb_all = analysis.union_all(jj_rb_1, jj_rb_2)
	vb_all = analysis.union_all(vb_1, vb_2)
	#print nn_all

	#vector = [1, 0.1, ...]
	vector_nn1 = analysis.get_vector(nn_all, nn_1, nn_2)
	vector_nn2 = analysis.get_vector(nn_all, nn_2, nn_1)
	vector_jj_rb1 = analysis.get_vector(jj_rb_all, jj_rb_1, jj_rb_2)
	vector_jj_rb2 = analysis.get_vector(jj_rb_all, jj_rb_2, jj_rb_1)
	vector_vb1 = analysis.get_vector(vb_all, vb_1, vb_2)
	vector_vb2 = analysis.get_vector(vb_all, vb_2, vb_1)
	print vector_nn1
	print vector_nn1

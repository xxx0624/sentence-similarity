from __future__ import division
from parser import Parser
import logging
from nltk.corpus import wordnet as wn
from math import e as mathe


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
		return word1_synsets[0].lowest_common_hypernyms(word2_synsets[0])[0]

	#word1 = 'dogs'
	#word2 = 'cats'
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

	#word1 = 'dogs'
	#word2 = 'cats'
	def cal_w1_w2_similar(self, word1, word2):
		my_wordnet = myWordNet()
		dis = my_wordnet.get_shortest_distance_from_wordnet(word1, word2)
		lcs = my_wordnet.get_lcs_from_wordnet(word1, word2)
		lcs_depth = lcs.min_depth()
		ans = (mathe**(self.alpha*dis) - 1.0) / (mathe**(self.alpha*dis) + mathe**(self.beta*lcs_depth) - 2)
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


if __name__ == '__main__':
	sentence1 = 'this cats are very cute.'
	sentence2 = 'i like these dogs.'
	analysis = Analysis()
	print analysis.get_2sentence_vector_tag(sentence1, sentence2, ['NN'])
	print analysis.get_2sentence_vector_tag(sentence1, sentence2, ['JJ', 'RB'])
	print analysis.get_2sentence_vector_tag(sentence1, sentence2, ['VB'])
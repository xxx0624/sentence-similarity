#coding:utf-8
from __future__ import division
from gensim import corpora, models, similarities
from porter_stemer import PorterStemmer
import os
import codecs
import sys


reload(sys)
sys.setdefaultencoding('utf-8')


class LSA(object):
	
	stemmer = None
	stopwords = []
	
	def __init__(self):
		self.stemmer = PorterStemmer()
		self.STOP_WORDS_FILE = '%s/../Data/english.stop' %  os.path.dirname(os.path.realpath(__file__))
		with codecs.open(self.STOP_WORDS_FILE, 'r') as f:
			self.stopwords = f.read().split()

	def remove_stop_wrods(self, word_list):
		return [word for word in word_list if word not in self.stopwords]

	def _pre_solve_1(self, sentence):
		sentence = sentence.replace(unicode('’', 'utf-8'), '\'')
		return sentence.lower()

	def _pre_solve_stemmer(self, sentence):
		words_list = []
		for w in sentence.split(' '):
			words_list.append(self.stemmer.stem(w, 0, len(w)-1))
		return ' '.join(words_list)

	def _pre_solve_filter_stopwords(self, sentence):
		word_list = sentence.split(' ')
		return ' '.join(self.remove_stop_wrods(word_list))

	def pre_solve(self, sentence):
		sentence = self._pre_solve_1(sentence)
		sentence = self._pre_solve_stemmer(sentence)
		return self._pre_solve_filter_stopwords(sentence)

	def get_documents(self, file_path):
		documents = []
		documents_words = []
		line_num = 0
		with codecs.open(file_path, 'r') as fopen:
			fopen.readline()
			line_num += 1
			while fopen:
				line = fopen.readline()
				#print 'line_num:', line_num
				line_num += 1
				if len(line) == 0:
					break
				line = line.strip().split('	')
				#print 'line[3] = ', line[3]
				#pre solve
				sentence = self.pre_solve(line[3])
				documents_words.append(sentence.split(' '))
				documents.append(sentence)
		return documents, documents_words

	def main(self, query, target_id, sorurce_file_path, documents, documents_words, num_topics=20):
		#documents, documents_words = self.get_documents(sorurce_file_path)
		dictionary = corpora.Dictionary(documents_words)
		corpus = [dictionary.doc2bow(documents_word) for documents_word in documents_words]
		tfidf = models.TfidfModel(corpus)
		corpus_tfidf = tfidf[corpus]

		lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=num_topics)
		corpus_lsi = lsi[corpus_tfidf]
		index = similarities.MatrixSimilarity(lsi[corpus])
		query = self.pre_solve(query)
		query_word_list = query.split(' ')
		query_bow = dictionary.doc2bow(query_word_list)
		query_lsi = lsi[query_bow]

		sims = list(index[query_lsi])
		#print 'sims[', target_id, ']=', sims[target_id]
		return sims[target_id]


if __name__ == '__main__':
	lsa = LSA()
	sorurce_file_path = '%s/../Corpus/msr_paraphrase_train.txt' %  os.path.dirname(os.path.realpath(__file__))
	target_id = 0
	documents, documents_words = lsa.get_documents(sorurce_file_path)
	yes_cnt = 0
	all_cnt = 0
	threshold = 0.5
	with codecs.open(sorurce_file_path) as f:
		f.readline()
		while f:
			line = f.readline()
			if len(line) == 0:
				break
			line = line.split('	')
			sentence = line[4].strip()
			score = lsa.main(sentence, target_id, sorurce_file_path, documents, documents_words, num_topics=20)
			target_id += 1
			if score >= threshold:
				yes_cnt += 1
			all_cnt += 1
			print  yes_cnt,'/', all_cnt, "; rate = ", yes_cnt*1.0 / all_cnt

from porter_stemer import PorterStemmer
words = 'it\'s those dogs i liked'
stem = PorterStemmer()
print stem.stem(words, 0, len(words)-1)


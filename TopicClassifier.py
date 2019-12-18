import spacy
import nltk
import xml.etree.ElementTree as ET
import os
import random
from gensim import corpora
import gensim
import pickle
basepath = 'papers_to_index/'
NUM_TOPICS = 15
spacy.load('en')
from spacy.lang.en import English
parser = English()

def tokenize(text):
	lda_tokens = []
	tokens = parser(text)
	for token in tokens:
		if token.orth_.isspace():
			continue
		elif token.like_url:
			lda_tokens.append('URL')
		elif token.orth_.startswith('\\x'):
			continue
		else:
			lda_tokens.append(token.lower_)
	return lda_tokens


from nltk.corpus import wordnet as wn
def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma
    
from nltk.stem.wordnet import WordNetLemmatizer
def get_lemma2(word):
	return WordNetLemmatizer().lemmatize(word)

nltk.download('stopwords')
en_stop = set(nltk.corpus.stopwords.words('english'))

def prepare_text_for_lda(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [get_lemma(token) for token in tokens]
    return tokens

def main():
	text_data = []
	for entry in os.listdir(basepath):
		with open(basepath+entry, encoding="ISO-8859-1") as f:
			# first_line = f.readline()
			lines = f.readlines()
			first_line = lines[0]
			if len(first_line) <= 21:
				continue
			else:
				first_line = first_line[10:-13]
			token = prepare_text_for_lda(first_line)
			if random.random() > .99:
				text_data.append(token)
			lastline = lines[-1]
			if len(lastline) <= 29:
				continue
			else:
				lastline = lastline[14:-17]
			token = prepare_text_for_lda(lastline)
			if random.random() > .99:
				text_data.append(token)
		f.close()
	dictionary = corpora.Dictionary(text_data)
	corpus = [dictionary.doc2bow(text) for text in text_data]
	pickle.dump(corpus, open('corpus.pkl', 'wb'))
	dictionary.save('dictionary.gensim')
	ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=NUM_TOPICS, id2word = dictionary, passes = 20)
	ldamodel.save('model15.gensim')
	topics = ldamodel.print_topics(num_words=8)
	for topic in topics:
		print(topic)
		

if __name__=="__main__":
	main()
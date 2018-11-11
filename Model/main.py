import gensim

# load model
model = gensim.models.KeyedVectors.load_word2vec_format('word2vec_twitter_model.bin', binary=True, unicode_errors='ignore')

# get vector for 'bristol'
model['bristol']

# do simple arithmetic      Woman + king - Man ~ Queen
model.wv.most_similar(positive=['woman', 'king'], negative=['man'])
 
# find vectors that are as close to vector of bristol as possible, that is find similar words
model.wv.most_similar(positive=['bristol'])


# find the word that does not fit well, hopefully cereal.
model.wv.doesnt_match("breakfast cereal dinner lunch".split())

# get similarity measure between woman and a man. Note that greater value => more similar
model.wv.similarity('woman', 'man')

# get similarity measure between twitter and a man. Hopefully lower value than woman and a man.
model.wv.similarity('twitter', 'man')

# P.S. do not forget to print all of these stuff. I was using this in interpreter.
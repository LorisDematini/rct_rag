from nltk.stem import PorterStemmer, WordNetLemmatizer

ps = PorterStemmer()
wnl = WordNetLemmatizer()
example_words = ["program","programming","programer","programs","programmed"]

print("{0:20}{1:20}{2:20}".format("--Word--","--Stem--", "--Lemma--"))
for word in example_words:
   print ("{0:20}{1:20}{2:20}".format(word, ps.stem(word), wnl.lemmatize(word, pos="v")))
import sys
import math
import json
from requests_oauthlib import OAuth1Session

CK = '44qASnFSZRM02R1j6DZOcT3TF'                             # Consumer Key
CS = 'KINULwsKeFf8zb01Q8pog0okf22uFcAE9HWckcPzOyrVfMLyKV'         # Consumer Secret
AT = '729507927879344128-s7JZU0x3dVdNgI4cS99rZRm7zx67dQh' # Access Token
AS = 'YNIhdUrbPW2Ahe5vyiI7fZs3imZ6Jpj8vSf6iDJ4Jm7T0'         # Accesss Token Secert

session = OAuth1Session(CK, CS, AT, AS)

class naivebayes():

	def __init__(self):
		self.vocabularies = set()
		self.word_count = {}
		self.category_count = {}


	def word_count_up(self, word, category):
		self.word_count.setdefault(category, {})
		self.word_count[category].setdefault(word, 0)
		self.word_count[category][word] += 1
		self.vocabularies.add(word)

	def category_count_up(self, category):
		self.category_count.setdefault(category, 0)
		self.category_count[category] += 1

	def train(self, words, category):
		for word in words:
			self.word_count_up(word, category)
		self.category_count_up(category)

	def prior_prob(self, category):
		num_of_categories = sum(self.category_count.values())
		num_of_docs_of_the_category = self.category_count[category]
		return num_of_docs_of_the_category / float(num_of_categories)

	def num_of_appearance(self, word, category):
		if word in self.word_count[category]:
			return self.word_count[category][word]
		return 0

	def word_prob(self, word, category):
		numerator = self.num_of_appearance(word, category) + 1
		denominator = sum(self.word_count[category].values()) + len(self.vocabularies)
		prob = numerator / float(denominator)
		return prob

	def score(self, words, category):
		score = math.log(self.prior_prob(category))
		for word in words:
			score += math.log(self.word_prob(word, category))
		return score

	def classify(self, words):
		best_guessed_category = None
		max_prob_before = -sys.maxsize

		for category in self.category_count.keys():
			prob = self.score(words, category)
			if prob > max_prob_before:
				max_prob_before = prob
				best_guessed_category = category
		return best_guessed_category

def tweet_get(input):
	url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
	res = session.get(url, params = {'screen_name':input, 'count':10})

	new_tweet = []
	res_text = json.loads(res.text)
	for tweet in res_text:
		new_tweet.append(tweet['text'])
	return new_tweet


if __name__ == '__main__':
	nb = naivebayes()

	f_name_menhera = "menhera.txt"
	f_name_not_menhera = "notmenhera.txt"

	with open(f_name_menhera, "r") as f:
		m_text = f.read()
		m_words = m_text.split(" ")
		nb.train(m_words,"menhera")

	with open(f_name_not_menhera, "r") as f:
		n_text = f.read()
		n_words = n_text.split(" ")
		nb.train(n_words,"not_menhera")

	scname_input = sys.argv[1]
	new_text = tweet_get(str(scname_input))

	print(nb.classify(new_text))

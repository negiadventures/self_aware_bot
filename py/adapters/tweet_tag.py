from chatterbot.adapters.logic import LogicAdapter
from chatterbot.conversation import Statement
from textblob.classifiers import NaiveBayesClassifier
import nltk

from config import *
import tweepy
from tweepy import OAuthHandler


class TwitterTagAdapter(LogicAdapter):
    def __init__(self, **kwargs):
        super(TwitterTagAdapter, self).__init__(**kwargs)

        training_data = [
            ('what are people talking about', 1),
            ("what's trending in", 0),
            ('what is going on with', 1),
            ('what are reviews', 1)
        ]

        self.classifier = NaiveBayesClassifier(training_data)

    def process(self, statement):
        confidence = self.classifier.classify(statement.text.lower())
        tokens = nltk.word_tokenize(str(statement))
        tagged = nltk.pos_tag(tokens)
        nouns = [word for word, pos in tagged if
                 (pos == 'NN' or pos == 'NNP')]
        downcased = [x.lower() for x in nouns]
        searchTerm = " ".join(downcased).encode('utf-8')
        #"http://where.yahooapis.com/v1/places.q('Place name')?appid=yourappidhere"
        if len(nouns) != 0:
            auth = OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
            auth.set_access_token(twitter_access_key, twitter_access_secret)

            api = tweepy.API(auth)
            for status in tweepy.Cursor(api.search, q='#'+searchTerm).items(20):
                response=Statement(status.text)
        else:
           response = Statement("People seem to be involved in something else.")
        return confidence, response


#what's trending in city
#movie reviews
#people talking about some topic
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
            ('what are reviews', 1),
            ('what is going on',1),
            ('tweetind',1),
            ('what can you tell me about', 0),
            ('what do you know about', 0),
            ('any clue about', 0),
            ('where is',0),
            ('located', 0),
            ('what is happening', 0)
        ]

        self.classifier = NaiveBayesClassifier(training_data)

    def process(self, statement):
        confidence = self.classifier.classify(statement.text.lower())
        tokens = nltk.word_tokenize(str(statement))
        tagged = nltk.pos_tag(tokens)
        nouns = [word for word, pos in tagged if
                 (pos == 'NN' or pos == 'NNP' or pos =='JJ' or pos == 'NNS' or pos == 'NNPS')]
        downcased = [x.lower() for x in nouns]
        searchTerm = " ".join(downcased).encode('utf-8')
        #"http://where.yahooapis.com/v1/places.q('Place name')?appid=yourappidhere"
        st=""
        if len(nouns) != 0:
            auth = OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
            auth.set_access_token(twitter_access_key, twitter_access_secret)

            api = tweepy.API(auth)
            for status in tweepy.Cursor(api.search, q='#'+searchTerm).items(20):
                st = st+status.text
            response = Statement("Jarvis: "+st)
        else:
            response = Statement("Jarvis: "+"Sorry sir, Nothing Found")
        return confidence, response


#what's trending in city
#movie reviews
#people talking about some topic
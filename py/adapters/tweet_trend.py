from chatterbot.adapters.logic import LogicAdapter
from chatterbot.conversation import Statement
from textblob.classifiers import NaiveBayesClassifier
import nltk
from config import *
import tweepy
from tweepy import OAuthHandler
from bs4 import BeautifulSoup
import urllib


class TwitterTrendAdapter(LogicAdapter):
    def __init__(self, **kwargs):
        super(TwitterTrendAdapter, self).__init__(**kwargs)

        training_data = [
            ("what's trending in ", 1),
            ('what is trending in', 1),
            ('what is', 0),
            ('who is', 0),
            ('who was', 0),
            ('what can you tell me about', 0),
            ('what do you know about', 0),
            ('any clue about', 0),
            ('where is',0),
            ('located', 0),
            ('what is happening', 1)
        ]

        self.classifier = NaiveBayesClassifier(training_data)

    def process(self, statement):
        confidence = self.classifier.classify(statement.text.lower())
        tokens = nltk.word_tokenize(str(statement))
        tagged = nltk.pos_tag(tokens)
        nouns = [word for word, pos in tagged if (pos == 'NN' or pos == 'NNP' or pos =='JJ' or pos == 'NNS' or pos == 'NNPS')]
        auth = OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
        auth.set_access_token(twitter_access_key, twitter_access_secret)
        api = tweepy.API(auth)
        trendsName = ""
        for noun in nouns:
            try:
                html = urllib.urlopen(
                    'http://where.yahooapis.com/v1/places.q(' + noun + ')?appid=' + yahoo_client_Id).read()
                soup = BeautifulSoup(html, 'html.parser')
                woeids = soup.find('woeid').contents
                for woeid in woeids:
                    id = ' '.join(woeid.string.split())
                    trends1 = api.trends_place(str(id))
                    data = trends1[0]
                    # grab the trends
                    trends = data['trends']
                    names1 = [trend['name'] for trend in trends]
                    trendsName += ' '.join(names1)
            except:
                pass
        if len(nouns) != 0 and len(trendsName)!=0:
            response = Statement("Jarvis: "+trendsName)
        else:
            response = Statement("")
            confidence=0
        return confidence, response


        # what's trending in city
        # movie reviews
        # people talking about some topic

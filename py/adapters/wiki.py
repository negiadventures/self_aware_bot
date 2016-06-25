from chatterbot.adapters.logic import LogicAdapter
from chatterbot.conversation import Statement
from textblob.classifiers import NaiveBayesClassifier
import wikipedia
import nltk
import nltk.data


class WikipediaAdapter(LogicAdapter):
    def __init__(self, **kwargs):
        super(WikipediaAdapter, self).__init__(**kwargs)
        training_data = [
            ("what do you know about", 1),
            ('what is', 1),
            ('who is', 1),
            ('who was', 1),
            ('Could you tell me', 1),
            ('what can you tell me about', 1),
            ("what's trending in ",0),
            ('what is trending in', 0),
            ('what is going on with', 0),
            ('how are you', 0),
            ('how is', 0),
            ('how are', 0),
            ('how will', 0),
            ('how would you', 0),
            ('what people are talking about', 0),
            ('what are reviews', 0),
            ('what the', 0),
            ('do you know the time', 0),
            ('it is time to go to sleep', 0),
            ('what is your favorite color', 0),
            ('i had a great time', 0),
            ('what time is it', 0),
            ('do you know the time', 0),
            ('do you know what time it is', 0),
            ('what is the time', 0),
            ('how are you?', 0)
        ]
        self.classifier = NaiveBayesClassifier(training_data)

        # def can_process(self, statement):
        #   return true

    def process(self, statement):
        confidence = self.classifier.classify(statement.text.lower())
        tokens = nltk.word_tokenize(str(statement))
        tagged = nltk.pos_tag(tokens)
        nouns = [word for word, pos in tagged if
                 (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS' or pos == 'VBG')]
        downcased = [x.lower() for x in nouns]
        searchTerm = " ".join(downcased).encode('utf-8')
        response = Statement("")
        if len(nouns) != 0:
            try:
                response = Statement(wikipedia.summary(searchTerm, sentences=1))
            except wikipedia.exceptions.DisambiguationError:
                response = Statement(
                    "Sir, there seems to be more than one entries for this term in my dictionary. Try to be more specific please.")
            except:
                confidence = 0

        else:
            confidence = 0
        # else:
        #    response = Statement("Sorry, Nothing Found.")
        return confidence, response

        # about some noun

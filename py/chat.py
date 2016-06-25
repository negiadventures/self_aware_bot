from chatterbot import ChatBot
from chatterbot.training.trainers import ChatterBotCorpusTrainer
from chatterbot.training.trainers import ListTrainer

bot = ChatBot("Terminal",
    storage_adapter="chatterbot.adapters.storage.JsonDatabaseAdapter",
    logic_adapters=[
        "chatterbot.adapters.logic.MathematicalEvaluation",
        "chatterbot.adapters.logic.ClosestMatchAdapter",
        "chatterbot.adapters.logic.ClosestMeaningAdapter",
        "adapters.tweet_tag.TwitterTagAdapter",
        "adapters.tweet_trend.TwitterTrendAdapter",
        "adapters.wiki.WikipediaAdapter",
        "chatterbot.adapters.logic.TimeLogicAdapter"
    ],
    input_adapter="chatterbot.adapters.input.VariableInputTypeAdapter",
    output_adapter="chatterbot.adapters.output.TerminalAdapter",
    database="../database.db"
)
# conversation = [
#     "Hello",
#     "Hi there!",
#     "How are you doing?",
#     "I'm doing great.",
#     "That is good to hear",
#     "Thank you.",
#     "You're welcome."
# ]

#bot.set_trainer(ListTrainer)
bot.set_trainer(ChatterBotCorpusTrainer)
bot.train("training.conversations")

#bot.train("chatterbot.corpus.english")
print("Jarvis: "+"Hey There! I am Jarvis, your personal assistant. Any queries?")

while True:
    try:
        print("You: ")
        bot_input = bot.get_response(raw_input())
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
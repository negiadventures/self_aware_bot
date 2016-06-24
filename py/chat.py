from chatterbot import ChatBot
from chatterbot.training.trainers import ChatterBotCorpusTrainer

bot = ChatBot("Terminal",
    storage_adapter="chatterbot.adapters.storage.JsonDatabaseAdapter",
    logic_adapters=[
        "chatterbot.adapters.logic.MathematicalEvaluation",
        "chatterbot.adapters.logic.TimeLogicAdapter",
        "chatterbot.adapters.logic.ClosestMatchAdapter",
        "adapters.twitter.TwitterAdapter"
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
#bot.train(conversation)

bot.set_trainer(ChatterBotCorpusTrainer)
bot.train("chatterbot.corpus.english")
print("Hey There! I am Jarvis, your personal assistant. Do you have any queries?")

while True:
    try:
        bot_input = bot.get_response(raw_input())
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
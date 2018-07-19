from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from watson_developer_cloud import ConversationV1
import json

context = None


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    print('Received /start command')
    update.message.reply_text('Hi!')


def message(bot, update):
    print('Received an update')
    global context

    conversation = ConversationV1(username='7405d895-fb87-4785-a931-8499e313dc4f',  # TODO
                                  password='mF3wu4pHNwug',  # TODO
                                  version='2018-02-16')

    # get response from watson
    response = conversation.message(
        workspace_id='25acc319-55ec-4fda-a803-5b220661c844',  # TODO
        input={'text': update.message.text},
        context=context)
    print(json.dumps(response, indent=2))
    if len(response['entities'])>0:    	
	entity=response['entities'][0]['entity']
    	value=response['entities'][0]['value']
    if len(response['intents'])>0:
    	intent=response['intents'][0]['intent']
    #context = response['context']
    # build response
    resp=''
    if intent == 'Greeting':
        resp = "I am your calorie counting bot"
    
    if intent == 'foodConsumed':
        resp = "How much did you have?"

    if intent == 'countCalorie':
        resp = "What have you eaten?"

    if intent == 'WhatCanIEat':
        resp = "What is your calorie count today?"
    print(intent)
    update.message.reply_text(resp)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater('515850760:AAGjN106zbtr-hRj8Qm7rU0BQOqMvQJiQ1s')  # TODO

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    #dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, message))

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

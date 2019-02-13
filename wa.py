from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from telegram.error import (TelegramError, Unauthorized, BadRequest, 
						TimedOut, ChatMigrated, NetworkError)
from watson_developer_cloud import AssistantV1
from flask import jsonify
import json
import sqlite3
context= None
d={'name':'user'}
food = ''
# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
	print('Received /start command')
	update.message.reply_text('Hi!')


def error_callback(bot, update, error):
	print(error.message)


def message(bot, update):
	print('Received an update')
	global context
	print('abc')
	conversation = AssistantV1(username='7405d895-fb87-4785-a931-8499e313dc4f',  # TODO
							  password='mF3wu4pHNwug',  # TODO
							  version='2018-02-16')

# get response from watson
	print('bbb')
	response = conversation.message(
		workspace_id='25acc319-55ec-4fda-a803-5b220661c844',  # TODO
		input={'text': update.message.text},
		context=context)
	#try:	
	#	print(json.dumps(response, indent=2))
	#except Exception as e:
	#	print(e)
	print(response.result['intents'])
# handle no entities
	if len(response.result['entities'])>0:
		entity=response.result['entities'][0]['entity']
		value=response.result['entities'][0]['value']
	print('ii')
# handle no intents
	if len(response.result['intents'])>0:
		intent=response.result['intents'][0]['intent']
		#print(response)
		print(intent)

		print('allaa')
	context = response.result['context']
# build response

#storing date in the database
	conn = sqlite3.connect('calorie.db')
	c = conn.cursor()

	resp=''
#foods1=''
	if intent == 'Greeting':
		resp = "I am your calorie counting bot. Please tell me what you had today"
		update.message.reply_text(resp)
#users.getFullUser
#id:InputUser = UserFull
#print(id)
	elif intent == 'countCalorie':  # how many calories consumed so far
	# TODO check if calorie count for the day exists for the user
	#resp = "You haven't told me what you ate so far today. What did you eat?"
		query4 = "SELECT calorie FROM foodConsumed"
		print(query4)
		c.execute(query4)
		print(query4)
		r=c.fetchall()
		total = 0
		for row in r:
			total = total+ int(row[0])
		resp = ("Your total calorie count is")
		update.message.reply_text(resp)
		update.message.reply_text(total)
	elif intent == 'foodConsumed':  # what food items have i eaten so far
		#print('a')
		print(entity)
		if entity == 'foods':
			print('a')
			resp = "How much did you have?"
			update.message.reply_text(resp)
			print('kkk')
			print('+++++++++++++++++++++++++++++++',response.result['context']['foods'],'+++++++++++++++++++++')
			foodItem = response.result['context']['foods']
			food =  foodItem.encode('ascii','ignore')
			print('aaa')
			print(food)
			
		if entity == 'quantity':
			count = response.result['context']['quantity']
			print(count)
			print('aaa')
			print(response.result['context'])	
			foods = response.result['context']['foods']
			print(foods)		
			query = "SELECT kcal FROM calories WHERE food ='" +foods+ "'"
			print('laaa')
			c.execute(query)
			print(query)
			print('+++++++++++++++++++++++++++',response.result['context']['quantity'],'+++++++++++++++')
			r= c.fetchall()
			cal = ''
			for row in r:
				cal = int(row[0])
				cal = cal*count
			update.message.reply_text("Your calorie count is ")
			update.message.reply_text(cal)
				#query0 = "DROP TABLE if exists foodConsumed"
		#c.execute(query0)
		#print(query0)
		#query1 = "CREATE TABLE foodConsumed (id int, kcal int, primary key (id))"
		#c.execute(query1)
		#print(query1)
			print('aaaaaa')
			query2 = 'INSERT INTO foodConsumed(calorie) VALUES("%s")'%(cal)
			print(query2)
			c.execute(query2)
			response.result['context'].pop('foods', None)
			response.result['context'].pop('quantity', None)

	elif intent == 'Goodbye':  #Clear table
		resp = "Thank you for using our calorie counting bot. Have a nice day."
		update.message.reply_text(resp)
		query0 = "DELETE from foodConsumed"
		c.execute(query0)

	conn.commit()
	conn.close()

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

# to handle error
	dp.add_error_handler(error_callback)

# Start the Bot
	updater.start_polling()

# Block until the user presses Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()

#storing date in the database
#conn=sqlite3.connect('calorie.db')
#c = conn.cursor()

#conn.commit()
#conn.close()
if __name__ == '__main__':
	main()

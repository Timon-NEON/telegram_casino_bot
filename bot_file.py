"""
FILE FOR COMMUNICATION WITH TELEGRAM
"""



import telebot


f = open ('api.txt')
BOT_TOKEN = f.readline()

print("well done!") #audit

bot = telebot.TeleBot(BOT_TOKEN)

"""
SLOT GAME FILE
"""



import time
import telebot
import random

import technical_functions
from bot_file import bot

from telebot import types




"""LAUNCH OF THE GAME"""

"""game visualization"""

def test_ask (message):
  answer = technical_functions.bet(message.text, balance = technical_functions.get_info_balance(message.from_user.id)[0])
  if str (type (answer)) != "<class 'int'>":
     bot.reply_to(message, technical_functions.errors[answer], reply_markup=technical_functions.start_menu)
     bot.send_message(message.from_user.id, 'Гра скасовується')
     return None
  column1_left, column1_mid, column1_right = "🟥", "🟥", "🟥"
  column2_left, column2_mid, column2_right = "🟥", "🟥", "🟥"
  column3_left, column3_mid, column3_right = "🟥", "🟥", "🟥"
  msg = bot.send_message(message.chat.id, "░." + column1_left + column1_mid + column1_right + ".░" + "\n" + "►" + column2_left + column2_mid + column2_right + "◄" + "\n" + "░." + column3_left + column3_mid + column3_right + ".░")
  time.sleep (0.7)
  
  try:
    for i in range (16): # scroll count parameter
      if i < 8:
        column2_left, column2_mid, column2_right, column3_left, column3_mid, column3_right = column1_left, column1_mid, column1_right, column2_left, column2_mid, column2_right
        column1_left, column1_mid, column1_right = Spin.spinning(message, i)
      elif i <12:
        column2_mid, column2_right, column3_mid, column3_right = column1_mid, column1_right, column2_mid, column2_right
        column1_mid, column1_right = Spin.spinning(message, i)
      elif i <16:
        column2_right, column3_right = column1_right, column2_right
        column1_right = Spin.spinning(message, i)
      bot.edit_message_text(chat_id = message.chat.id, message_id = msg.message_id, text = "░." + column3_left + column3_mid + column3_right + ".░" + "\n" + "►" + column2_left + column2_mid + column2_right + "◄" + "\n" + "░." + column1_left + column1_mid + column1_right + ".░")
      time.sleep(0.1) # scroll speed parameter
  except:
    time.sleep(0.7)
    bot.send_message(message.from_user.id, 'Крр-грр-пшшш')
    bot.send_message(message.from_user.id, 'Ох, вибачте, автомат заглох\nЗараз спробуємо ще раз запустити...')
    time.sleep(1.7)
    test_ask(message)
  else:
    time.sleep (0.5)
    winning = Spin.check (message, list(column2_left + column2_mid + column2_right))* answer
    technical_functions.upd_bal_minus (message.from_user.id, answer)
    if winning != 0:
       technical_functions.upd_bal_plus (message.from_user.id, winning)
       msg = bot.send_message(message.chat.id, "Ваш виграш:  " + str(winning) + '$')
    else:
      msg = bot.send_message(message.chat.id, "Ваш програш:  -" + str(answer) + '$')
  
    last_bet = answer
    technical_functions.counting_game_plus(message.from_user.id)
  
    technical_functions.postLastBet(message.from_user.id, last_bet)
  
    bot.send_message(message.chat.id, "Що далі?", reply_markup=technical_functions.game_menu)
      

"""randomization process"""

class Spin ():
  def spinning (self, count):
    self.emoji = ["🍍", "🍍","🍍","🍍","🍍","🍍","🍍","🍍","🍍","🍍","🍍",
                  "🍍","🍍","🍍","🍍","🍍","🍍","🍍","🍍","🍍","🍍","🍉",
                  "🍉","🍉","🍉","🍉","🍉","🍉","🍉","🍉","🍉","🍉","🍉",
                  "🍉","🍉","🍉","🍉","🍉","🍉","🍉", "🍒", "🍒","🍒","🍒",
                  "🍒","🍋","🍋","🍋","🍋","🍋","🍋","🍋","🍋","🍋","🍋","🍋",
                  "🍋","🍋","🍋","🍋","🍋","🍋", "7️⃣", "7️⃣","7️⃣","7️⃣","7️⃣", "💰"]
    spin_list = []
    for x in range (4 - count // 4):
      spin_list.append (self.emoji[random.randint(0, 67)])
    if count < 8:
      return (spin_list[0], spin_list[1], spin_list[2])
    elif count < 12:
      return spin_list[0], spin_list[1]
    elif count < 16:
      return spin_list[0]


  def check (self, result):
    self.price = {"🍍":7, "🍉":13, "🍒":9, "🍋":15, "7️⃣":28, "💰":100}
    score = 0
    if len (set (result)) == 1:
      self.time_value = list (set(result))[0]
      score = self.price[self.time_value]
    elif "🍒" in result:
      if result.count ("🍒") == 1:
        score+=3
      elif result.count ("🍒") == 2:
        score=+5

    return (score)

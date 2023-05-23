"""
POKER GAME FILE
"""



import random
import time

from bot_file import bot
import technical_functions



"""LAUNCH OF THE GAME"""

"""value generation and processing"""

class Dice ():
  
  def diceRand(self):


    self.diceStr = ''
    self.combination = []
    self.pok = 0
    self.sq = 0
    self.fh = 0
    self.thr = 0
    self.twoP = 0
    self.oneP = 0
    self.str = 0
    self.bust = 0
    self.countedBal = 0
    for i in range(1, 6):
      a = random.randint(1, 6)
      self.diceStr += str(a)
      self.combination.append(a)
    Dice.check (self)
    aim = None

    if self.pok != 0: aim = "Poker"
    elif self.sq != 0: aim = "Square"
    elif self.fh != 0: aim = "Full House"
    elif self.thr != 0: aim = "Three"
    elif self.twoP != 0: aim = "Two pairs"
    elif self.oneP != 0: aim = "One pair"
    elif self.str != 0: aim = "Straight"
    elif self.bust != 0: aim = "Bust"
    
    return ([self.diceStr, aim, self.countedBal])

  def check (self):
    if len(set(self.combination)) == 1:
        self.pok += 1
        self.countedBal = 50
    helpArr = []
    helpArr2 = []
    helpArrK = []
    for k in range(7):
        count = self.combination.count(k)
        if count == 4:
            self.sq += 1
            helpArr2.append(count)
            self.countedBal = k*4*2
        if count == 3:
            helpArr.append(count)
            helpArrK.append(k)
        if count == 2:
            helpArr.append(count)
            helpArrK.append(k)
    if len(helpArr) == 2 and len(set(helpArr)) != 1:
        self.fh += 1
        self.countedBal = (helpArrK[1]*2 + helpArrK[0]*3)*2
    if len(set(helpArr)) == 1 and helpArr[0] == 3:
        self.thr += 1
        self.countedBal = helpArrK[0]*3
    if len(set(helpArr)) == 1 and len(helpArr) == 2:
        self.twoP += 1
        self.countedBal = helpArrK[0]*2 + helpArrK[1]*2
    if len(helpArr) == 1 and helpArr[0] != 3:
        self.oneP += 1
        self.countedBal = helpArrK[0]*2

    arrStraight1 = [1, 2, 3, 4, 5]
    arrStraight2 = [2, 3, 4, 5, 6]
    if self.combination == arrStraight1 or self.combination == arrStraight2:
      self.str += 1
      self.countedBal = 40

    if self.combination != arrStraight1 and self.combination != arrStraight2 and len(helpArr) == 0 and len(helpArr2) == 0:
        self.bust += 1

i = 0
answer = 0

"""game process"""

def dicer(message):
  global last_bet, answer

  answer = technical_functions.bet(message.text, balance = technical_functions.get_info_balance(message.from_user.id)[0])
  
  if str (type (answer)) != "<class 'int'>":
     bot.reply_to(message, technical_functions.errors[answer], reply_markup=technical_functions.start_menu)
     bot.send_message(message.from_user.id, 'Гра скасовується')
     return None
  
  last_bet = answer
  technical_functions.postLastBet(message.from_user.id, last_bet)
  
  """receiving user points"""

  time.sleep(0.2)

  diceResult1 = Dice.diceRand(message)
  dice_face = ''
  for value in list (diceResult1[0]):
        dice_face = dice_face + technical_functions.dice_values[value]
  result = ' '
  result = technical_functions.dice_values[diceResult1[1]]
  msg = bot.send_message(chat_id = message.from_user.id, text = f"Ваш бросок:\n\n◽{dice_face}◽\n\n \nВаші бали:")
  for x in range (5):
    diceResult1 = Dice.diceRand(message)
    dice_face = ''
    for value in list (diceResult1[0]):
      dice_face = dice_face + technical_functions.dice_values[value]
    if x != 4:
      result = " "
      diceResult1[2] = ''
    else:
      result = technical_functions.dice_values[diceResult1[1]]
    bot.edit_message_text(chat_id = message.chat.id, message_id = msg.message_id, text = f"Ваш бросок:\n\n◽{dice_face}◽\n\n{result} \nВаші бали: {str(diceResult1[2])}")

    time.sleep(0.2)

  """receiving user points"""

  time.sleep(0.5)
  dice_face = ''

  diceResult2 = Dice.diceRand(message)
  for value in list (diceResult2[0]):
        dice_face = dice_face + technical_functions.dice_values[value]
  result = " "
  msg = bot.send_message(chat_id = message.from_user.id, text = f"Бросок бота:\n\n◽{dice_face}◽\n\n\nВаші бали:")
  for x in range (5):
    diceResult2 = Dice.diceRand(message)
    dice_face = ''
    for value in list (diceResult2[0]):
      dice_face = dice_face + technical_functions.dice_values[value]
    if x != 4:
      result = " "
      diceResult2[2] = ''
    else:
      result = technical_functions.dice_values[diceResult2[1]]
    bot.edit_message_text(chat_id = message.chat.id, message_id = msg.message_id, text = f"Бросок бота:\n\n◽{dice_face}◽\n\n{result} \nВаші бали: {str(diceResult2[2])}")

    time.sleep(0.2)

  time.sleep(0.5)


  if diceResult1[2] > diceResult2[2]:
      won = f"Ваш виграш: {int(message.text)}$"
  elif diceResult2[2] > diceResult1[2]:
     won = f"Ваш програш: -{int(message.text)}$"
  else:
     won = f"Нічия"

  bot.send_message(message.chat.id, won)

  technical_functions.counting_game_plus(message.from_user.id)

  if diceResult1[2] > diceResult2[2]:
    technical_functions.upd_bal_plus(message.from_user.id, int(message.text))
  elif diceResult1[2] < diceResult2[2]:
    technical_functions.upd_bal_minus(message.from_user.id, int(message.text))

  bot.send_message(message.chat.id, "Що далі?", reply_markup=technical_functions.game_menu)
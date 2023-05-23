"""
FILE WITH PROGRAM FUNCTIONS
"""



import sqlite3
from telebot import types
from dotenv import load_dotenv
import time
from telebot import types

from bot_file import bot



"""CONSTANTS"""

"""anonymous time function"""

tconv = lambda x: time.strftime("%H:%M:%S %d.%m.%Y", time.localtime(x)) 

"""error cases"""

errors = {"type": "Ви ввели неправильне значення, введіть будь-ласка ціле число", "low_money": "У вас недостатньо грошей", 'low_law':'У вас не достатньо прав для виконання цієї команди',
          'success_command':'Команда виконана вдало', 'unsuccess_command':'Команда не виконана', 'wrong_gata_command':'Ви ввели напривильно значення',}

"""constants for poker"""

dice_values = {"Poker":'Покер', "Square":'Каре', "Full House":'Фул Хаус', "Three":'Трійка', "Two pairs":'Дві пари', "One pair":'Одна пара', "Straight":'Стріт', "Bust":'Баст',
               '1':'1⃣', '2':'2⃣', '3':'3⃣', '4':'4⃣', '5':'5⃣', '6':'6⃣'}

"""cases of receiving money"""

source_of_money = ['Ви зустріли Містера Біста', "Ви знайшли нафту на ваші загородній ділянці", "Нігерійський принц вирішив поділитися із вами спадком",
                   "Ви спіймали золоту рибку", "Ви створили вдалого телеграм-бота", "Ви знайшли піратський скарб", "Помилка банку", "Ви вчасно продали свій Біткойн",
                   "Бабуся дала вам подарунок", "Ви вчасно вийшли з фінансової піраміди", "Ви пограбували банк"]



"""FUNCTIONS FOR GAMES"""

"""checking the bet"""

def bet (message, balance):
   try:
    if int (message) <= 0: return ('type') 
    if int (balance) >= int(message):
       return (int (message))
    else:
       return ("low_money")
   except:
      return("type")



"""DATABASE FUNCTIONS"""

"""database connection"""

conn = sqlite3.connect('db/teleBotDatabase.db', check_same_thread=False)
cursor = conn.cursor()
load_dotenv()

"""entering data about a new user"""

def db_table_val(user_id: int, user_name: str, user_surname: str, username: str):
    cursor.execute(f"INSERT INTO `userI` VALUES (NULL, ?, ?, ?, ?, 100, 1, 0, 100, 0)", (user_id, user_name, user_surname, username))
    conn.commit()

"""updating user information"""

def update_val(user_id: int, user_name: str, user_surname: str, username: str):
  sql = '''UPDATE `userI` SET USER_NAME=(?) WHERE USER_ID = (?) '''
  cursor.execute(sql, (user_name, user_id))
  sql = '''UPDATE `userI` SET USER_SURNAME=(?) WHERE USER_ID = (?) '''
  cursor.execute(sql, (user_surname, user_id))
  sql = '''UPDATE `userI` SET USERNAME=(?) WHERE USER_ID = (?) '''
  cursor.execute(sql, (username, user_id))
  conn.commit()

"""adding to the user's balance"""

def upd_bal_plus(user_id: str, bal: int):
    sql = f'''UPDATE `userI` SET BALANCE=BALANCE+{bal} WHERE USER_ID = '{user_id}' '''
    cursor.execute(sql)
    conn.commit()

"""subtraction from the user's balance"""

def upd_bal_minus(user_id: str, bal: int):
  sql = f'''UPDATE `userI` SET BALANCE=BALANCE-{bal} WHERE USER_ID = '{user_id}' '''
  cursor.execute(sql)
  conn.commit()

"""request the value of the user's balance"""

def get_info_balance(user_id: int):
    cursor.execute(f"SELECT balance FROM userI WHERE USER_ID = '{user_id}'")
    result = cursor.fetchone()
    return result

"""recording the last time the user received rewards"""

def upd_update_teme_get_rewards(user_id: int, time):
  sql = '''UPDATE `userI` SET TIMEREWARDS=(?) WHERE USER_ID = (?) '''
  cursor.execute(sql, (time, user_id))
  conn.commit()

"""request the last time the user received rewards"""

def get_info_get_time_rewards(user_id: int):
    cursor.execute(f"SELECT timerewards FROM userI WHERE USER_ID = '{user_id}'")
    result = cursor.fetchone()
    return result

"""recording the user's last bet"""

def postLastBet(user_id:int, bet: int):
  sql = '''UPDATE `userI` SET LAST_BET=(?) WHERE USER_ID = (?) '''
  cursor.execute(sql, (bet, user_id))
  conn.commit()

"""request the user's last bet"""

def getLastBet(user_id: int):
  cursor.execute(f"SELECT last_bet FROM userI WHERE USER_ID = '{user_id}'")
  result = cursor.fetchone()
  return result[0]

"""request the user's status"""

def check_status (user_id):
   cursor.execute(f"SELECT Status FROM userI WHERE USER_ID = '{user_id}'")
   result = cursor.fetchone()
   return result[0]

"""increases the number of played games by user"""

def counting_game_plus(user_id: str):
    sql = f'''UPDATE `userI` SET Counting_games=Counting_games+{1} WHERE USER_ID = '{user_id}' '''
    cursor.execute(sql)
    conn.commit()
   
"""request the number of played games by user"""

def check_counting_gameds (user_id):
   cursor.execute(f"SELECT Counting_games FROM userI WHERE USER_ID = '{user_id}'")
   result = cursor.fetchone()
   return int (result[0])



"""COMMAND FUNCTIONS"""

"""getting information about all users"""

def getAllInfo():
  all = []
  i = 1
  prev = 0
  allStr = ""
  cursor.execute("SELECT id FROM userI")

  massive_big = cursor.fetchall()
  for x in range(1, (max(massive_big)[0] + 1)):
    cursor.execute(f"SELECT * FROM userI WHERE ID = '{x}'")
    result = cursor.fetchone()
    prev = result
    time.sleep(0.1)
    if prev != None:
      allStr += f"{prev} \n \n"
  return (allStr)

"""sets user balance"""

def update_bal(msg):
  if len(msg.text.split()) == 3:
    try:
      text = msg.text
      user_id = text.split() [0]
      balance = text.split() [1]
      sending = text.split() [2]
      sql = '''UPDATE `userI` SET BALANCE=(?) WHERE USER_ID = (?) '''
      cursor.execute(sql, (balance, user_id))
      conn.commit()
      if sending == "True":
         bot.send_message (user_id, 'Значення вашого балансу було змінено\nТепер ви маєте: ' + balance)
      bot.send_message(msg.chat.id,  errors["success_command"])
    except:
      bot.send_message(msg.chat.id,  errors["unsuccess_command"])
  else:
    bot.send_message(msg.chat.id,  errors["wrong_gata_command"])

"""sets user status"""

def set_status (msg):
  if len(msg.text.split()) >= 3:
    try:
      text = msg.text
      user_id = text.split() [0]
      status = int (text.split() [1])
      reason = ''
      if len(msg.text.split()) >= 3:
        reason = ' '.join( text.split() [2:])
      sql = '''UPDATE `userI` SET STATUS=(?) WHERE USER_ID = (?) '''
      cursor.execute(sql, (status, user_id))
      conn.commit()
      if status == '0':
        bot.send_message (user_id, 'Вас було забанено.\nПричина: ' + reason)
      elif status == '1':
        bot.send_message (user_id, 'Вас було раззабанено.')
      elif status == '2':
        bot.send_message (user_id, 'Вас було раззабанено.')
      bot.send_message(msg.chat.id,  errors["success_command"])
    except:
      bot.send_message(msg.chat.id,  errors["unsuccess_command"])
  else:
    bot.send_message(msg.chat.id,  errors["wrong_gata_command"])

"""granting administrator status to the first user"""

def get_admin_for_first_user(msg):
  sql = '''UPDATE `userI` SET STATUS=(?) WHERE   ID = (?) '''
  cursor.execute(sql, (2, 1))
  conn.commit()

"""sends a message to all users"""

def say (msg):
  text = msg.text
  all_users = getAllUser_ID()
  for user_id in all_users:
    bot.send_message(user_id, text)
    
"""getting user_id from  all users"""

def getAllUser_ID():
  all = []
  i = 1
  prev = 0
  cursor.execute("SELECT id FROM userI")

  massive_big = cursor.fetchall()
  for x in range(1, (max(massive_big)[0] + 1)):
    cursor.execute(f"SELECT user_id FROM userI WHERE ID = '{i}'")
    result = cursor.fetchone()
    prev = result
    if prev != None:
      all.append(prev)
  return all



"""MENU BUTTONS"""

"""main menu"""

start_menu = types.ReplyKeyboardMarkup(True, True)
start_menu.row('🎰 Грати 🎰', '🪙 Призи 🪙')
start_menu.row('ℹ️ Про нас ℹ️', '🙋‍♂️ Профіль 🙋‍♀️')

"""game menu"""

game_menu = types.ReplyKeyboardMarkup(True, True)
game_menu.row('🎲 Покер 🎲', '🚪 Назад 🚪', '7⃣ Слоти 7⃣')

"""rewards menu"""

rewards_menu= types.ReplyKeyboardMarkup(True, True)
rewards_menu.row('💸 Отримати щоденний приз 💸')





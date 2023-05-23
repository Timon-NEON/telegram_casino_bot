"""
MAIN FILE THAT HANDLES MESSAGES
"""



from telebot import types

import math
import sqlite3
import random
import time

from bot_file import bot
import game_spin
import game_dice
import technical_functions




"""PROCESSING COMMANDS"""

"""command start"""

@bot.message_handler(commands=['start'])
def send_welcome(message):
    us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username

    bot.send_message(message.from_user.id, f"Ви були зареєстровані під іменем {us_name}")

    try:
      technical_functions.db_table_val(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username)
    except sqlite3.IntegrityError:
      technical_functions.update_val(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username)
      bot.send_message(message.chat.id, "Ви успішно оновили інформацію про себе")

    bot.send_message(message.chat.id, "Вітаємо на ресепшені, куди далі?", reply_markup=technical_functions.start_menu)


"""command help_for_admins"""

@bot.message_handler(commands=['help_for_admins'])
def handle_text(message):
  bot.send_message(message.from_user.id, 'Довідка щодо команд для адмінів\n' +
                 '/all_users — отримати повну інформацію щодо інших гравців для подальшого використання в командах(послідовність відповідає значенню значенню в базі даних: номер, user_id, user_name, user_surname, username, balance, status, timerewards, last_bet< counting_games);\n' + 
                 '/get_admin_for_first_user — надання першому зареєстрованому гравцю статуса адміна;\n' +
                 '/update_ball — задання значення балансу гравця за user_id;\n' +
                 '/status — задання статусу гравця за його user_id (0 — бан гравця, 1 — звичайні повноваження граця, 2 — статус адміна);\n' +
                 '/say — зробити повідомлення усім гравцям;')


"""command help"""

@bot.message_handler(commands=['help'])
def handle_text(message): 
  bot.send_message(message.from_user.id, 'Бот пропонує два види безпечних розваг: гру в покер та слоти.\n\n' +
                 'Як рахується виграш?\n\n' + 
                 'Покер\n' +
                 'Після того, як ви кинули кості, ваши бали підраховуються за класичними правилами покеру. Якщо у вас більше балів, ніж у бота, то ваш виграш дорівнює вашій ставці.' + 
                 ' Якщо балів менше, то ви програєте ставку.\n\n' +
                 'Слоти\n' +
                 "Гра в слоти - це азартний автомат, що випадково складає в ряд символи. Нагорода залежить від комбінацій символів. " + 
                 "Головна мета - отримати 3 однакові знаки в ряду, що означатиме помноження вашої ставки!\n" +
                 'Випробуйте удачу, зібравши в ряд символи і помноживши ставку за таким принципом:\n' +
                 '🍍:7 , 🍉:13 , 🍒:9 , 🍋:15 , 7️⃣:28 , 💰:100\n' +
                 'Бонусні умови: один символ 🍒 дає примноження ставки в 2 рази; 2 символи - в 5 разів.\n' +
                 "Слід пам'ятати: за кожну гру в слоти ви віддаєте свою ставку, навіть якщо гра була переможною.\n\n" +
                 'Інтерфейс\n' +
                 'Інтерфейс бота майже повністю побудован на кнопках, меню котрих ви можете активувати кнопкою справа. Якщо ви ввели некоректне значення, гра перенесе вас у початкове меню.\n' +
                 'Якщо після нажаття на кнопку нічого не змінеться, тоді активуйте меню кнопок самостійно та зробіть вибір ще раз\n\n' +
                 'Ставки\n' + 
                 'Обираючи ставку вам запропоновано 2 значення: зліва найближча до вашого балансу степінь десяти, друга ваша остання ставка. ' +
                 'Також ви можете самостійно ввести потрібну вам цілочислена ставку через чат'
                 'Вітаємо, ви дізнались все про розваги! Не забувайте отримувати щоденні подарунки та насолоджуйтесь грою!')
                 
  
"""command get_admin_for_first_user"""

@bot.message_handler(commands=['get_admin_for_first_user']) 
def handle_text(message):
  technical_functions.get_admin_for_first_user(1)
  bot.send_message(message.from_user.id, technical_functions.errors['success_command'])


"""command all_users"""

@bot.message_handler(commands=['all_users']) 
def handle_text(message):
  if technical_functions.check_status(message.from_user.id) == 2:
    bot.send_message (message.chat.id, f"{technical_functions.getAllInfo()}")
  else:
    bot.send_message(message.chat.id, technical_functions.errors['low_law'])


"""command update_ball"""

@bot.message_handler(commands=['update_ball']) 
def handle_text(message):
  if technical_functions.check_status(message.from_user.id) == 2:
    msg = bot.send_message (message.chat.id, 'Увведіть user.id, бажану суму балансу та статус відправки повідомлення про надання коштів (True користувач отримає повідомлення, False - ні)')
    bot.register_next_step_handler(msg, technical_functions.update_bal)
  else:
    bot.send_message(message.chat.id, technical_functions.errors['low_law'])


"""command status"""

@bot.message_handler(commands=['status']) 
def handle_text(message):
  if technical_functions.check_status(message.from_user.id) == 2:
    msg = bot.send_message (message.chat.id, 'Увведіть юзернейм, статус (0 разбан, 1 бан) та причину')
    bot.register_next_step_handler(msg, technical_functions.set_status)
  else:
    bot.send_message(message.chat.id, technical_functions.errors['low_law'])

"""command say"""

@bot.message_handler(commands=['say']) 
def handle_text(message):
  if technical_functions.check_status(message.from_user.id) == 2:
    msg = bot.send_message (message.chat.id, 'Увведіть ваше повідомлення')
    bot.register_next_step_handler(msg, technical_functions.say)
  else:
    bot.send_message(message.chat.id, technical_functions.errors['low_law'])




"""PROCESSING MESSAGES"""

"""receiving messages"""

@bot.message_handler(content_types=['text'])
def handle_text(message):
  if technical_functions.check_status(message.from_user.id) != 0:
    if message.text == "🎰 Грати 🎰":
      msg = bot.send_message(message.chat.id, "Добре! В що граємо?", reply_markup=technical_functions.game_menu)
      bot.register_next_step_handler(msg, handle_games)
    elif message.text == "bal":
      technical_functions.get_info_balance (message.from_user.id)
    elif message.text == "🪙 Призи 🪙":
      msg = bot.send_message(message.chat.id, "Отримайте щоденний приз!", reply_markup=technical_functions.rewards_menu)
    elif message.text == "💸 Отримати щоденний приз 💸":
      get_rewards (message)
    elif message.text == "🙋‍♂️ Профіль 🙋‍♀️": 
      try:
        bot.send_message(message.chat.id, "Нік: " + message.from_user.username +
                         "\nБаланс: " + str(technical_functions.get_info_balance(message.from_user.id)[0]) + '$' + 
                         "\nКількість ігор: " + str(technical_functions.check_counting_gameds(message.from_user.id)) + 
                         '\n\n/help - дізнайтеся більше про гру', reply_markup=technical_functions.start_menu)
      except:
        bot.send_message(message.chat.id, "Нік: " +
                         "\nБаланс: " + str(technical_functions.get_info_balance(message.from_user.id)[0]) + '$' + 
                         "\nКількість ігор: " + str(technical_functions.check_counting_gameds(message.from_user.id)) + 
                         '\n\n/help - дізнайтеся більше про гру', reply_markup=technical_functions.start_menu)
      
    elif message.text == "ℹ️ Про нас ℹ️": 
        bot.send_message(message.chat.id, "Засновано WEXEL Union" + 
                         "\nУчасники проекту @Timon_NEON та @Grooove4life"  +
                       "\nДякуємо за вашу підтримку та кожний кинутий кубик!" + 
                       "\nПосилання на репозіторій програми на Github: https://github.com/Timon-NEON/telegram_casino_bot" + 
                       "\nНасолоджуйтесь безпечною грою!",  reply_markup=technical_functions.start_menu, disable_web_page_preview=True)
      
    elif message.text == "🎲 Покер 🎲" or message.text == "7⃣ Слоти 7⃣" or message.text == "Спіни" or message.text == "Покер":
      handle_games(message)
    elif message.text == "🚪 Назад 🚪":
      bot.send_message(message.chat.id, "Вітаємо на ресепшені, куди далі?", reply_markup=technical_functions.start_menu)
    else:
      bot.send_message(message.chat.id, "Некоректне значення")
      bot.send_message(message.chat.id, "Вітаємо на ресепшені, куди далі?", reply_markup=technical_functions.start_menu)
  else:
    bot.send_message(message.from_user.id, "Вибачте, але наразі ви забанені.\nЗв'яжіться з @Timon_NEON для з'ясування деталей.")


"""preparation for the start of the game"""

def handle_games(message):
  bet_menu = types.ReplyKeyboardMarkup(True, True)
  bal = technical_functions.get_info_balance(message.from_user.id)[0]
  last_bet = f"{technical_functions.getLastBet(message.from_user.id)}"

  if bal > 0:
    bet_menu.row(str (int (10 ** (math.floor (math.log(bal, 10))))), last_bet)
  else:
    bet_menu.row(str (0), last_bet)

  if message.text == "🎲 Покер 🎲" or message.text == "Покер":
      msg = bot.reply_to(message,  "Ваша ставка?", reply_markup=bet_menu)
      bot.register_next_step_handler(msg, game_dice.dicer)
  elif message.text == "7⃣ Слоти 7⃣" or message.text == "Спіни":
    msg = bot.send_message(chat_id = message.chat.id, reply_to_message_id=message.message_id, text="Ваша ставка?", reply_markup=bet_menu)
    bot.register_next_step_handler(msg, game_spin.test_ask)




"""ADDITIONAL FUNCTIONS"""

"""daily rewards"""

def get_rewards (message):
    open_rewards = ((time.time() - 43200) // 86400 ) * 86400 + 43200
    get_rewards_by_user = technical_functions.get_info_get_time_rewards(message.from_user.id)[0]
    if open_rewards > get_rewards_by_user:
        reward1 = random.randint (10, 2000)
        reward2 = int (technical_functions.get_info_balance(message.from_user.id)[0]) * reward1 / 5000
        if reward1 > reward2: rewards = int (reward1)
        else: rewards = int (reward2)
        technical_functions.upd_bal_plus (message.from_user.id, rewards)
        technical_functions.upd_update_teme_get_rewards (message.from_user.id, str(time.time()))
        bot.send_message(message.chat.id, "Вітаємо!\n" + random.choice(technical_functions.source_of_money) +'\nВаш баланс попвнено на ' f'{rewards}' + '$', reply_markup=technical_functions.start_menu) 
    else:
        bot.send_message(message.chat.id, "Вибачте, але сьогодні і так був насичений день. Завтра після 12:00 ви обов'язково знайдете дещо цікаве!", reply_markup=technical_functions.start_menu)



bot.infinity_polling()

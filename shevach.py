"""
A simple 3-state fast food bot that takes customer orders
"""

import sys
import telebot
# from meal import Meal
import meal
import all_orders
from all_orders import add_new_order
from telebot import types
import dbhelper

NUM_OF_STATES = 5

SERVED_IN, TOPPINGS = 'Served in', 'Toppings'
MC, FALAFEL, SHAWARMA = 'Main Component', 'falafel', 'shawarma'
HAS_CHOSEN_TOPPINGS = False

SERVED_IN_LIST = ['pita', 'lafa', 'plate']
main_components = [FALAFEL, SHAWARMA]
TOPPINGS_LIST = ['tehina', 'hummus', 'onions', 'tomato']

bot = telebot.TeleBot("914612655:AAHlgacfo71BTDA5IErN5yTo3Ss8FfFGO4I")

@bot.message_handler(commands=['start', 'help'])
def start(message):
    cid = message.chat.id
    all_orders.add_new_order(cid, TOPPINGS_LIST, NUM_OF_STATES)
    keyboard = types.InlineKeyboardMarkup()
    for bread_type in SERVED_IN_LIST:
        keyboard.add(types.InlineKeyboardButton(
            bread_type, callback_data=bread_type))
    bot.send_message(cid, "Welcome To Shevach Falafel!\nWhat type of meal would you like?",
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in SERVED_IN_LIST)
def update_bread_type(call):
    cid = call.message.chat.id
    all_orders.update_bread_type(cid, call.data)
    # all_orders.orders[cid][all_orders.MEAL].set_bread_type(call.data)
    # meal[SERVED_IN] = call.data
    choose_main_comp(cid)

def choose_main_comp(cid):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(FALAFEL, callback_data=FALAFEL),
                 types.InlineKeyboardButton(SHAWARMA, callback_data=SHAWARMA))
    bot.send_message(cid, "Would you like Falafel or Shawarma?", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data in main_components)
def update_mc(call):
    """ 
    Handles query after main component has been chosen, 
    then calls choose toppings function
    Arguments:
        call {[type]} -- [description]
    """
    cid = call.message.chat.id
    all_orders.update_mc(cid, call.data)
    choose_toppings(cid, TOPPINGS_LIST, True)

def kb_with_toppings_builder(toppings):
    num_of_rows = int(len(toppings)/2) if len(toppings) > 1 else 1
    buttons_in_row = int(len(toppings)/num_of_rows)
    markup = types.ReplyKeyboardMarkup(row_width=num_of_rows+1)
    for row in range(num_of_rows):
        toppings_in_row = []
        for i in range(buttons_in_row):
            index = row*buttons_in_row + i
            button = types.KeyboardButton(toppings[index])
            toppings_in_row.append(button)
        markup.row(*toppings_in_row)
    return markup

def choose_toppings(cid, toppings, first_choice=False):
    """ 
    Choose toppings for your meal
    """
    exist_more_toppings_to_choose = True
    if len(toppings) > 0:
        markup = kb_with_toppings_builder(toppings)
    else:
        markup = types.ReplyKeyboardMarkup(row_width=1)
        exist_more_toppings_to_choose = False
    markup.row(types.KeyboardButton('make order'))
    if first_choice:
        bot.send_message(cid, 'Choose toppings and make your order:', reply_markup=markup)
    else:
        if exist_more_toppings_to_choose:
            bot.send_message(cid, 'Any more toppings?', reply_markup=markup)
        else:
            bot.send_message(cid, 'All Done!\nPlease click "make order" to continue :)', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in TOPPINGS_LIST)
def add_topping(message):
    cid = message.chat.id
    remaining_toppings = all_orders.add_topping(cid, message.text)
    choose_toppings(cid, remaining_toppings)

@bot.message_handler(func=lambda message: message.text == 'make order')
def make_order(message):
    cid = message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('yes', callback_data='yes, final order'),
                 types.InlineKeyboardButton('no', callback_data='no, go back'))
    final_order = all_orders.get_order_string(cid)
    bot.send_message(cid,
                     "please review your final order: " + final_order + "\nIf you click no, you'll be taken back to the beginning :/",
                      reply_markup=keyboard)

    # tester line
    # print(len(all_orders.orders))


@bot.callback_query_handler(func=lambda call: call.data == 'no, go back')
def start_over(call):
    start(call.message)

@bot.callback_query_handler(func=lambda call: call.data == 'yes, final order')
def finalize_order(call):
    cid = call.message.chat.id
    bot.send_message(cid, "Thanks for ordering Shevach!")

    # db.add_item(meal)
    # TODO 
    # **DONE make it so after i choose a button (inline or custom keyboard) i CANNOT choose it again
    #   - idea for this - remove button from inline keyboard once chosen
    #   - OR do not remove the buttons, just have the toppings be a python set
    # - send order to falafel maker with reference no. to the customer
    # - save orders in a db
    #   - see that i am collecting all orders of all customers in one eb for one shop
    # - set up webhook(simulation for now) instead of polling
    # - add payment options 

    # tester line
    print(meal)

# TODO polling is shitty, setup webhook
bot.polling()

# TODO design - put orders and meal into same file

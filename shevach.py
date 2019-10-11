import telebot
import meal
from telebot import types
from dbhelper import DBHelper


SERVED_IN = 'Served in'
MC = 'Main Component'
TOPPINGS = 'Toppings'
HAS_CHOSEN_TOPPINGS = False

meal = {
    SERVED_IN: '',
    MC: '',                # Falafel or Shawarma
    TOPPINGS: []            # [tehina, hummus, onions]
}

served_in = ['pita', 'lafa', 'plate']
main_components = ['falafel', 'shawarma']
toppings = ['tehina', 'hummus', 'onions', 'tomato']

bot = telebot.TeleBot("914612655:AAHlgacfo71BTDA5IErN5yTo3Ss8FfFGO4I")
db = DBHelper()


# @bot.callback_query_handler(lambda query: query.data == "v")
# def process_callback_1(query):
#     print('gay')




@bot.message_handler(commands=['start', 'help'])
def start(message):
    # toppings.extend(['tehina', 'hummus', 'onions', 'tomato'])
    keyboard = types.InlineKeyboardMarkup()
    for bread_type in served_in:
        keyboard.add(types.InlineKeyboardButton(
            bread_type, callback_data=bread_type))
    cid = message.chat.id
    bot.send_message(cid, "Welcome To Shevach Falafel!\nWhat type of meal would you like?",
                     reply_markup=keyboard)


def choose_main_comp(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('falafel', callback_data='falafel'),
                 types.InlineKeyboardButton('shawarma', callback_data='shawarma'))

    bot.send_message(chat_id, "Would you like Falafel or Shawarma?", reply_markup=keyboard)
    # TODO edit the previous keyboard to have a little checkmark at the bottom of the chosen button


@bot.callback_query_handler(func=lambda call: call.data in served_in)
def callback_handler_yes(call):
    chat_id = call.message.chat.id
    meal[SERVED_IN] = call.data
    # TODO edit the previous keyboard to have a little checkmark at the bottom of the chosen button
    choose_main_comp(chat_id)


@bot.callback_query_handler(func=lambda call: call.data in main_components)
def callback_handler_yes(call):
    """ handles query after main component has been chosen, 
    then calls choose toppings func
    Arguments:
        call {[type]} -- [description]
    """
    chat_id = call.message.chat.id
    meal[MC] = call.data
    # bot.send_message(chat_id, "Choose toppings and make your order:")
    choose_toppings(chat_id, toppings, True)

def choose_toppings(chat_id, toppings, first_choice=False):
    """ Choose toppings for your meal
    """
    # TODO check that the rounding of the int is correct
    num_of_rows = int(len(toppings)/2) + 1
    buttons_in_row = int(len(toppings)/num_of_rows)
    markup = types.ReplyKeyboardMarkup(row_width=num_of_rows)
    for row in range(num_of_rows-1):
        toppings_in_row = []
        for i in range(buttons_in_row):
            index = row*buttons_in_row + i
            button = types.KeyboardButton(toppings[index])
            toppings_in_row.append(button)
        # toppings_in_row = [types.KeyboardButton(toppings[row*buttons_in_row + i])\
        #      for i in range(buttons_in_row)]
        markup.row(*toppings_in_row)
    markup.row(types.KeyboardButton('make order'))
    if first_choice:
        bot.send_message(chat_id, 'Choose toppings and make your order:', reply_markup=markup)
    else:
        bot.send_message(chat_id, 'Any more toppings?', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in toppings)
def add_topping(message):
    meal[TOPPINGS].append(message.text)
    # remove the button that represents the topping
    toppings.remove(message.text)
    choose_toppings(message.chat.id, toppings)


@bot.message_handler(func=lambda message: message.text == 'make order')
def make_order(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('yes', callback_data='yes, final order'),
                 types.InlineKeyboardButton('no', callback_data='no, go back'))
    
    bot.send_message(message.chat.id, "Is this your final order?: " + meal, reply_markup=keyboard)
    # TODO if no, then take user back to the beginning


@bot.message_handler(func=lambda message: message.text == 'yes, final order')
def finalize_order(message):
    bot.reply_to(message, "Thanks for ordering Shevach!")
    # db.add_item(meal)
    # TODO 
    # **DONE make it so after i choose a button (inline or custom keyboard) i CANNOT choose it again
    #   - idea for this - remove button from inline keyboard once chosen
    # - send order to falafel maker with reference no. to the customer
    # - save orders in a db
    #   - see that i am collecting all orders of all customers in one eb for one shop
    # - set up webhook(simulation for now) instead of polling
    # - add payment options 
    print(meal)

# TODO polling is shitty, setup webhook
bot.polling()





############REFERENCE CODE#############################################


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
        # bot.reply_to(message, "Howdy, how are you doing?")
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtna = types.KeyboardButton('a')
    itembtnv = types.KeyboardButton('v')
    itembtnc = types.KeyboardButton('c')
    itembtnd = types.KeyboardButton('d')
    itembtne = types.KeyboardButton('e')
    # markup.add(itembtn1, itembtn2, itembtn3)
    markup.row(itembtna, itembtnv)
    markup.row(itembtnc, itembtnd, itembtne)
    bot.reply_to(message, "Choose one letter:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in ['a', 'b', 'c'])
def echo_all(message):
    # echo_all = bot.message_handler(echo_all)
    bot.reply_to(message, message.text + "gay")


@bot.message_handler(func=lambda message: message.text in ['d', 'e'])
def echo_all(message):
    # echo_all = bot.message_handler(echo_all)
    # bot.reply_to(message, "not gay")
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Yes', callback_data='yes'),
                 types.InlineKeyboardButton('No', callback_data='no'))

    cid = message.chat.id
    bot.send_message(cid, "are you sure you are not gay?",
                     reply_markup=keyboard)


def gay(cid):
    bot.send_message(cid, "it is possible that you in fact are gay")


@bot.callback_query_handler(func=lambda call: call.data in ['yes'])
def callback_handler_yes(call):
    gay(call.message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data in ['yes', 'no'])
def callback_handler(call):

    cid = call.message.chat.id
    mid = call.message.message_id
    answer = call.data
    # update_lang(cid, answer)
    try:
        bot.edit_message_text("You voted: " + answer, cid,
                              mid, reply_markup=keyboard)
    except:
        pass

# TODO polling is shitty, setup webhook
bot.polling()

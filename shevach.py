import telebot
from telebot import types


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

# @bot.callback_query_handler(lambda query: query.data == "v")
# def process_callback_1(query):
#     print('gay')




@bot.message_handler(commands=['start', 'help'])
def start(message):
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
    choose_toppings(chat_id)

def choose_toppings(chat_id):
    """ Choose toppings for your meal
    """
    markup = types.ReplyKeyboardMarkup(row_width=3)
    topping1 = types.KeyboardButton('onions')
    topping2 = types.KeyboardButton('lettuce')
    topping3 = types.KeyboardButton('spicy shit')
    topping4 = types.KeyboardButton('tomato')
    make_order = types.KeyboardButton('make order')
    markup.row(topping1, topping2)
    markup.row(topping3, topping4)
    markup.row(make_order)
    bot.send_message(chat_id, 'Choose toppings and make your order:', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in toppings)
def add_topping(message):
    # bot.send_message(chat_id, "Would you like Falafel or Shawarma?", reply_markup=keyboard)
    meal[TOPPINGS].append(message.text)


@bot.message_handler(func=lambda message: message.text == 'make order')
def make_order(message):
    # echo_all = bot.message_handler(echo_all)
    bot.reply_to(message, "Thanks for ordering Shevach!")
    # TODO 
    # 1. add payment options 
    # 2. send order to falafel maker with reference no. to the customer
    # 3. save orders in a db
    # 4. make it so after i choose a button (inline or custom keyboard) i CANNOT choose it again

    print(meal)


# TODO polling is shitty, setup webhook
bot.polling()


#########################################################


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

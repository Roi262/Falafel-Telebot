# # -*- coding: utf-8 -*-
# import telebot
# import config
# import pb
# import datetime
# import pytz
# import json
# import traceback

# P_TIMEZONE = pytz.timezone(config.TIMEZONE)
# TIMEZONE_COMMON_NAME = config.TIMEZONE_COMMON_NAME

# bot = telebot.TeleBot(config.TOKEN)
# bot.polling(none_stop=True)


# @bot.message_handler(commands=['start'])
# def start_command(message):
#     bot.send_message(
#         message.chat.id,
#         'Greetings! I can show you PrivatBank exchange rates.\n' +
#         'To get the exchange rates press /exchange.\n' +
#         'To get help press /help.'
#     )


# @bot.message_handler(commands=['help'])
# def help_command(message):
#     keyboard = telebot.types.InlineKeyboardMarkup()
#     keyboard.add(
#         telebot.types.InlineKeyboardButton(
#             'Message the developer', url='telegram.me/artiomtb'
#             )
#     )
#     bot.send_message(
#         message.chat.id,
#         '1) To receive a list of available currencies press /exchange.\n' +
#         '2) Click on the currency you are interested in.\n' +
#         '3) You will receive a message containing information regarding the source and the target currencies, ' +
#         'buying rates and selling rates.\n' +
#         '4) Click “Update” to receive the current information regarding the request. ' +
#         'The bot will also show the difference between the previous and the current exchange rates.\n' +
#         '5) The bot supports inline. Type @<botusername> in any chat and the first letters of a currency.',
#         reply_markup=keyboard
#     )


# @bot.message_handler(commands=['exchange'])
# def exchange_command(message): # < br > 
#     keyboard = telebot.types.InlineKeyboardMarkup()


# keyboard.row(
#     telebot.types.InlineKeyboardButton('USD', callback_data='get-USD')
# )
# keyboard.row(
#     telebot.types.InlineKeyboardButton('EUR', callback_data='get-EUR'),
#     telebot.types.InlineKeyboardButton('RUR', callback_data='get-RUR')
# )

# bot.send_message(
#     message.chat.id, 'Click on the currency of choice:', reply_markup=keyboard)


# @bot.callback_query_handler(func=lambda call: True)
# def iq_callback(query):
#     data = query.data
#     if data.startswith('get-'):
#         get_ex_callback(query)


# def get_ex_callback(query):
#     bot.answer_callback_query(query.id)
#     send_exchange_result(query.message, query.data[4:])


# def send_exchange_result(message, ex_code):
#     bot.send_chat_action(message.chat.id, 'typing')
#     ex = pb.get_exchange(ex_code)
#     bot.send_message(
#         message.chat.id, serialize_ex(ex),
#         reply_markup=get_update_keyboard(ex),
#         parse_mode='HTML'
#     )


# def get_update_keyboard(ex):
#     keyboard = telebot.types.InlineKeyboardMarkup()
#     keyboard.row(
#         telebot.types.InlineKeyboardButton(
#             'Update',
#             callback_data=json.dumps({
#                 't': 'u',
#                 'e': {
#                     'b': ex['buy'],
#                     's': ex['sale'],
#                     'c': ex['ccy']
#                 }
#             }).replace(' ', '')
#         ),
#         telebot.types.InlineKeyboardButton(
#             'Share', switch_inline_query=ex['ccy'])
#     )
#     return keyboard


# def serialize_ex(ex_json, diff=None):
#     result = '<b>' + ex_json['base_ccy'] + ' -> ' + ex_json['ccy'] + ':</b>\n\n' + \
#              'Buy: ' + ex_json['buy']
#     if diff:
#         result += ' ' + serialize_exchange_diff(diff['buy_diff']) + '\n' + \
#                   'Sell: ' + ex_json['sale'] + \
#                   ' ' + serialize_exchange_diff(diff['sale_diff']) + '\n'
#     else:
#         result += '\nSell: ' + ex_json['sale'] + '\n'
#     return result


# def serialize_exchange_diff(diff):
#     result = ''
#     if diff > 0:
#         result = '(' + str(diff) + ' <img draggable="false" data-mce-resize="false" data-mce-placeholder="1" data-wp-emoji="1" class="emoji" alt="<img draggable="false" data-mce-resize="false" data-mce-placeholder="1" data-wp-emoji="1" class="emoji" alt="<img draggable="false" data-mce-resize="false" data-mce-placeholder="1" data-wp-emoji="1" class="emoji" alt="<img draggable="false" data-mce-resize="false" data-mce-placeholder="1" data-wp-emoji="1" class="emoji" alt="<img draggable="false" data-mce-resize="false" data-mce-placeholder="1" data-wp-emoji="1" class="emoji" alt="↗️" src="https://s.w.org/images/core/emoji/2.3/svg/2197.svg">" src="https://s.w.org/images/core/emoji/2.3/svg/2197.svg">" src="https://s.w.org/images/core/emoji/2.3/svg/2197.svg">" src="https://s.w.org/images/core/emoji/72x72/2197.png">" src="https://s.w.org/images/core/emoji/72x72/2197.png">)'
#     elif diff < 0:
#         result = '(' + str(diff)[1:] + ' <img draggable="false" data-mce-resize="false" data-mce-placeholder="1" data-wp-emoji="1" class="emoji" alt="<img draggable="false" data-mce-resize="false" data-mce-placeholder="1" data-wp-emoji="1" class="emoji" alt="<img draggable="false" data-mce-resize="false" data-mce-placeholder="1" data-wp-emoji="1" class="emoji" alt="<img draggable="false" data-mce-resize="false" data-mce-placeholder="1" data-wp-emoji="1" class="emoji" alt="<img draggable="false" data-mce-resize="false" data-mce-placeholder="1" data-wp-emoji="1" class="emoji" alt="↘️" src="https://s.w.org/images/core/emoji/2.3/svg/2198.svg">" src="https://s.w.org/images/core/emoji/2.3/svg/2198.svg">" src="https://s.w.org/images/core/emoji/2.3/svg/2198.svg">" src="https://s.w.org/images/core/emoji/72x72/2198.png">" src="https://s.w.org/images/core/emoji/72x72/2198.png">)'
#     return result


# @bot.callback_query_handler(func=lambda call: True)
# def iq_callback(query):
#     data = query.data
#     if data.startswith('get-'):
#         get_ex_callback(query)
#     else:
#         try:
#             if json.loads(data)['t'] == 'u':
#                 edit_message_callback(query)
#         except ValueError:
#             pass


# def edit_message_callback(query):
#     data = json.loads(query.data)['e']
#     exchange_now = pb.get_exchange(data['c'])
#     text = serialize_ex(
#         exchange_now,
#         get_exchange_diff(
#             get_ex_from_iq_data(data),
#             exchange_now
#         )
#     ) + '\n' + get_edited_signature()
#     if query.message:
#         bot.edit_message_text(
#             text,
#             query.message.chat.id,
#             query.message.message_id,
#             reply_markup=get_update_keyboard(exchange_now),
#             parse_mode='HTML'
#         )
#     elif query.inline_message_id:
#         bot.edit_message_text(
#             text,
#             inline_message_id=query.inline_message_id,
#             reply_markup=get_update_keyboard(exchange_now),
#             parse_mode='HTML'
#         )


# def get_ex_from_iq_data(exc_json):
#     return {
#         'buy': exc_json['b'],
#         'sale': exc_json['s']
#     }


# def get_exchange_diff(last, now):
#     return {
#         'sale_diff': float("%.6f" % (float(now['sale']) - float(last['sale']))),
#         'buy_diff': float("%.6f" % (float(now['buy']) - float(last['buy'])))
#     }


# def get_edited_signature():
#     return '<i>Updated ' + \
#            str(datetime.datetime.now(P_TIMEZONE).strftime('%H:%M:%S')) + \
#            ' (' + TIMEZONE_COMMON_NAME + ')</i>'


# @bot.inline_handler(func=lambda query: True)
# def query_text(inline_query):
#     bot.answer_inline_query(
#         inline_query.id,
#         get_iq_articles(pb.get_exchanges(inline_query.query))
#     )

# def get_iq_articles(exchanges):
#     result = []
#     for exc in exchanges:
#         result.append(
#             telebot.types.InlineQueryResultArticle(
#                 id=exc['ccy'],
#                 title=exc['ccy'],
#                 input_message_content=telebot.types.InputTextMessageContent(
#                     serialize_ex(exc),
#                     parse_mode='HTML'
#                 ),
#                 reply_markup=get_update_keyboard(exc),
#                 description='Convert ' + exc['base_ccy'] + ' -> ' + exc['ccy'],
#                 thumb_height=1
#             )
#         )
#     return result

# # def main():
# #     updater = Updater(TOKEN)

# #     updater.dispatcher.add_handler(CommandHandler('start', start))
# #     updater.dispatcher.add_handler(CallbackQueryHandler(button))
# #     updater.dispatcher.add_handler(CommandHandler('help', help))
# #     updater.dispatcher.add_error_handler(error)

# #     # Start the Bot
# #     updater.start_polling()

# #     # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
# #     # SIGTERM or SIGABRT
# #     updater.idle()


# # if __name__ == '__main__':
# #     main()










import telebot
from telebot import types

bot = telebot.TeleBot("914612655:AAHlgacfo71BTDA5IErN5yTo3Ss8FfFGO4I")

# @bot.callback_query_handler(lambda query: query.data == "v")
# def process_callback_1(query):
#     print('gay')


# @bot.message_handler(commands=['start', 'help'])
# def start():
#     bot.



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
    bot.send_message(cid, "are you sure you are not gay?", reply_markup=keyboard)

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
        bot.edit_message_text("You voted: " + answer, cid, mid, reply_markup=keyboard)
    except:
        pass


bot.polling()


# import telebot

# Using the ReplyKeyboardMarkup class
# It's constructor can take the following optional arguments:
# - resize_keyboard: True/False (default False)
# - one_time_keyboard: True/False (default False)
# - selective: True/False (default False)
# - row_width: integer (default 3)
# row_width is used in combination with the add() function.
# It defines how many buttons are fit on each row before continuing on the next row.
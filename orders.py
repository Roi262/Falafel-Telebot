"""
A file that holds a dictionary of all the current orders
Element template:
    chat_id: (meal, delivery_time, meal_status)
"""
import meal
import shevach
from time import time, ctime

FALAFEL_PREP_TIME = 5
SHAWARMA_PREP_TIME = 10

# meal status types
TAKING_ORDER = 0
QUEUED = 1
IN_MAKING = 2
READY = 3
IN_DELIVERY = 4

t = time()

orders = {}

def add_new_order(chat_id, meal):

def add_order(chat_id, meal, delivery_time, meal_status=QUEUED):
    # TODO deal with delivery time later
    if meal_status == READY:
        # TODO
        pass
    prep_time = FALAFEL_PREP_TIME if \
         meal.get_main_component() == shevach.FALAFEL else SHAWARMA_PREP_TIME
    orders[chat_id] = (meal, delivery_time + prep_time, meal_status)

def remove_order(chat_id):
    if chat_id in orders.keys():
        orders.pop(chat_id)
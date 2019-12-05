"""
A file that holds a dictionary of all the current orders
Element template:
    chat_id: (meal, delivery_time, meal_status)
"""
import meal
# import shevach
from time import time, ctime

FALAFEL_PREP_TIME = 5
SHAWARMA_PREP_TIME = 10

MEAL = 0
DELIVERY_TIME = 1
MEAL_STATUS = 2

# meal status types
TAKING_ORDER = 0
QUEUED = 1
IN_MAKING = 2
READY = 3
IN_DELIVERY = 4

t = time()

orders = {}

def add_new_order(chat_id, possible_toppings, num_of_states):
    new_meal = meal.Meal(possible_toppings, num_of_states)
    orders[chat_id] = (new_meal, 0, TAKING_ORDER)

def get_order_string(chat_id):
    order = orders[chat_id][MEAL] 
    order_string = order.get_bread_type() + ", " + \
        order.get_main_component()
    for topping in order.get_toppings():
        order_string += ", " + topping
    return order_string


def add_order(chat_id, meal, delivery_time, meal_status=QUEUED):
    # TODO deal with delivery time later
    if meal_status == READY:
        # TODO
        pass
    # prep_time = FALAFEL_PREP_TIME if \
    #      meal.get_main_component() == shevach.FALAFEL else SHAWARMA_PREP_TIME
    # orders[chat_id] = (meal, delivery_time + prep_time, meal_status)

def remove_order(chat_id):
    if chat_id in orders.keys():
        orders.pop(chat_id)

def update_bread_type(cid, bread_type):
    orders[cid][MEAL].set_bread_type(bread_type)

def update_mc(cid, mc):
    orders[cid][MEAL].set_main_component(mc)

def add_topping(cid, topping):
    return orders[cid][MEAL].add_topping(topping)

def get_state(cid):
    return orders[cid][MEAL].get_state()


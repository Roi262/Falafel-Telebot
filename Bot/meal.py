""" Meal class for a meal object

Returns:
    [type] -- [description]
"""

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


class Meal():
    """ A class for a meal object
    """

    def __init__(self, possible_toppings, num_of_states):
        """
        bread_type{string} - type of bread
        ...
        meal_state{int} - the state of the meal order:
        num_of_states{int} - the number of states in this meal order
        Arguments:
            possible_toppings {[type]} -- [description]
        """
        self.bread_type = ''
        self.main_component = ''
        self.toppings = set()
        self.possible_toppings = possible_toppings
        self.meal_state = 0 
        self.num_of_states = num_of_states

    def get_toppings(self):
        return self.toppings

    def get_main_component(self):
        return self.main_component
    
    def set_main_component(self, main_component) :
        self.main_component = main_component

    def get_bread_type(self):
        return self.bread_type

    def set_bread_type(self, bread_type):
        self.bread_type = bread_type

    def add_topping(self, topping):
        self.toppings.add(topping)
        self.possible_toppings.remove(topping)
        return self.possible_toppings
    
    def get_state(self):
        return self.meal_state

    def set_bread_type(self, state):
        self.meal_state = state



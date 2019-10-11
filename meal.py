

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

    def __init__():
        self.meal = {}
        self.bread_type = ''
        self.main_component = ''
        self.toppings = []

    def get_toppings(self):
        return self.toppings

    def set_toppings(self, toppings) :
    	self.toppings = toppings

    def get_main_component(self):
        return self.main_component
    
    def set_main_component(self, main_component) :
        self.main_component = main_component

    def get_bread_type(self):
        return self.bread_type

    def set_bread_type(self, bread_type):
        self.bread_type = bread_type

    def remove_topping(self, topping):
        self.toppings.remove(topping)



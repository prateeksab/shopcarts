# Test Factory
import factory
import random
from factory.fuzzy import FuzzyChoice
from service.models import Shopcart, Item

class ItemFactory(factory.Factory):
    """ Creates fake items  """

    class Meta:
        model = Item

    id = factory.Sequence(lambda n: n)
    item_name = FuzzyChoice(choices=["item_dog", "item_cat", "item_b", "item_fish","large_cat_food_is_long_word_test"])
    item_quantity = random.randint(1,11)
    item_price = FuzzyChoice(choices=[10.0,15.46,17.51,199999.2,66,2183])

class ShopcartFactory(factory.Factory):
    """ Creates fake Shopcarts """

    class Meta:
        model = Shopcart

    customer_id = random.randint(1,99999)
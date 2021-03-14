# Copyright 2016, 2019 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyChoice
from service.models import Shopcart

class ShopcartFactory(factory.Factory):
    """ Creates fake shopcart  """

    class Meta:
        model = Shopcart

    id = factory.Sequence(lambda n: n)
    customer_id = factory.Sequence(lambda n: n)
    item_sku = factory.Sequence(lambda n: n)
    #item_name = FuzzyChoice(choices=["item_dog", "item_cat", "item_bird", "item_fish"])
    item_name = "item_dog"
    item_quantity = factory.Sequence(lambda n: n)
    item_quantity = factory.Sequence(lambda n: n)
    
class ItemFactory(factory.Factory):
    pass


from datetime import datetime
from . import consts
import math


def total_calculation(cart_items, delivery_fee) -> int:
    if (cart_items.cart_value >= consts.FREE_DELIVERY_THRESHOLD):
        delivery_fee = 0
    else:
        delivery_fee = cart_value_surcharge(cart_items.cart_value)
        
        delivery_fee += distance_fee(cart_items)
        
        delivery_fee += extra_items_fee(cart_items)
        
        delivery_fee += rush_time_fee(cart_items.time, delivery_fee)

    return min(delivery_fee, consts.MAX_DELIVERY_FEE)

def cart_value_surcharge(cart_value) -> int:
    '''
        This function is used to calculate the minimum required cart value.
        If the cart value is less than 10 euros, it will add the difference 
        between the cart value and 10 euros to the delivery fee.
        Otherwise, it will return 0.
    '''
    cart_value_surcharge = 0
    if (cart_value < consts.MINIMUM_REQUIRED_CART_VALUE):
        cart_value_surcharge = consts.MINIMUM_REQUIRED_CART_VALUE - cart_value
    return cart_value_surcharge

def distance_fee(cart_items) -> int:
    '''
        This function is used to calculate the distance fee.
        If the delivery distance is greater than 1 kilometer, 
        it will add the extra distance fee 1 euro per less than equal 500 meters to the delivery fee.
        Otherwise, it will return 0.
    '''

    extra_distance_fee = consts.BASE_DELIVERY_FEE
    if (cart_items.delivery_distance > consts.FIRST_KILOMETER_THRESHOLD):
        extra_distance = cart_items.delivery_distance - consts.FIRST_KILOMETER_THRESHOLD
        extra_distance_fee = (math.ceil(extra_distance / 500) * 100) + consts.BASE_DELIVERY_FEE
    return extra_distance_fee

def extra_items_fee(cart_items) -> int:
    '''
        This function is used to calculate the extra items fee.
        If the number of items is greater than 4, it will add 50 cents per item to the delivery fee.
        If the number of items is greater than 12, it will add 50 cents per item
        plus it will add 1.2 euros to the delivery fee as a big package fee.
        Otherwise, it will return 0.
    '''
    big_package_fee = consts.BIG_PACKAGE_FEE if (cart_items.number_of_items > consts.BIG_PACKAGE) else 0
    items_extra_surcharge = 0
    if (cart_items.number_of_items > consts.MINIMUM_ITEMS):
        items_extra_surcharge = ((cart_items.number_of_items - consts.MINIMUM_ITEMS) * 50 + big_package_fee)
    return items_extra_surcharge

def rush_time_fee(datetime_object, delivery_fee) -> int:
    '''
        This function is used to calculate the rush time fee.
        If the day is Friday and the time is between 15:00 and 19:00, 
        it will multiply the delivery fee to 1.2X.
        Otherwise, it will return the minimum value between the delivery fee and 15 euros.
    '''
    rushhour_surcharge = 0
    start_rushhour = datetime.strptime("15:00:00", "%H:%M:%S").time()
    end_rushhour = datetime.strptime("19:00:00", "%H:%M:%S").time()
    day = datetime.strftime(datetime_object, "%A")
    if (day == "Friday" and (start_rushhour <= datetime_object.time() <= end_rushhour)):
        rushhour_surcharge = int (consts.RUSH_HOURE_PERCENTAGE * delivery_fee)
    return rushhour_surcharge
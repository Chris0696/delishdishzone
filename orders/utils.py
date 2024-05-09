import datetime
import simplejson as json


def generate_order_number(pk):
    current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')  #300420241349 + pk
    order_number = current_time + str(pk)
    return order_number

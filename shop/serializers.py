import json
from datetime import datetime


def serialize_customer(customer):
    return {
        'id': customer.id,
        'name': customer.name,
        'username': customer.username,
        'email': customer.email,
        'country': customer.country,
        'state': customer.state,
        'city': customer.city,
        'address': customer.address,
        'zipcode': customer.zipcode,
        'date_created': customer.date_created,
        'profile': customer.profile if customer.profile else 'default-profile.png'  # Handle profile attribute
    }






import json

def serialize_order(order):
    # orders_dict = order.orders if isinstance(order.orders, dict) else json.loads(order.orders) if order.orders else {}
    
    return {
        'id': order.id,
        'invoice': order.invoice,
        'status': order.status,
        'date_created': order.date_created,
        # 'orders': orders_dict
    }



    return {
        'id': order.id,
        'status': order.status,
        'total': order.total,  # Make sure this is included
        'date_created': order.date_created
    }




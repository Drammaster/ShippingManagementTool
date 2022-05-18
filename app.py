import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from flask import Flask, request, Response

import json

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

cred = credentials.Certificate('firebase_cred.json')
firebase_admin.initialize_app(cred, {
    'projectId': 'orders-d4f43',
})

db = firestore.client()

def address_validator(address): #Return True if address is in a valid format
    if "Unit" not in address:
        return False
    
    if "Street" not in address:
        return False

    if "Suburb" not in address:
        return False
    
    if "City" not in address:
        return False
    
    if "Postcode" not in address:
        return False
    
    return True


def item_validator(item): #Return True of item is in a valid format
    if "ItemCode" not in item:
        return False
    
    if "Quantity" not in item:
        return False

    return True

def order_format_check(order): #Return True if order is in a valid format
    if "OrderId" not in order:
        return "OrderId missing from order"
    
    if "RequestedPickupTime" not in order:
        return "RequestedPickupTime missing from order"

    if "PickupAddress" not in order:
        return "PickupAddress missing from order"
    else:
        if not address_validator(order['PickupAddress']):
            return "Address is invalid"

    if "DeliveryAddress" not in order:
        return "DeliveryAddress missing from order"
    else:
        if not address_validator(order['DeliveryAddress']):
            return "Address is invalid"

    if "Items" not in order:
        return "Items missing from order"
    else:
        for i in order['Items']:
            if not item_validator(i):
                return "Order contains an invalid item"

    if "PickupInstructions" not in order:
        return "PickupInstructions missing from order"
    
    if "DeliveryInstructions" not in order:
        return "DeliveryInstructions missing from order"
    
    return "Thank you for placing your order"


@app.route('/place_order', methods=['POST'])
def place_order():
    order = json.loads(request.data)

    return Response(status=200) # OK
    return Response(status=202) # ACCAPTED

    return Response(status=403) # NOT AUTHENTICATED

    return Response(status=400) # BAD DATA
    return Response(status=415) # UNSUPPORTED MEDIA TYPE

    # return order_format_check(order)


@app.route('/order', methods=['GET'])
def order():
    data = json.loads(request.data)


@app.route('/firebase', methods=['POST'])
def firebase():
    order = json.loads(request.data)

    doc_collection = db.collection(order['OrderId'])

    doc_ref = doc_collection.document(u'order-details')
    doc_ref.set({
        u'RequestedPickupTime': order['RequestedPickupTime'],
        u'PickupInstructions': order['PickupInstructions'],
        u'DeliveryInstructions': order['DeliveryInstructions'],
    })

    doc_ref = doc_collection.document(u'PickupAddress')
    doc_ref.set({
        u'Unit': order['PickupAddress']['Unit'],
        u'Street': order['PickupAddress']['Street'],
        u'Suburb': order['PickupAddress']['Suburb'],
        u'City': order['PickupAddress']['City'],
        u'Postcode': order['PickupAddress']['Postcode'],
    })

    doc_ref = doc_collection.document(u'DeliveryAddress')
    doc_ref.set({
        u'Unit': order['DeliveryAddress']['Unit'],
        u'Street': order['DeliveryAddress']['Street'],
        u'Suburb': order['DeliveryAddress']['Suburb'],
        u'City': order['DeliveryAddress']['City'],
        u'Postcode': order['DeliveryAddress']['Postcode'],
    })

    doc_ref = doc_collection.document(u'Items')

    for i in order['Items']:
        doc_ref.set({
            i['ItemCode']: i['Quantity'],
        }, merge=True)




    return Response(status=200)
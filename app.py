import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import requests
from flask import Flask, request, Response
import psycopg2

# try:
#     import config
# except:
HOST = "ec2-54-165-90-230.compute-1.amazonaws.com"
DATABASE = "d9b43n4vl9j0uv"
USER = "gkjbbjzwzjmppj"
PORT = "5432"
PASSWORD = "1cccdd63ad5416a76bf858006354e49d663055971c0ecd34edf3b1810d89302e"
DATABASE_URL = "postgres://gkjbbjzwzjmppj:1cccdd63ad5416a76bf858006354e49d663055971c0ecd34edf3b1810d89302e@ec2-54-165-90-230.compute-1.amazonaws.com:5432/d9b43n4vl9j0uv"

import json

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

conn = psycopg2.connect(
    # database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT
    DATABASE_URL
)

conn.autocommit = True

cursor = conn.cursor()

sql_init = '''
CREATE TABLE IF NOT EXISTS ORDERS(
   ORDER_ID CHAR(20) NOT NULL,
   REQUESTED_PICKUP_TIME CHAR(50) NOT NULL,
   PICKUP_INSTRUCTIONS CHAR(255),
   DELIVERY_INSTRUCTIONS CHAR(255),
   PRIMARY KEY(ORDER_ID)
);

CREATE TABLE IF NOT EXISTS DELIVERY_ADDRESS(
   ORDER_ID CHAR(20) NOT NULL,
   UNIT CHAR(20) NOT NULL,
   STREET CHAR(50),
   SUBURB CHAR(50),
   CITY CHAR(255),
   POSTCODE CHAR(20),
   CONSTRAINT fk_order
    FOREIGN KEY(ORDER_ID)
        REFERENCES ORDERS(ORDER_ID)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS PICKUP_ADDRESS(
   ORDER_ID CHAR(20) NOT NULL,
   UNIT CHAR(20) NOT NULL,
   STREET CHAR(50),
   SUBURB CHAR(50),
   CITY CHAR(255),
   POSTCODE CHAR(20),
   CONSTRAINT fk_order
    FOREIGN KEY(ORDER_ID)
        REFERENCES ORDERS(ORDER_ID)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ITEMS(
   ITEM_ID CHAR(20) NOT NULL,
   ORDER_ID CHAR(20) NOT NULL,
   QUANTITY CHAR(20),
   PRIMARY KEY(ITEM_ID),
   CONSTRAINT fk_order
    FOREIGN KEY(ORDER_ID)
        REFERENCES ORDERS(ORDER_ID)
        ON DELETE CASCADE
);
'''

cursor.execute(sql_init)


def create_order(order):
    order_sql = '''
    INSERT INTO ORDERS(ORDER_ID, REQUESTED_PICKUP_TIME, PICKUP_INSTRUCTIONS, DELIVERY_INSTRUCTIONS)
    VALUES (%s,%s,%s,%s)
    '''

    try:
        cursor.execute(order_sql, (order['OrderId'], order['RequestedPickupTime'], order['PickupInstructions'], order['DeliveryInstructions']))
    except:
        pass

    create_del_address(order['OrderId'], order['DeliveryAddress'])
    create_pic_address(order['OrderId'], order['PickupAddress'])
    for i in order['Items']:
        create_item(order['OrderId'], i)


def create_del_address(order_id, del_address):
    del_address_sql = '''
    INSERT INTO DELIVERY_ADDRESS(ORDER_ID, UNIT, STREET, SUBURB, CITY, POSTCODE)
    VALUES (%s,%s,%s,%s,%s,%s)
    '''

    cursor.execute(del_address_sql, (order_id, del_address['Unit'], del_address['Street'], del_address['Suburb'], del_address['City'], del_address['Postcode']))

def create_pic_address(order_id, pic_address):
    pic_address_sql = '''
    INSERT INTO PICKUP_ADDRESS(ORDER_ID, UNIT, STREET, SUBURB, CITY, POSTCODE)
    VALUES (%s,%s,%s,%s,%s,%s)
    '''

    cursor.execute(pic_address_sql, (order_id, pic_address['Unit'], pic_address['Street'], pic_address['Suburb'], pic_address['City'], pic_address['Postcode']))

def create_item(order_id, item):
    item_sql = '''
    INSERT INTO ITEMS(ITEM_ID, ORDER_ID, QUANTITY)
    VALUES (%s,%s,%s)
    '''

    cursor.execute(item_sql, (item['ItemCode'], order_id, item['Quantity']))

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

    
    url = "https://postman-echo.com/basic-auth"
    header = {"Authorization" : "Basic cG9zdG1hbjpwYXNzd29yZA=="}
    response = requests.get(url, headers=header)
    print(response.status_code)
    print(response.json())

    create_order(order)

    return Response(status=200) # OK
    # return Response(status=202) # ACCAPTED

    # return Response(status=403) # NOT AUTHENTICATED

    # return Response(status=400) # BAD DATA
    # return Response(status=415) # UNSUPPORTED MEDIA TYPE

    # return order_format_check(order)


@app.route('/order', methods=['GET'])
def order():
    data = json.loads(request.data)

    doc_ref = db.collection(data['OrderId'])

    doc = doc_ref.get()
    # if doc.exists:
    for i in doc:
        print(i)
    # print(doc)
    # else:
    #     print(u'No such document!')

    return Response(status=200)


@app.route('/all_orders', methods=['GET'])
def all_orders():
    all_orders = db.collection('orders').get()

    print(all_orders)

    return Response(status=200)


@app.route('/firebase', methods=['POST'])
def firebase():
    order = json.loads(request.data)

    db_collection = db.collection(u'orders')

    db_order = db_collection.document(order['OrderId'])

    db_order.set({
        u'RequestedPickupTime': order['RequestedPickupTime'],
        u'PickupInstructions': order['PickupInstructions'],
        u'DeliveryInstructions': order['DeliveryInstructions'],
    })

    db_order.collection(u'PickupAddress').document(u'detials').set({
        u'Unit': order['PickupAddress']['Unit'],
        u'Street': order['PickupAddress']['Street'],
        u'Suburb': order['PickupAddress']['Suburb'],
        u'City': order['PickupAddress']['City'],
        u'Postcode': order['PickupAddress']['Postcode'],
    })
    db_order.collection(u'DeliveryAddress').document(u'detials').set({
        u'Unit': order['DeliveryAddress']['Unit'],
        u'Street': order['DeliveryAddress']['Street'],
        u'Suburb': order['DeliveryAddress']['Suburb'],
        u'City': order['DeliveryAddress']['City'],
        u'Postcode': order['DeliveryAddress']['Postcode'],
    })

    for i in order['Items']:
        db_order.collection(u'Items').document(i['ItemCode']).set({
            u'Quantity': i['Quantity'],
        })

    return Response(status=200)
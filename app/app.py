from flask import Flask, request, Response
import psycopg2, json

try:
    from ..config import DATABASE_URL, USERNAME, PASSWORD
    print("test")
    conn = psycopg2.connect(
        dbname="netlogix", user="postgres", password="root", host="db", port="5432"
    )
except:
    import os
    DATABASE_URL = os.environ.get('DATABASE_URL')
    USERNAME = os.environ.get('USERNAME')
    PASSWORD = os.environ.get('PASSWORD')
    conn = psycopg2.connect(
        DATABASE_URL
    )

import database

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

conn.autocommit = True

cursor = conn.cursor()

cursor.execute(database.sql_init)


def create_order(order):
    try:
        cursor.execute(database.create_order_sql, (order['OrderId'], order['RequestedPickupTime'], order['PickupInstructions'], order['DeliveryInstructions']))
    except:
        pass

    create_del_address(order['OrderId'], order['DeliveryAddress'])
    create_pic_address(order['OrderId'], order['PickupAddress'])
    for i in order['Items']:
        create_item(order['OrderId'], i)


def create_del_address(order_id, del_address):
    cursor.execute(database.create_delivery_address_sql, (order_id, del_address['Unit'], del_address['Street'], del_address['Suburb'], del_address['City'], del_address['Postcode']))


def create_pic_address(order_id, pic_address):
    cursor.execute(database.create_pickup_address_sql, (order_id, pic_address['Unit'], pic_address['Street'], pic_address['Suburb'], pic_address['City'], pic_address['Postcode']))


def create_item(order_id, item):
    try:
        cursor.execute(database.create_item_sql, (item['ItemCode'], order_id, item['Quantity']))
    except:
        pass


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

    auth_gotten = request.authorization

    if USERNAME != auth_gotten['username'] or PASSWORD != auth_gotten['password']:
        return Response(status=401)
    else:

        create_order(order)

        return Response(status=202) # OK

    # return Response(status=202) # ACCAPTED

    # return Response(status=403) # NOT AUTHENTICATED

    # return Response(status=400) # BAD DATA
    # return Response(status=415) # UNSUPPORTED MEDIA TYPE

    # return order_format_check(order)


@app.route('/get_order', methods=['GET'])
def get_order():
    data = json.loads(request.data)

    order_sql = '''
    SELECT * FROM ORDERS
    WHERE Order_id LIKE '%{0}%'
    '''.format(data['OrderId'])
    
    pick_address_sql = '''
    SELECT * FROM PICKUP_ADDRESS
    WHERE Order_id LIKE '%{0}%'
    '''.format(data['OrderId'])
    
    deliv_address_sql = '''
    SELECT * FROM DELIVERY_ADDRESS
    WHERE Order_id LIKE '%{0}%'
    '''.format(data['OrderId'])
    
    items_sql = '''
    SELECT * FROM ITEMS
    WHERE Order_id LIKE '%{0}%'
    '''.format(data['OrderId'])

    cursor.execute(order_sql)
    order = cursor.fetchone()

    if order == None:
        return "Order does not exist"
    else:
        cursor.execute(pick_address_sql)
        pick_address = cursor.fetchone()

        cursor.execute(deliv_address_sql)
        deliv_address = cursor.fetchone()


        items_list = []
        cursor.execute(items_sql)
        items = cursor.fetchall()

        for i in items:
            items_list.append({
                "ItemCode": i[0].rstrip(),
                "Quantity": i[2].rstrip()
            })

        order_format = { 
            "OrderId": order[0].rstrip(),
            "RequestedPickupTime" : order[1].rstrip(),
            "PickupAddress":
                {
                    "Unit": pick_address[1].rstrip(),
                    "Street": pick_address[2].rstrip(),
                    "Suburb": pick_address[3].rstrip(),
                    "City": pick_address[4].rstrip(),
                    "Postcode": pick_address[5].rstrip()
                },
            "DeliveryAddress":
                {
                    "Unit": deliv_address[1].rstrip(),
                    "Street": deliv_address[2].rstrip(),
                    "Suburb": pick_address[3].rstrip(),
                    "City": deliv_address[4].rstrip(),
                    "Postcode": deliv_address[5].rstrip()
                },
            "Items": items_list,
            "PickupInstructions": order[2].rstrip(),
            "DeliveryInstructions": order[3].rstrip()
        }

        return order_format


@app.route('/all_orders', methods=['GET'])
def all_orders():
    all_orders_list = []

    cursor.execute('''SELECT * FROM ORDERS''')
    all_orders = cursor.fetchall()

    cursor.execute('''SELECT * FROM PICKUP_ADDRESS''')
    all_picup_address = cursor.fetchall()

    cursor.execute('''SELECT * FROM DELIVERY_ADDRESS''')
    all_delivery_address = cursor.fetchall()

    cursor.execute('''SELECT * FROM ITEMS''')
    all_items = cursor.fetchall()

    for order in all_orders:
        p_count = 0
        d_count = 0
        i_count = 0

        for p_address in all_picup_address:
            if p_address[0].rstrip() == order[0].rstrip():
                pick_address = all_picup_address.pop(p_count)

            p_count += 1
        
        for d_address in all_delivery_address:
            if d_address[0].rstrip() == order[0].rstrip():
                deliv_address = all_delivery_address.pop(d_count)
                
            d_count += 1
        
        order_format = { 
            "OrderId": order[0].rstrip(),
            "RequestedPickupTime" : order[1].rstrip(),
            "PickupAddress":
                {
                    "Unit": pick_address[1].rstrip(),
                    "Street": pick_address[2].rstrip(),
                    "Suburb": pick_address[3].rstrip(),
                    "City": pick_address[4].rstrip(),
                    "Postcode": pick_address[5].rstrip()
                },
            "DeliveryAddress":
                {
                    "Unit": deliv_address[1].rstrip(),
                    "Street": deliv_address[2].rstrip(),
                    "Suburb": deliv_address[3].rstrip(),
                    "City": deliv_address[4].rstrip(),
                    "Postcode": deliv_address[5].rstrip()
                },
            "Items": [],
            "PickupInstructions": order[2].rstrip(),
            "DeliveryInstructions": order[3].rstrip()
        }

        all_orders_list.append(order_format)

    print(all_orders_list)

    
    return Response(status=200)
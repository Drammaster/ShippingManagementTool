from flask import Flask, request, Response
import psycopg2, json
import database
import datetime


import os
DATABASE_URL = os.environ.get('DATABASE_URL')
USERNAME = "username"
PASSWORD = "password"

conn = psycopg2.connect(
    "postgres://gkjbbjzwzjmppj:1cccdd63ad5416a76bf858006354e49d663055971c0ecd34edf3b1810d89302e@ec2-54-165-90-230.compute-1.amazonaws.com:5432/d9b43n4vl9j0uv"
)

from validators import get_order_validator, order_format_check


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


def create_trip_function():


    cursor.execute(database.create_trip_sql, ("FIRST_TRIP","start", "end", 10, 10, datetime.date.today(), "carrier code"))

    #some logic

    # database.create_trip_order_ref_sql

    # trip = {
    #     "ID": "",
    #     "start": "",
    #     "end": "",
    #     "distance": "",
    #     "fuel": "",
    #     "planned date": "",
    #     "orderIDs": [],
    #     "carrier code": ""
    # }


@app.route('/place_order', methods=['POST'])
def place_order():
    order = json.loads(request.data)

    auth_gotten = request.authorization
    
    if auth_gotten == None:
        return Response(status=401)
    else:
        if USERNAME != auth_gotten['username'] or PASSWORD != auth_gotten['password']:
            return Response(status=401)
        else:

            if order_format_check(order):
                create_order(order)

                return Response(status=202)
            else:
                return Response(status=400)


@app.route('/get_order', methods=['GET'])
def get_order():
    data = json.loads(request.data)

    auth_gotten = request.authorization
    
    if auth_gotten == None:
        return Response(status=401)
    else:

        if USERNAME != auth_gotten['username'] or PASSWORD != auth_gotten['password']:
            return Response(status=401)
        else:

            if get_order_validator(data):
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
            else:
                return Response(status=400)


@app.route('/all_orders', methods=['GET'])
def all_orders():
    auth_gotten = request.authorization
    
    if auth_gotten == None:
        return Response(status=401)
    else:
        
        if USERNAME != auth_gotten['username'] or PASSWORD != auth_gotten['password']:
            return Response(status=401)
        else:

            all_order_ids = []

            cursor.execute('''SELECT * FROM ORDERS''')
            all_orders = cursor.fetchall()

            for i in all_orders:
                all_order_ids.append(i[0].rstrip())

            all_orders_dict = dict.fromkeys(all_order_ids, "OrderId")

            return all_orders_dict


@app.route('/create_trip', methods=['POST'])
def create_trip():
    auth_gotten = request.authorization
    
    if auth_gotten == None:
        return Response(status=401)
    else:
        
        if USERNAME != auth_gotten['username'] or PASSWORD != auth_gotten['password']:
            return Response(status=401)
        else:

            create_trip_function()

            return Response(status=202) 

if __name__ == "__main__":
    app.run(debug=False)
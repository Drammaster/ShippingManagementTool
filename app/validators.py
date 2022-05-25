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
        return False
    
    if "RequestedPickupTime" not in order:
        return False

    if "PickupAddress" not in order:
        return False
    else:
        if not address_validator(order['PickupAddress']):
            return False

    if "DeliveryAddress" not in order:
        return False
    else:
        if not address_validator(order['DeliveryAddress']):
            return False

    if "Items" not in order:
        return False
    else:
        for i in order['Items']:
            if not item_validator(i):
                return False

    if "PickupInstructions" not in order:
        return False
    
    if "DeliveryInstructions" not in order:
        return False
    
    return True


def get_order_validator(order_id): #Return True if get order is in a valid format
    if "OrderId" not in order_id:
        return False

    return True
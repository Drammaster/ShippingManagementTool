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


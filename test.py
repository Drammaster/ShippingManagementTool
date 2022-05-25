import unittest
import app.validators as validators

class TestCases(unittest.TestCase):
    def test_address_validator(self):
        self.assertTrue(validators.address_validator(
            {
                "Unit": "174",
                "Street": "West Tamaki Road",
                "Suburb": "Glendowie",
                "City": "Auckland",
                "Postcode": "1072"
            }
        ))
        self.assertFalse(validators.address_validator(
            {
                "Street": "West Tamaki Road",
                "Suburb": "Glendowie",
                "City": "Auckland",
                "Postcode": "1072"
            }
        ))
        self.assertFalse(validators.address_validator(
            {
                "Unit": "174",
                "Suburb": "Glendowie",
                "City": "Auckland",
                "Postcode": "1072"
            }
        ))
        self.assertFalse(validators.address_validator(
            {
                "Unit": "174",
                "Street": "West Tamaki Road",
                "City": "Auckland",
                "Postcode": "1072"
            }
        ))
        self.assertFalse(validators.address_validator(
            {
                "Unit": "174",
                "Street": "West Tamaki Road",
                "Suburb": "Glendowie",
                "Postcode": "1072"
            }
        ))
        self.assertFalse(validators.address_validator(
            {
                "Unit": "174",
                "Street": "West Tamaki Road",
                "Suburb": "Glendowie",
                "City": "Auckland"
            }
        ))

    def test_item_validator(self):
        self.assertTrue(validators.item_validator(
            {
                "ItemCode": "AMZ-01",
                "Quantity": 10
            }
        ))
        self.assertTrue(validators.item_validator(
            {
                "ItemCode": "AMZ-02",
                "Quantity": 2
            }
        ))
        self.assertFalse(validators.item_validator(
            {
                "Quantity": 1
            }
        ))
        self.assertFalse(validators.item_validator(
            {
                "ItemCode": "AMZ-02"
            }
        ))
        self.assertFalse(validators.item_validator(
            {
                "FastFood": "KFC"
            }
        ))

    def test_order_format_check(self):
        self.assertTrue(validators.order_format_check(
            { 
                "OrderId": "CH-1001",
                "RequestedPickupTime" : "2022/05/19 07:00:00",
                "PickupAddress":
                    {
                        "Unit": "174",
                        "Street": "West Tamaki Road",
                        "Suburb": "Glendowie",
                        "City": "Auckland",
                        "Postcode": "1072"
                    },
                "DeliveryAddress":
                    {
                        "Unit": "35",
                        "Street": "Over the hill street",
                        "Suburb": "Mountaintop Place",
                        "City": "Shelbyville",
                        "Postcode": "2013"
                    },
                "Items": [
                    {
                    "ItemCode": "AMZ-02",
                    "Quantity": 1
                    }
                ],
                "PickupInstructions": "Be gentel",
                "DeliveryInstructions": "Place infront of the door"
            }
        ))
        self.assertTrue(validators.order_format_check(
            { 
                "OrderId": "DE-20",
                "RequestedPickupTime" : "2022/05/19 07:00:00",
                "PickupAddress":
                    {
                        "Unit": "174",
                        "Street": "West Tamaki Road",
                        "Suburb": "Glendowie",
                        "City": "Auckland",
                        "Postcode": "1072"
                    },
                "DeliveryAddress":
                    {
                        "Unit": "35",
                        "Street": "Over the hill street",
                        "Suburb": "Mountaintop Place",
                        "City": "Shelbyville",
                        "Postcode": "2013"
                    },
                "Items": [
                    {
                    "ItemCode": "AMZ-02",
                    "Quantity": 1
                    },
                    {
                    "ItemCode": "AMZ-200",
                    "Quantity": 100
                    },
                ],
                "PickupInstructions": "Quickly Please",
                "DeliveryInstructions": "Throw through window"
            }
        ))
        self.assertFalse(validators.order_format_check(
            { 
                "OrderId": "DE-20",
                "RequestedPickupTime" : "2022/05/19 07:00:00",
                "PickupAddress":
                    {
                        "Unit": "174",
                        "Street": "West Tamaki Road",
                        "Suburb": "Glendowie",
                        "City": "Auckland",
                        "Postcode": "1072"
                    },
                "DeliveryAddress":
                    {
                        "Unit": "35",
                        "Street": "Over the hill street",
                        "Suburb": "Mountaintop Place",
                        "City": "Shelbyville",
                        "Postcode": "2013"
                    },
                "Items": [
                    {
                    "ItemCode": "AMZ-02",
                    "Quantity": 1
                    },
                    {
                    "ItemCode": "AMZ-200",
                    "Quantity": 100
                    },
                ],
                "PickupInstructions": "Quickly Please"
            }
        ))
        self.assertFalse(validators.order_format_check(
            { 
                "OrderId": "DE-20",
                "PickupAddress":
                    {
                        "Unit": "174",
                        "Street": "West Tamaki Road",
                        "Suburb": "Glendowie",
                        "City": "Auckland",
                        "Postcode": "1072"
                    },
                "DeliveryAddress":
                    {
                        "Unit": "35",
                        "Street": "Over the hill street",
                        "Suburb": "Mountaintop Place",
                        "City": "Shelbyville",
                        "Postcode": "2013"
                    },
                "PickupInstructions": "Quickly Please"
            }
        ))

    def test_get_order_validator(self):
        self.assertTrue(validators.get_order_validator(
            {
                "OrderId": "BC-1"
            }
        ))
        self.assertFalse(validators.get_order_validator(
            {
                
            }
        ))
        self.assertFalse(validators.get_order_validator(
            {
                "Food": "Cheeseburger"
            }
        ))

if __name__ == '__main__':
    unittest.main()
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

    def test_items(self):
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

    def test_order_format(self):
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


if __name__ == '__main__':
    unittest.main()
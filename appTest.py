import unittest
from app import app, db, catalog, purchases

class TestCatalog(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.catalog_data = [
            {'item': 'item1', 'price': 10},
            {'item': 'item2', 'price': 20},
            {'item': 'item3', 'price': 30}
        ]
        self.purchases_data = [
            {'item': 'item1', 'price': 10, 'date': '2023-04-17 10:00:00'},
            {'item': 'item2', 'price': 20, 'date': '2023-04-17 11:00:00'}
        ]
        catalog.insert_many(self.catalog_data)
        purchases.insert_many(self.purchases_data)

    def tearDown(self):
        catalog.delete_many({})
        purchases.delete_many({})

if __name__ == '__main__':
    unittest.main()        
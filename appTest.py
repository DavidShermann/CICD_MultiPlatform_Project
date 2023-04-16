import unittest
import app

class FlaskTest(unittest.TestCase):

    # Check if the app is running and returning 200 status code
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    # Check if the new product is inserted in the catalog
    def test_insert_product(self):
        tester = app.test_client(self)
        response = tester.post("/insert_product/", data=dict(insert_product_name='Product X', insert_product_price=10), follow_redirects=True)
        self.assertIn(b'Product X', response.data)

    # Check if the product is deleted from the catalog
    def test_delete_product(self):
        tester = app.test_client(self)
        response = tester.post("/delete_product/", data=dict(product_1='on'), follow_redirects=True)
        self.assertNotIn(b'Product 1', response.data)

if __name__ == '__main__':
    unittest.main()        
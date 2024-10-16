from django.test import TestCase
from .models import Product, Order

class ProductOrderTestCase(TestCase):

    def setUp(self):
        # Set up initial product
        self.product = Product.objects.create(
            name="Test Product",
            description="This is a test product.",
            price=100.00
        )

    def test_product_creation(self):
        # Test product creation
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.description, "This is a test product.")
        self.assertEqual(self.product.price, 100.00)

    def test_order_creation(self):
        # Test order creation
        order = Order.objects.create(product=self.product, quantity=2, total_price=200.00)
        self.assertEqual(order.product, self.product)
        self.assertEqual(order.quantity, 2)
        self.assertEqual(order.total_price, 200.00)

    def test_order_total_price(self):
        # Test if total price is correctly calculated
        quantity = 3
        total_price = self.product.price * quantity
        order = Order.objects.create(product=self.product, quantity=quantity, total_price=total_price)
        self.assertEqual(order.total_price, 300.00)

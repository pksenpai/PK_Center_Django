from django.test import TestCase
from apps.items.models import Item
from apps.users.models import Address
from apps.orders.models import Order, OrderItem, Discount
from django.contrib.auth import get_user_model; User = get_user_model()

from django.urls import reverse
from django.db import IntegrityError
from django.core.exceptions import ValidationError


class OrderTests(TestCase):
    
    fixtures = [
        "categories.json",
        "items.json",
        "users.json",
        "addresses.json",
    ]
    
    def setUp(self):
        
        """\___________________[USER]___________________/"""
        self.user1 = User.objects.get(id=1)
        self.user2 = User.objects.get(id=2)
        self.user3 = User.objects.get(id=3)
        
        """\___________________[ITEM]___________________/"""
        self.item1 = Item.objects.get(id=1)
        self.item2 = Item.objects.get(id=2)
        
        """\___________________[ADDRESS]___________________/"""
        self.address1 = Address.objects.get(id=1)
        self.address2 = Address.objects.get(id=2)
        self.address3 = Address.objects.get(id=3)
        
        """\___________________[ORDER]___________________/"""
        self.order1 = Order.objects.create(
            status = "In Card",
            created_at = "2023-02-01",
            updated_at = "2023-01-22",
            receiving_date = "2023-03-23",
            # item = set(self.item1),
            user = self.user1,
            address = self.address1
        )
        self.order2 = Order.objects.create(
            status = "In Process",
            created_at = "2023-01-22",
            updated_at = "2023-01-22",
            receiving_date = "2023-02-03",
            # item = set(self.item2),
            user = self.user1,
            address = self.address2
        )
        self.order3 = Order.objects.create(
            status= "Done",
            created_at= "2021-02-23",
            updated_at= "2021-02-23",
            receiving_date= "2022-10-15",
            # item = set(self.item1),
            user= self.user2,
            address= self.address3
        )
        
    """\_______________[UNIQUE]_______________/"""
    def test_unique_id(self):
        with self.assertRaises(IntegrityError):
            Order.objects.create(
                status         = "In Card",
                receiving_date = "2023-03-23",
                user           = self.user1,
                address        = self.address1,
                id             = 1, # this id already EXISTS!
            )
        
    """\_______________[MANDATORY]_______________/"""
    def test_has_status(self):
        self.assertEqual(self.order1.status, "In Card")
        self.assertEqual(self.order2.status, "In Process")
        self.assertEqual(self.order3.status, "Done")
        
    def test_has_receiving_date(self):
        self.assertEqual(self.order1.receiving_date, "2023-03-23")
        self.assertEqual(self.order2.receiving_date, "2023-02-03")
        self.assertEqual(self.order3.receiving_date, "2022-10-15")

    # def test_has_item(self): TEST IT LATER!!! ASK IT LATER !!!
    #     self.assertEqual(self.order1.item, self.item1)
    #     self.assertEqual(self.order2.item, self.item2)
    #     self.assertEqual(self.order3.item, self.item1)

    def test_has_user(self):
        self.assertEqual(self.order1.user, self.user1)
        self.assertEqual(self.order2.user, self.user1)
        self.assertEqual(self.order3.user, self.user2)

    def test_has_address(self):
        self.assertEqual(self.order1.address, self.address1)
        self.assertEqual(self.order2.address, self.address2)
        self.assertEqual(self.order3.address, self.address3)

    """\_______________[METHOD]_______________/"""
    def test_get_absolute_url(self):
        order1_expected_url = reverse(
            "orders:order_details",
            args=[
                self.order1.id
            ]
        )
        order2_expected_url = reverse(
            "orders:order_details",
            args=[
                self.order2.id
            ]
        )
        order3_expected_url = reverse(
            "orders:order_details",
            args=[
                self.order3.id
            ]
        )
        
        order1_actual_url = self.order1.get_absolute_url()
        order2_actual_url = self.order2.get_absolute_url()
        order3_actual_url = self.order3.get_absolute_url()
        
        self.assertEqual(
            order1_expected_url,
            order1_actual_url,
        )
    
        self.assertEqual(
            order2_expected_url,
            order2_actual_url,
        )
        
        self.assertEqual(
            order3_expected_url,
            order3_actual_url,
        )
        
    def test_str(self):
        order1_expected_str = "sogol123"
        order2_expected_str = "sogol123"
        order3_expected_str = "S2arKhamBoY"
        
        order1_actual_str = str(self.order1)
        order2_actual_str = str(self.order2)
        order3_actual_str = str(self.order3)

        self.assertEqual(
            order1_expected_str,
            order2_actual_str,
            )
        
        self.assertEqual(
            order2_expected_str,
            order2_actual_str,
            )
        
        self.assertEqual(
            order3_expected_str,
            order3_actual_str,
        )
        
        
class OrderItemTest(TestCase):
    
    fixtures = [
        "categories.json",
        "users.json",
        "addresses.json",
        "items.json",
    ]
    
    def setUp(self):
        """\___________________[USER]___________________/"""
        self.user1 = User.objects.get(id=1)
        self.user2 = User.objects.get(id=2)
        self.user3 = User.objects.get(id=3)
        
        """\___________________[ADDRESS]___________________/"""
        self.address1 = Address.objects.get(id=1)
        self.address2 = Address.objects.get(id=2)
        self.address3 = Address.objects.get(id=3)
        
        """\___________________[ORDER]___________________/"""
        self.order1 = Order.objects.create(
            status = "In Card",
            created_at = "2023-02-01",
            updated_at = "2023-01-22",
            receiving_date = "2023-03-23",
            user = self.user1,
            address = self.address1
        )
        self.order2 = Order.objects.create(
            status = "In Process",
            created_at = "2023-01-22",
            updated_at = "2023-01-22",
            receiving_date = "2023-02-03",
            user = self.user1,
            address = self.address2
        )
        self.order3 = Order.objects.create(
            status= "Done",
            created_at= "2021-02-23",
            updated_at= "2021-02-23",
            receiving_date= "2022-10-15",
            user= self.user2,
            address= self.address3
        )
    
        """\___________________[ITEM]___________________/"""
        self.item1 = Item.objects.get(id=1)
        self.item2 = Item.objects.get(id=2)
        
        """\___________________[ORDERITEM]___________________/"""
        self.orderitem1 = OrderItem.objects.create(
            count = 2,
            order = self.order1,
            item  = self.item1,
        )
        self.orderitem2 = OrderItem.objects.create(
            count = 3,
            order = self.order2,
            item  = self.item2,
        )
        self.orderitem3 = OrderItem.objects.create(
            count = 4,
            order = self.order3,
            item  = self.item1,
        )
        
    """\_______________[MANDATORY]_______________/"""
    
    def test_has_count(self):
        self.assertEqual(self.orderitem1.count, 2)
        self.assertEqual(self.orderitem2.count, 3)
        self.assertEqual(self.orderitem3.count, 4)
        
    def test_has_order(self):
        self.assertEqual(self.orderitem1.order, self.order1)
        self.assertEqual(self.orderitem2.order, self.order2)
        self.assertEqual(self.orderitem3.order, self.order3)
        
    def test_has_item(self):
        self.assertEqual(self.orderitem1.item, self.item1)
        self.assertEqual(self.orderitem2.item, self.item2)
        self.assertEqual(self.orderitem3.item, self.item1)

        
class DiscountTest(TestCase):
    
    fixtures = [
        "categories.json",
        "users.json",
        "addresses.json",
        "items.json",
    ]
    
    def setUp(self):

        """\___________________[USER]___________________/"""
        self.user1 = User.objects.get(id=1)
        self.user2 = User.objects.get(id=2)
        self.user3 = User.objects.get(id=3)
        
        """\___________________[ADDRESS]___________________/"""
        self.address1 = Address.objects.get(id=1)
        self.address2 = Address.objects.get(id=2)
        self.address3 = Address.objects.get(id=3)
        
        """\___________________[ORDER]___________________/"""
        self.order1 = Order.objects.create(
            status = "In Card",
            created_at = "2023-02-01",
            updated_at = "2023-01-22",
            receiving_date = "2023-03-23",
            user = self.user1,
            address = self.address1
        )
        self.order2 = Order.objects.create(
            status = "In Process",
            created_at = "2023-01-22",
            updated_at = "2023-01-22",
            receiving_date = "2023-02-03",
            user = self.user1,
            address = self.address2
        )
        
        """\___________________[ITEM]___________________/"""
        self.item1 = Item.objects.get(id=1)
        self.item2 = Item.objects.get(id=2)
        
        """\_________________[DISCOUNT]_________________/"""
        self.discount1 = Discount.objects.create(
            mode = "Percent Mode",
            percent = 30,
            expire_datetime = "2024-04-07 12:00:00",
            count = 1,
            item = self.item1,
        )
        self.discount2 = Discount.objects.create(
            mode = "Cash Mode",
            cash = 30_000.99,
            expire_datetime = "2025-07-07 12:00:00",
            count = 5,
            order = self.order2,
        )
        self.discount3 = Discount.objects.create(
            mode = "Percent Mode",
            percent = 70,
            expire_datetime = "2030-04-07 12:00:00",
            count = 0,
            item = self.item2,
        )
        
    """\_______________[MANDATORY]_______________/"""
    
    def test_has_mode(self):
        self.assertEqual(self.discount1.mode, "Percent Mode")
        self.assertEqual(self.discount2.mode, "Cash Mode")
        self.assertEqual(self.discount3.mode, "Percent Mode")
   
    def test_has_expire_datetime(self):
        self.assertIsNotNone(self.discount1.expire_datetime)
        self.assertIsNotNone(self.discount2.expire_datetime)
        self.assertIsNotNone(self.discount3.expire_datetime)
   
    def test_has_count(self):
        self.assertTrue(self.discount1.count)
        self.assertTrue(self.discount2.count)
        self.assertFalse(self.discount3.count)
       
    """\_______________[METHOD]_______________/"""
    
    def test_str(self):
        discount1_expected_str = "Percent Mode"
        discount2_expected_str = "Cash Mode"
        discount3_expected_str = "Percent Mode"
        
        discount1_actual_str = str(self.discount1)
        discount2_actual_str = str(self.discount2)
        discount3_actual_str = str(self.discount3)

        self.assertEqual(
            discount1_expected_str,
            discount1_actual_str,
        )
        
        self.assertEqual(
            discount2_expected_str,
            discount2_actual_str,
        )

        self.assertEqual(
            discount3_expected_str,
            discount3_actual_str,
        )
    
    def test_clean(self):
        with self.assertRaises(IntegrityError):
            Discount.objects.create(
                mode = "Cash Mode",
                cash = 30_000,
                expire_datetime = "2018-07-07 12:00:00",
                count = 5,
                order = self.order2,
            )
        
    def test_clean_mode(self):
        with self.assertRaises(IntegrityError):
            Discount.objects.create(
                mode = "Cash Mode",
                percent = 30,
                cash = 30_000,
                expire_datetime = "2025-07-07 12:00:00",
                count = 5,
                item = self.item1
            )
    

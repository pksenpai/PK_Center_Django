from django.test import TestCase
from apps.sellers.models import Seller
from apps.core.models import Category
from apps.items.models import Item, Rating
from django.contrib.auth import get_user_model; User = get_user_model()


from django.urls import reverse
from django.db import IntegrityError
from django.core.exceptions import ValidationError


class ItemTests(TestCase):
    
    fixtures = ["categories.json", "users.json", "items.json"]
    
    def setUp(self):
        """\___________________[ITEM]___________________/"""
        self.car = Item.objects.get(id=1)
        self.pc1 = Item.objects.get(id=2)
        self.pc2 = Item.objects.get(id=3)
        self.usb = Item.objects.get(id=4)
    
    """\_______________[MANDATORY]_______________/"""
    
    def test_has_name(self):
        self.assertEqual(self.car.name, "Ford Mostang 1969")
        self.assertEqual(self.pc1.name, "Asus 1080xp")
        self.assertEqual(self.pc2.name, "IBM xc4000D")
        self.assertEqual(self.usb.name, "USB xpk003")
        
    def test_has_brand(self):
        self.assertEqual(self.car.brand, "Ford")
        self.assertEqual(self.pc1.brand, "Asus")
        self.assertEqual(self.pc2.brand, "IBM")
        self.assertEqual(self.usb.brand, "PK")
        
    def test_has_price(self):
        self.assertTrue(self.car.price)
        self.assertTrue(self.pc1.price)
        self.assertTrue(self.pc2.price)
        self.assertTrue(self.usb.price)
        
    def test_has_category(self):
        self.assertTrue(self.car.category)
        self.assertTrue(self.pc1.category)
        self.assertTrue(self.pc2.category)
        self.assertTrue(self.usb.category)
        
    def test_has_seller(self):
        self.assertTrue(self.car.seller)
        self.assertTrue(self.pc1.seller)
        self.assertTrue(self.pc2.seller)
        self.assertTrue(self.usb.seller)
        
    """\_______________[METHOD]_______________/"""
    def test_get_absolute_url(self):
        car_expected_url = reverse(
            "items:item_details",
            args=[
                self.car.id
            ]
        )
        usb_expected_url = reverse(
            "items:item_details",
            args=[
                self.usb.id
            ]
        )
        
        car_actual_url = self.car.get_absolute_url()
        usb_actual_url = self.usb.get_absolute_url()
        
        self.assertEqual(
            car_expected_url,
            car_actual_url,
        )
    
        self.assertEqual(
            usb_expected_url,
            usb_actual_url,
        )

    def test_str(self):
        car_expected_str = "Ford Mostang 1969"
        pc1_expected_str = "Asus 1080xp"
        pc2_expected_str = "IBM xc4000D"
        usb_expected_str = "USB xpk003"
        
        car_actual_str = str(self.car)
        pc1_actual_str = str(self.pc1)
        pc2_actual_str = str(self.pc2)
        usb_actual_str = str(self.usb)
        
        self.assertEqual(
            car_expected_str,
            car_actual_str,
            )
        
        self.assertEqual(
            pc1_expected_str,
            pc1_actual_str,
            )
        
        self.assertEqual(
            pc2_expected_str,
            pc2_actual_str,
        )
        
        self.assertEqual(
            usb_expected_str,
            usb_actual_str,
        )
     
        
class ScoreTests(TestCase):
       
    fixtures = ["categories.json", "users.json", "items.json"]
    
    def setUp(self):
        """\___________________[USER]___________________/"""
        self.user1 = User.objects.get(id=1)
        self.user2 = User.objects.get(id=1)
        self.user3 = User.objects.get(id=2)
        
        """\___________________[ITEM]___________________/"""
        self.item1 = Item.objects.get(id=1)
        self.item2 = Item.objects.get(id=2)
        
        """\___________________[RATING]___________________/"""
        
        self.rate1 = Rating.objects.create(
            user  = self.user1,
            item  = self.item1,
            score = "4"
        )

        self.rate2 = Rating.objects.create(
            user  = self.user2,
            item  = self.item2,
            score = "2"
        )
    
        self.rate3 = Rating.objects.create(
            user  = self.user3,
            item  = self.item2,
            score = "1"
        )

    """\_______________[MANDATORY]_______________/"""
    
    def test_has_score(self):
        self.assertEqual(self.rate1.score, "4")
        self.assertEqual(self.rate2.score, "2")
        self.assertEqual(self.rate3.score, "1")
        
    def test_has_user(self):
        self.assertEqual(self.rate1.user, self.user1)
        self.assertEqual(self.rate2.user, self.user2)
        self.assertEqual(self.rate3.user, self.user3)
        
    def test_has_item(self):
        self.assertEqual(self.rate1.item, self.item1)
        self.assertEqual(self.rate2.item, self.item2)
        self.assertEqual(self.rate3.item, self.item2)
                
    """\_______________[METHOD]_______________/"""
    
    def test_cached_average(self):... # cover it later!
    def test_clean(self):
        rate1 = Rating.objects.create(
            user = self.user1,
            item = self.item1,
            score = "1",
        )
        rate2 = Rating.objects.create(
            user = self.user1,
            item = self.item1,
            score = "4",
        )
        
        self.assertRaises(ValidationError, rate1.clean)
        self.assertRaises(ValidationError, rate2.clean)
    
    def test_str(self):
        rate1_expected_str = "4"
        rate2_expected_str = "2"
        rate3_expected_str = "1"
        
        rate1_actual_str = str(self.rate1)
        rate2_actual_str = str(self.rate2)
        rate3_actual_str = str(self.rate3)
        
        self.assertEqual(
            rate1_expected_str,
            rate1_actual_str,
            )
        
        self.assertEqual(
            rate2_expected_str,
            rate2_actual_str,
            )
        
        self.assertEqual(
            rate3_expected_str,
            rate3_actual_str,
        )
        

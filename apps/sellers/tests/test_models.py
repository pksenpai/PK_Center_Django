from django.test import TestCase
from apps.sellers.models import Seller
from django.contrib.auth import get_user_model; User = get_user_model()

from django.urls import reverse
from django.db import IntegrityError
from django.core.exceptions import ValidationError


class SellerTests(TestCase):
    
    fixtures = ['seller_users.json']
    
    def setUp(self):
        """\___________________[USER]___________________/"""
        self.user1 = User.objects.get(username="SoSShop", is_seller=True)
        self.user2 = User.objects.get(username="masazone", is_seller=True)
        self.user3 = User.objects.get(username="mmmmmmmmm123", is_seller=True)
        
        self.user4 = User.objects.create(
                username = 'test',
                password = 'abc123test'
            )
        
        """\___________________[SELLER]___________________/"""
        
        # SoS Shop
        self.seller1 = Seller.objects.create(
                user        = self.user1,
                rank        = None,
                name        = "SoS Shop",
                description = "Sos is the best Sos in the world! we are new in pk center! please support us! :3"
            )
        
        # Masazone Shop
        self.seller2 = Seller.objects.create(
                user        = self.user2,
                rank        = 7,
                name        = "Masazone Shop",
                description = "We are a shop that sell best books around the world. Quality is more important to us than quantity!"
            )

        # M Shop
        self.seller3 = Seller.objects.create(
                user        = self.user3,
                rank        = 2,
                name        = "M Shop",
                description = "We are ...!"
            )
        
    """\_______________[MANDATORY]_______________/"""
    
    def test_has_name(self):
        self.assertEqual(self.seller1.name, "SoS Shop")
        self.assertEqual(self.seller2.name, "Masazone Shop")
        
    def test_has_rank(self):
        self.assertIsNone(self.seller1.rank)
        self.assertEqual(self.seller2.rank, 7)
        
    def test_has_user(self):
        self.assertEqual(self.seller1.user, self.user1)
        self.assertEqual(self.seller2.user, self.user2)
        
    """\_______________[UNIQUE]_______________/"""

    def test_unique_id(self):
        with self.assertRaises(IntegrityError):
            Seller.objects.create(
                user = self.user4,
                name = 'test',
                id   = 1, # this id already EXISTS!
            )
            
    def test_unique_name(self):
        with self.assertRaises(IntegrityError):
            Seller.objects.create(
                User = self.user4,
                name = "Masazone Shop",
            )

    def test_unique_rank(self):
        with self.assertRaises(IntegrityError):
            Seller.objects.create(
                user = self.user4,
                name = "test",
                rank = 7,
            )
            
    def test_unique_user(self):
        with self.assertRaises(IntegrityError):
            Seller.objects.create(
                user = self.user1,
                name = "test"
            )

    """\________________[ROLE]________________/"""
        
    def test_is_seller(self):
        self.assertEqual(self.seller1.is_seller, True)
        self.assertEqual(self.seller2.is_seller, True)

    """\_______________[METHOD]_______________/"""

    def test_str(self):
        seller1_expected_str = "SoS Shop"
        seller2_expected_str = "Masazone Shop"

        seller1_actual_str = str(self.seller1)
        seller2_actual_str = str(self.seller2)

        self.assertEqual(
                seller1_expected_str,                
                seller1_actual_str,
            )
        
        self.assertEqual(
                seller2_expected_str,
                seller2_actual_str,  
            )
        
    """\_______________[META]_______________/"""
    
    def test_ordering(self):
        all_sellers = Seller.objects.all()
        top_seller = all_sellers.first()
        
        self.assertEqual(top_seller, self.seller3)
    

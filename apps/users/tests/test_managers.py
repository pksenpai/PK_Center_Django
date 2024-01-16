from django.test import TestCase
from apps.users.models import Profile, Address
from apps.sellers.models import Seller
from django.contrib.auth import get_user_model; User = get_user_model()

from django.urls import reverse
from django.db import IntegrityError
from django.core.exceptions import ValidationError


class ProfileManagerTest(TestCase):
    
    fixtures = ['users.json']
    
    def setUp(self):
        """\___________________[user]___________________/"""
        self.customer_user = User.objects.get(email="customer@test.test", is_seller=False)
        self.seller_user   = User.objects.get(email="info@masazone.test", is_seller=True)
        
        """\___________________[PROFILE]___________________/"""
        
        self.customer_profile = Profile.objects.create(
            user = self.customer_user,
            name = "mamad gholi",
            description = "I love Books! i post some videos about books that i buyed here X3"
        )
        
        self.seller_profile = Profile.objects.create(
            user = self.seller_user, # this user is an admin seller so It should not be made with this Model!
            name = "Masazone Shop",
            description = "We are a shop that sell best books around the world. Quality is more important to us than quantity!"
        )

    """\_______________[QUERYSET]_______________/"""
    def test_get_queryset(self):
        all_profiles = Profile.objects.all()
        
        self.assertIn(self.customer_profile, all_profiles)
        self.assertIn(self.seller_profile, all_profiles)

    """\______________[CUSTOME]______________/"""
    
    def test_customer(self):
        customer_profiles = Profile.objects.customer()
        
        self.assertIn(self.customer_profile, customer_profiles)
        self.assertNotIn(self.seller_profile, customer_profiles)
        

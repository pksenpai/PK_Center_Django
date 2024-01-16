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
        self.user_customer = User.objects.get(email="customer@test.test", is_seller=False)
        self.user_seller   = User.objects.get(email="info@masazone.test", is_seller=True)
        
        """\___________________[PROFILE]___________________/"""
        
        self.profile_customer = Profile.objects.create(
            user = self.user_customer,
            name = "mamad gholi",
            description = "I love Books! i post some videos about books that i buyed here X3"
        )

        # self.profile_seller_sm = 
    """\_______________[EXISTS]_______________/"""
    def test_profile_customer_exists(self):
        self.assertTrue(self.profile_customer)

    """\______________[NOCREATE]______________/"""
    
    def test_seller_not_find_to_create(self):
        profile = Profile.objects.create(
            user = self.user_seller, # this user is an admin seller so It should not be made with this Model!
            name = "Masazone Shop",
            description = "We are a shop that sell best books around the world. Quality is more important to us than quantity!"
        )
        
        self.assertFalse(profile)
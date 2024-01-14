from django.test import TestCase
from core.models import User, Profile, Address

from django.urls import reverse
from django.db import IntegrityError

from datetime import datetime


class UserTests(TestCase):
    def setUp(self):
        """\___________________[USER]___________________/"""

        self.user_customer = User.objects.create(
            username = "jj1912",
            password = "cleancode123",
            email    = "customer@test.test",
            is_superuser = False,
            is_seller    = False,
            is_staff     = False,
            phone_number = "33334445577",
            first_name   = "Jenifer",
            last_name    = "Jackson",
        )
        
        self.user_seller = User.objects.create(
            username = "masazone",
            password = "m123a123s123a123",
            email    = "info@masazone.test",
            is_superuser = False,
            is_seller    = True, # seller True
            is_staff     = False,
            phone_number = "11122233344",
        )
        
        self.user_staff = User.objects.create(
            username = "staff001",
            password = "ssttaaffff001",
            email    = "staff001@pk.test",
            is_superuser = False,
            is_seller    = False,
            is_staff     = True, # staff True
            phone_number = "00008881244",
            first_name   = "Parsa",
            last_name    = "Ahmd",
        )
        
    """\_______________[UNIQUE]_______________/"""

    def test_unique_id(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(
                username = "jsfaklja",
                password = "asfuopqwuo23",
                id       = 1, # this id already EXISTS!
            )
    def test_unique_username(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(
                username = "jj1912",
                password = "asfuopqwuo23",
            )
    def test_unique_email(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(
                username = "sdgsfwqwerf322",
                password = "asfuopqwuo23",
                email    = "customer@test.test",
            )
    def test_unique_phone_number(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(
                username = "fklsdhjfo2i3wh3224sd",
                password = "asfuopqwuo23",
                phone_number = "00008881244",
            )
    
    """\_______________[MANDATORY]_______________/"""
    
    def test_has_username(self):
        self.assertEqual(self.user_customer.username, "jj1912")
        self.assertEqual(self.user_seller.username, "masazone")
        self.assertEqual(self.user_seller.username, "staff001")
        
    def test_has_password(self):
        self.assertEqual(self.user_customer.password, "cleancode123")
        self.assertEqual(self.user_seller.password, "m123a123s123a123")
        self.assertEqual(self.user_seller.password, "ssttaaffff001")

    """\________________[ROLE]________________/"""
    
    def test_is_staff(self):
        self.assertEqual(self.user_customer.is_staff, False)
        self.assertEqual(self.user_seller.is_staff, False)
        self.assertEqual(self.user_seller.is_staff, True)
        
    def test_is_seller(self):
        self.assertEqual(self.user_customer.is_seller, False)
        self.assertEqual(self.user_seller.is_seller, True)
        self.assertEqual(self.user_seller.is_seller, False)

    def test_is_customer(self):
        self.assertEqual(
                not (
                    self.user_customer.is_staff or
                    self.user_customer.is_seller or
                    self.user_customer.is_superuser
                ),
                True
            )
        
        self.assertEqual(
                not (
                    self.user_seller.is_staff or
                    self.user_seller.is_seller or
                    self.user_seller.is_superuser
                ),
                False
            )
        
        self.assertEqual(
                not (
                    self.user_staff.is_staff or
                    self.user_staff.is_seller or
                    self.user_staff.is_superuser
                ), 
                False
            )

    """\______________[VALIDATION]______________/"""

    def test_valid_phone_number(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(
                username = "234hjohasf0h2",
                password = "sdkhj29wuh92",
                phone_number = "0000abc1244",
            )
        
        with self.assertRaises(IntegrityError):
            User.objects.create(
                username = "woe2pesd",
                password = "sfop2qw",
                phone_number = "12443",
            )
        
        with self.assertRaises(IntegrityError):
            User.objects.create(
                username = "234hjohasf0h2",
                password = "sdkhj29wuh92",
                phone_number = "34238947281479874",
            )
        
    def test_valid_birth_date(self):... ########################### Complete this later!!!
    
    def test_valid_password(self):
        # blank password test
        with self.assertRaises(IntegrityError):
            User.objects.create(
                username = "fsdhjfhwiofhdfssd231",
                password = "",
            )

        # Just numeric password test
        with self.assertRaises(IntegrityError):
            User.objects.create(
                username = "4234jkl4k",
                password = "1234567891011",
            )

        # minimum length password test(above 8)
        with self.assertRaises(IntegrityError):
            User.objects.create(
                username = "fsdhjfhwiofhdfssd231",
                password = "abc123",
            )

    """\_______________[METHOD]_______________/"""
    
    def test_str(self):
        customer_expected_str = "jj1912"
        seller_expected_str = "masazone"
        staff_expected_str = "staff001"
        
        customer_actual_str = str(self.user_customer)
        seller_actual_str = str(self.user_seller)
        staff_actual_str = str(self.user_staff)

        self.assertEqual(
            customer_expected_str,
            customer_actual_str,
            )
        
        self.assertEqual(
            seller_expected_str,
            seller_actual_str,
            )
        
        self.assertEqual(
            staff_expected_str,
            staff_actual_str,
        )
        
        
class ProfileTest(TestCase):
    user_customer = User.objects.get(email="customer@test.test", is_seller=False)
    user_seller = User.objects.get(email="info@masazone.test", is_seller=True)
    
    def setUp(self):
        """\___________________[user]___________________/"""
        self.user_customer = self.__class__.user_customer
        self.user_seller =self.__class__.user_seller
        
        """\___________________[PROFILE]___________________/"""
        
        self.profile_customer = Profile.objects.create(
            user = self.user_customer,
            name = "mamad gholi", # if no value for this field --> with a Custom Manager it takes automate value from get_full_name() of user!
            dascription = "I love Books! i post some videos about books that i buyed here X3"
        )
        
        self.profile_seller = Profile.objects.create(
            user = self.user_seller,
            name = "Masazone Shop", # it must be takes a value for sellers!
            dascription = "We are a shop that sell best books around the world. Quality is more important to us than quantity!"
        )
        
        self.profile_customer.follows.add(self.profile_seller)
    
    """\_______________[MANDATORY]_______________/"""
    
    def test_has_name(self):
        self.assertEqual(self.profile_customer.name, "mamad gholi")
        self.assertEqual(self.profile_seller.name, "Masazone Shop")
    
    """\_______________[CURRENT]_______________/"""
        
    def test_current_user(self):
        self.assertEqual(self.profile_customer.user, self.user_customer)
        self.assertEqual(self.profile_seller.user, self.user_seller)

    def test_current_follows(self):
        self.assertIn(self.profile_seller, self.profile_customer.follows)
    
    """\_______________[METHOD]_______________/"""
    
    def test_get_absolute_url(self):
        customer_expected_url = reverse(
            "user_profile",
            kwargs={
                "id": self.profile_customer.id
            }
        )
        seller_expected_url = reverse(
            "user_profile",
            kwargs={
                "id": self.profile_seller.id
            }
        )
        
        customer_actual_url = self.profile_customer.get_absolute_url()
        seller_actual_url   = self.profile_seller.get_absolute_url()
        
        self.assertEqual(
            customer_expected_url,
            customer_actual_url,
        )
    
        self.assertEqual(
            seller_expected_url,
            seller_actual_url,
        )

    def test_str(self):
        customer_expected_str = "jj1912"
        seller_expected_str = "masazone"
        
        customer_actual_str = str(self.profile_customer)
        seller_actual_str = str(self.profile_seller)

        self.assertEqual(
            customer_expected_str,
            customer_actual_str,
            )
        
        self.assertEqual(
            seller_expected_str,
            seller_actual_str,
            )
        
        
class AddressTest(TestCase):
    user_customer = User.objects.get(email="customer@test.test", is_seller=False)
    user_seller = User.objects.get(email="info@masazone.test", is_seller=True)
    
    def setUp(self):
        """\___________________[user]___________________/"""
        self.user_customer = self.__class__.user_customer
        self.user_seller =self.__class__.user_seller
        
        """\___________________[ADDRESS]___________________/"""
        
        self.customer_address = Address.objects.create(
            user = self.user_customer,
            city = "Tehran",
            state = "Tehran",
            address = "meydoon azadi, sar charah sadeghieh, pelak x23"
        )
        
        self.seller_address = Address.objects.create(
            user = self.user_seller,
            city = "Shiraz",
            state = "Shiraz",
            address = "meydoon Takhti, Kenar mamad golabi, pelak y85"
        )
    
    """\_______________[MANDATORY]_______________/"""
    
    def test_has_city(self):
        self.assertEqual(self.customer_address.city, "Tehran")
        self.assertEqual(self.seller_address.city, "Shiraz")
   
    def test_has_state(self):
        self.assertEqual(self.customer_address.state, "Tehran")
        self.assertEqual(self.seller_address.state, "Shiraz")

    def test_has_address(self):
        self.assertEqual(self.customer_address.address, "meydoon azadi, sar charah sadeghieh, pelak x23")
        self.assertEqual(self.seller_address.address, "meydoon Takhti, Kenar mamad golabi, pelak y85")
    
    """\_______________[METHOD]_______________/"""
    
    def test_str(self):
        customer_expected_str = "jj1912"
        seller_expected_str = "masazone"
        
        customer_actual_str = str(self.customer_address)
        seller_actual_str = str(self.seller_address)

        self.assertEqual(
            customer_expected_str,
            customer_actual_str,
            )
        
        self.assertEqual(
            seller_expected_str,
            seller_actual_str,
            )
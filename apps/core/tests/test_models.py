from django.test import TestCase
from apps.core.models import Category, Comment, Report
from datetime import datetime
from django.db import IntegrityError


class CategoryTests(TestCase):
    def setUp(self):...
    def test_instance(self):...
    def test_has_name(self):...
    def test_unique_pk(self):...
    def test_slug_value(self):...
    def test_str(self):...

class CommentTests(TestCase):    
    def setUp(self):...
    def test_instance(self):...
    def test_unique_pk(self):...
    def test_approved_false_by_default(self):...
    def test_str(self):...
    
class ReportTests(TestCase):    
    def setUp(self):...
    def test_instance(self):...
    def test_has_reason(self):...
    def test_unique_pk(self):...
    def test_approved_false_by_default(self):...
    def test_str(self):...

class TimeStampBaseModelTests(TestCase):
    def setUp(self):...
    def test_auto_add_date(self):...
    
class LogicalQuerySetTests(TestCase):
    def setUp(self): ...
    def test_delete(self):...
    def test_hard_delete(self):...
    
class LogicalManagerTests(TestCase):
    def setUp(self):...
    def test_get_queryset(self):...
    def test_archive(self):...
    def test_deleted(self):...
    
class LogicalBaseModelTests(TestCase):
    def setUp(self):...
    def test_delete(self):...
    def test_hard_delete(self):...
    def test_undelete(self):...
    
class StatusMixinTests(TestCase):
    def setUp(self):...
    def test_status(self):...
    

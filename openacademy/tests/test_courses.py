from odoo.tests.common import TransactionCase
from datetime import date
import unittest

# Run test module  --test-enable


class TestAcademyCourses(TransactionCase):
    def test_create_course(self):
        data_test = self.env['academy.courses'].create({
            'name': 'Course',
            'description': 'Course description'
        })
        self.assertEqual(data_test.name, 'Course')
        self.assertEqual(data_test.description, 'Course description')

from odoo.tests.common import TransactionCase
from datetime import date
import unittest

# Run test module  --test-enable


class TestAcademyCourses(TransactionCase):
    def setUp(self):
        super(TestAcademyCourses, self).setUp()
        self.academy_courses = self.env['academy.courses'].create({
            'name': 'nametest'
        })
        self.academy_session = self.env['academy.session'].create({
            'name': 'test',
            'course_id': self.academy_courses.id,
            'seats': 10,
        })

    def test_create_course(self):
        data_test = self.env['academy.courses'].create({
            'name': 'Course',
            'description': 'Course description',
            'responsible_id': self.env.user.id,
            'session_ids': self.academy_session.ids,
        })
        self.assertEqual(data_test.name, 'Course')
        self.assertEqual(data_test.description, 'Course description')
        self.assertEqual(data_test.responsible_id.id, self.env.user.id)
        self.assertEqual(data_test.session_ids, self.academy_session)

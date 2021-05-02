from odoo.tests.common import TransactionCase
from datetime import date
import unittest


class TestAcademySession(TransactionCase):
    def setUp(self):
        super(TestAcademySession, self).setUp()
        self.academy_courses = self.env['academy.courses'].create({
            'name': 'JavaScript'
        })

    def test_academy_session(self):
        data = self.env['academy.session'].create({
            'name': 'Session of JavaScript language',
            'instructor_id': self.env.user.id,
            'course_id': self.academy_courses.id,

        })
        self.assertEqual(data.name, 'Session of JavaScript language')
        self.assertEqual(data.instructor_id.id, self.env.user.id)
        self.assertEqual(data.course_id.id, self.academy_courses.id)



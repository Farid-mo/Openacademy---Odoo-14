from odoo.tests.common import TransactionCase
import datetime
import unittest


class TestAcademySession(TransactionCase):
    def setUp(self):
        super(TestAcademySession, self).setUp()
        self.academy_attendee_ids = self.env['res.partner'].create({
            'name': 'name',
        })
        self.academy_courses = self.env['academy.courses'].create({
            'name': 'JavaScript'
        })

    def test_academy_session(self):
        data = self.env['academy.session'].create({
            'name': 'Session of JavaScript programing language',
            'instructor_id': self.env.user.id,
            'course_id': self.academy_courses.id,
            'attendee_ids': self.academy_attendee_ids.ids,
            'start_date': '2021-5-4',
        })
        self.assertEqual(data.name, 'Session of JavaScript programing language')
        self.assertEqual(data.instructor_id.id, self.env.user.id)
        self.assertEqual(data.course_id.id, self.academy_courses.id)
        self.assertEqual(data.attendee_ids, self.academy_attendee_ids)
        self.assertEqual(data.start_date, datetime.date(2021, 5, 4))



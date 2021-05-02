# -*- coding: utf-8 -*-
# from odoo import models, fields, api

# class OpenAcademy(models.Model):
#     _name = 'academy.academy'
#     _description = 'academy.academy'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import timedelta


class AcademyCourses(models.Model):
    _name = 'academy.courses'
    _description = 'All courses of our Academy'
    _rec_name = 'name'

    name = fields.Char(string='Title', required=True)
    description = fields.Text()
    responsible_id = fields.Many2one('res.users', ondelete='set null', string='Responsible', index=True)
    session_ids = fields.One2many('academy.session', 'course_id', string='Sessions')
    color = fields.Integer()

    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "The title of the course should not be the description"),

        ('name_unique',
         'UNIQUE(name)',
         "The course title must be unique"),
    ]

    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))])
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(AcademyCourses, self).copy(default)


class Session(models.Model):
    _name = 'academy.session'
    _description = 'Academy Sessions'
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True)
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6, 2), help='Duration in days')
    seats = fields.Integer(string='Number of seats')
    instructor_id = fields.Many2one('res.partner', string='Instructor')
                                    # domain=['|', ('instructor', '=', True)])
    course_id = fields.Many2one('academy.courses', ondelete='cascade',
                                string='Course')
    attendee_ids = fields.Many2many('res.partner', string='Attendees')
    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')
    remaining_seats = fields.Integer(string='Remaining Places', compute='_seats_taken')
    active = fields.Boolean(default=True)
    end_date = fields.Date(string="End Date", store=True,
                           compute='_get_end_date', inverse='_set_end_date')
    attendees_count = fields.Integer(string="Attendees count", store=True,
                                     compute='_get_attendees_count')
    color = fields.Integer()
    duration_change_type = fields.Integer(string='Duration hours', help='Duration', compute='_get_duration_type')

    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for r in self:
            r.attendees_count = len(r.attendee_ids)

    @api.depends('duration')
    def _get_duration_type(self):
        for record in self:
            record.duration_change_type = int(record.duration)

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                r.end_date = r.start_date
                continue

            # Add duration to start_date, but: Monday + 5 days = Saturday, so
            # subtract one second to get on Friday instead
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = r.start_date + duration

    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.end_date):
                continue
            # Compute the difference between dates, but: Friday - Monday = 4 days,
            # so add one day to get 5 days instead
            r.duration = (r.end_date - r.start_date).days + 1

    @api.depends('seats', 'attendee_ids')
    def _seats_taken(self):
        for record in self:
            if not record.seats:
                record.remaining_seats = 0
            else:
                record.remaining_seats = record.seats - len(record.attendee_ids)

    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for record in self:
            if not record.seats:
                record.taken_seats = 0.0
            else:
                record.taken_seats = 100.0 * len(record.attendee_ids) / record.seats

    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': "Incorrect 'seats' value",
                    'message': "The number of available seats may not be negative",
                },
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': "Too many attendees",
                    'message': "Increase seats or remove excess attendees",
                },
            }

    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendee_ids:
                raise ValidationError("A session's instructor can't be an attendee")

# # #
# class Partner(models.Model):
#     _inherit = 'res.partner'
#
#     instructor = fields.Boolean('Instructor', default=False)
#     session_ids = fields.Many2many('academy.session', string='Attended Sessions',
# #                                   readonly=True)

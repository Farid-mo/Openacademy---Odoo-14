from odoo import models,  fields


class Wizard(models.TransientModel):
    _name = 'academy.wizard.create.attendees'
    _description = 'Wizard : Quick registration  of attendees to session'

    def subscribe(self):
        return self.env['academy.session'].browse(self._context.get('active_id')).create({'session_ids': self.session_ids,
                                                                                          'attendee_ids': self.attendee_ids})

    session_ids = fields.Many2one('academy.session', string='Session', required=True)
                                  # required=True, default=_default_session)
    attendee_ids = fields.Many2one('res.partner', string='Attendees')

    # def subscribe(self):
    #     for record in self.session_ids:
    #         # print(record)
    #         record.attendee_ids |= self.attendee_ids
    #         # print(record.attendee_ids)
    #     return {}

    # def subscribe(self):
    #     self.session_id.attendee_ids |= self.attendee_ids
    #     return {}

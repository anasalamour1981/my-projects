# -*- coding: utf-8 -*-
from openerp import models, api, fields, _, exceptions
import logging



class Transaction(models.Model):
    _name = 'cm.transaction.out'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'Outgoing Transaction'
    _order = 'date desc, name'


    @api.depends('out_date', 'date')
    def _compute_hijri(self):
        H = self.env['odex.hijri']
        for r in self:
            r.out_date_hijri = r.out_date and H.convert(r.out_date) or ''
            r.date_hijri = r.date and H.convert(r.date) or ''

    def _default_employee_id(self):
        user = self.env.user
        em = self.env['cm.entity'].search([('user_id', '=', user.id)], limit=1)
        return len(em) and em or self.env['cm.entity']

    name = fields.Char(string='Outgoing Number', default='#')
    out_date = fields.Date(string='Transaction Date', default=fields.Date.today)
    out_date_hijri = fields.Char(string='Transaction Date (Hijri)', compute='_compute_hijri')
    state = fields.Selection(string='State', selection=[
        ('draft', _('Under Editing')),
        ('processed', _('Processed')),
        ('closed', _('Closed')),
        ], default='draft')

    to_ids = fields.Many2many('cm.entity', 'transaction_entity_rel', 'transaction_id', 'entity_id', string='Send To')
    cc_ids = fields.Many2many('cm.entity', 'transaction_entity_cc_rel', 'transaction_id', 'entity_id', string='CC To')
    important_id = fields.Many2one('cm.transaction.important', string='Important Degree')
    type = fields.Selection(string='Outgoing Type', selection=[
        ('new', _('New Transaction')),
        ('forward', _('Forwarded Transaction')),
        ('reply', _('Reply')),
    ], default='new')
    subject = fields.Char(string='Subject')
    subject_type_id = fields.Many2one('cm.subject.type', string='Subject Type')
    transaction_number = fields.Char(string='Transaction Number')
    date = fields.Datetime(string='Created Date', default=fields.Datetime.now)
    follow_reply = fields.Boolean(string='Follow Reply ?')
    from_id = fields.Many2one('cm.entity', string='Outgoing From')
    employee_id = fields.Many2one('cm.entity', string='Created By', default=lambda self: self._default_employee_id())
    entity_id = fields.Many2one('cm.entity', string='Unit Responsible', related='employee_id.parent_id', store=True)
    user_id = fields.Many2one('res.users', string='Created By', related='employee_id.user_id', store=True)
    incoming_id = fields.Many2one('cm.transaction.in', string='Incoming Transaction')
    # 
    preparation_id = fields.Many2one('cm.entity', string='Preparation Unit')
    dispatch_id = fields.Many2one('cm.dispatch', string='Dispatch Level')
    confidential_level_id = fields.Many2one('cm.confidential', string='Confidential Level')
    procedure_id = fields.Many2one('cm.procedure', string='Exec. Procedure')

    # attachments
    attachment_num = fields.Integer(string='No. of Attachments')


    # messaging
    @api.multi
    def message_auto_subscribe(self, updated_fields, values=None):
        users = []
        self.message_subscribe(users, [])
        return super(Transaction, self).message_auto_subscribe(updated_fields, values=values)


    @api.model
    def _needaction_domain_get(self):
        return [('state', '=', 'draft')]

    # end messaging

    @api.multi
    def launch_procedures(self):
        return {
            'name': _('Forward Transaction'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': False,
            'res_model': 'cm.forward.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {
                'default_document_id': self.id
            },
        }

    @api.multi
    def send(self):
        return {
            'name': _('Send Transaction'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': False,
            'res_model': 'cm.send.out.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {
                'default_document_id': self.id
            },
        }

    @api.multi
    def close(self):
        return {
            'name': _('Close Transaction'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': False,
            'res_model': 'cm.close.out.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {
                'default_document_id': self.id
            },
        }

    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        seq = self.env['ir.sequence'].get('cm.transaction.out')
        vals['name'] = seq
        return super(Transaction, self).create(vals)
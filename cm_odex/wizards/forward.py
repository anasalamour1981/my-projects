# -*- coding: utf-8 -*-
from openerp import api, models, fields, _, exceptions

import logging


_logger = logging.getLogger(__name__)


class Wizard(models.TransientModel):
    _name = 'cm.forward.wizard'

    document_id = fields.Many2one('cm.transaction.out', string='Document')
    user_id = fields.Many2one('cm.entity', string='Employee')

    @api.multi
    def run(self):
        for r in self:
            if not len(r.document_id):
                raise exceptions.Warning(_('Please select a document befor proceed!'))
            
            subj = _('Message Has been forwarded !')
            msg = _(u'{} &larr; {}').format(r.document_id.user_id.name, r.user_id.name)
            r.document_id.write({
                'user_id': r.user_id.id,
            })
            r.document_id.message_post(subject=subj, body=msg)


class SendOut(models.TransientModel):
    _name = 'cm.send.out.wizard'

    document_id = fields.Many2one('cm.transaction.out', string='Document')
    user_id = fields.Many2one('cm.entity', string='Employee', related='document_id.employee_id')

    @api.multi
    def run(self):
        for r in self:
            if not len(r.document_id):
                raise exceptions.Warning(_('Please select a document befor proceed!'))
            
            subj = _('Message Has been send !')
            msg = _(u'{} &larr; {}').format(r.document_id.employee_id.name, u' / '.join([k.name for k in r.document_id.to_ids]))
            r.document_id.write({
                'state': 'processed',
            })
            r.document_id.message_post(subject=subj, body=msg)

class CloseOut(models.TransientModel):
    _name = 'cm.close.out.wizard'

    document_id = fields.Many2one('cm.transaction.out', string='Document')
    user_id = fields.Many2one('cm.entity', string='Employee', related='document_id.employee_id')

    @api.multi
    def run(self):
        for r in self:
            if not len(r.document_id):
                raise exceptions.Warning(_('Please select a document befor proceed!'))
            
            subj = _('Message Has been closed !')
            msg = _(u'{} &larr; {}').format(r.document_id.employee_id.name, fields.Datetime.now())
            r.document_id.write({
                'state': 'closed',
            })
            r.document_id.message_post(subject=subj, body=msg)
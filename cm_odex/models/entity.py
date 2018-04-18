# -*- coding: utf-8 -*-
from openerp import models, api, fields, _, exceptions
import logging

_logger = logging.getLogger(__name__)


class JobTitle(models.Model):
    _name = 'cm.job.title'
    _description = 'Job Titles'
    
    name = fields.Char(string='Job Title')



class Entity(models.Model):
    _name = 'cm.entity'
    _description = 'Transactions Contacts'
    _order = 'sequence, name'


    @api.constrains('code')
    def _check_code(self):
        count = self.search_count([('code', '=', self.code), ('id', '!=', self.id)])
        if count:
            ex = exceptions.ValidationError(_('Entity Code Must Be unique !'))
            ex.args = (_('Validation Error !'), ex.value)
            raise ex

    code = fields.Char(string='Code')
    sequence = fields.Integer(string='Sequence')
    partner_id = fields.Many2one('res.partner', string='Partner', readonly=True, ondelete='cascade', copy=False)
    name = fields.Char(string='Name', related='partner_id.name', store=True)
    type = fields.Selection(string='Entity Type', selection=[
        ('unit', _('Internal Unit')),
        ('employee', _('Employee')),
        ('external', _('External Unit')),
    ], default='unit')

    parent_id = fields.Many2one('cm.entity', string='Parent Entity')
    manager_id = fields.Many2one('cm.entity', string='Unit Manager')
    user_id = fields.Many2one('res.users', string='Related User')
    job_title_id = fields.Many2one('cm.job.title', string='Job Title')


    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        if 'partner_id' not in vals:
            if vals.get('type', False) == 'employee':
                userid = vals.get('user_id', False)
                if userid:
                    partner = self.env['res.users'].sudo().browse(userid).partner_id
                    vals['partner_id'] = partner.id
                else:
                    partner = self.env['res.partner'].create({
                        'name': vals.get('name', ''),
                        'email': vals.get('email', ''),
                        'city': vals.get('city', _('Riyadh')),
                        'is_company': vals.get('is_company', True),
                        'country_id': self.env.ref('base.sa', True).id,
                    })
                    vals['partner_id'] = partner.id
            else:
                partner = self.env['res.partner'].create({
                    'name': vals.get('name', ''),
                    'email': vals.get('email', ''),
                    'city': vals.get('city', _('Riyadh')),
                    'is_company': vals.get('is_company', True),
                    'country_id': self.env.ref('base.sa', True).id,
                })
                vals['partner_id'] = partner.id
        if not vals.get('city', False):
            vals['city'] = _('Riyadh')
        return super(Entity, self).create(vals)


    @api.returns('self', lambda value: value.id)
    def copy(self, cr, uid, id, default=None, context=None):
        raise exceptions.Warning(_(u'You cannot duplicate an entity!'))
        return super(Entity, self).copy(cr, uid, id, default=default, context=context)

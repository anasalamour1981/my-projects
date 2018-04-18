# -*- coding: utf-8 -*-
from openerp import models, api, fields, _, exceptions
import logging


class SubjectType(models.Model):
    _name = 'cm.subject.type'

    name = fields.Char(string='Subject Type')


class ImportantDegree(models.Model):
    _name = 'cm.transaction.important'

    name = fields.Char(string='Important Degree')

# 
class DispatchLevel(models.Model):
    _name = 'cm.dispatch'

    name = fields.Char(string='Dispatch Level')


class ConfidentialLevel(models.Model):
    _name = 'cm.confidential'

    name = fields.Char(string='Confidential Level')


class Procedure(models.Model):
    _name = 'cm.procedure'

    name = fields.Char(string='Procedure Name')

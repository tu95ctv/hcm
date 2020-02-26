# -*- coding: utf-8 -*-

from odoo import models, fields, api,exceptions,tools,_

class Department(models.Model):
    _name = 'user.department'
    name = fields.Char()

class User(models.Model):
    _inherit = 'res.users'
    user_department_id = fields.Many2one('hr.department')
    

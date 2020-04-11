# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons.hcmkpi.models.dl_models.dl_p3 import dl_p3
from odoo.exceptions import UserError


class DownloadCVI(models.TransientModel):

    _inherit = "downloadwizard.download"
    department_id = fields.Many2one('hr.department', default = lambda self: self.env.user.user_department_id)
    def default_month(self):
        d = fields.Date.context_today(self)
        return d.month
        # raise UserError('%s - type(%s)'%(d, type(d)))
    month  = fields.Integer(string='Tháng', default=lambda self: fields.Date.context_today(self).month)
    year = fields.Integer(string='Năm', default=lambda self: fields.Date.context_today(self).year)
    user_department_id = fields.Many2one('hr.department', default = lambda self: self.env.user.user_department_id)
    
    

    
    def gen_pick_func(self): 
        rs = super(DownloadCVI, self).gen_pick_func()
        pick_func = {'download_kpi':dl_p3}
        rs.update(pick_func)
        return rs
    
    
    
    
    def gen_model_verbal_dict(self): 
        rs = super(DownloadCVI, self).gen_model_verbal_dict()
        rs.update({'download_kpi':'Download KPI'})
        return rs
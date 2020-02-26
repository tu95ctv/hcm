# -*- coding: utf-8 -*-

from odoo import models, fields, api

class TVCVCate(models.Model):
    _name = 'kpi.tvcvcate'
    name = fields.Char(string=u'Tên',required=True)

class TVCV(models.Model):
    _name = 'kpi.tvcv'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    cate_id = fields.Many2one('kpi.tvcvcate','Phân Loại')
    name = fields.Char(string=u'Nội dung thực hiện công việc',required=True)
    # loai_record = fields.Selection([(u'Công Việc',u'Công Việc'),(u'Sự Cố',u'Sự Cố'),(u'Sự Vụ',u'Sự Vụ'),(u'Comment',u'Comment')], string = u'Loại Record')
    code = fields.Char(string=u'Mã công việc')
    dieu_chinh = fields.Float('Điều chỉnh',digits=(6,2))
    note = fields.Text('Ghi chú')
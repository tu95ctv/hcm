# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    # department_id = fields.Many2one('repeater.department')
    hcm_department_id = fields.Many2one('repeater.department', string="Đài")

class Department(models.Model):
    _name = 'repeater.department'

    name = fields.Char()
    parent_id = fields.Many2one('repeater.department','Đơn vị cha')
    manager_ids = fields.Many2many('res.partner','repeater_department_partner_rel','department_id','partner_id','Quản Lý')

class Repeater(models.Model):
    _name = 'repeater.repeater'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    state = fields.Selection([('draft','Bản Nháp'), ('confirm','Xác nhận'), ('cancel','Xóa')],'Trạng thái Record',
        default='draft', track_visibility="onchange", required=True)
    working_state = fields.Selection([('begin','Khởi động'),
        ('working','Đang hoạt động'), ('fail','Đã hỏng'), ('eviction','Đã thu hồi')],'Tình trạng hiện tại',
        default='working', track_visibility="onchange")
    name = fields.Char('Tên Repeater')
    category_id = fields.Many2one('repeater.category','Loại thiết bị')
    brand_id = fields.Many2one('repeater.category','Hãng sản xuất')
    model_id = fields.Many2one('repeater.model')
    serial_number = fields.Char('Serial Number')
    address = fields.Char('Địa chỉ')
    lat = fields.Float(string="Lat", digits=(16,6))
    long = fields.Float(string="Lon", digits=(16,6))
    image_ids = fields.One2many('repeater.image','repeater_id', string='Ảnh')
    ma_diem_den = fields.Char('Mã điểm đen')
    ma_pa_khach_hang = fields.Char('Mã phản ánh khách hàng')
    mang2g3g4g = fields.Selection([('2G','2G'),('3G','3G'),('4G','4G'),('2G/3G','2G/3G'),('3G/4G','3G/4G'),('2G/3G/4G','2G/3G/4G')],string='2G/3G/4G')
    
    partner_id = fields.Many2one('res.partner','Nhân viên chuyên quản', track_visibility='onchange')
    phone = fields.Char('SĐT NV')
    
    dau_moi_hcm_id = fields.Many2one('res.partner','Đầu mối VTHCM')
    hcm_phone = fields.Char('SĐT VTHCM')
    
    customer = fields.Char('Khách Hàng')
    customer_phone = fields.Char(string="SĐT KH")
    
    start_time = fields.Date('Thời gian thực hiện')
    bien_ban_xac_nhan_ids = fields.One2many('repeater.attachment', 'repeater_id')
    start_note = fields.Text('Ghi chú nghiệm thu')
    thu_hoi_time = fields.Datetime('Thời gian thu hồi')
    nguyen_nhan_thu_hoi = fields.Text('Nguyên nhân thu hồi')
    nhan_vien_thu_hoi_id = fields.Many2one('res.partner','Nhân viên thu hồi', track_visibility='onchange')
    thu_hoi_phone = fields.Char('SĐT NVTH')
    don_vi_thu_hoi = fields.Char('Đơn vị thu hồi')
    note = fields.Text('Ghi chú', track_visibility='onchange')
    hcm_department_id = fields.Many2one('repeater.department', string="Đài", default= lambda self: self.hcm_department_id)
    
    def action_draft(self):
        return self.write({'state': 'draft'})

    def action_confirm(self):
        return self.write({'state': 'confirm'})
    
    def action_cancel(self):
        return self.write({'state': 'cancel'})

    def update_related_partner(self, vals):
        
        if 'phone' in vals:
            self.partner_id.write({'phone': vals['phone']})
        if 'hcm_phone' in vals:
            self.dau_moi_hcm_id.write({'phone': vals['phone']})

    @api.model
    def create(self, vals):
        rec = super(Repeater, self).create(vals)
        rec.update_related_partner(vals)
        return rec

    def write(self, vals):
        rs = super(Repeater, self).write(vals)
        for rec in self:
            rec.update_related_partner(vals)
        return rs
    
    def name_get(self):
        result = []
        for r in self:
            name = (('Tên: ' + r.name + ' ') if r.name else '') + 'Đ/c: ' +  r.address
            result.append((r.id, name))
        return result

    def _message_log(self, **kwargs):
        mail_message_ids = super(Repeater, self)._message_log(**kwargs)
        for mme_id in mail_message_ids:
            char_track = []
            for track in mme_id.tracking_value_ids:
                old_value = track.get_old_display_value()
                old_value = ' '.join(old_value)
                new_value = track.get_new_display_value()
                new_value = ' '.join(new_value)
                value_track = track.field + ': ' + ( old_value + '->'  if old_value else '') + new_value
                char_track.append(value_track)
            char_track = '<br></br>'.join(char_track)
            subject = 'Thông báo thay đổi Repeater %s'%self.name_get()[0][1]
            mail_id = self.env['mail.mail'].create({
                'subject':subject,
                # 'email_to':'ductu19871@gmail.com',
                'recipient_ids':[(6,0,self.hcm_department_id.manager_ids.ids)],
                'mail_message_id':mme_id.id,
                'body_html':char_track,
                })
            mail_id.send()
        return mail_message_ids


class RepeaterCategory(models.Model):
    _name = 'repeater.category'
    name = fields.Char()

class RepeaterBrand(models.Model):
    _name = 'repeater.brand'
    name = fields.Char()

class RepeaterModel(models.Model):
    _name = 'repeater.model'
    name = fields.Char()


class ProductImage(models.Model):
    _name = 'repeater.image'
    image = fields.Binary('Ảnh')
    repeater_id = fields.Many2one('repeater.repeater')

class AttachmentOfRepeater(models.Model):
    _name = 'repeater.attachment'

    name = fields.Char('Tên File')
    filedata = fields.Binary('File')
    repeater_id = fields.Many2one('repeater.repeater')



    
    
    

    

      




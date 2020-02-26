# -*- coding: utf-8 -*-

from odoo import models, fields, api,exceptions,tools,_


class MonthlyWorkItem(models.Model):
    _name = 'monthly.work.item'
    name = fields.Char()
    tvcv_id = fields.Many2one('kpi.tvcv','Thư viện công việc')
    cate_id = fields.Many2one('kpi.tvcvcate', related='tvcv_id.cate_id')#,'Phân Loại'
    code = fields.Char(related='tvcv_id.code')
    dieu_chinh = fields.Float('Điều chỉnh',digits=(6,2), related='tvcv_id.dieu_chinh', store=True)
    qty = fields.Float('Số lượng',digits=(6,2))
    personal_mark = fields.Float('Điểm cá nhân tự ĐG',digits=(6,2),compute='_compute_personal_mark', store=True)
    station_evaluation = fields.Float('Điểm Trạm ĐG',digits=(6,2), compute='_compute_station_evaluation', store=True)
    council_evaluation = fields.Float('Điểm hội đồng ĐG',digits=(6,2), compute='_compute_council_evaluation', store=True)
    result_mark = fields.Float('Điểm trong tháng',digits=(6,2), compute='_compute_result_mark', store=True)
    monthly_work_id = fields.Many2one('monthly.work')
    dx_hay_dk = fields.Selection([('dx','Đột xuất'), ('dk','Định kỳ'), ('tinh_than','Tinh thần')],default ='dk',string="Định kỳ hay đột xuất")

    @api.depends('dieu_chinh','qty')
    def _compute_personal_mark(self):
        for r in self:
            r.personal_mark = r.qty * r.dieu_chinh

    @api.depends('personal_mark')
    def _compute_station_evaluation(self):
        for r in self:
            r.station_evaluation = r.personal_mark

    @api.depends('station_evaluation')
    def _compute_council_evaluation(self):
        for r in self:
            r.council_evaluation = r.station_evaluation

    @api.depends('council_evaluation')
    def _compute_result_mark(self):
        for r in self:
            r.result_mark = (r.personal_mark + r.station_evaluation + r.council_evaluation)/3
    


    
    # def update_evavluation(self, vals):
        
    #     if 'phone' in vals:
    #         self.partner_id.write({'phone': vals['phone']})
    #     if 'customer_phone' in vals:
    #         self.customer_id.write({'phone': vals['customer_phone']})

    # @api.model
    # def create(self, vals):
    #     rec = super(MonthlyWorkItem, self).create(vals)
    #     rec.update_evavluation(vals)
    #     return rec

    # def write(self, vals):
    #     rs = super(MonthlyWorkItem, self).write(vals)
    #     for rec in self:
    #         rec.update_evavluation(vals)
    #     return rs


class MonthlyWork(models.Model):
    _name = 'monthly.work'
    name = fields.Char(compute='_name_compute',store= True)
    user_id = fields.Many2one('res.users', string='Nhân viên', default= lambda self: self.env.user)
    department_id = fields.Many2one('hr.department', related='user_id.user_department_id')
    month  = fields.Integer(string='Tháng')
    year = fields.Integer(string='Năm')
    dk_cvi_ids = fields.One2many('monthly.work.item','monthly_work_id', domain=[('dx_hay_dk','=','dk')], string="Định Kỳ", copy=True)
    dx_cvi_ids = fields.One2many('monthly.work.item','monthly_work_id', domain=[('dx_hay_dk','=','dx')], string="Đột xuất", copy=True)
    # tinh_than_cvi_ids = fields.One2many('monthly.work.item','monthly_work_id', domain=[('tvcv_id.cate_id.name','=','c')], string="Tinh thần ", copy=True)
    tinh_than_cvi_ids = fields.One2many('monthly.work.item','monthly_work_id', domain=[('dx_hay_dk','=','tinh_than')], string="Đột xuất", copy=True)

    diem_co_dinh = fields.Float(compute = 'diem_tong_ket_thang_',store = True, string='A.Điểm định kỳ cá nhân tự ĐG')
    diem_dot_xuat = fields.Float(compute = 'diem_tong_ket_thang_',store = True, string='B. Điểm đột xuất cá nhân tự ĐG')
    diem_tinh_than = fields.Float(compute = 'diem_tong_ket_thang_',store = True, string='C.Điểm tinh thần cá nhân tự ĐG')
    diem_tong_ket_thang = fields.Float(compute = 'diem_tong_ket_thang_',store = True,string='Điểm tổng kết tháng cá nhân tự ĐG')
    
    diem_co_dinh_station = fields.Float(compute = 'diem_tong_ket_thang_',store = True, string='Điểm cố định Trạm ĐG')
    diem_dot_xuat_station = fields.Float(compute = 'diem_tong_ket_thang_',store = True, string='Điểm đột xuất Trạm ĐG')
    diem_tinh_than_station = fields.Float(compute = 'diem_tong_ket_thang_',store = True, string='C.Điểm tinh thần Trạm ĐG')
    diem_tong_ket_thang_station = fields.Float(compute = 'diem_tong_ket_thang_',store = True,string='Điểm tổng kết tháng Trạm ĐG')

    diem_co_dinh_council = fields.Float(compute = 'diem_tong_ket_thang_',store = True, string='Điểm cố định HĐ ĐG')
    diem_dot_xuat_council = fields.Float(compute = 'diem_tong_ket_thang_',store = True, string='Điểm đột xuất HĐ ĐG')
    diem_tinh_than_council = fields.Float(compute = 'diem_tong_ket_thang_',store = True, string='C.Điểm tinh thần HĐ ĐG')
    diem_tong_ket_thang_council = fields.Float(compute = 'diem_tong_ket_thang_',store = True,string='Điểm tổng kết tháng HĐ ĐG')

    diem_co_dinh_result = fields.Float(compute = 'diem_tong_ket_thang_',store = True, string='Điểm cố định cuối cùng')
    diem_dot_xuat_result = fields.Float(compute = 'diem_tong_ket_thang_',store = True, string='Điểm đột xuất cuối cùng')
    diem_tinh_than_result = fields.Float(compute = 'diem_tong_ket_thang_',store = True, string='C.Điểm tinh thần cuối cùng')
    diem_tong_ket_thang_result = fields.Float(compute = 'diem_tong_ket_thang_',store = True,string='Điểm tổng kết tháng cuối cùng')



    @api.depends('user_id','month','year')
    def _name_compute(self):
        for r in self:
            r.name = '%s-Tháng %s-%s'%(r.user_id.name, r.month, r.year)

    @api.depends('dk_cvi_ids.qty')
    def diem_tong_ket_thang_(self):
        for r in self:
            r.diem_co_dinh= sum(r.dk_cvi_ids.mapped('personal_mark'))
            r.diem_dot_xuat= sum(r.dx_cvi_ids.mapped('personal_mark'))
            r.diem_tinh_than = sum(r.tinh_than_cvi_ids.mapped('personal_mark'))
            r.diem_tong_ket_thang = r.diem_co_dinh + r.diem_dot_xuat + r.diem_tinh_than 

            r.diem_co_dinh_station= sum(r.dk_cvi_ids.mapped('station_evaluation'))
            r.diem_dot_xuat_station= sum(r.dx_cvi_ids.mapped('station_evaluation'))
            r.diem_tinh_than_station = sum(r.tinh_than_cvi_ids.mapped('station_evaluation'))
            r.diem_tong_ket_thang_station = r.diem_co_dinh_station + r.diem_dot_xuat_station + r.diem_tinh_than_station

            r.diem_co_dinh_council= sum(r.dk_cvi_ids.mapped('council_evaluation'))
            r.diem_dot_xuat_council= sum(r.dx_cvi_ids.mapped('council_evaluation'))
            r.diem_tinh_than_council = sum(r.tinh_than_cvi_ids.mapped('council_evaluation'))
            r.diem_tong_ket_thang_council = r.diem_co_dinh_council + r.diem_dot_xuat_council + r.diem_tinh_than_council

            r.diem_co_dinh_result = sum(r.dk_cvi_ids.mapped('result_mark'))
            r.diem_dot_xuat_result = sum(r.dx_cvi_ids.mapped('result_mark'))
            r.diem_tinh_than_result = sum(r.tinh_than_cvi_ids.mapped('result_mark'))
            r.diem_tong_ket_thang_result = r.diem_co_dinh_result + r.diem_dot_xuat_result + r.diem_tinh_than_result

    
    

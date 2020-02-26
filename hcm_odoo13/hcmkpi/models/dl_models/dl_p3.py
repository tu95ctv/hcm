# -*- coding: utf-8 -*-
from odoo.addons.downloadwizard.models.dl_models.dl_model import  download_model
from openerp.http import request
import xlwt
from odoo.exceptions import UserError
from copy import deepcopy
# from odoo.addons.tutool.mytools import  convert_odoo_datetime_to_vn_str
from collections import  OrderedDict
# from odoo.addons.tutool.mytools import  Convert_date_orm_to_str
from collections import  OrderedDict
from odoo.addons.downloadwizard.models.dl_models.dl_model import  write_all_row,generate_easyxf
# from odoo.addons.downloadwizard.models.dl_models.dl_model import  get_width
from odoo.addons.downloadwizard.models.dl_models.dl_model import  stt_
from odoo.addons.downloadwizard.models.dl_models.dl_model import  bold_style, normal_style, header_bold_style, center_border_style
from dateutil.relativedelta import relativedelta

# from odoo.addons.tutool.mytools import  convert_utc_native_dt_to_gmt7
import datetime

def gen_domain_kpi(dl_obj,theo_sql = False):
    domain = [('monthly_work_id.month', '=', dl_obj.month), ('monthly_work_id.year', '=', dl_obj.year)]
    return domain

# def gen_domain_cvi_date(dl_obj,theo_sql = False):
#     if not theo_sql:
#         domain = [('loai_record','=',u'Công Việc')]
#     else:
#         where_clause_list = []
#     if dl_obj.chon_thang ==u'Tháng Này':
#         utc_time = datetime.datetime.now()
#         vn_time = convert_utc_native_dt_to_gmt7(utc_time)
#         vn_thang_nay_date_begin = vn_time.strftime('%Y-%m-01')
#         vn_time_offset_thang_sau =  vn_time + relativedelta(months=1)
#         vn_thang_nay_date_end = vn_time_offset_thang_sau.strftime('%Y-%m-01')
#         if not theo_sql:
#             domain.extend([('ngay_bat_dau','>=',vn_thang_nay_date_begin),('ngay_bat_dau','<',vn_thang_nay_date_end)])
#         else:
#             where_clause_list.append('cvi.ngay_bat_dau >= %s'%vn_thang_nay_date_begin)
#             where_clause_list.append('cvi.ngay_bat_dau < %s'%vn_thang_nay_date_end)
#     elif dl_obj.chon_thang ==u'Tháng Trước':
#         utc_time = datetime.datetime.now()
#         vn_time = convert_utc_native_dt_to_gmt7(utc_time)
#         thang_truoc_time = vn_time + relativedelta(months=-1)
#         thang_truoc_date_begin = thang_truoc_time.strftime('%Y-%m-01')
#         thang_truoc_date_end = vn_time.strftime('%Y-%m-01')
#         if not theo_sql:
#             domain.extend([('ngay_bat_dau','>=',thang_truoc_date_begin),('ngay_bat_dau','<',thang_truoc_date_end)])
#         else:
#             where_clause_list.append("cvi.ngay_bat_dau >= '%s'"%thang_truoc_date_begin)
#             where_clause_list.append("cvi.ngay_bat_dau < '%s'"%thang_truoc_date_end)
#     else:
#         if dl_obj.date:
#             if not theo_sql:
#                 domain.append(('ngay_bat_dau','>=',dl_obj.date))
#             else:
#                 where_clause_list.append("cvi.ngay_bat_dau >= '%s'"%dl_obj.date)
#         if dl_obj.end_date:
#             if not theo_sql:
#                 domain.append(('ngay_bat_dau','<=',dl_obj.end_date))
#             else:
#                 where_clause_list.append("cvi.ngay_bat_dau <= '%s'"%dl_obj.end_date)
#     if not theo_sql:
#         return domain
#     else:
#         return where_clause_list



# FIELDNAME_FIELDATTR_cvi =OrderedDict( [
#         ('stt_not_model',{'is_not_model_field':True,'string':u'STT', 'func':stt_}),
#         ('ngay_bat_dau',{'func': lambda v,n: Convert_date_orm_to_str(v),'width':10}),
#         ('gio_bat_dau',{'func':lambda val,n: convert_odoo_datetime_to_vn_str(val, format='%d/%m/%Y %H:%M:%S' )}),
#         ('gio_ket_thuc',{'func':lambda val,n: convert_odoo_datetime_to_vn_str(val, format='%d/%m/%Y %H:%M:%S' )}),
#         ('code',{}),
#         ('tvcv_id_name',{}),
#         ('noi_dung',{}),
#         ('slncl',{}),
#          ('cd_children_ids',{'func':lambda val,n: ','.join(map(lambda v:u'%s'%v.login ,val.mapped('user_id')))}),
#          ('diem_tvcv',{}),
#          ('so_luong',{}),
#          ('so_lan',{}),
#          ('slncl',{}),
#          ('ti_le_chia_diem',{}),
#          ('diemtc',{}),
#          ('diemld',{}),    
#                     ]
                                     
#                                      )

FIELDNAME_FIELDATTR_cvi =OrderedDict( [
        ('stt_not_model',{'is_not_model_field':True,'string':u'STT', 'func':stt_}),
        ('tvcv_id',{}),
        ('cate_id',{'width':40}),
        ('code',{}),
        ('dx_hay_dk',{}),
        ('result_mark',{}),
                    ]
                                     
                                     )

order_dx_hay_dk = {'dk':1, 'dx':2, 'tinh_than': 3}
order_cate_tvcv = {'Công tác khác':0}

Export_Para_cvi = {
    'exported_model':'monthly.work.item',
#     'max_char_width':50,
    'FIELDNAME_FIELDATTR':FIELDNAME_FIELDATTR_cvi,
    'gen_domain':gen_domain_kpi,
    'search_para':{'order': 'id desc'},#desc
    'key_sorted' : lambda r: (order_dx_hay_dk[r.dx_hay_dk], order_cate_tvcv.get(r.tvcv_id.cate_id.name, 1))
    }





def dl_p3_per_user(dl_obj,monthly_work, wb = None, tram=None):
    font_height =dl_obj.font_height
    bold_style = xlwt.easyxf(generate_easyxf(height=font_height,bold=True))
    center_style = xlwt.easyxf(generate_easyxf(height=font_height,vert = 'center',horiz='center'))
    # def sum_(worksheet,f_name,fixups,needdata,row_index,dl_obj, **kargs):
    #     begin_row = needdata['instance_dict']['table']['begin_row'] +2
    #     end_row = needdata['instance_dict']['table']['end_row']
    #     if end_row > begin_row:
    #         worksheet.write(row_index, 4, xlwt.Formula('SUM(%s%s:%s%s)'%('P',begin_row + 1,'P',end_row+1)),center_style)
    #     return 1# 1 row
    def table_detail_p3_(worksheet,f_name, fixups, needdata, row_index, dl_obj, **kargs):
        Export_Para_cvi_copy = deepcopy(Export_Para_cvi)
        n_row = download_model(dl_obj,
                     Export_Para=Export_Para_cvi_copy,
                    #  append_domain=kargs['append_domain_user_id'],
                    append_domain = [('monthly_work_id.user_id','=',user_id.id)],
                     workbook=None,
                     worksheet=worksheet,
                     ROW_TITLE = row_index + 1,
                     return_more_thing_for_bcn = True,
                     no_gray = True,
                     OFFSET_COLUMN = 1,
                     
                    #  sorted_func = 
                                                   
                 )
        return n_row
    user_id = monthly_work.user_id
    fixups =[  
                 ('trung_tam1',{'range':[0,0,0,3],'val':u'TRUNG TÂM HẠ TẦNG MẠNG MIỀN NAM', 'style':xlwt.easyxf(generate_easyxf(bold=True,height=11, vert = 'center',horiz = 'center'))}),
                 ('trung_tam2',{'range':[1,1,0,3],'val':u'ĐÀI VIỄN THÔNG HCM', 'style':xlwt.easyxf(generate_easyxf(bold=True,underline=True,height=12, vert = 'center',horiz = 'center'))}),
                 ('diem_tong_nhan_vien_cham_title',{'range':[5, 3],'val':u'Điểm Tổng Nhân Viên Chấm'}),
                 ('diem_tong_nhan_vien_cham_title',{'range':[5, 4],'val':monthly_work.diem_tong_ket_thang_result}),
                 ('ho_ten_title',{'range':[3, 3],'val':u'Họ Tên','style':bold_style}),
                 ('ho_ten',{'range':[3, 4],'val':user_id.name}),
                 ('tram_tilte',{'range':[4, 3],'val':u'Trạm'}),
                 ('tram',{'range':[4, 4],'val':tram,'style':bold_style}),
                 ('table',{'range':[9, 0],'val':None,'func':table_detail_p3_ ,'offset':3 ,'kargs':{'append_domain_user_id':[('user_id','=',user_id.id)]}}),
                #  ('sum',{'range':[5, 4],'func':sum_ })
                 ] 
    wb = write_all_row(fixups, dl_obj,None,wb = wb,ws_name=user_id.name, font_height=font_height )
    return wb
def gen_department_id(dl_obj):
    if dl_obj.department_id:
        if dl_obj.user_has_groups('base.group_erp_manager'):
            dp_id = dl_obj.department_id
        else:
            dp_id = dl_obj.env.user.department_id
    else:
            dp_id = dl_obj.env.user.department_id
    return dp_id
def dl_p3(dl_obj,append_domain = []):
    # department_id = gen_department_id(dl_obj)
    # cates = dl_obj.env['res.users'].search([('department_id','=',department_id.id)])
    # user_ids =  dl_obj.env['monthly.work'].search([('department_id','=',dl_obj.department_id.id)]).mapped('user_id')
    monthly_works =  dl_obj.env['monthly.work'].search([('department_id','=',dl_obj.department_id.id), ('month','=',dl_obj.month), ('year','=',dl_obj.year)])
    workbook = xlwt.Workbook()
    # if dl_obj.chi_tiet_hay_danh_sach =='danh_sach':
    if 0:
        filename = u'p3_ds_%s'%department_id.name
        wb = download_cvi_by_userlist(dl_obj)
    else:
        filename = u'p3_user'
        workbook = download_cvi_by_userlist(dl_obj)
        for monthly_work in monthly_works:
            # wb = dl_p3_per_user(dl_obj, user_id, wb, department_id.name)
            workbook = dl_p3_per_user(dl_obj, monthly_work, workbook)
    name = "%s%s" % (filename, '.xls')
    return workbook, name

# def gen_date_and_department_domain(dl_obj):
#     domain = []
#     dp_id =gen_department_id(dl_obj)
#     domain = [('department_id','=',dp_id.id)]
#     domain_date = gen_domain_cvi_date(dl_obj)
#     domain.extend(domain_date)
#     return domain
def gen_read_group_domain_user_in_department(dl_obj):
    # domain = gen_date_and_department_domain(dl_obj)
    domain = []
    read_group_rsul = dl_obj.env['cvi'].read_group(domain, ['user_id'], ['user_id'], orderby='id')
    return read_group_rsul

# def download_cvi_by_userlist(dl_obj, workbook = None):
#     # read_group_rsul = gen_read_group_domain_user_in_department(dl_obj)
#     # users_in_a_departments = self.env['res.users'].search([('user_department_id','=',dl_obj.department_id.id)])
#     monthly_works = dl_obj.env['monthly.work'].search([('department_id','=',dl_obj.department_id.id),('month','=',dl_obj.month), ('year','=',dl_obj.year)])
#     if workbook == None:
#         workbook = xlwt.Workbook()
#     worksheet = workbook.add_sheet('Tổng kết KPI')
#     normal_style = xlwt.easyxf("font:  name Times New Roman, height 240")
#     worksheet.write(0,0,'STT',header_bold_style)
#     worksheet.write(0,1,u'Tên',header_bold_style)
#     worksheet.write(0,2,u'Điểm', header_bold_style)
#     row_index = 1
#     stt =1
#     for rs in monthly_works:
#         worksheet.write(row_index,0,stt,center_border_style)
#         worksheet.write(row_index,1, rs.user_id.name,center_border_style)
#         worksheet.write(row_index,2, rs.diem_tong_ket_thang, center_border_style)
#         # worksheet.write(row_index,2,rs['diemtc'],normal_style)
#         row_index += 1
#         stt +=1
#     return workbook


# def download_cvi_by_userlist(dl_obj, workbook = None):
#     monthly_works = dl_obj.env['monthly.work'].search([('department_id','=',dl_obj.department_id.id),('month','=',dl_obj.month), ('year','=',dl_obj.year)])
#     if workbook == None:
#         workbook = xlwt.Workbook()
#     worksheet = workbook.add_sheet('Tổng kết KPI')
#     normal_style = xlwt.easyxf("font:  name Times New Roman, height 240")
#     worksheet.write(0,0,'STT',header_bold_style)
#     worksheet.write(0,1,u'Tên',header_bold_style)
#     worksheet.write(0,2,u'Điểm', header_bold_style)
#     row_index = 1
#     stt =1
#     for rs in monthly_works:
#         worksheet.write(row_index,0,stt,center_border_style)
#         worksheet.write(row_index,1, rs.user_id.name,center_border_style)
#         worksheet.write(row_index,2, rs.diem_tong_ket_thang, center_border_style)
#         # worksheet.write(row_index,2,rs['diemtc'],normal_style)
#         row_index += 1
#         stt +=1
#     return workbook

def download_cvi_by_userlist(dl_obj):
    FIELDNAME_FIELDATTR_cvi =OrderedDict( [
        ('stt_not_model',{'is_not_model_field':True,'string':u'STT', 'func':stt_}),
        ('user_id',{}),
        # ('cate_id',{'width':40}),
        # ('code',{}),
        # ('dx_hay_dk',{}),
        ('diem_tong_ket_thang_result',{}),
                    ]
                                     )

    Export_Para_kpi = {
    'exported_model':'monthly.work',
    'FIELDNAME_FIELDATTR':FIELDNAME_FIELDATTR_cvi,
    'gen_domain':lambda dl_obj: [('department_id','=',dl_obj.department_id.id),('month','=',dl_obj.month), ('year','=',dl_obj.year)],
    'search_para':{'order': 'id desc'},#desc
    # 'key_sorted' : lambda r: (order_dx_hay_dk[r.dx_hay_dk], order_cate_tvcv.get(r.tvcv_id.cate_id.name, 1))
    }
    workbook = download_model(dl_obj,
                    Export_Para=Export_Para_kpi,
                    # append_domain = [('monthly_work_id.user_id','=',user_id.id)],
                    # workbook=None,
                    # worksheet=worksheet,
                    # ROW_TITLE = row_index + 1,
                    # return_more_thing_for_bcn = True,
                    # no_gray = True,
                    # OFFSET_COLUMN = 1,
                 )
    return workbook
        # return n_row





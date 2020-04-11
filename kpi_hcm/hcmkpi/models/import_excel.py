# -*- coding: utf-8 -*-
from odoo import models, fields, api
# from odoo.addons.dai_tgg.models.import_excel_model_dict_folder.model_dict_tvcv import  gen_tvcv_model_dict
# from odoo.addons.dai_tgg.models.import_excel_model_dict_folder.model_dict_user_department import  gen_user_department_model_dict




def gen_user_department_model_dict():
    user_model_dict = {
        
     u'User': {
        'title_rows' : [1], 
        'begin_data_row_offset_with_title_row' :2,
        'sheet_names': ['Sheet1'],
        'model':'res.users',
        'fields' : [
                ('name', {'func':None,'xl_title':u'Họ và Tên','key':True,'required':True}),
                ('login',{'func':None,'xl_title':u'Địa chỉ email','key':True ,'required':True}),
                # ('birth_day',{'func':birth_day_,'xl_title':u'ngày sinh', 'offset_write_xl_diff':4,}),
                ('password',{'func':None,'required':True,'set_val':'123456', 'write_field':False}),
                # ('lang',{'set_val':'vi_VN'}),
                ('phone',{'func':None,'xl_title':u'Số điện thoại','key':False, 'offset_write_xl_diff':1}),
                # ('cac_sep_ids',{'key':False,'required':False,'allow_create':False,
                #                         'fields':[
                #                                  ('login',{'xl_title':u'Cấp trên',  'key':True, 'required':True, 'st_is_x2m_field':True}),
                #                                  ]
                # }),  
                ('groups_id',{'key':False,
                                    'offset_write_xl_diff':2,
                                    'offset_write_xl':3,
                                    'required':False ,
                                    'remove_all_or_just_add_one_x2m': 'add_one',
                                    'fields':[
                                             ('name',{'xl_title':u'groups_id',  'key':True, 'required': True,'st_is_x2m_field':True}),     
                                              ]
                                    }
                 ),  
                #  ('job_id',{'key':False,'required':False,
                #                    'fields':[
                #                                 ('name',{'xl_title':u'Chức vụ',  'key':True, 'required':True, 'func':lambda v,n: u'Nhân viên' if v==False else v }),
                #                                ]
                # }),  
                ('user_department_id',{'key':False,'required':True,'raise_if_False':True,
                                           'fields':[
                                                    ('name',{'xl_title':u'Bộ Phận',  'key':True, 'required': True}),
                                                    ('parent_id',{
                                                        'fields':[
                                                            ('name',{'xl_title':u'parent_department_id', 'key':True, 'required': True}),
                                                        ]

                                                    }),
                                                    
                                                    ]
                                                 }),  
                # ('partner_id',{'key':False,'required':False,
                #                'fields':[
                #                             ('name',{'xl_title':None,  'key':True, 'required': True, 'func':lambda val,needdata: needdata['vof_dict']['name']['val']}),
                #                             ('email',{'xl_title':None,  'key':True, 'required': True, 'func':lambda val,needdata: needdata['vof_dict']['login']['val']}),
                #                             ('department_id',{'xl_title':None,  'key':False, 'required': True, 'func':lambda val,needdata: needdata['vof_dict']['department_id']['val']}),
                #                             ('parent_id',{'key':False,'required':False,
                #                                         'fields':[
                #                                                  ('name',{'xl_title':None,  'key':True, 'required': True, 'func':lambda val,needdata: needdata['vof_dict']['department_id']['fields']['name']['val'] }),
                                                                  
                #                                                  ]
                #                             }),  
                                             
                #                         ]
                #                     }
                #  ),  
                      ]
                },#End users'
  
          
       
                              
                   }
                   
    return user_model_dict
class ImportExcel(models.Model):
    _inherit = 'importexcel.importexcel' 
    # import_key = fields.Selection(selection_add=[('User','User')])
    
    def gen_model_dict(self):
        rs = super(ImportExcel, self).gen_model_dict()
        # rs.update(gen_tvcv_model_dict())
        rs.update(gen_user_department_model_dict())
        return rs
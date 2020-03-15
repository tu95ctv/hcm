# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # to_email_repeater_change = fields.Many2many('res.parter','res_config_partner_relate','config_id', 'partner_id')
    # to_email_repeater_change = fields.Many2one('res.parter')
    to_email_repeater_change_id = fields.Many2one('res.partner')
    is_send_mail_change_repeater = fields.Boolean('Kích hoạt gửi mail')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()

        res['to_email_repeater_change_id'] = int(self.env['ir.config_parameter'].sudo().get_param('repeater.to_email_repeater_change_id',default=0))
        res['is_send_mail_change_repeater'] = self.env['ir.config_parameter'].sudo().get_param('repeater.is_send_mail_change_repeater')
        return res

    @api.model
    def set_values(self):
        self.env['ir.config_parameter'].sudo().set_param('repeater.to_email_repeater_change_id', self.to_email_repeater_change_id.id)
        self.env['ir.config_parameter'].sudo().set_param('repeater.is_send_mail_change_repeater', self.is_send_mail_change_repeater)
        super(ResConfigSettings, self).set_values()

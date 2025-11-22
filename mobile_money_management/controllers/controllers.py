# -*- coding: utf-8 -*-
# from odoo import http


# class MobileMoneyManagement(http.Controller):
#     @http.route('/mobile_money_management/mobile_money_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mobile_money_management/mobile_money_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mobile_money_management.listing', {
#             'root': '/mobile_money_management/mobile_money_management',
#             'objects': http.request.env['mobile_money_management.mobile_money_management'].search([]),
#         })

#     @http.route('/mobile_money_management/mobile_money_management/objects/<model("mobile_money_management.mobile_money_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mobile_money_management.object', {
#             'object': obj
#         })


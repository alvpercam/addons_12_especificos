# -*- coding: utf-8 -*-
##############################################################################
#
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2017-Today Sitaram
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

from odoo import api, fields, models

class SrpricelistItemQty(models.Model):
    _inherit = 'product.pricelist.item'

    product_uom_qty = fields.Float(string='Ordered Quantity', required=True, default=1.0)


class SrMultiProduct(models.TransientModel):
    _name = 'sr.multi.product'

    prices_ids = fields.Many2many('product.pricelist.item', string="Precios")
    product_ids = fields.Many2many('product.product', string="Product")
    remolque = fields.Many2one(string="Tipo de vehiculo",
                               comodel_name="product.category",
                               ondelete="cascade",
                               help="Selecciona la acción a realizar.")
    categ_id = fields.Selection(
        string="Acción",
        selection=[
            ('Remolque', 'Remolque'),
            ('Rep in Situ', 'Rep in Situ'),
            ('Suplidos', 'Suplidos'),
            ('Alquiler', 'Alquiler'),
        ],
    )
    pricelist_id = fields.Many2one('product.pricelist',
                                   string="Complemento",
                                   default="_default_products")
    @api.multi
    def add_product(self):
        for line in self.prices_ids:
            self.env['sale.order.line'].create({
                'product_id': line.product_id.id,
                'product_uom_qty': line.product_uom_qty,
                'order_id': self.id,
                'pricelist_id': self.pricelist_id.id
            })
        return

    @api.model
    def _prepare_default_get(self, order):
        default = {
            'pricelist_id': order.pricelist_id.id,
            'categ_id': order.categ_id,
            'remolque': order.remolque.id,
        }
        return default

    @api.model
    def default_get(self, fields):
        res = super(SrMultiProduct, self).default_get(fields)
        assert self._context.get('active_model') == 'sale.order',\
            'active_model should be sale.order'
        order = self.env['sale.order'].browse(self._context.get('active_id'))
        default = self._prepare_default_get(order)
        res.update(default)
        return res

'''    @api.multi
    @api.onchange('prices_ids')
    def _compute_user_id(self):
        vals = {}
        partner_id = self.pricelist_id.partner_id.id
        vals['partner_id'] = partner_id
        categ_id = self.product_tmpl_id.categ_id.id
        vals['product_categ_id'] = categ_id
        self.update(vals)   '''
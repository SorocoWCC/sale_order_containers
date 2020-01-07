# -*- coding: utf-8 -*-

from odoo import models, fields, api
from openerp.exceptions import ValidationError
from odoo.exceptions import UserError
from openerp.exceptions import Warning
from openerp import models, fields, api
from datetime import datetime
from pytz import timezone 
from datetime import timedelta  
import subprocess
import time
import base64
from openerp.http import request
from odoo_pictures import IM

class sale_order(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    fecha_ingreso = fields.Date(string="Fecha Ingreso", readonly=True, default=fields.Date.today())
    fecha_salida = fields.Date(string="Fecha Salida")
    description = fields.Text()
    numero_contenedor = fields.Char(string="Numero Contenedor")
    marchamo = fields.Char(string="Marchamo")
    contenedor = fields.Selection([('20','20 Pies'), ('40','40 pies')], string="Contenedor")
    estado = fields.Selection([('Cargando','Cargando'), ('Cargado','Cargado'), ('Enviado CON peso','Enviado CON peso'), ('Enviado SIN peso','Enviado SIN peso'), ('Cancelado','Cancelado')], string='Estado')
    peso_ingreso_completo = fields.Integer(string="Contenedor Completo")
    peso_ingreso_cabezal = fields.Integer(string="Cabezal")
    peso_salida_cabezal = fields.Integer(string="Cabezal")
    peso_salida_completo = fields.Integer(string="Contenedor Completo")
    total = fields.Float(compute='action_calcular_peso', store=True, string="Peso contenedor(kg)")

    @api.one
    @api.depends('peso_salida_completo', 'peso_ingreso_completo', 'peso_ingreso_cabezal', 'peso_salida_cabezal')
    def action_calcular_peso(self):
        if self.peso_ingreso_cabezal > 0 or self.peso_ingreso_completo > 0 :
            self.estado = 'Cargando'
            if self.peso_salida_completo > 0 or self.peso_salida_cabezal > 0 :
                self.total = float(self.peso_salida_completo - ((self.peso_ingreso_completo - self.peso_ingreso_cabezal) + self.peso_salida_cabezal))
            else:
                self.total = 0
        else:
            self.total = 0    

        if self.total > 0:
            contiene_linea_chatarra = False
            for order_line in self.order_line:
                if order_line.product_id.name == "Chatarra":
                    order_line.product_uom_qty = self.total
                    contiene_linea_chatarra = True
                    self.estado = "Cargado"
            if not contiene_linea_chatarra and self.state != 'new':
                order_id = self.env['sale.order'].search([('name', '=', self.name)])
                producto = self.env['product.template'].search([('name', '=', 'Chatarra')])
                self.order_line.create({'name': str(producto.name), 'order_id': order_id.id, 'product_uom_qty': self.total, 'product_id': int(producto.id)})
                self.estado = "Cargado"

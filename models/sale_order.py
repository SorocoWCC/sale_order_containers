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
    #mostrar_campos = fields.Boolean(string="Contenedor")
    tipo = fields.Selection([('Regular','Regular'), ('Contenedor','Contenedor')], string="Tipo", default='Regular')
    estado = fields.Selection([('Cargando','Cargando'), ('Enviado CON peso','Enviado CON peso'), ('Enviado SIN peso','Enviado SIN peso'), ('Cancelado','Cancelado')], string='Estado', default='Cargando')
    peso_ingreso_completo = fields.Integer(string="Contenedor Completo")
    peso_ingreso_cabezal = fields.Integer(string="Cabezal")
    peso_salida_cabezal = fields.Integer(string="Cabezal")
    peso_salida_completo = fields.Integer(string="Contenedor Completo")
    #total = fields.Float(compute='_compute_total', store=True, string="Peso contenedor(kg)")

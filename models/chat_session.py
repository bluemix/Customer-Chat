# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ChatSession(models.Model):
    _name = "customer.chat.session"
    _description = "Chat Session"

    name = fields.Char("Session Name", required=True)
    customer_id = fields.Many2one("res.partner", string="Customer", required=True)
    agent_id = fields.Many2one("res.users", string="Support Agent")
    message_ids = fields.One2many("customer.chat.message", "session_id", string="Messages")
    state = fields.Selection([
        ('open', 'Open'),
        ('closed', 'Closed')
    ], default='open', string="Status")

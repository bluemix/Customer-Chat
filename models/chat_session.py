# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ChatSession(models.Model):
    _name = "customer.chat.session"
    _description = "Chat Session"
    _order = "create_date desc"

    name = fields.Char("Session Name", required=True)
    customer_id = fields.Many2one("res.partner", string="Customer", required=True)
    agent_id = fields.Many2one("res.users", string="Support Agent")
    message_ids = fields.One2many("customer.chat.message", "session_id", string="Messages")
    state = fields.Selection([
        ('open', 'Open'),
        ('closed', 'Closed')
    ], default='open', string="Status")

    @api.model
    def create_session(self, customer_id):
        """Create a new chat session if one doesn't exist"""
        session = self.search([('customer_id', '=', customer_id), ('state', '=', 'open')], limit=1)
        if not session:
            session = self.create({
                "name": f"Chat with {self.env['res.partner'].browse(customer_id).name}",
                "customer_id": customer_id,
                "agent_id": None,  # Assign later
            })
        return session

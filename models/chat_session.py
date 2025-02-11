# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ChatSession(models.Model):
    _name = "customer.chat.session"
    _description = "Chat Session"
    _order = "create_date desc"

    client_session_id = fields.Char('Client Session ID')
    agent_id = fields.Many2one("res.users", string='Support Agent', default=None)
    message_ids = fields.One2many('customer.chat.message',
                                  'session_id', string='Messages')
    state = fields.Selection([
        ('open', 'Open'),
        ('closed', 'Closed')
    ], default='open', string='Status')

    @api.model
    def create_session(self, session_id):
        """Create a new chat session if it doesn't exist"""
        session = self.search([
            ('client_session_id', '=', session_id),
            ('state', '=', 'open')
        ], limit=1)
        if not session:
            session = self.create({
                'client_session_id': session_id
            })
        return session

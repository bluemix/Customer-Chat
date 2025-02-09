# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ChatMessage(models.Model):
    _name = "customer.chat.message"
    _description = "Chat Messages"

    session_id = fields.Many2one("customer.chat.session", string="Chat Session", required=True)
    sender_id = fields.Many2one("res.users", string="Sender", required=True)
    message = fields.Text("Message", required=True)
    timestamp = fields.Datetime("Timestamp", default=fields.Datetime.now)

    def send_chat_message(self):
        """Send message via Odoo's Bus Service"""
        self.env['bus.bus']._sendone(
            'customer.chat.session_%s' % self.session_id.id,
            'new_message',
            {
                "session_id": self.session_id.id,
                "sender_id": self.sender_id.id,
                "message": self.message,
                "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            }
        )

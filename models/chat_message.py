# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ChatMessage(models.Model):
    _name = 'customer.chat.message'
    _description = 'Chat Messages'
    _order = 'timestamp asc'

    session_id = fields.Many2one('customer.chat.session', string='Chat Session', required=True, ondelete='cascade')
    sender_id = fields.Many2one('res.users', string='Sender',
                                default=lambda self: self.env.user,
                                required=True, ondelete='cascade')
    message = fields.Text('Message', required=True)
    timestamp = fields.Datetime('Timestamp', default=fields.Datetime.now, required=True, index=True)

    @api.model_create_multi
    def create(self, vals):
        results = super(ChatMessage, self).create(vals)
        for record in results:
            # send message to the customer only when it is not from a public user (or only when it
            # is sent from an agent (internal user)
            public_user = self.env.ref('base.public_user')
            if record.sender_id.id != public_user.id:
                record.send_chat_message()
        return results

    def send_chat_message(self):
        """Send message via the bus service to the front-end (customer)"""
        self.env['bus.bus']._sendone(
            f'customer.chat.session_{self.session_id.id}',
            'new_message',
            {
                'session_id': self.session_id.id,
                'sender_id': self.sender_id.id,
                'message': self.message,
                'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }
        )

# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class ChatController(http.Controller):

    @http.route('/chat/send', type='json', auth='user')
    def send_message(self, session_id, message):
        """Send a message and trigger real-time updates"""
        session = request.env['customer.chat.session'].browse(session_id)
        if session:
            chat_msg = request.env['customer.chat.message'].create({
                'session_id': session_id,
                'sender_id': request.env.user.id,
                'message': message
            })
            chat_msg.send_chat_message()  # Trigger real-time update
            return {"success": True, "message_id": chat_msg.id}
        return {"success": False, "error": "Invalid session"}

    @http.route('/chat/typing', type='json', auth='user')
    def user_typing(self, session_id):
        """Notify other users that someone is typing"""
        request.env['bus.bus']._sendone(
            'customer.chat.session_%s' % session_id,
            'user_typing',
            {"session_id": session_id, "user": request.env.user.name}
        )
        return {"success": True}

# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class ChatController(http.Controller):

    @http.route('/chat/start', type='json', auth='user')
    def start_chat(self, customer_id):
        """Start or retrieve an existing chat session for the customer"""
        session = request.env['customer.chat.session'].sudo().create_session(customer_id)
        return {"success": True, "session_id": session.id}

    @http.route('/chat/send', type='json', auth='user')
    def send_message(self, session_id, message):
        """Send a message and assign an agent if not assigned"""
        session = request.env['customer.chat.session'].sudo().browse(session_id)
        if session:
            if not session.agent_id and request.env.user.has_group('base.group_user'):
                session.agent_id = request.env.user.id  # Assign the agent on first response

            chat_msg = request.env['customer.chat.message'].sudo().create({
                'session_id': session_id,
                'sender_id': request.env.user.id,
                'message': message
            })
            chat_msg.send_chat_message()
            return {"success": True, "message_id": chat_msg.id}
        return {"success": False, "error": "Invalid session"}

    @http.route('/chat/sessions', type='json', auth='user')
    def get_sessions(self):
        """Retrieve all active chat sessions"""
        sessions = request.env['customer.chat.session'].sudo().search([('state', '=', 'open')])
        return {
            "success": True,
            "sessions": [{
                "id": session.id,
                "name": session.name,
                "customer_id": session.customer_id.id,
                "customer_name": session.customer_id.name
            } for session in sessions]
        }

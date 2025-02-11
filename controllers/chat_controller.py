# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

# class ChatPortal(http.Controller):
#
#     @http.route('/chat', type='http', auth='public', website=True)
#     def chat_page(self):
#         return request.render('customer_chat.chat_page_template', {
#             "use_invoice_terms": "yes, use invoice terms"
#         })


class ChatController(http.Controller):

    @http.route('/chat', type='http', auth='public', website=True)
    def start_chat(self):
        """Start or retrieve an existing chat session for the customer"""
        _logger.info(f'start_chat, request.session.sid: {request.session.sid}')
        session = request.env['customer.chat.session'].sudo().create_session(request.session.sid)
        _logger.info(f'start_chat, session: {session}')

        return request.render('customer_chat.chat_page_template', {
            'session_id': session.id
        })


    @http.route('/chat/send', type='json', auth='public')
    def send_message(self, session_id, message):
        session = request.env['customer.chat.session'].browse(session_id)
        if session:
            chat_msg = request.env['customer.chat.message'].create({
                'session_id': session_id,
                'sender_id': request.env.user.id,
                'message': message
            })
            # `read` will return result in an array, so there will be index 0 here
            message_json = chat_msg.read(['sender_id', 'message', 'timestamp'])[0]
            return {'success': True,
                    'message': message_json}
        return {'success': False, 'error': 'Invalid session'}

    @http.route('/chat/messages/<int:session_id>', type='json', auth='public')
    def get_messages(self, session_id):
        _logger.info(f'get_messages, session_id: {session_id}')

        session = request.env['customer.chat.session'].browse(session_id)
        if session:
            messages = session.message_ids.read(['sender_id', 'message', 'timestamp'])
            return {'success': True, 'messages': messages}
        return {'success': False, 'error': 'Invalid session'}

    @http.route('/chat/session', type='json', auth='public')
    def get_sessions(self):
        """Retrieve active chat session"""
        session = (request.env['customer.chat.session'].sudo()
                    .search([('state', '=', 'open'),
                             ('client_session_id', '=', request.session.sid),]))
        _logger.info(f'get_sessions, session: {session}')

        return {
            'success': True,
            'session': session.id
        }

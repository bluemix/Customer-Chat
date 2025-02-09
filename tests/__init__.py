# -*- coding: utf-8 -*-
from odoo.tests import TransactionCase
from odoo.exceptions import AccessError


class TestChat(TransactionCase):

    def setUp(self):
        """ Set up test data before running tests """
        super(TestChat, self).setUp()
        self.customer = self.env['res.partner'].create({
            'name': 'Test Customer',
            'email': 'customer@example.com'
        })
        self.agent = self.env['res.users'].create({
            'name': 'Support Agent',
            'login': 'agent@example.com',
            'email': 'agent@example.com',
            'groups_id': [(6, 0, [self.env.ref('base.group_user').id])]
        })
        self.chat_session = self.env['customer.chat.session'].create({
            'name': 'Test Chat Session',
            'customer_id': self.customer.id,
            'agent_id': self.agent.id
        })

    def test_create_chat_session(self):
        """ Test chat session creation """
        self.assertEqual(self.chat_session.name, "Test Chat Session")
        self.assertEqual(self.chat_session.customer_id, self.customer)

    def test_send_message(self):
        """ Test sending a chat message """
        message = self.env['customer.chat.message'].create({
            'session_id': self.chat_session.id,
            'sender_id': self.agent.id,
            'message': "Hello, how can I help you?"
        })
        self.assertEqual(message.session_id, self.chat_session)
        self.assertEqual(message.message, "Hello, how can I help you?")

    def test_customer_cannot_access_other_sessions(self):
        """ Ensure customers cannot access other chat sessions """
        another_customer = self.env['res.partner'].create({'name': 'Another Customer'})
        with self.assertRaises(AccessError):
            self.chat_session.sudo(another_customer).read()


from odoo.tests import TransactionCase, tagged
from odoo.exceptions import AccessError
import random

@tagged('-at_install', 'post_install')  # Ensures test runs after Odoo is installed
class TestChat(TransactionCase):

    def setUp(self):
        """ Set up test data before running tests """
        super(TestChat, self).setUp()

        # Create test users
        self.client_session_id = str(random.random())
        self.agent = self.env['res.users'].create({
            'name': 'Support Agent',
            'login': 'agent@example.com',
            'email': 'agent@example.com',
            'groups_id': [(6, 0, [self.env.ref('base.group_user').id])]
        })

        # Create a chat session
        self.chat_session = self.env['customer.chat.session'].create({
            'client_session_id': self.client_session_id,
            'agent_id': self.agent.id
        })

    def test_create_chat_session(self):
        """ Test if a chat session is created successfully """
        session = self.env['customer.chat.session'].create_session(self.client_session_id)
        self.assertEqual(session.client_session_id, self.client_session_id)
        self.assertEqual(session.state, 'open')

    def test_send_message(self):
        """ Test sending a message and storing it """
        message = self.env['customer.chat.message'].create({
            'session_id': self.chat_session.id,
            'sender_id': self.agent.id,
            'message': "Hello, how can I help you?"
        })
        self.assertEqual(message.session_id.id, self.chat_session.id)
        self.assertEqual(message.message, "Hello, how can I help you?")

    def test_fetch_messages(self):
        """ Ensure messages are fetched correctly for a session """
        self.env['customer.chat.message'].create({
            'session_id': self.chat_session.id,
            'sender_id': self.agent.id,
            'message': "Test message"
        })
        messages = self.chat_session.message_ids
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message, "Test message")


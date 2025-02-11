/** @odoo-module **/
import {registry} from "@web/core/registry";
import {Component, useState, useRef, onMounted, onPatched} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";

export class ChatWidget extends Component {

    setup() {
        this.rpc = useService('rpc');
        this.bus = this.env.services.bus_service;
        this.chatBodyRef = useRef("chat-body");  // Reference to the chat list

        this.state = useState({
            session_id: this.props['session_id'],
            messages: [],
            newMessage: "",
        });

        onMounted(() => {
            this.loadMessages(this.state.session_id);
            this.listenForNewMessages();
        });
        onPatched(() => {
            this.scrollToBottom();  // Ensure new messages scroll into view
        });
    }
    async loadMessages(sessionId) {
        let result = await this.rpc(`/chat/messages/${sessionId}`);
        if (result.success) {
            this.state.messages = result.messages;
        }
    }

    async sendMessage(event) {
        // call the API only when the user presses Enter or Send button
        if (event.type === 'keydown' && event.key !== 'Enter') return;

        let message = this.state.newMessage.trim();
        if (!message) return;

        let result = await this.rpc('/chat/send',
            {session_id: this.state.session_id, message: message});

        if (result.success) {
            this.state.messages.push(result.message);
            this.state.newMessage = "";
        }
    }

    scrollToBottom() {
        // scroll to bottom of the list when a new message is inserted
        if (this.chatBodyRef.el) {
            this.chatBodyRef.el.scrollTop = this.chatBodyRef.el.scrollHeight;
        }
    }

    listenForNewMessages() {
        // when the customer agent sends a message from the backoffice, it will update
        // `this.state.messages`
        this.bus.addChannel(`customer.chat.session_${this.state.session_id}`);
        this.bus.start();
        this.bus.subscribe("new_message", (data) => {
            if (data.session_id === this.state.session_id) {
                this.state.messages.push(data);
            }
        });
    }
}

ChatWidget.template = 'customer_chat.ChatWidget';
registry.category("public_components").add("customer_chat.ChatWidget", ChatWidget);

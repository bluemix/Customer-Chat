/** @odoo-module **/
import {registry} from "@web/core/registry";
import {Component, useState, useRef, onMounted, onPatched} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";

import {EventBus} from "@odoo/owl";

export class ChatWidget extends Component {

    setup() {
        this.rpc = useService('rpc');
        this.bus = this.env.services.bus_service;
        this.chatBodyRef = useRef("chat-body");  // Reference to the chat list
        console.log('ChatWidget setup ...')
        console.log('ChatWidget setup, this.props: ' + this.props)
        console.log('ChatWidget setup, JSON.stringify(this.props): ' + JSON.stringify(this.props))
        console.log('ChatWidget setup, this.props.session_data: ' + this.props.session_id)

        this.state = useState({
            session_id: this.props['session_id'],
            messages: [],
            newMessage: "",
        });
        console.log('ChatWidget setup, this.state.session_id: ' + this.state.session_id)

        onMounted(() => {
            this.selectSession(this.state.session_id);
            this.listenForNewMessages();
        });
        onPatched(() => {
            this.scrollToBottom();  // Ensure new messages scroll into view
        });
    }

    // async loadSession() {
    //     let result = await this.rpc('/chat/session');
    //     console.log('loadSession, result: ' + result)
    //
    //     if (result.success) {
    //         this.state.session = result.session;
    //         await this.selectSession(result.session.id);
    //     }
    // }

    async selectSession(sessionId) {
        // this.state.currentSessionId = sessionId;

        let result = await this.rpc(`/chat/messages/${sessionId}`);
        console.log('selectSession, result: ' + result)
        console.log('selectSession, JSON.stringify(result): ' + JSON.stringify(result))
        if (result.success) {
            this.state.messages = result.messages;
        }
    }

    async sendMessage(event) {
        console.log('sendMessage ...')

        if (event.type === 'keydown' && event.key !== 'Enter') return;
        // if (!this.state.currentSessionId) return;

        let message = this.state.newMessage.trim();
        if (!message) return;

        let result = await this.rpc('/chat/send',
            {session_id: this.state.session_id, message: message});
        console.log('sendMessage, result: ' + result)
        console.log('sendMessage, JSON.stringify(result): ' + JSON.stringify(result))

        if (result.success) {
            console.log('sendMessage, JSON.stringify(result.message): ' + JSON.stringify(result.message))
            // this.state.messages = [...this.state.messages, result.message];
            this.state.messages.push(result.message);
            this.state.newMessage = "";
            // this.scrollToBottom()
        }
    }

    scrollToBottom() {
        console.log('scrollToBottom, JSON.stringify(state.messages): ' + JSON.stringify(this.state.messages))
        if (this.chatBodyRef.el) {
            this.chatBodyRef.el.scrollTop = this.chatBodyRef.el.scrollHeight;
        }
    }

    listenForNewMessages() {
        this.bus.addChannel(`customer.chat.session_${this.state.session_id}`);
        this.bus.start();
        this.bus.subscribe("new_message", (data) => {
            console.log('listenForNewMessages, data.session_id === this.state.session_id: ' + data.session_id === this.state.session_id);

            if (data.session_id === this.state.session_id) {
                console.log('listenForNewMessages, will insert message: ' + JSON.stringify(data));
                this.state.messages.push(data);
            }
        });
    }
}

ChatWidget.template = "customer_chat.ChatWidget";
registry.category("public_components").add("customer_chat.ChatWidget", ChatWidget);

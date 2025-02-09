/** @odoo-module **/

import { Component, useState, onMounted } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class ChatWidget extends Component {
    setup() {
        this.rpc = useService("rpc");
        this.bus = useService("bus_service");
        this.state = useState({
            sessions: [],
            currentSessionId: null,
            messages: [],
            newMessage: "",
            user: odoo.session_info.user_id
        });

        onMounted(() => {
            this.loadSessions();
            this.listenForNewMessages();
        });
    }

    async loadSessions() {
        let result = await this.rpc("/chat/sessions");
        if (result.success) {
            this.state.sessions = result.sessions;
            if (result.sessions.length > 0) {
                this.selectSession(result.sessions[0].id);
            }
        }
    }

    async selectSession(sessionId) {
        this.state.currentSessionId = sessionId;
        this.state.messages = [];

        let result = await this.rpc(`/chat/messages/${sessionId}`);
        if (result.success) {
            this.state.messages = result.messages;
        }
    }

    async sendMessage(event) {
        if (event.type === "keydown" && event.key !== "Enter") return;
        if (!this.state.currentSessionId) return;

        let message = this.state.newMessage.trim();
        if (!message) return;

        let result = await this.rpc("/chat/send", { session_id: this.state.currentSessionId, message: message });
        if (result.success) {
            this.state.newMessage = "";
        }
    }

    listenForNewMessages() {
        this.bus.addChannel("customer.chat.session_" + this.state.currentSessionId);
        this.bus.start();
        this.bus.on("new_message", "chat_widget", (data) => {
            if (data.session_id === this.state.currentSessionId) {
                this.state.messages.push(data);
            }
        });
    }
}

ChatWidget.template = "customer_chat.ChatWidget";

/** @odoo-module **/

import { Component, useState, onMounted, useRef } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import {session} from "../../../../web/static/src/session";

export class ChatWidget extends Component {
    setup() {
        this.rpc = useService("rpc");
        this.bus = useService("bus_service");
        this.typingTimeout = null;
        this.inputRef = useRef("chatInput");

        this.state = useState({
            messages: [],
            newMessage: "",
            typingUser: null,
            user: session.user_id
        });

        onMounted(() => {
            this.loadMessages();
            this.listenForNewMessages();
            this.listenForTyping();
        });
    }

    async loadMessages() {
        let result = await this.rpc("/chat/messages/1");  // Hardcoded session_id for now
        if (result.success) {
            this.state.messages = result.messages;
        }
    }

    async sendMessage(event) {
        if (event.type === "keydown" && event.key !== "Enter") return;

        let message = this.state.newMessage.trim();
        if (!message) return;

        let result = await this.rpc("/chat/send", { session_id: 1, message: message });
        if (result.success) {
            this.state.newMessage = "";  // Clear input
            this.state.typingUser = null;  // Hide typing indicator
        }
    }

    async notifyTyping() {
        // Clear previous timeout to prevent spam
        clearTimeout(this.typingTimeout);

        // Send typing event to server
        await this.rpc("/chat/typing", { session_id: 1 });

        // Hide typing indicator after 3 seconds of inactivity
        this.typingTimeout = setTimeout(() => {
            this.state.typingUser = null;
        }, 3000);
    }

    listenForNewMessages() {
        this.bus.addChannel("customer.chat.session_1");  // Hardcoded session_id for now
        this.bus.start();
        this.bus.on("new_message", "chat_widget", (data) => {
            this.state.messages.push(data);
        });
    }

    listenForTyping() {
        this.bus.on("user_typing", "chat_widget", (data) => {
            this.state.typingUser = data.user;
        });
    }
}

ChatWidget.template = "customer_chat.ChatWidget";

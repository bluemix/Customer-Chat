/** @odoo-module **/

import { ChatWidget } from "../src/js/chat_widget";
import { mount } from "@odoo/owl";
import { nextTick } from "@web/../tests/helpers/utils";

import { makeTestEnv } from "@web/../tests/helpers/mock_env";

QUnit.module("ChatWidget", (hooks) => {
    let env;
    let widget;

    hooks.beforeEach(async () => {
        env = await makeTestEnv();
        widget = await mount(ChatWidget, { env });
    });

    hooks.afterEach(() => {
        widget.unmount();
    });

    QUnit.test("Chat widget should render correctly", async (assert) => {
        assert.ok(widget.el, "The chat widget should be mounted in the DOM.");
        assert.strictEqual(widget.el.querySelector(".chat-header").textContent.trim(), "Customer Chat", "Chat header should be present.");
    });

    QUnit.test("Send a message and check if it appears in the list", async (assert) => {
        const input = widget.el.querySelector("input");
        input.value = "Hello, test!";
        input.dispatchEvent(new Event("input"));

        widget.el.querySelector(".send-btn").click();
        await nextTick();

        const messages = widget.el.querySelectorAll(".chat-message");
        assert.ok(messages.length > 0, "A new message should be added to the chat.");
        assert.strictEqual(messages[messages.length - 1].textContent.trim(), "Hello, test!", "The last message should be 'Hello, test!'");
    });

    QUnit.test("Messages should be fetched from the backend", async (assert) => {
        widget.state.messages = [
            { id: 1, message: "Backend Message", sender_id: 1 }
        ];
        await nextTick();

        const messages = widget.el.querySelectorAll(".chat-message");
        assert.strictEqual(messages.length, 1, "One message should be displayed.");
        assert.strictEqual(messages[0].textContent.trim(), "Backend Message", "The message should match the backend response.");
    });
});

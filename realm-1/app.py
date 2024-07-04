import flet as ft
from client import ChatClient
import json

def main(page: ft.Page):
    client = ChatClient()

    def on_login(e):
        username = username_input.value
        password = password_input.value
        response = client.proses(f'auth {username} {password}')
        
        if "logged in" in response:
            show_dashboard_page(username)
        else:
            result_text.value = response
            page.update()

    def show_dashboard_page(username):
        page.controls.clear()  # Clear the current page controls
        
        welcome_text = ft.Text(f"Welcome, {username}!")
        logout_button = ft.ElevatedButton(text="Logout", on_click=on_logout)
        private_message_button = ft.ElevatedButton(text="Private Message", on_click=show_private_message_page)
        inbox_button = ft.ElevatedButton(text="Inbox", on_click=show_inbox_page)
        
        # Add controls to the dashboard page
        page.add(welcome_text, private_message_button, inbox_button, logout_button)
        page.update()

    def show_private_message_page(e=None):
        page.controls.clear()  # Clear the current page controls

        username_to_input = ft.TextField(label="Username to")
        message_input = ft.TextField(label="Message")
        send_button = ft.ElevatedButton(text="Send", on_click=lambda e: on_send_message(username_to_input.value, message_input.value))
        back_button = ft.ElevatedButton(text="Back to Dashboard", on_click=lambda _: show_dashboard_page(username_input.value))

        page.add(username_to_input, message_input, send_button, back_button)
        page.update()

    def show_inbox_page(e=None):
        page.controls.clear()  # Clear the current page controls

        inbox_messages = get_inbox_messages()
        inbox_list = ft.ListView()

        for message in inbox_messages:
            message_text = ft.Text(f"From: {message['msg_from']}\nMessage: {message['msg']}")
            inbox_list.controls.append(message_text)
        
        back_button = ft.ElevatedButton(text="Back to Dashboard", on_click=lambda _: show_dashboard_page(username_input.value))

        page.add(inbox_list, back_button)
        page.update()

    def on_send_message(user, message):
        response = client.proses(f'send {user} {message}')
        result_text.value = response
        page.update()

    def on_logout(e):
        client.logout()
        show_login_page()

    def show_login_page():
        page.controls.clear()  # Clear the current page controls

        page.add(
            username_input,
            password_input,
            login_button,
            result_text
        )
        page.update()

    def get_inbox_messages():
        # Fetch the inbox messages from the server
        response = client.proses('inbox')
        try:
            message_data = json.loads(response)
            # Assuming the response is a dictionary with the user's messages
            if isinstance(message_data, dict):
                all_messages = []
                for user, messages in message_data.items():
                    all_messages.extend(messages)
                return all_messages
            else:
                return []
        except json.JSONDecodeError:
            return []

    username_input = ft.TextField(label="Username")
    password_input = ft.TextField(label="Password", password=True)
    login_button = ft.ElevatedButton(text="Login", on_click=on_login)
    result_text = ft.Text()

    show_login_page()  # Initial display is the login page

ft.app(target=main)

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
        page.controls.clear()
        
        welcome_text = ft.Text(f"Welcome, {username}!", width=300, text_align="center")
        logout_button = ft.ElevatedButton(text="Logout", on_click=on_logout)
        private_message_button = ft.ElevatedButton(text="Private Message", on_click=show_private_message_page)
        group_message_button = ft.ElevatedButton(text="Group Message", on_click=show_group_message_page)
        
        page.add(
            ft.Column(
                [
                    welcome_text, 
                    private_message_button,
                    group_message_button,
                    logout_button
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        page.update()

    def show_private_message_page(e=None):
        page.controls.clear()

        username_to_input = ft.TextField(label="Username to", width=300)
        message_input = ft.TextField(label="Message", width=300)
        send_button = ft.ElevatedButton(text="Send", on_click=lambda e: on_send_message(username_to_input.value, message_input.value))
        inbox_button = ft.ElevatedButton(text="Inbox", on_click=show_inbox_page)
        back_button = ft.ElevatedButton(text="Back to Dashboard", on_click=lambda _: show_dashboard_page(username_input.value))

        page.add(
            ft.Column(
                [
                    username_to_input, 
                    message_input, 
                    send_button, 
                    inbox_button, 
                    back_button
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        page.update()

    def show_group_message_page(e=None):
        page.controls.clear()

        create_group_button = ft.ElevatedButton(text="Create Group", on_click=show_create_group_page)
        join_group_button = ft.ElevatedButton(text="Join Group", on_click=show_join_group_page)
        inbox_group_button = ft.ElevatedButton(text="Inbox Group", on_click=show_inbox_group_page)
        send_group_message_button = ft.ElevatedButton(text="Send Group Message", on_click=show_send_group_message_page)
        back_button = ft.ElevatedButton(text="Back to Dashboard", on_click=lambda _: show_dashboard_page(username_input.value))

        page.add(
            ft.Column(
                [
                    create_group_button,
                    join_group_button,
                    inbox_group_button,
                    send_group_message_button,
                    back_button
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        page.update()

    def show_send_group_message_page(e=None):
        page.controls.clear()

        group_name_input = ft.TextField(label="Group Name", width=300)
        message_input = ft.TextField(label="Message", width=300)
        send_button = ft.ElevatedButton(text="Send", on_click=lambda e: on_send_group_message(group_name_input.value, message_input.value))
        back_button = ft.ElevatedButton(text="Back to Group Message", on_click=show_group_message_page)

        page.add(
            ft.Column(
                [
                    group_name_input, 
                    message_input, 
                    send_button, 
                    back_button
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        page.update()

    def show_inbox_page(e=None):
        page.controls.clear()

        inbox_messages = get_inbox_messages()
        inbox_list = ft.ListView()

        for message in inbox_messages:
            message_text = ft.Text(f"From: {message['msg_from']}\nMessage: {message['msg']}", width=300, text_align="center")
            inbox_list.controls.append(message_text)
        
        back_button = ft.ElevatedButton(text="Back to Private Message", on_click=show_private_message_page)

        page.add(
            ft.Column(
                [
                    inbox_list, 
                    back_button
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        page.update()

    def show_create_group_page(e=None):
        page.controls.clear()

        group_name_input = ft.TextField(label="Group Name", width=300)
        create_button = ft.ElevatedButton(text="Create Group", on_click=lambda e: on_create_group(group_name_input.value))
        back_button = ft.ElevatedButton(text="Back to Group Message", on_click=show_group_message_page)

        page.add(
            ft.Column(
                [
                    group_name_input, 
                    create_button, 
                    back_button
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        page.update()

    def show_join_group_page(e=None):
        page.controls.clear()

        group_name_input = ft.TextField(label="Group Name", width=300)
        join_button = ft.ElevatedButton(text="Join Group", on_click=lambda e: on_join_group(group_name_input.value))
        back_button = ft.ElevatedButton(text="Back to Group Message", on_click=show_group_message_page)

        page.add(
            ft.Column(
                [
                    group_name_input, 
                    join_button, 
                    back_button
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        page.update()

    def show_inbox_group_page(e=None):
        page.controls.clear()

        group_name_input = ft.TextField(label="Group Name", width=300)
        fetch_inbox_button = ft.ElevatedButton(text="Fetch Group Inbox", on_click=lambda e: on_fetch_group_inbox(group_name_input.value))
        back_button = ft.ElevatedButton(text="Back to Group Message", on_click=show_group_message_page)

        page.add(
            ft.Column(
                [
                    group_name_input,
                    fetch_inbox_button,
                    back_button
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        page.update()

    def on_create_group(group_name):
        response = client.proses(f'create_group {group_name}')
        result_text.value = response
        page.update()

    def on_join_group(group_name):
        response = client.proses(f'join_group {group_name}')
        result_text.value = response
        page.update()

    def on_fetch_group_inbox(group_name):
        response = client.inbox_group(group_name)
        page.controls.clear()

        try:
            messages = json.loads(response)
            inbox_list = ft.ListView()

            if isinstance(messages, dict):
                for group, msgs in messages.items():
                    for message in msgs:
                        message_text = ft.Text(f"From: {message['msg_from']}\nMessage: {message['msg']}", width=300, text_align="center")
                        inbox_list.controls.append(message_text)

            back_button = ft.ElevatedButton(text="Back to Group Message", on_click=show_group_message_page)
            page.add(
                ft.Column(
                    [
                        inbox_list,
                        back_button
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        except json.JSONDecodeError:
            result_text.value = "Failed to fetch group inbox"
            page.add(result_text)

        page.update()

    def on_send_group_message(group_name, message):
        response = client.proses(f'send_group {group_name} {message}')
        result_text.value = response
        page.update()

    def on_send_message(user, message):
        response = client.proses(f'send {user} {message}')
        result_text.value = response
        page.update()

    def on_logout(e):
        client.logout()
        show_login_page()

    def show_login_page():
        page.controls.clear()

        page.add(
            ft.Row(
                [
                    ft.Column(
                        [
                            username_input,
                            password_input,
                            login_button,
                            result_text
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        page.update()

    def get_inbox_messages():
        response = client.proses('inbox')
        try:
            message_data = json.loads(response)
            if isinstance(message_data, dict):
                all_messages = []
                for user, messages in message_data.items():
                    all_messages.extend(messages)
                return all_messages
            else:
                return []
        except json.JSONDecodeError:
            return []

    username_input = ft.TextField(label="Username", width=300)
    password_input = ft.TextField(label="Password", password=True, width=300)
    login_button = ft.ElevatedButton(text="Login", on_click=on_login)
    result_text = ft.Text()

    show_login_page()

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

ft.app(target=main)

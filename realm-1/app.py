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
        
        # Add controls to the dashboard page
        page.add(welcome_text, private_message_button, logout_button)
        page.update()

    def show_private_message_page(e):
        page.controls.clear()  # Clear the current page controls

        users = get_all_users()
        user_list = ft.ListView()

        for user in users:
            user_list.controls.append(ft.Text(user))
        
        back_button = ft.ElevatedButton(text="Back to Dashboard", on_click=lambda _: show_dashboard_page(username_input.value))

        page.add(user_list, back_button)
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

    def get_all_users():
        # Fetch the list of users from the server
        response = client.proses('get_all_users')
        user_data = json.loads(response)
        usernames = list(user_data.keys())
        return usernames

    username_input = ft.TextField(label="Username")
    password_input = ft.TextField(label="Password", password=True)
    login_button = ft.ElevatedButton(text="Login", on_click=on_login)
    result_text = ft.Text()

    show_login_page()  # Initial display is the login page

ft.app(target=main)

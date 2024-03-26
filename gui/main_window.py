import flet as ft
import datetime


def main(page: ft.Page):
    page.title = "Admin Data Entry"

    birthday = "Your Birth Date"
    # Create input fields
    name_input = ft.TextField(label="Name", width=page.window_width // 2)
    phone_input = ft.TextField(label="Phone Number", width=page.window_width // 2)
    email_input = ft.TextField(label="Email", width=page.window_width // 2)

    birthday_input = ft.DatePicker()
    date_button = ft.ElevatedButton(
        "Birth Date",
        icon=ft.icons.CALENDAR_MONTH,
        on_click=lambda _: birthday_input.pick_date(),
        expand=1,
    )

    birthday_placeholder = ft.TextField(read_only=True, label=str(birthday), expand=2)

    birthday_row = ft.Row(
        controls=[birthday_placeholder, date_button], width=page.window_width // 2
    )

    # Placeholder for photo (update with actual photo handling logic)
    photo_placeholder = ft.Image(
        src="https://via.placeholder.com/150",
        width=page.window_width // 2,
    )

    # Button to submit the form
    submit_btn = ft.ElevatedButton(
        "Submit",
        on_click=lambda e: submit_form(
            page, name_input, phone_input, email_input, birthday_input
        ),
    )

    # Add elements to the page
    page.add(
        ft.Row(
            controls=[
                ft.Column(
                    controls=[name_input, phone_input, email_input, birthday_row]
                ),
                ft.Column(controls=[photo_placeholder]),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        ),
        birthday_input,
        ft.Row(controls=[submit_btn], alignment=ft.MainAxisAlignment.CENTER),
    )

    # Function to handle form submission
    def submit_form(page, name, phone, email, birthday):
        # Here you would handle the form submission, e.g., save data, update UI, etc.
        # For demonstration, we'll just print the values to the console
        print(
            f"Name: {name.value}, Phone: {phone.value}, Email: {email.value}, Birthday: {birthday.value}"
        )
        birthday_placeholder.label = str(birthday)
        page.update()

    def update_textbox_width(e):
        name_input.width = page.window_width // 2
        phone_input.width = page.window_width // 2
        email_input.width = page.window_width // 2
        birthday_row.width = page.window_width // 2
        photo_placeholder.width = page.window_width // 2
        page.update()

    # Assign the resize event handler
    page.on_resize = update_textbox_width


# ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=5000)
ft.app(target=main)

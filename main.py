import flet as ft

from todo_app import TodoApp


async def main(page: ft.Page):

    page.title = "ToDo App"
    page.padding = 20

    app = TodoApp()
    await page.add_async(app)


ft.app(main)

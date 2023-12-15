import flet as ft


class Task(ft.UserControl):

    def __init__(self, task_name, task_status_change, task_delete):

        super().__init__()

        self.completed = False
        self.task_name = task_name
        self.task_delete = task_delete
        self.task_status_change = task_status_change
    
    async def status_changed(self, e):
        self.completed = self.task_entity.value
        await self.task_status_change(self)

    def build(self):

        self.task_entity = ft.Checkbox(label=self.task_name, value=False, on_change=self.status_changed)
        self.edit_name = ft.TextField(expand=True)

        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.task_entity,
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(icon=ft.icons.CREATE_OUTLINED, tooltip="Edit To-Do", on_click=self.edit_clicked),
                        ft.IconButton(icon=ft.icons.DELETE_OUTLINED, tooltip="Delete To-Do", on_click=self.delete_clicked),
                    ]
                )
            ]
        )

        self.edit_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_name,
                ft.IconButton(icon=ft.icons.DONE_OUTLINE_OUTLINED, tooltip="Update To-Do", on_click=self.save_clicked),
            ]
        )

        return ft.Column(
            controls=[self.display_view, self.edit_view],
        )

    async def edit_clicked(self, e):
        self.edit_name.value = self.task_entity.label
        self.display_view.visible = False
        self.edit_view.visible = True
        await self.update_async()

    async def save_clicked(self, e):
        self.task_entity.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        await self.update_async()

    async def delete_clicked(self, e):
        await self.task_delete(self)
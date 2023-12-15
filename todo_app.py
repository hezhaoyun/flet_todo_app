import flet as ft

from task import Task


class TodoApp(ft.UserControl):

    def __init__(self):

        super().__init__()

        self.new_task = ft.TextField(hint_text='Whats needs to be done?', expand=True)
        self.tasks = ft.Column()

        self.filter = ft.Tabs(
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[ft.Tab(text='all'), ft.Tab(text='active'), ft.Tab(text='completed')]
        )

        self.items_left = ft.Text("0 items left")

        self.view = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(value="Todos", style="headlineMedium")
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    controls=[
                        self.new_task,
                        ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_task)
                    ]
                ),
                ft.Column(
                    spacing=25,
                    controls=[
                        self.filter,
                        self.tasks,
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                self.items_left,
                                ft.OutlinedButton(text="Clear completed", on_click=self.clear_clicked),
                            ],
                        ),
                    ]
                )
            ]
        )

    def build(self):
        return self.view

    async def update_async(self):

        count = 0
        status = self.filter.tabs[self.filter.selected_index].text

        for task in self.tasks.controls:
            
            task.visible = (
                status == 'all'
                or (status == 'active' and not task.completed)
                or (status == 'completed' and task.completed)
            )
            
            if not task.completed:
                count += 1

        self.items_left.value = f"{count} active item(s) left"
        await super().update_async()

    async def add_task(self, e):
        self.tasks.controls.append(
            Task(self.new_task.value, self.task_status_change, self.task_delete)
        )
        self.new_task.value = ''
        await self.new_task.focus_async()
        await self.update_async()

    async def task_delete(self, task):
        self.tasks.controls.remove(task)
        await self.update_async()

    async def task_status_change(self, task):
        await self.update_async()

    async def tabs_changed(self, e):
        await self.update_async()

    async def clear_clicked(self, e):
            for task in self.tasks.controls[:]:
                if task.completed:
                    await self.task_delete(task)
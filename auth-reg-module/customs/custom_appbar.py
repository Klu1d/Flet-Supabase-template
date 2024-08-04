import flet as ft
import random

class CustomAppBar(ft.AppBar):
    def __init__(
        self, 
        leading: ft.Control = None,
        leading_width: int = None,
        title: ft.Control = None,
        center_title: bool = None,
        actions: list = None,
    ):
        super().__init__()
        self.leading = ft.Text('')
        self.adaptive = True
        self.leading_width = leading_width
        self.title = title
        self.center_title = center_title

    def build(self):
        self.bgcolor = 'black'
        self.toolbar_height = 50
        self.actions = [
            ft.Container(
                on_click=lambda _: print("avatar"),
                height=50, width=45, border_radius=10, padding=5, ink=True,
                content=ft.Container(
                    border_radius=360, height=35, width=35,
                    content=ft.Image(
                        f"https://web-zoopark.ru/wp-content/uploads/2018/11/3-{random.randint(1,15)}.jpg",
                        fit=ft.ImageFit.COVER,
                    ),
                    #content=ft.Image("https://i.pinimg.com/originals/b7/5b/29/b75b29441bbd967deda4365441497221.png")
                ),
            )
        ]
        

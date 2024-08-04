import flet as ft

from database.supabase_client import SupabaseClient
from customs.custom_appbar import CustomAppBar

class HomeView(ft.View):
    def __init__(self, page: ft.Page, database: SupabaseClient):
        super().__init__()
        self.page = page
        self.database = database

        self.route = '/home'
        self.appbar = CustomAppBar()
        self.vertical_alignment = ft.MainAxisAlignment.SPACE_AROUND
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.fullscreen_dialog = True
        self.padding = ft.padding.symmetric(vertical=25, horizontal=15)



    def build(self):
        self.controls = [
            ft.TextButton("Exit", on_click=lambda _: self.database.sign_out())
        ]
import flet as ft

from database.supabase_client import SupabaseClient


class SignUpView(ft.View):
    def __init__(self, page: ft.Page, database: SupabaseClient):
        super().__init__()
        self.page = page
        self.database = database

        self.route = '/sign_in'
        self.fullscreen_dialog = True
        self.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER


    def build(self):
        self.email = ft.TextField(
            hint_text='Почта', 
            bgcolor='secondarycontainer, 0.5',
            height=50, 
            border_width=0,
            border_radius=10,
            content_padding=ft.padding.symmetric(0, 10),
        )
        
        self.password = ft.TextField(
            height=50, 
            border_width=0,
            border_radius=10,
            hint_text='Пароль', 
            bgcolor='secondarycontainer, 0.5',
            on_change=self.on_change_password,
            content_padding=ft.padding.symmetric(0, 10),
            password=True, can_reveal_password=True,
        )
        
        self.confirm_password = ft.TextField(
            height=50, 
            border_width=0,
            border_radius=10,
            hint_text='Подтвердить', 
            bgcolor='secondarycontainer, 0.5',
            password=True, can_reveal_password=True,
            on_change=self.on_change_password,
            content_padding=ft.padding.symmetric(0, 10),
        )
        
        self.create_account = ft.FilledTonalButton(
            'Создать аккаунт', 
            height=45, 
            on_click=self.on_click_create_account,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        )
        
        self.invalid_sign_up = ft.SnackBar(
            duration=4000,
            bgcolor=ft.colors.ERROR_CONTAINER,
            behavior=ft.SnackBarBehavior.FLOATING,
            dismiss_direction=ft.DismissDirection.DOWN,
            content=ft.Text('Неправильный логин или пароль', color=ft.colors.ERROR),
        )
        
        self.controls = [
            ft.Container(
                shadow=ft.BoxShadow(
                    color=ft.colors.with_opacity(0.05, ft.colors.ON_BACKGROUND), 
                    spread_radius=10, 
                    blur_radius=20, 
                    offset=ft.Offset(0, 0),
                    blur_style=ft.ShadowBlurStyle.OUTER,
                ),
                border_radius=10,
                bgcolor=ft.colors.BACKGROUND,
                padding=ft.padding.symmetric(20, 20),
                content=ft.Column(
                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text('Новый аккаунт', size=36, weight=ft.FontWeight.BOLD),
                        self.email,
                        self.password,
                        self.confirm_password,

                        ft.Row(
                            controls=[
                                ft.Container(expand=1, height=50, border_radius=10, bgcolor=ft.colors.PRIMARY_CONTAINER,
                                    alignment=ft.alignment.center,
                                    content=ft.Icon(ft.icons.KEYBOARD_BACKSPACE_ROUNDED, color=ft.colors.PRIMARY),
                                    on_click=self.on_click_back_to_sign_in,
                                ),
                                ft.Container(expand=1, height=50),
                                ft.Container(expand=3, height=50, border_radius=10, bgcolor=ft.colors.PRIMARY_CONTAINER,
                                    alignment=ft.alignment.center,
                                    content=ft.Text('Создать', color=ft.colors.PRIMARY, weight=ft.FontWeight.BOLD, size=16),
                                    on_click=self.on_click_create_account,
                                ),
                            ]
                        )
                    ]
                )
            )
        ]
    
    def on_click_back_to_sign_in(self, e: ft.ControlEvent):
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)
    
    def on_click_create_account(self, e: ft.ControlEvent):
        confirm_password = bool(self.password.value == self.confirm_password.value)
        data = self.database.sign_up(self.email.value, self.password.value)
        # Тут надо исправить, ты помнишь это. Почта регается игнорируя ошибку
        if data['success']:
            if confirm_password:
                self.page.go('/home')
            else:
                self.invalid_sign_up.content.value = 'Пароли должны совпадать'
                self.page.open(self.invalid_sign_up)
        else:
            self.invalid_sign_up.content.value = data['message']
            self.page.open(self.invalid_sign_up)
        self.page.update()

    def on_change_password(self, e: ft.ControlEvent):
        if self.password.value != self.confirm_password.value:
            self.password.bgcolor = 'error, 0.1'
            self.confirm_password.bgcolor = 'error, 0.1'
        else:
            self.password.bgcolor = 'secondarycontainer, 0.5'
            self.confirm_password.bgcolor = 'secondarycontainer, 0.5'
        self.page.update()







            

    

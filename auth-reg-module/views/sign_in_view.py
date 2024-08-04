import flet as ft

from database.supabase_client import SupabaseClient


class SignInView(ft.View):
    def __init__(self, page: ft.Page, database: SupabaseClient):
        super().__init__()
        self.page = page
        self.database = database

        
        self.route = '/sign_in'
        self.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER


    def build(self):
        self.email = ft.TextField(
            height=45, 
            border_width=0,
            border_radius=10,
            hint_text='Почта', 
            bgcolor='secondarycontainer, 0.5',
            on_change=self.on_change_email,
            content_padding=ft.padding.symmetric(0, 10),
        )
        
        self.password = ft.TextField(
            height=45, 
            border_width=0,
            border_radius=10,
            hint_text='Пароль', 
            content_padding=ft.padding.symmetric(0, 10),
            bgcolor='secondarycontainer, 0.5',
            password=True, 
            can_reveal_password=True,
        )

        self.sign_in = ft.FilledTonalButton(
            'Войти',    
            on_click=self.on_click_sign_in,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        )

        
        self.invalid_sign_in = ft.SnackBar(
            duration=4000,
            bgcolor=ft.colors.ERROR_CONTAINER,
            behavior=ft.SnackBarBehavior.FLOATING,
            dismiss_direction=ft.DismissDirection.DOWN,
            content=ft.Text('Неправильный логин или пароль', color=ft.colors.ERROR),
        )
        
        self.controls = [
            ft.Container(

                shadow=ft.BoxShadow(
                    color=ft.colors.with_opacity(0.06, ft.colors.ON_BACKGROUND), 
                    spread_radius=10, 
                    blur_radius=20, 
                    offset=ft.Offset(0, 0),
                    blur_style=ft.ShadowBlurStyle.OUTER,
                ),
                bgcolor=ft.colors.BACKGROUND,
                border_radius=10,
                padding=15,

                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls = [
                        ft.Text('Вход в аккаунт', size=36, weight=ft.FontWeight.BOLD),
                        ft.Container(   
                            content=ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.END,
                                controls=[
                                    self.email,
                                    self.password,
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        spacing=30,
                                        controls=[
                                            ft.Container(
                                                expand=1, 
                                                height=50, 
                                                border_radius=10, 
                                                bgcolor=ft.colors.PRIMARY_CONTAINER, 
                                                content=ft.Icon(ft.icons.PERSON_ADD_ALT_1_ROUNDED, color=ft.colors.PRIMARY),
                                                on_click=lambda _: self.page.go('/sign_up')),
                                            ft.Container(expand=1, height=50),
                                            ft.Container(
                                                expand=3, 
                                                height=50, 
                                                border_radius=10, ink=True,
                                                alignment=ft.alignment.center, 
                                                bgcolor=ft.colors.PRIMARY_CONTAINER,
                                                on_click=self.on_click_sign_in,
                                                content=ft.Text('Войти', size=16, weight=ft.FontWeight.BOLD, color=ft.colors.PRIMARY)),
                                        ]
                                    ),
                                    ft.Text('', size=13, spans=[ft.TextSpan('Забыли пароль?',
                                        on_click=self.on_click_forgot_password,
                                        style=ft.TextStyle(color=ft.colors.PRIMARY))]
                                    ),
                                ]
                            )
                        )
                    ]
                )
            )
        ]

    def on_change_email(self, e: ft.ControlEvent):
        self.email.bgcolor = 'secondarycontainer, 0.5'
        self.email.update()

    def on_click_forgot_password(self, e: ft.ControlEvent):
        if self.email.value:
            data = self.database.reset_password(self.email.value)

            if data['success']:
                self.page.open(
                    ft.AlertDialog(
                        adaptive=True,
                        title=ft.Text('Сброс пароля', text_align=ft.TextAlign.CENTER),
                        content=ft.Text(data['message'], text_align=ft.TextAlign.CENTER),
                        actions=[ft.TextButton('Ок', on_click=lambda e: self.page.close(e.control))],
                        actions_alignment=ft.MainAxisAlignment.END,
                    )
                )
            else:
                self.invalid_sign_in.content.value = data['message']
                self.page.open(self.invalid_sign_in)
        else:
            self.email.bgcolor = 'error, 0.1'
        self.page.update()

    def on_click_sign_in(self, e: ft.ControlEvent):
        data = self.database.sign_in(self.email.value, self.password.value)

        if data['success']:
            self.page.go('/home')
            self.password.value = ''
        else:
            self.invalid_sign_in.content.value = data['message']
            self.page.open(self.invalid_sign_in)
        self.page.update()
        
import flet as ft

from database.supabase_client import SupabaseClient
from views.sign_in_view import SignInView
from views.sign_up_view import SignUpView
from views.home_view import HomeView


class Controller:
    def __init__(self, page: ft.Page, database: SupabaseClient):
        self.page = page
        self.database = database
        
        self.routes = {
            "/sign_in": SignUpView(page, database),
            "/sign_up": SignInView(page, database),
            "/home": HomeView(page, database),
        }

    def route_change(self, route: ft.RouteChangeEvent):
        route = route.route
        view_exists = any(view.route == route for view in self.page.views)

        if not view_exists:
            self.page.views.append(self.routes[route])
        self.page.update()

    def view_pop(self, view: ft.ViewPopEvent):
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)
        
import logging
import flet as ft

from controller import Controller
from database.supabase_client import SupabaseClient
from views.sign_in_view import SignInView

#logging.basicConfig(level=logging.DEBUG)
#logging.getLogger("supabase").setLevel(logging.INFO)


def main(page: ft.Page):
    database = SupabaseClient(page)
    router = Controller(page, database)
    index = SignInView(page, database)
    
    page.views[0] = index
    page.on_route_change = router.route_change
    page.on_view_pop = router.view_pop
    if database.relevance_of_token():
        page.go('/home')

    page.update()
    
if __name__ == "__main__":
    ft.app(target=main, assets_dir='assets')

    
import time
import json
import flet as ft
from datetime import date, datetime
from gotrue.types import Session, User, AuthResponse, UserIdentity
from gotrue.errors import AuthError
from supabase import create_client, Client

from config import SUPABASE_KEY, SUPABASE_URL, WEB_SITE

error_messages = {
    "For security purposes, you can only request this once every 60 seconds": "В целях безопасности вы можете запросить только один раз каждые 60 секунд",
    "Unable to validate email address: invalid format":"Неверный формат почты",
    "Password should be at least 6 characters.":"Пароль должен иметь не менее 6 символов",
    "Invalid login credentials": "Неправильный логин или пароль",
    "Signup requires a valid password": "Укажите пароль и подтвердите его",
    "User already registered": "Пользователь с такой почтой уже существует",
    "Cannot send a request, as the client has been closed." : "Cannot send a request, as the client has been closed",
    "Email rate limit exceeded":"Превышен лимит попыток регистрации, вернитесь позже",
    "You must provide either an email or phone number and a password": "Поля не должны быть пустыми",
    "Password expired": "Срок действия пароля истек",
    "Account locked": "Аккаунт заблокирован",
}

class SupabaseClient:
    def __init__(self, page: ft.Page):
        self.page = page
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        self.web_site: str = WEB_SITE

        self.user: User = None
        self.session: Session = None

        self.access_token: str = page.client_storage.get('access_token')
        self.refresh_token: str = page.client_storage.get('refresh_token')
        self.expires_at: str = page.client_storage.get('expires_at')

    def sign_up(self, email: str, password: str) -> dict:
        try:
            response: AuthResponse = self.supabase.auth.sign_up(
                credentials={
                    "email": email,
                    "password": password,
                }
            )


            self.__save_auto_response(response)
            
            return {'success': True}
            
        except AuthError as exp:
            return {'success': False, 'message': error_messages[exp.message]}

    def sign_in(self, email: str, password: str) -> dict:
        try:
            response: AuthResponse = self.supabase.auth.sign_in_with_password(
                credentials={
                    "email": email,
                    "password": password,
                }
            )
            
            self.__save_auto_response(response)
    
            return {'success': True}
        
        except AuthError as exp:
            return {'success': False, 'message': error_messages[exp.message]}
   
    def sign_out(self) -> None:
        self.page.go('/home')
        del self.page.views[1:]

        self.page.client_storage.clear()
        self.supabase.auth.sign_out()

    def reset_password(self, email: str) -> dict:
        try:
            self.supabase.auth.reset_password_email(email)

            return {'success': True, 'message': f'Письмо со ссылкой было отправлено на указанный электронный адрес - {email}'}
        
        except AuthError as exp:
            return {'success': False, 'message': error_messages[exp.message]}
    
    def relevance_of_token(self) -> bool:
        current_time = time.time()
        if self.access_token:
            if self.expires_at > current_time:
                response: AuthResponse = self.supabase.auth.set_session(self.access_token, self.refresh_token)
                self.__save_auto_response(response)
                return True # User token is relevance
            else:
                return self.__on_refresh_token() # User have token, but need to refresh
        else:
            return False # User not have token, we ask the user to enter
        
    def __on_refresh_token(self) -> bool:
        try:

            response: AuthResponse = self.supabase.auth.refresh_session(
                refresh_token=self.refresh_token
            )

            self.__save_auto_response(response)

            return True
        
        except AuthError as exp:
            return False # Failed to update the token, we ask the user to enter
    
    def __save_auto_response(self, response: AuthResponse) -> None:
        self.user = response.user
        self.session = response.session

        self.page.client_storage.set('access_token', response.session.access_token)
        self.page.client_storage.set('refresh_token', response.session.refresh_token)
        self.page.client_storage.set('expires_at', response.session.expires_at)

from allauth.account.adapter import DefaultAccountAdapter


class NoSignupAccountAdapter(DefaultAccountAdapter):
    """
    Адаптер для отключения регистрации новых пользователей.
    """
    def is_open_for_signup(self, request):
        """
        Возвращаем False, чтобы запретить регистрацию.
        """
        return False
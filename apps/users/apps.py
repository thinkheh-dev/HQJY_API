from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = "后台用户管理"
    
    def ready(self):
        import users.signals

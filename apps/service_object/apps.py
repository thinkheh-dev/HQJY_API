from django.apps import AppConfig


class ServiceObjectConfig(AppConfig):
    name = 'service_object'
    verbose_name = '服务/需求管理'
    
    def ready(self):
        import service_object.signals

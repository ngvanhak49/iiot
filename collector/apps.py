from django.apps import AppConfig
from .mqtt import datasource_mqtt_init

class CollectorConfig(AppConfig):
    name = 'collector'

    def ready(self):
        print("collector done")
        #datasource_mqtt_init()

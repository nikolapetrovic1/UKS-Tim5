from django.apps import apps
from django.contrib import admin


# Register your models here.
app_models = apps.get_app_config('GitApp').get_models()

for model in app_models:
    admin.site.register(model)
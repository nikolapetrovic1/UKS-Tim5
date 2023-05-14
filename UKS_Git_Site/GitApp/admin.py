from django.contrib import admin

from .models import Repository
from .models import CustomUser
# Register your models here.

admin.site.register(Repository)
admin.site.register(CustomUser)
from django.contrib import admin

from .models import Repository
from .models import User
# Register your models here.

admin.site.register(Repository)
admin.site.register(User)
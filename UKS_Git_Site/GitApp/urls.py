from django.urls import path
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:repository_id>/", views.single_repo, name="single_repository"),
    path("testredispage/", views.cached_initial, name="test_redis_page"),
    path("login/", views.user_login, name="login"),
    path("test/",views.test,name="test")
]
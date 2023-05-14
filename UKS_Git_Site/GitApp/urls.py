from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:repository_id>/", views.single_repo, name="single_repository"),
    path("testredispage/", views.cached_initial, name="test_redis_page"),
    path("<int:repository_id>/<int:user_id>/",views.add_users_to_repo, name="add_users_to_repo")
]
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:repository_id>/", views.single_repo, name="single_repository"),
    path("testredispage/", views.cached_initial, name="test_redis_page"),
    path("profile_page/<int:user_id>", views.profile_page, name="profile_page"),
    path("new_star/<int:repository_id>", views.new_star, name="new_star"),
    path("delete_star/<int:star_id>", views.delete_star, name="delete_star")
]
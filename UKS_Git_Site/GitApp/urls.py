from django.urls import path, include
from . import views, user_view, repo_views

urlpatterns = [
    path("", views.index, name="index"),
    path("repo/<int:repository_id>/", views.single_repo, name="single_repository"),
    path("repo/<int:repository_id>/milestones", repo_views.get_milestones, name="repo_milestones"),
    path("repo/<int:repository_id>/milestone/create",repo_views.create_milestone,name="create_milestone"),
    path("repo/create",repo_views.create_repository,name="create_repository"),
    path("<int:user_id>/repos",repo_views.get_repos_by_user,name="repo_by_user"),
    path("testredispage/", views.cached_initial, name="test_redis_page"),
    path("login/", user_view.user_login, name="login"),
    path("logout/", user_view.user_logout, name="logout"),
    path("user/delete/",user_view.delete_user, name="delete_user"),
    path("test/",user_view.test,name="test"),
    path("profile/",user_view.user_profile,name="user_profile"),
    path("profile/repos/",repo_views.get_logged_user_repos,name="repo_by_user"),
    path("register/",user_view.user_register,name="user_register"),
    path("edit_profile",user_view.user_update,name="user_update"),
    path("change_password",user_view.user_change_password,name="change_password"),
    path("new_star/<int:repository_id>", views.new_star, name="new_star"),
    path("delete_star/<int:star_id>", views.delete_star, name="delete_star"),
]
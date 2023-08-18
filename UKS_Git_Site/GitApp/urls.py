from django.urls import path, include
from . import views, user_view
from .model_views import milestone_views, issue_views, repo_views


issue_patterns = [
    path(
        "repo/<int:repository_id>/issue/<int:issue_id>",
        issue_views.get_issue,
        name="issue_page",
    ),
    path(
        "repo/<int:repository_id>/issues/create",
        issue_views.create_issue,
        name="create_issue",
    ),
    path(
        "repo/<int:repository_id>/issue/<int:issue_id>/update",
        issue_views.update_issue,
        name="update_issue",
    ),
    path(
        "repo/<int:repository_id>/issue/<int:issue_id>/close",
        issue_views.close_issue,
        name="close_issue",
    ),
    path(
        "repo/<int:repository_id>/issue/<int:issue_id>/open",
        issue_views.open_issue,
        name="open_issue",
    ),
]


milestone_patterns = [
    path(
        "repo/<int:repository_id>/milestone/<int:milestone_id>",
        milestone_views.get_milestone,
        name="milestone_page",
    ),
    path(
        "repo/<int:repository_id>/milestone/<int:milestone_id>/close",
        milestone_views.close_milestone,
        name="close_milestone",
    ),
    path(
        "repo/<int:repository_id>/milestone/<int:milestone_id>/open",
        milestone_views.open_milestone,
        name="open_milestone",
    ),
    path(
        "repo/<int:repository_id>/milestones",
        milestone_views.get_milestones,
        name="repo_milestones",
    ),
    path(
        "repo/<int:repository_id>/milestones/create",
        milestone_views.create_milestone,
        name="create_milestone",
    ),
    path(
        "repo/<int:repository_id>/milestone/<int:milestone_id>/update",
        milestone_views.update_milestone,
        name="update_milestone",
    ),
    path(
        "repo/<int:repository_id>/milestone/<int:milestone_id>/delete",
        milestone_views.delete_milestone,
        name="delete_milestone",
    ),
    path(
        "repo/<int:repository_id>/milestone/<int:milestone_id>/open_issues",
        milestone_views.milestone_open_issues,
        name="milestone_open_issues",
    ),
    path(
        "repo/<int:repository_id>/milestone/<int:milestone_id>/closed_issues",
        milestone_views.milestone_closed_issues,
        name="milestone_closed_issues",
    ),
]

user_patterns = [
    path("login/", user_view.user_login, name="login"),
    path("logout/", user_view.user_logout, name="logout"),
    path("user/delete/", user_view.delete_user, name="delete_user"),
    path("test/", user_view.test, name="test"),
    path("profile/", user_view.user_profile, name="user_profile"),
    path("profile/repos/", repo_views.get_logged_user_repos, name="repo_by_user"),
    path("register/", user_view.user_register, name="user_register"),
    path("edit_profile", user_view.user_update, name="user_update"),
    path("change_password", user_view.user_change_password, name="change_password"),
    path("labels", views.get_labels, name="labels"),
]

repo_patterns = [
    path("fork/<int:repository_id>", repo_views.fork_repo, name="fork_repo"),
    path("watch/<int:repository_id>", repo_views.watch_repo, name="watch_repo"),
    path("repo/rename/<int:repository_id>", repo_views.rename_repo, name="rename_repo"),
    path("repo/<int:repository_id>/delete", repo_views.delete_repo, name="delete_repo"),
    path("repo/create", repo_views.create_repository, name="create_repository"),
    path("repo/<int:repository_id>/", repo_views.single_repo, name="single_repository"),
    path(
        "repo/<int:repository_id>/issues",
        repo_views.get_repo_issues,
        name="repo_issues",
    ),
    path(
        "<int:user_id>/repos",
        repo_views.get_repos_by_user_id,
        name="repos_by_user_id",
    ),
    path(
        "repo/<int:repository_id>/default_branch",
        repo_views.select_default_branch,
        name="select_default_branch",
    ),
    path(
        "repo/<int:repository_id>/create_branch",
        repo_views.create_branch,
        name="create_branch",
    ),
]

urlpatterns = (
    [
        path("", views.index, name="index"),
        path("testredispage/", views.cached_initial, name="test_redis_page"),
        path("new_star/<int:repository_id>", views.new_star, name="new_star"),
        path("delete_star/<int:star_id>", views.delete_star, name="delete_star"),
        path(
            "create_comment/<int:task_id>", views.create_comment, name="create_comment"
        ),
        path(
            "create_reaction/<int:comment_id>/<str:reaction_type>",
            views.create_reaction,
            name="create_reaction",
        ),
    ]
    + repo_patterns
    + issue_patterns
    + milestone_patterns
    + user_patterns
)

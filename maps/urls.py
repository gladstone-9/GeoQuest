from django.urls import path, include
from . import views

app_name = "maps"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("create", views.CreateView.as_view(), name="create"),
    path("approve", views.ApproveView.as_view(), name="approve"),
    # path("<int:pk>", views.DetailsView.as_view(), name="details"),
    path("<int:pk>", views.UpdateView.as_view(), name="details"),
    path("play/<int:pk>", views.PlayView.as_view(), name="play"),
    path("play/<int:pk>/<int:locnum>", views.GuessView.as_view(), name="guess"),
    path("search", views.SearchView.as_view(), name="search"),
    path("leaderboard", views.LeaderboardView.as_view(), name="leaderboard"),
    path("myQuests", views.QuestView.as_view(), name="myQuests"),
]

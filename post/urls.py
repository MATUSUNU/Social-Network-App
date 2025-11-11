from django.urls import path

from .views import (
  PostListView, PostCreateView,
  PostDetailView, PostUpdateView,
  PostDeleteView, like_post,
  comment_create, comment_delete,
)


app_name = "post"

urlpatterns = [
  path("", PostListView.as_view(), name="post_list"),
  path("create/", PostCreateView.as_view(), name="post_create"),
  path("<int:pk>/", PostDetailView.as_view(), name="post_detail"),
  path("<int:pk>/update/", PostUpdateView.as_view(), name="post_update"),
  path("<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),

  path("<int:pk>/like/", like_post, name="like_post"),
  path("<int:pk>/comment/", comment_create, name="comment_create"),
  # path("<int:pk>/comment/update/", comment_update, name="comment_update"),
  path("<int:pk>/comment/delete/", comment_delete, name="comment_delete"),
]

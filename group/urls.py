from django.urls import path

from .views import (
  GroupListView, GroupDetailView,
  GroupCreateView, GroupUpdateView,
  GroupDeleteView, member_group,
)

app_name = "group"

urlpatterns = [
  path("", GroupListView.as_view(), name="group_list"),
  path("<int:pk>/", GroupDetailView.as_view(), name="group_detail"),
  path("create/", GroupCreateView.as_view(), name="group_create"),
  path("<int:pk>/update/", GroupUpdateView.as_view(), name="group_update"),
  path("<int:pk>/delete/", GroupDeleteView.as_view(), name="group_delete"),

  path("<int:pk>/member/", member_group, name="member_group"),
]

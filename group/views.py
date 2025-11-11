from django.shortcuts import render, redirect, get_object_or_404

from django.views.generic import (
  TemplateView, ListView, DetailView,
  CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .models import Group, Membership


class GroupListView(ListView):
  template_name = "group/group_list.html"
  context_object_name = "groups"
  model = Group

  # Filter by creator only
  # def get_queryset(self):
  #   return Group.objects.filter(created_by=self.request.user)


class GroupDetailView(DetailView):
  template_name = "group/group_detail.html"
  context_object_name = "group"
  model = Group

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    if self.request.user == self.object.created_by:
      context["is_owner"] = True
    else:
      context["is_owner"] = False
    context["posts"] = self.object.posts.all()
    return context


class GroupCreateView(LoginRequiredMixin, CreateView):
  template_name = "group/group_form.html"
  model = Group
  fields = ["name", "description"]
  success_url = reverse_lazy("group:group_list")

  def form_valid(self, form):
    form.instance.created_by = self.request.user  # The creator is currently auth user.
    # return super().form_valid(form)
    response = super().form_valid(form)

    # Automatically make the creator a member
    Membership.objects.get_or_create(
        user=self.request.user,
        group=self.object
    )
    return response


class GroupUpdateView(LoginRequiredMixin, UpdateView):
  template_name = "group/group_form.html"
  model = Group
  fields = ["name", "description"]
  success_url = reverse_lazy("group:group_list")


class GroupDeleteView(LoginRequiredMixin, DeleteView):
  template_name = "group/group_confirm_delete.html"
  model = Group
  success_url = reverse_lazy("group:group_list")


@login_required
def member_group(request, pk):
  group = get_object_or_404(Group, pk=pk)

  member, created = group.memberships.get_or_create(
    user = request.user,
    group = group
  )
  if not created:  # If the "user is already a member", this request is treated as a "leave action".
    member.delete()
  return redirect("group:group_detail", pk=group.id)

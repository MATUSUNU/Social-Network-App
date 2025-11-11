from django.shortcuts import render, redirect, get_object_or_404

from django.views.generic import (
  TemplateView, ListView, DetailView,
  CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .models import Post, Comment
from group.models import Group


class PostListView(ListView):
  template_name = "post/post_list.html"
  context_object_name = "posts"
  model = Post

  # Filter by user only
  # def get_queryset(self):
  #   return Post.objects.filter(user=self.request.user)


class PostDetailView(DeleteView):
  template_name = "post/post_detail.html"
  model = Post

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['comments'] = self.object.comments.all()
    return context


class PostCreateView(LoginRequiredMixin, CreateView):
  template_name = "post/post_form.html"
  model = Post
  fields = ["content", "image", "group"]
  success_url = reverse_lazy("post:post_list")

  def get_form(self, form_class=None):
    form = super().get_form(form_class)
    form.fields['group'].queryset = Group.objects.filter(created_by=self.request.user)
    return form

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
  template_name = "post/post_form.html"
  model = Post
  fields = ["content", "image"]
  success_url = reverse_lazy("post:post_list")


class PostDeleteView(LoginRequiredMixin, DeleteView):
  template_name = "post/post_confirm_delete.html"
  model = Post
  success_url = reverse_lazy("post:post_list")


@login_required
def like_post(request, pk):
  # First try
  # post = Post.objects.get(pk=pk)
  # post.likes.create(user=request.user, post=post)
  # return redirect("post:post_list")

  # Second Solution
  post = get_object_or_404(Post, pk=pk)
  like, created = post.likes.get_or_create(user=request.user, post=post)
  if not created:
    like.delete()
  return redirect("post:post_list")

  # Notes:-
  ## It checks if a "Like object" exists for this "post" and "user".
  ## If it exists: "created = False", and it "returns the existing like".
  ## If it doesn’t: it "creates a new Like object", and "created = True".

@login_required
def comment_create(request, pk):
  post = get_object_or_404(Post, pk=pk)

  if request.method == "POST":
    content = request.POST['content']

    if content:
      Comment.objects.create(
        user = request.user,
        post = post,
        content = content
      )
  return redirect("post:post_detail", pk=post.id)

# @login_required
# def comment_update(request, pk):
#   comment = get_object_or_404(Comment, pk=pk)

#   if request.method == "POST":
#     content = request.POST['content']

#     if content:
#       comment.content = content
#       comment.save()
#   return redirect("post:post_detail", pk=comment.post.id)

@login_required
def comment_delete(request, pk):
  comment = get_object_or_404(Comment, pk=pk)

  if request.method == "POST":
    comment.delete()

  return redirect("post:post_detail", pk=comment.post.id)

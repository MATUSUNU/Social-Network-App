from django.db import models

from django.contrib.auth.models import User
from group.models import Group


class Post(models.Model):
  user = models.ForeignKey(
    User, on_delete=models.CASCADE, related_name="posts"
  )
  group = models.ForeignKey(
    Group, on_delete=models.CASCADE, related_name="posts"
  )
  content = models.TextField()
  image = models.ImageField(
    upload_to="post_images/", blank=True, null=True
  )
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    ordering = ["-updated_at"]

  def __str__(self):
    return self.content[:15]

  @property
  def num_likes(self):
      return self.likes.count()


class Like(models.Model):
  user = models.ForeignKey(
    User, on_delete=models.CASCADE, related_name="likes"
  )
  post = models.ForeignKey(
    Post, on_delete=models.CASCADE, related_name="likes"
  )
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    unique_together = ('user', 'post')

  def __str__(self):
    return f"Like by {self.user}"


class Comment(models.Model):
  user = models.ForeignKey(
    User, on_delete=models.CASCADE, related_name="comments"
  )
  post = models.ForeignKey(
    Post, on_delete=models.CASCADE, related_name="comments"
  )
  content = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"Comment by {self.user}"

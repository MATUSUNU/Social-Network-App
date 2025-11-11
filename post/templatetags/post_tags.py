from django import template

register = template.Library()

@register.filter
def user_liked_post(post, user):
    """Check if a user liked a specific post"""
    return post.likes.filter(user=user).exists()

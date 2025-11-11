from django import template

register = template.Library()


@register.filter
def user_joined_group(group, user):
  """check user joined the specific group."""
  return group.memberships.filter(user=user).exists()

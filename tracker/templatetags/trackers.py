from django import template
from tracker.models import Tracker

register = template.Library()

@register.tag
def get_trackers(parser, token):
  try:
    tag_name, limit, middle, var_name = token.contents.split()
  except ValueError:
    msg = 'Tag requires arguments'
    raise template.TemplateSyntaxError(msg)
  if 'as' != middle:
    msg = 'Invalid syntax: must be "<tag_name> as <var_name>"'
    raise template.TemplateSyntaxError(msg)
  try:
    limit = int(limit)
  except ValueError:
    msg = 'Invalid syntax: limit must be integer"'
    raise template.TemplateSyntaxError(msg)

  return TrackersNode(var_name, limit)
  
class TrackersNode(template.Node):
  def __init__(self, var_name, limit):
    self.var_name = var_name
    self.limit = limit

  def render(self, context):
    if hasattr(context['request'], 'muaccount'):
      trackers = Tracker.objects.filter(muaccount = context['request'].muaccount)
    else:
      trackers = Tracker.objects.filter(is_public=True)
    if self.limit:
      trackers = trackers[:self.limit]
    context[self.var_name] = trackers
    return ''


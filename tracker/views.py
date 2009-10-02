from tracker.models import TwitSource, TwitSourceGroup
from django.views.generic.simple import direct_to_template
from urlparse import urlparse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.views.generic.create_update import update_object, delete_object
from django.core.urlresolvers import reverse

def save_source(name, type):
  try:
    TwitSource.objects.get(name = name)
  except ObjectDoesNotExist:
    source = TwitSource()
    source.name = name
    source.type = type
    source.save()    

def add_user_by_name(name):
#  if twitter_user_exists(name):
  save_source(name, TwitSource.USER)

def add_user_by_url(url):
  name = urlparse(url)[2]
  name = name.strip('/ ')
  add_user_by_name(name)

def add_term(term):
  save_source(term, TwitSource.TERM)

@login_required()
def waw(request):
  context_vars = dict()
  if request.method == 'POST':
    username = request.POST.get('nametxt', '')
    userurl = request.POST.get('slugtxt', '')
    termtext = request.POST.get('termtxt', '')
    try:
      if username: add_user_by_name(username)
      if userurl: add_user_by_url(userurl)
      if termtext: add_term(termtext)
    except Exception, e:
      context_vars['error'] = e

  sources = TwitSource.objects.all()
  context_vars['users'] = sources.filter(type=1)
  context_vars['terms'] = sources.filter(type=2)
  return direct_to_template(request, template='tweets/waw.html', extra_context=context_vars)

@login_required()
def edit_twitsource(request, object_id):
  return update_object(request, object_id=object_id, model=TwitSource, login_required=True, template_name='tweets/form.html', post_save_redirect=reverse('tweets_waw'))

@login_required()  
def delete_twitsource(request, object_id):
  """
  Until we don't use muaccounts, we delete object from db here
  """
  context_vars = dict()
  if request.method == 'POST':
    try:
      object = TwitSource.objects.get(id=object_id)
    except ObjectDoesNotExist:
      context_vars['error'] = True
      request.method = 'GET'

  return delete_object(request, object_id=object_id, model=TwitSource, post_delete_redirect=reverse('tweets_waw'), login_required=True, template_name='tweets/delete_source.html', extra_context=context_vars)

from tracker.forms import SourceListForm
def process_source_form(form_obj, group):
  if form_obj.is_valid():
    form_data = form_obj.cleaned_data
    if group:
      users = TwitSource.objects.filter(id__in=form_data['users'])
      for item in users:
        group.twit_sources.add(item)
      group.save()


@login_required()
def manage_groups(request, group_id=None, source_id=None):
  context_vars = dict()
  sources = TwitSource.objects.all()
  context_vars['userlist_form'] = SourceListForm(sources.filter(type=TwitSource.USER))
  context_vars['termlist_form'] = SourceListForm(sources.filter(type=TwitSource.TERM))
  context_vars['groups'] = TwitSourceGroup.objects.all()

  if group_id:
    try:
      context_vars['group'] = TwitSourceGroup.objects.get(id=group_id)
    except ObjectDoesNotExist:
      context_vars['error'] = 'Cannot edit non-existent group'
      
    if source_id:
      try:
        source = TwitSource.objects.get(id=source_id)
        context_vars['group'].twit_sources.remove(source)
        context_vars['group'].save()
      except Exception, e:
        context_vars['error'] = e

  if request.method == 'POST':
    group_name = request.POST.get('nametxt', '')
    group_slug = request.POST.get('slugtxt', '')
    description = request.POST.get('descrtxt', '')
    max_status = request.POST.get('maxstatustxt', '')
    update_interval = request.POST.get('updatetxt', '')

    if group_name:
      try:
        group = TwitSourceGroup()
        group.name = group_name
        group.slug = group_slug  #TODO: generate slug from name
        group.description = description
        group.max_status = int(max_status)
        group.update_interval = int(update_interval)
        group.save()
      except Exception, e:
        context_vars['error'] = e

    if group_id:
      userlist_form = SourceListForm(sources.filter(type=TwitSource.USER), request.POST, request.FILES)
      termlist_form = SourceListForm(sources.filter(type=TwitSource.TERM), request.POST, request.FILES)
      process_source_form(userlist_form, context_vars['group'])
      process_source_form(termlist_form, context_vars['group'])
    
  return direct_to_template(request, template='tweets/manage.html', extra_context=context_vars)

@login_required()
def delete_twitgroup(request, object_id):
  context_vars = dict()
  if request.method == 'POST':
    try:
      object = TwitSource.objects.get(id=object_id)
    except ObjectDoesNotExist:
      context_vars['error'] = True
      request.method = 'GET'

  return delete_object(request, object_id=object_id, model=TwitSourceGroup, post_delete_redirect=reverse('tweets_manage_groups'), login_required=True, template_name='tweets/delete_group.html', extra_context=context_vars)

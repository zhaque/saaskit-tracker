from tracker.models import Tracker
from django.views.generic.simple import direct_to_template
from urlparse import urlparse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.views.generic.create_update import update_object, delete_object
from django.core.urlresolvers import reverse
from django.views.generic.create_update import create_object
from tracker.forms import TrackerForm
from django.http import HttpResponseRedirect
from django.http import Http404

def index(request):
    context_vars = dict()
    context_vars['trackers'] = Tracker.objects.filter(muaccount = request.muaccount)
    return direct_to_template(request, template='tracker/index.html', extra_context=context_vars)
    
def add(request):
    context_vars = dict()
    form = TrackerForm()
    if request.method == 'POST':
        form = TrackerForm(request.POST, request.FILES)
        if form.is_valid():
            tracker = form.save(commit=False)
            tracker.status = Tracker.PENDING
            tracker.muaccount = request.muaccount
            tracker.save()
            return HttpResponseRedirect(reverse('tracker_index'))
    context_vars['form'] = form
    return direct_to_template(request, template='tracker/form.html', extra_context=context_vars)

def edit(request, tracker_id):
    context_vars = dict()
    try:
        tracker = Tracker.objects.get(id=tracker_id)
    except ObjectDoesNotExist:
        raise Http404
    form = TrackerForm(instance=tracker)
    if request.method == 'POST':
        form = TrackerForm(request.POST, request.FILES, instance=tracker)
        if form.is_valid():
            tracker = form.save()
            return HttpResponseRedirect(reverse('tracker_index'))
    context_vars['form'] = form
    return direct_to_template(request, template='tracker/form.html', extra_context=context_vars)

def delete(request, tracker_id):
    return delete_object(request,object_id=tracker_id, model=Tracker, post_delete_redirect=reverse('tracker_index'), login_required=True, template_name='tracker/delete_tracker.html')



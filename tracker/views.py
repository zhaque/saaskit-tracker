from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from django.views.generic.create_update import update_object, delete_object
from django.http import HttpResponseRedirect
from django.http import Http404
from tracker.models import Tracker, Trend, Pack
from tracker.forms import TrackerForm, TrendForm

@login_required
def index(request):
    context_vars = dict()
    context_vars['trackers'] = Tracker.objects.filter(muaccount = request.muaccount)
    return direct_to_template(request, template='tracker/index.html', extra_context=context_vars)
    
@login_required
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
            form.save_m2m()
            return HttpResponseRedirect(reverse('tracker_index'))
    context_vars['form'] = form
    return direct_to_template(request, template='tracker/form.html', extra_context=context_vars)

@login_required
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

@login_required
def index_trends(request):
    context_vars = dict()
    context_vars['trends'] = Trend.objects.filter(muaccount = request.muaccount)
    return direct_to_template(request, template='tracker/index_trends.html', extra_context=context_vars)

@login_required
def add_trend(request):
    context_vars = dict()
    form = TrendForm()
    if request.method == 'POST':
        form = TrendForm(request.POST, request.FILES)
        if form.is_valid():
            trend = form.save(commit=False)
            trend.muaccount = request.muaccount
            trend.save()
            form.save_m2m()
            return HttpResponseRedirect(reverse('tracker_trend_index'))
    context_vars['form'] = form
    return direct_to_template(request, template='tracker/form.html', extra_context=context_vars)

@login_required
def edit_trend(request, trend_id):
    context_vars = dict()
    try:
        trend = Trend.objects.get(id=trend_id)
    except ObjectDoesNotExist:
        raise Http404
    form = TrendForm(instance=trend)
    if request.method == 'POST':
        form = TrendForm(request.POST, request.FILES, instance=trend)
        if form.is_valid():
            trend = form.save()
            return HttpResponseRedirect(reverse('tracker_trend_index'))
    context_vars['form'] = form
    return direct_to_template(request, template='tracker/form.html', extra_context=context_vars)

@login_required
def delete_trend(request, trend_id):
    return delete_object(request,object_id=trend_id, model=Trend, post_delete_redirect=reverse('tracker_trend_index'), login_required=True, template_name='tracker/delete_trend.html')

@login_required
def admin(request):
    context_vars = dict()
    all_packs = Pack.objects.all()
    if request.method == 'POST':
        muaccount = request.muaccount
        pack_ids = request.POST.getlist('packs')
        if len(pack_ids) < muaccount.owner.quotas.muaccount_packs:
            for pack in all_packs:
                muaccount.packs.remove(pack)
            for pack_id in pack_ids:
                pack = Pack.objects.get(id=pack_id)
                muaccount.packs.add(pack)
            muaccount.save()

    context_vars['packs'] = all_packs
    context_vars['packs_used'] = all_packs.filter(muaccounts = request.muaccount).count()
    
    context_vars['trackers'] = Tracker.objects.filter(muaccount = request.muaccount)
    context_vars['trends'] = Trend.objects.filter(muaccount = request.muaccount)
    return direct_to_template(request, template='manage_apps.html', extra_context=context_vars)

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from django.views.generic.create_update import update_object, delete_object
from django.http import HttpResponseRedirect
from django.http import Http404
from tracker.models import Tracker, Trend, Pack, TrendStatistics, TrackerStatistics, PackStatistics, ChannelStatistics, Statistics, ParsedResult
from tracker.forms import TrackerForm, TrendForm

@login_required
def index(request):
    context_vars = dict()
    context_vars['trackers'] = Tracker.objects.filter(muaccount = request.muaccount)
    return direct_to_template(request, template='tracker/index.html', extra_context=context_vars)
    
@login_required
def add(request):
    context_vars = dict()
    context_vars['caption'] = 'Add tracker'
    form = TrackerForm()
    if request.method == 'POST':
        form = TrackerForm(request.POST, request.FILES)
        if form.is_valid():
            tracker = form.save(commit=False)
            tracker.status = Tracker.PENDING
            tracker.muaccount = request.muaccount
            tracker.save()
            form.save_m2m()
            return HttpResponseRedirect(reverse('tracker_advanced_query', args=[tracker.id]))
    context_vars['form'] = form
    return direct_to_template(request, template='tracker/form.html', extra_context=context_vars)

@login_required
def advanced_query(request, tracker_id):
    context_vars = dict()
    values = dict()
    context_vars['caption'] = 'Refine query'
    tracker = Tracker.objects.get(id=tracker_id)
    has_twitter = False
    for pack in tracker.packs.all():
        for channel in pack.channels.all():
            if 'TwitterSearch' == channel.api:
                has_twitter=True
            if 'YqlSearch' == channel.api:
                return HttpResponseRedirect(reverse('tracker_index'))
    context_vars['pack_has_twitter'] = has_twitter
    values['ands'] = tracker.query
    
    if request.method == 'POST':
        values['ands'] = request.POST.get('ands', '')
        values['phrase'] = request.POST.get('phrase', '')
        values['ors'] = request.POST.get('ors', '')
        values['nots'] = request.POST.get('nots', '')
        values['url'] = request.POST.get('url', '')
        values['from'] = request.POST.get('from', '')
        values['to'] = request.POST.get('to', '')
        values['ref'] = request.POST.get('ref', '')
        values['near'] = request.POST.get('near', '')
        values['pos_tude'] = request.POST.get('pos_tude', '')
        values['neg_tude'] = request.POST.get('neg_tude', '')
        values['q_tude'] = request.POST.get('q_tude', '')
        values['filter'] = request.POST.get('filter', '')

        if values['ands']: query = values['ands']
        if values['phrase']: query += " \"%s\"" % values['phrase']
        if values['ors']:
            words = values['ors'].split() 
            for word in words:
                query += " %s OR" % word
            query = query[:-3]
        if values['nots']:
            words = values['nots'].split() 
            for word in words:
                query += " -%s" % word
        if values['url']:
            import re
            regexp = re.compile('^(?#Protocol)(?:(?:ht|f)tp(?:s?)\:\/\/|~/|/)?(?#Username:Password)(?:\w+:\w+@)?(?#Subdomains)(?:(?:[-\w]+\.)+(?#TopLevel Domains)(?:com|org|net|gov|mil|biz|info|mobi|name|aero|jobs|museum|travel|[a-z]{2}))(?#Port)(?::[\d]{1,5})?(?#Directories)(?:(?:(?:/(?:[-\w~!$+|.,=]|%[a-f\d]{2})+)+|/)+|\?|#)?(?#Query)(?:(?:\?(?:[-\w~!$+|.,*:]|%[a-f\d{2}])+=(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)(?:&(?:[-\w~!$+|.,*:]|%[a-f\d{2}])+=(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)*)*(?#Anchor)(?:#(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)?$')
            res = regexp.match(values['url'])
            if 'http://' != values['url'][:7] and 'ftp://' != values['url'][:6]:
                values['url'] = 'http://' + values['url']
            if res:
                query += ' ' + values['url']
        if values['from']:
            query += ' from:%s' % values['from']
        if values['to']:
            query += ' to:%s' % values['to']
        if values['ref']:
            query += ' @%s' % values['ref']
        if values['near']:
            words = values['near'].split()
            if len(words) > 1:
                query += ' near:\"%s\"' % values['near']
            else:
                query += ' near:%s' % values['near']
        if values['pos_tude']:
            query += ' ' + values['pos_tude']
        if values['neg_tude']:
            query += ' ' + values['neg_tude']
        if values['q_tude']:
            query += ' ' + values['q_tude']
        if values['filter']:
            query += ' filter:%s' % values['filter']

        tracker.query = query
        tracker.save()
        return HttpResponseRedirect(reverse('tracker_index'))
    context_vars['values'] = values
    return direct_to_template(request, template='tracker/adv_queryform.html', extra_context=context_vars)

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

@login_required
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

@login_required
def stats(request, stats_id=None):
    context_vars = dict()
    trend_stats = list(TrendStatistics.objects.all())
    for ts in trend_stats[:]:
        if ts.trend.muaccount != request.muaccount:
            trend_stats.remove(ts)    
    context_vars['trend_stats'] = trend_stats
    
    if stats_id:
        context_vars['cur_stats'] = Statistics.objects.get(id=stats_id)
        context_vars['latest'] = context_vars['cur_stats'].owner.get_latest()
        if isinstance(context_vars['cur_stats'].owner, TrackerStatistics):
            tracker = context_vars['cur_stats'].owner.tracker
            context_vars['tracker'] = tracker

    return direct_to_template(request, template='stats.html', extra_context=context_vars)

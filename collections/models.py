from django.db import models
#from muaccount.models import MUAccount

class TwitSourceGroup(models.Model):
  """
  Model groups twitter sources, Every plan owner has its own list of groups
  """
  # group name
  name = models.CharField('name', max_length=255)
  slug = models.SlugField('slug')
  description = models.TextField('description', blank=True)
  # max status, default value is maximum
  max_status = models.PositiveSmallIntegerField('max status', default=100)
  # update interval in minuites, default value is a minimum
  update_interval = models.PositiveSmallIntegerField('update interval', default=30)

  # muaccount this group belongs to, groups are not reusable by others, so we use ForeignKey instead of ManyToManyField
#  account = models.ForeignKey(MUAccount, verbose_name='account')
  
  class Meta:
#    unique_together = ('name', 'account')
    ordering = ['name']
    verbose_name = 'twitter source group'
    verbose_name_plural = 'twitter source groups'

  def __unicode__(self):
    return self.name

class TwitSource(models.Model):
  """
  TwitSource model describes twitter data source, i.e. twitter user or search terms/phrases, 
  TwitSources are organized in groups and belong to payed account owner (muaccount).
  """
  USER = 1
  TERM = 2
  SOURCE_TYPES = (
    (USER, 'user'),
    (TERM, 'search term')
  )
  # source name, i.e. twitter user name or twitter search term/phrase
  name = models.CharField('name', max_length=255)
  # TwitSource may be of 2 types: user or term
  type = models.DecimalField('type', choices = SOURCE_TYPES, max_digits=1, decimal_places=0)
  # muaccount this source is connected to, if we delete TwitSource for defined muaccount, it should not disappear for others
#  accounts = models.ManyToManyField(MUAccount, verbose_name='accounts')
  # TwitSource may be in any amount of groups (TwitSourceGroup) or may be in 'uncategorized' default group if NULL
  groups = models.ManyToManyField(TwitSourceGroup, verbose_name='groups', blank=True, null=True, related_name='twit_sources')

  class Meta:
    unique_together = ('name', 'type')
    ordering = ['name']
    verbose_name = 'twitter source'
    verbose_name_plural = 'twitter sources'

  def __unicode__(self):
    return self.name


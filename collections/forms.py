from django import forms

class SourceListForm(forms.Form):
  users = forms.MultipleChoiceField(choices=())

  def __init__(self, sources=None, *args, **kwargs):
    super(SourceListForm, self).__init__(*args, **kwargs)
    if sources:
      self.fields['users'].queryset = sources
      choices =[]
      for source in sources:
        choices.append((source.id, source.name))
      self.fields['users'].choices = choices

  def as_simpleinput(self):
    return self._html_output(u'%(field)s%(help_text)s', u'%s', '', u' %s', True)

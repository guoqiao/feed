#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django import forms
from . import models as m

class BaseModelForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

class FeedForm(BaseModelForm):

    class Meta:
        model = m.Feed
        fields = ('url',)

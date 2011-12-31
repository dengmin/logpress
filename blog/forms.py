#!/usr/bin/env python
# *_* encoding=utf-8*_*

from django import forms as forms
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode
from django.forms.util import ErrorDict
from blog.models import Post,Page,Comment
import datetime

class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget = forms.Textarea(attrs={'id':'content','cols':90,'rows':20})
        self.fields['password'].widget= forms.PasswordInput()
    class Media:
        js= (
             '/static/kindeditor/kindeditor-min.js',
             '/static/kindeditor/lang/zh_CN.js',
             '/static/kindeditor/textarea.js',
             )
    class Meata:
        model = Post

class PageForm(PostForm):
    class Meata:
        model = Page

class CommentForm(forms.Form):
    author = forms.CharField(widget=forms.TextInput(attrs={'id':'author'}),max_length=50)
    email = forms.EmailField(widget=forms.TextInput(attrs={'id':'email'}))
    url = forms.URLField(widget=forms.TextInput(attrs={'id':'url'}),required=False)
    content = forms.CharField(widget=forms.Textarea,max_length=300)
    
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_pk = forms.CharField(widget=forms.HiddenInput)

    parent_id = forms.IntegerField(widget = forms.HiddenInput,required = False)
   
    def __init__(self, target_object, data=None, initial=None):
        self.target_object = target_object
        if initial is None:
            initial = {}
        initial.update({
            'content_type'  : str(self.target_object._meta),
            'object_pk': str(self.target_object._get_pk_val()),
        })
        super(CommentForm, self).__init__(data=data, initial=initial)

    def get_comment_object(self):
       
        if not self.is_valid():
            raise ValueError("get_comment_object may only be called on valid forms")

        new = Comment(
            content_type = ContentType.objects.get_for_model(self.target_object),
            object_pk    = force_unicode(self.target_object._get_pk_val()),
            author    = self.cleaned_data["author"],
            email   = self.cleaned_data["email"],
            weburl     = self.cleaned_data["url"],
            content=self.clean_comment(),
            date  = datetime.datetime.now(),
            is_public    = True,
            parent_id    = self.cleaned_data["parent_id"],
        )
        return new

    def security_errors(self):
        errors = ErrorDict()
        return errors
    
    def clean_comment(self):
        return self.cleaned_data["content"].replace('<script','&lt;script').replace('</script>','&lt;/script&gt;')

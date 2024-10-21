from django import forms
from django.shortcuts import render
from django.template.context_processors import request

from posts.models import Post, Comment


class PostForm(forms.Form):
    image = forms.ImageField()
    title = forms.CharField()
    content = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()     # проверяет все данные на правильность
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if (title and content) and (title.lower() == content.lower()):
            raise forms.ValidationError("Заголовок и контент не должны совпадать")
        return cleaned_data

    def clean_title(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')

        if title and title.lower() == "python":
            raise forms.ValidationError("Заголовок не может быть с таким названием")
        return title


class PostForm2(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'rate', 'image', 'tags')
        labels = {'title': 'Заголовок',
                  'content': 'Содержание',
                  'rate' : 'Рейтинг',
                  'image': 'Картинка',
                  'tags': 'Теги'}
    widgets = {'tags': forms.CheckboxSelectMultiple()}

    def clean_rate(self):
        rate = self.cleaned_data.get('rate')
        if rate < 1 or rate > 5:
            raise forms.ValidationError('Invalid rate, must be between 1 and 5')
        return rate

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text': 'Комментарий'}
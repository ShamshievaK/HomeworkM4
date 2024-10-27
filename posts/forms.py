from django import forms
from django.shortcuts import render
from django.template.context_processors import request

from posts.models import Post, Comment, Tag


class PostForm(forms.Form):
    image = forms.ImageField()
    title = forms.CharField()
    content = forms.CharField()
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())
    rate = forms.IntegerField()

    def clean(self):
        cleaned_data = super().clean()  # проверяет все данные на правильность
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
                  'rate': 'Рейтинг',
                  'image': 'Картинка',
                  'tags': 'Теги'}

    widgets = {'tags': forms.CheckboxSelectMultiple()}

    def clean_rate(self):
        rate = self.cleaned_data.get('rate')
        if rate < 1 or rate > 5:
            raise forms.ValidationError('Invalid rate, must be between 1 and 5')
        return rate


class CommentForm(forms.Form):
        text = forms.CharField(
            widget=forms.Textarea(
                attrs={
                    "placeholder": "Введите текст",
                    "rows": 5,
                    "cols": 20,
                    "class": "form-control",
                }
            )
        )


class SearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Введите текст для поиска",
                "class": "form-control",
            }
        )
    )
    tag = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )
    orderings = (
        ("title", "По названию"),
        ("-title", "по названию в обратном порядке"),
        ("rate", "По рейтингу"),
        ("-rate", "По рейтингу в обратном порядке"),
        ("created_at", "По дате создания"),
        ("-created_at", "По дате создания в обрвтном порядке")
    )
    ordering = forms.ChoiceField(
        required=False,
        choices=orderings,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

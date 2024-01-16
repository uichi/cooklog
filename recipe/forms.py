from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from markdownx.fields import MarkdownxFormField
from markdownx.widgets import MarkdownxWidget
from taggit.forms import TagField, TagWidget
from .models import Article, Category


class RecipeForm(forms.ModelForm):
    title = forms.CharField(
        max_length=32,
        label='料理名',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    overview = forms.CharField(
        max_length=64,
        label='ひとこと',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    category = forms.ModelChoiceField(
        Category.objects,
        label='カテゴリー',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    tag = TagField(
        label='タグ(カンマ区切りで複数可能)',
        required=False,
        widget=TagWidget(attrs={'class': 'form-control'})
    )
    image = forms.ImageField(
        label='画像',
        required=False,
        widget=forms.FileInput(attrs={'id': 'inputFile', 'class': 'custom-file-input'})
    )
    serving = forms.IntegerField(
        label='何人前',
        required=False,
        validators=[
            MinValueValidator(0)
        ],
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    cooking_time = forms.IntegerField(
        label='調理時間(分)',
        required=False,
        validators=[
            MinValueValidator(0)
        ],
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    body = MarkdownxFormField(
        label='作り方(Markdown)',
        required=False,
        widget=MarkdownxWidget(attrs={'class': 'form-control markdownx-field'})
    )
    publish_status = forms.fields.ChoiceField(
        label='公開設定',
        required=True,
        choices=(
            (2, '非公開'),
            (1, '公開'),
        ),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Article
        fields = ('title', 'overview', 'category', 'tag', 'image', 'serving', 'cooking_time', 'body', 'publish_status')

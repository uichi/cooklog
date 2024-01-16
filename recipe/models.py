from django.contrib.auth import get_user_model
from django.db import models
from markdownx.models import MarkdownxField
from taggit.managers import TaggableManager

User = get_user_model()


class Category(models.Model):
    name = models.CharField('カテゴリー', max_length=16, blank=False)

    def __str__(self):
        return self.name


# class Tag(models.Model):
#     name = models.CharField('タグ', max_length=16, blank=False)
#
#     def __str__(self):
#         return self.name


class Article(models.Model):

    PUBLISH_STATUS = ((1, '公開'), (2, '非公開'))

    title = models.CharField('料理名', max_length=32, null=False, blank=False)
    overview = models.CharField('ひとこと', max_length=128, null=True, blank=False)
    image = models.ImageField('画像', upload_to='recipe_images', null=True)
    body = MarkdownxField('本文')
    serving = models.PositiveSmallIntegerField('何人前', null=True, blank=False)
    cooking_time = models.PositiveSmallIntegerField('調理時間', null=True, blank=False)
    publish_status = models.PositiveSmallIntegerField('投稿設定', choices=PUBLISH_STATUS, default=2)
    created_at = models.DateTimeField('作成日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name='カテゴリー', null=False, blank=False, on_delete=models.CASCADE)
    tag = TaggableManager(verbose_name='タグ', blank=True)

    def __str__(self):
        return self.title


class Like(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


# class Ingredient(models.Model):
#     name = models.CharField('材料名', max_length=32, null=False, blank=False)
#     quantity = models.CharField('分量', max_length=16, null=False, blank=False)
#     article = models.ForeignKey(Article, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.name

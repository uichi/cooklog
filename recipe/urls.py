from django.urls import path
from . import views

app_name = 'recipe'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('recipe/<int:pk>', views.Recipe.as_view(), name='article'),
    path('recipe/category/<int:pk>', views.Category.as_view(), name='category'),
    path('recipe/create', views.CreateRecipe.as_view(), name='create'),
    path('recipe/edit/<int:pk>', views.EditRecipe.as_view(), name='edit'),
    path('recipe/manage-article', views.ManageRecipe.as_view(), name='manage_article'),
    path('recipe/like-article/<int:pk>', views.like_article, name='ajax_like_article')
]

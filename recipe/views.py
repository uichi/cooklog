from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from .forms import RecipeForm
from .models import Article, Like

User = get_user_model()


def _get_beginning_of_month(year_and_month):
    beginning_of_month = year_and_month.strftime('%Y-%m-01')
    return datetime.strptime(beginning_of_month, '%Y-%m-%d')


def _get_end_of_month(year_and_month):
    beginning_of_month = year_and_month.strftime('%Y-%m-01')
    beginning_of_month = datetime.strptime(beginning_of_month, '%Y-%m-%d')
    end_of_month = beginning_of_month + relativedelta(months=1, days=-1)
    return end_of_month


class Home(generic.TemplateView):
    template_name = 'recipe/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = datetime.today()
        this_month = datetime(today.year, today.month, 1)
        last_month = this_month + timedelta(days=-1)
        beginning_of_month = _get_beginning_of_month(last_month)
        end_of_month = _get_end_of_month(last_month)

        new_article = Article.objects.filter(publish_status=1).order_by('-created_at')[:9]

        two_week = today + timedelta(days=-14)
        two_week_articles = Article.objects.filter(created_at__range=[two_week, today], publish_status=1)
        two_week_liked = Like.objects.filter(article_id__in=two_week_articles.values('id'))\
            .annotate(total=Count('article_id'))\
            .order_by('total')
        pickup_week_trend_articles = two_week_articles.filter(id__in=two_week_liked.values_list('article_id'))[:2]

        last_month_articles = Article.objects.filter(created_at__range=[beginning_of_month, end_of_month], publish_status=1)
        good_last_month_liked = Like.objects.filter(article_id__in=last_month_articles.values('id'))\
            .annotate(total=Count('article_id'))\
            .order_by('total')
        pickup_last_month_article = last_month_articles.filter(id__in=good_last_month_liked)[:1]

        yesterday = today + timedelta(days=-1)
        today_articles = Article.objects.filter(created_at__range=[yesterday, today], publish_status=1)
        today_liked = Like.objects.filter(article_id__in=today_articles.values('id'))\
            .annotate(total=Count('article_id'))\
            .order_by('total')
        today_trend_articles = today_articles.filter(id__in=today_liked.values_list('article_id'))[:6]

        week = today + timedelta(days=-7)
        week_articles = Article.objects.filter(created_at__range=[week, today], publish_status=1)
        week_liked = Like.objects.filter(article_id__in=week_articles.values('id'))\
            .annotate(total=Count('article_id'))\
            .order_by('total')
        week_trend_articles = week_articles.filter(id__in=week_liked.values_list('article_id'))[:6]

        if new_article:
            context['article'] = {
                'first': new_article[0],
                'second': new_article[1:5],
                'third': new_article[5:]
            }
        context['pickup_last_month_article'] = pickup_last_month_article
        context['today_trend_articles'] = today_trend_articles
        context['week_trend_articles'] = week_trend_articles
        context['pickup_week_trend_articles'] = pickup_week_trend_articles
        return context


class Recipe(generic.DetailView):
    model = Article
    template_name = 'recipe/article.html'

    def get_queryset(self):
        return Article.objects.filter(id=self.kwargs['pk'], publish_status=1)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if Like.objects.filter(user_id=self.request.user.id, article_id=self.kwargs['pk']).first():
            context['is_liked'] = True
        else:
            context['is_liked'] = False
        return context


class Category(generic.ListView):
    template_name = 'recipe/category.html'
    odering = ['-created_at']
    paginate_by = 5

    def get_queryset(self):
        return Article.objects.filter(category_id=self.kwargs['pk'], publish_status=1)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['category'] = Category.objects.get(id=self.kwargs['pk'])
        return context


class CreateRecipe(LoginRequiredMixin, generic.CreateView):
    model = Article
    template_name = 'recipe/create.html'
    form_class = RecipeForm

    def get_success_url(self):
        return reverse('user:mypage', kwargs={'pk': self.request.user.pk})

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        messages.success(self.request, "保存しました")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "保存に失敗しました")
        return redirect('recipe:home')


class ManageRecipe(LoginRequiredMixin, generic.ListView):
    model = Article
    template_name = 'recipe/manage_article.html'
    paginate_by = 50

    def get_queryset(self):
        return Article.objects.filter(user_id=self.request.user.id).order_by('-created_at')


class EditRecipe(LoginRequiredMixin, generic.UpdateView):
    model = Article
    template_name = 'recipe/edit.html'
    form_class = RecipeForm
    success_url = reverse_lazy('recipe:manage_article')

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        messages.success(self.request, "保存しました")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "保存に失敗しました")
        return redirect('recipe:home')


def like_article(request, pk):
    if request.method == 'POST':
        is_success = False
        is_liked = ''
        maked_account = True if request.user.id else False
        liked_article = Like.objects.filter(user_id=request.user.id, article_id=pk)
        if not liked_article.first():
            try:
                like_article = Like.objects.create(user_id=request.user.id, article_id=pk)
                like_article.save()
                is_success = True
                is_liked = True
                # messages.success('いいねしました')
            except:
                # messages.error('いいねに失敗しました')
                pass
        else:
            try:
                liked_article.delete()
                is_success = True
                is_liked = False
                # messages.success('いいねを取り消しました')
            except:
                # messages.error('いいねの取り消しに失敗しました')
                pass
    return JsonResponse({'success': is_success, 'liked': is_liked, 'maked_account': maked_account})


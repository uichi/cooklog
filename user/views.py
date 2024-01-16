from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import get_template
from django.urls import reverse
from django.views import generic
from .forms import (
    AccountSettingsForm, CreateUserForm, LoginForm, ChangePasswordForm
)
from .models import User
from recipe.models import Article, Like


class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser


class Profile(generic.ListView):
    model = Article
    template_name = 'user/profile.html'
    paginate_by = 50

    def get_queryset(self):
        return Article.objects.filter(user_id=self.kwargs['pk'], publish_status=1).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_info = get_object_or_404(User, pk=self.kwargs['pk'])
        context['user_info'] = {
            'image': user_info.image,
            'username': user_info.username,
            'introduction': user_info.introduction
        }
        post_recipes = Article.objects.filter(user_id=self.kwargs['pk'], publish_status=1)
        context['count_post_recipe'] = post_recipes.count()
        context['count_liked'] = Like.objects.filter(article_id__in=post_recipes).count()
        return context


class MyPage(LoginRequiredMixin, OnlyYouMixin, generic.DetailView):
    model = User
    template_name = 'user/mypage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count_post_recipe'] = Article.objects.filter(user_id=self.request.user.pk).count()
        context['count_liked'] = Like.objects.filter(user_id=self.request.user.pk).count()
        return context


class CreateUser(generic.CreateView):
    template_name = 'user/create.html'
    form_class = CreateUserForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }
        subject_template = get_template('user/mail_templates/create/subject.txt')
        subject = subject_template.render(context)

        message_template = get_template('user/mail_templates/create/body.txt')
        message = message_template.render(context)

        user.email_user(subject, message)
        return redirect('user:thanks')


class Thanks(generic.TemplateView):
    template_name = 'user/thanks.html'


class CompleteCreationUser(generic.TemplateView):
    template_name = 'user/done_creation.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60 * 60 * 24)

    def get(self, request, **kwargs):
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        except SignatureExpired:
            return HttpResponseBadRequest()

        except BadSignature:
            return HttpResponseBadRequest()

        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoenNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()


class AccountSettings(LoginRequiredMixin, OnlyYouMixin, generic.UpdateView):
    model = User
    template_name = 'user/account_settings.html'
    form_class = AccountSettingsForm

    def get_success_url(self):
        return reverse('user:mypage', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, "編集しました")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "編集に失敗しました")
        return redirect('recipe:home')


class Login(LoginView):
    form_class = LoginForm
    template_name = 'user/login.html'


class Logout(LoginRequiredMixin, LogoutView):
    template_name = 'recipe/index.html'


class ChangePassword(LoginRequiredMixin, PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'user/change_password.html'

    def get_success_url(self):
        messages.success(self.request, 'パスワードを変更しました')
        return reverse('user:mypage', kwargs={'pk': self.request.user.pk})

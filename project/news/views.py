from typing import Any
from django.urls import reverse_lazy, resolve
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View



class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'news/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context
    

# News
class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = '-created'
    paginate_by = 10

    def get_queryset(self):
        post_type = 'A' if '/articles/' in self.request.path else 'N'
        queryset = super().get_queryset().filter(type=post_type)
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        if self.request.path.startswith('/news/'):
            return Post.objects.filter(type='N')
        elif self.request.path.startswith('/articles/'):
            return Post.objects.filter(type='A')
        else:
            return Post.objects.none()


class PostCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    permission_required = ('news.add_post')
    
    def form_valid(self, form):
        post = form.save(commit=False)

        if self.request.path.startswith('/news/'):
            post.type = 'N'
        elif self.request.path.startswith('/articles/'):
            post.type = 'A'

        return super().form_valid(form)

        #response = super().form_valid(form)

        #self.mail(post)

        #return response
    
    def mail(self, post: Post):
        users = set()
        for category in post.category.all():
            for user in category.subscribers.all():
                if user.email:
                    users.add(user)
        
        if not users:
            return
        
        preview_text = post.text if len(post.text) < 50 else post.text[:50]
        
        for user in users:
            categories_names = ', '.join(c.name for c in post.category.all())
            html_content = render_to_string(
                'email_notification.html',
                {
                    'post': post,
                    'user': user,
                    'categories_names': categories_names,
                    'preview_text': preview_text,
                }
            )

            msg = EmailMultiAlternatives(
                subject=f'{post.title}',
                from_email='makarendan-yan@yandex.ru',
                to=[user.email],
            )

            msg.attach_alternative(html_content, 'text/html')
            msg.send()




class PostUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    permission_required = ('news.change_post')

    def get_queryset(self):
        if self.request.path.startswith('/news/'):
            return Post.objects.filter(type='N')
        elif self.request.path.startswith('/articles/'):
            return Post.objects.filter(type='A')
        else:
            return Post.objects.none()


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'

    def get_success_url(self):
        if self.request.path.startswith('/news/'):
            return reverse_lazy('news_list')
        else:
            return reverse_lazy('article_list')

    def get_queryset(self):
        if self.request.path.startswith('/news/'):
            return Post.objects.filter(type='N')
        elif self.request.path.startswith('/articles/'):
            return Post.objects.filter(type='A')
        else:
            return Post.objects.none()


class CategoryView(DetailView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        category = context['category']
        user = self.request.user

        if user.is_authenticated:
            context['is_subscribed'] = category.subscribers.filter(pk=user.pk).exists()
        else:
            context['is_subscribed'] = False
        
        return context


@method_decorator(login_required, name='dispatch')
class ToggleSubscriptionView(View):
    def post(self, request, *args, **kwargs):
        category = get_object_or_404(Category, pk=kwargs['pk'])
        user = request.user

        if user in category.subscribers.all():
            category.subscribers.remove(user)
        else:
            category.subscribers.add(user)

        next_url = request.POST.get('next', f'/category/{category.pk}/')
        return redirect(next_url)
    
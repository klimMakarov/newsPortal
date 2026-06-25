from django.urls import reverse_lazy, resolve
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin



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
